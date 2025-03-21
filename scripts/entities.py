import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game
    from scripts.tilemap import TileMap

class PhysicsEntity:
    def __init__(self, game:'Game', e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = list(size)
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        
    def update(self, tilemap:'TileMap', movement=(0,0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # print(f'collided with rect x: {rect.x}, y: {rect.y} right: {rect.right} left: {rect.left}')
                # print(f'entity x: {entity_rect.x}, y: {entity_rect.y} right: {entity_rect.right} left: {entity_rect.left}')
                if frame_movement[0] > 0:
                    self.collisions['right'] = True
                    entity_rect.right = rect.left
                elif frame_movement[0] < 0:
                    self.collisions['left'] = True
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x 

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    self.collisions['down'] = True
                    entity_rect.bottom = rect.top
                elif frame_movement[1] < 0:
                    self.collisions['up'] = True
                    entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    def render(self, surf:pygame.Surface, offset=(0, 0)):
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))