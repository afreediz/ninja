import pygame

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import TileMap
from scripts.clouds import Clouds

class Game:
    def __init__(self) -> None:
        pygame.display.set_caption('Ninja Game')
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((400, 300))
        self.movement = [False, False]
        self.player = PhysicsEntity(self, 'player', (100, 100), (8, 15))
        self.tilemap = TileMap(self, tile_size=16)
        self.clouds = Clouds(load_images('clouds/'), count=16)
        self.assets = {
            'player': load_image('entities/player.png'),
            'decor': load_images('tiles/decor/'),
            'grass': load_images('tiles/grass/'),
            'large_decor': load_images('tiles/large_decor/'),
            'spawners': load_images('tiles/spawners/'),
            'stone': load_images('tiles/stone/'),
            'clouds': load_images('clouds/')
        }
        self.scroll = [0, 0]

    def run(self):
        running = True

        while running:
            self.scroll[0] += ((self.player.rect().centerx - self.display.get_width() / 2) - self.scroll[0]) / 32
            self.scroll[1] += ((self.player.rect().centery - self.display.get_height() / 2) - self.scroll[1]) / 32
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.display.fill((14, 219, 218))
            self.clouds.update()
            self.clouds.render(self.display, render_scroll)
            self.tilemap.render(self.display, offset=render_scroll)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

            self.clock.tick(60)

Game().run()