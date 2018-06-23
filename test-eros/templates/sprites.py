import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.game.player_img.set_clip(pg.Rect(0, 0, 52, 76))
        self.image = self.game.player_img.subsurface(self.game.player_img.get_clip())
        self.rect = self.image.get_rect()

        # REEMPLAZA
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        # self.rect = self.image.get_rect()
        self.frame = 0

        self.right_states = { 0: (0, 76, 52, 76), 1: (52, 76, 52, 76), 2: (156, 76, 52, 76) }
        self.left_states = { 0: (0, 152, 52, 76), 1: (52, 152, 52, 76), 2: (156, 152, 52, 76) }
        self.up_states = { 0: (0, 228, 52, 76), 1: (52, 228, 52, 76), 2: (156, 228, 52, 76) }
        self.down_states = { 0: (0, 0, 52, 76), 1: (52, 0, 52, 76), 2: (156, 0, 52, 76) }

        self.vel=vec(0,0)
        self.pos=vec(x,y) * TILESIZE
        self.state = 0
        # Reemplaza
        # self.vx, self.vy = 0, 0
        # self.x = x * TILESIZE
        # self.y = y * TILESIZE
###########################
    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.game.player_img.set_clip(pg.Rect(self.get_frame(clipped_rect)))
        else:
            self.game.player_img.set_clip(pg.Rect(clipped_rect))
        return clipped_rect
#############

    def pause(self, state):
        self.state = state
        self.vx = 0
        self.vy = 0

    def get_keys(self):
        if self.state : return
        self.vel=vec(0,0)
        # Reemplaza
        # self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.clip(self.left_states)
            self.vel.x = -PLAYER_SPEED
            self.image = self.game.player_img.subsurface(self.game.player_img.get_clip())
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.clip(self.right_states)
            self.vel.x = PLAYER_SPEED
            self.image = self.game.player_img.subsurface(self.game.player_img.get_clip())
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.clip(self.up_states)
            self.vel.y = -PLAYER_SPEED
            self.image = self.game.player_img.subsurface(self.game.player_img.get_clip())
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.clip(self.down_states)
            self.vel.y = PLAYER_SPEED
            self.image = self.game.player_img.subsurface(self.game.player_img.get_clip())

    def update(self):
        self.get_keys()
        self.pos+= self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x  = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x  = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y


class Bomb(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("../resources/images/bomb.png")
        self.rect = self.image.get_rect()
        self.rect.x = round(x / TILESIZE) * TILESIZE
        self.rect.y = round(y / TILESIZE) * TILESIZE
        self.start = pg.time.get_ticks()
        self.fires = []
        self.level = 4

    def track(self):
        if pg.time.get_ticks() - self.start > 3000:
            self.exploit()

        if pg.time.get_ticks() - self.start > 4000:
            for fire in self.fires:
                fire.kill()

    def exploit(self):
        self.fires.append( Fire(self.game, self.rect.x, self.rect.y) )


        for i in range(self.level):
            self.fires.append( Fire(self.game, self.rect.x, self.rect.y - TILESIZE*i) )
            self.fires.append( Fire(self.game, self.rect.x - TILESIZE*i, self.rect.y) )
            self.fires.append( Fire(self.game, self.rect.x + TILESIZE*i, self.rect.y) )
            self.fires.append( Fire(self.game, self.rect.x, self.rect.y + TILESIZE*i) )
        self.kill()

class Fire(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("../resources/images/fire.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE