import pygame
from typing import TYPE_CHECKING

NEIGHBOR_OFFSETS = [(-1, 0), (0, 0), (1, 0), (-1, -1), (0, -1), (1, -1), (-1, 1), (0, 1), (1, 1)]
X_NEIGHBOR_OFFSETS = [(-1, 0), (0, 0), (1, 0)]
Y_NEIGHBOR_OFFSETS = [(0, -1), (0, 0), (0, 1)]
PHYSICS_TILES = {'grass', 'stone'}

if TYPE_CHECKING:
    from game import Game

class TileMap:
    def __init__(self, game, tile_size):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {"type":"grass", "variant":1, "pos":(3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {"type":"stone", "variant":1, "pos":(10, 5 + i)}

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surf:pygame.Surface, offset=(0, 0)):
        # decors
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        # tilemap
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], ( tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1] ))
