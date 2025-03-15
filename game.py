import pygame

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import TileMap


class Game:
    def __init__(self) -> None:
        pygame.display.set_caption('Ninja Game')
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((400, 300))
        self.movement = [False, False]
        self.player = PhysicsEntity(self, 'player', (100, 100), (8, 15))
        self.tilemap = TileMap(self, tile_size=16)
        self.assets = {
            'player': load_image('entities/player.png'),
            'decor': load_images('tiles/decor/'),
            'grass': load_images('tiles/grass/'),
            'large_decor': load_images('tiles/large_decor/'),
            'spawners': load_images('tiles/spawners/'),
            'stone': load_images('tiles/stone/')
        }

    def run(self):
        running = True

        while running:
            self.display.fill((14, 219, 218))
            self.tilemap.render(self.display)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

            self.clock.tick(60)

Game().run()