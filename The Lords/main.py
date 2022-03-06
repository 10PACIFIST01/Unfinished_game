import pygame
import player
import map
import environments
from folders import *
from tools import *


class Game:

    def __init__(self):
        self.FPS = 30
        self.caption = "The lords"
        self.size = ()

    def run(self):
        pygame.init()
        info_object = pygame.display.Info()
        self.size = (info_object.current_w, info_object.current_h)
        screen = pygame.display.set_mode((info_object.current_w, info_object.current_h), pygame.FULLSCREEN)
        pygame.display.set_caption(self.caption)
        clock = pygame.time.Clock()
        npc_sprites = pygame.sprite.Group()
        env_sprites = pygame.sprite.Group()

        background = map.Map(screen, map_name)
        map_size = (background.map_width, background.map_height)

        for sprite in background.environment_sprites:
            env_sprites.add(sprite)

        friedrich = player.Player(map_size, (500, 700), env_sprites)
        npc_sprites.add(friedrich)

        camera = Camera(camera_configure, map_size[0], map_size[1], self.size)

        table = environments.Table(4, (500, 500), screen, "Деревня прямо по дороге", camera)
        table2 = environments.Table(4, (1000, 680), screen, "Эту табличку поставил некий Старейшина", camera)

        tree = environments.Environment(load(env_folder, "tree2", ".png", 2), 4, (1500, 1000), screen, True)
        env_sprites.add(table)
        env_sprites.add(table2)
        env_sprites.add(tree)

        while True:
            screen.fill((0, 0, 0))
            camera.update(friedrich.rect)

            background.blit_surface(camera.state.x, camera.state.y)

            for sprite in env_sprites:
                sprite.plr_rect = friedrich.rect
                screen.blit(sprite.image, camera.apply(sprite.rect))
                if sprite.parts:
                    screen.blit(sprite.image2, camera.apply(sprite.rect2))
            for sprite in npc_sprites:
                screen.blit(sprite.image, camera.apply(sprite.rect))
            for sprite in env_sprites:
                if friedrich.rect.bottom < sprite.rect.bottom:
                    screen.blit(sprite.image, camera.apply(sprite.rect))
                    if sprite.parts:
                        screen.blit(sprite.image2, camera.apply(sprite.rect2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()

            npc_sprites.update()
            env_sprites.update()

            pygame.display.flip()
            clock.tick(self.FPS)


    def run_test(self):
        pygame.init()
        info_object = pygame.display.Info()
        self.size = (info_object.current_w, info_object.current_h)
        screen = pygame.display.set_mode((info_object.current_w, info_object.current_h), pygame.FULLSCREEN)
        pygame.display.set_caption(self.caption)
        clock = pygame.time.Clock()
        npc_sprites = pygame.sprite.Group()
        #env_sprites = pygame.sprite.Group()
        env_sprites = []

        background = map.Map(screen, map_name)
        x, y = 0, 0
        dy = 0
        dx = 0
        speed = 10

        total_level_size = (background.map_width, background.map_height)
        camera = Camera(camera_configure, total_level_size[0], total_level_size[1], self.size)

        while True:
            screen.fill((0, 0, 0))

            background.blit_surface(camera.state.x, camera.state.y)

            for sprite in env_sprites:
                screen.blit(sprite["image"], camera.apply(sprite["rect"]))
            for sprite in npc_sprites:
                screen.blit(sprite.image, camera.apply(sprite.rect))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    image = load(env_folder, "tree2", ".png")
                    image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))
                    rect = image.get_rect()
                    mouse_pos = pygame.mouse.get_pos()
                    rect.centerx, rect.bottom = -camera.state.x + mouse_pos[0], -camera.state.y + mouse_pos[1]
                    tree = {
                        "image": image,
                        "rect": rect
                    }
                    env_sprites += [tree]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                    if event.key == pygame.K_s:
                        dy = 1
                    if event.key == pygame.K_w:
                        dy = -1
                    if event.key == pygame.K_d:
                        dx = 1
                    if event.key == pygame.K_a:
                        dx = -1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        dy = 0
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        dx = 0

            y += -speed * dy
            x += -speed * dx
            x = min(0, x)
            x = max(-(camera.state.width - camera.size[0]), x)
            y = min(0, y)
            y = max(-(camera.state.height - camera.size[1]), y)
            camera.state.x, camera.state.y = x, y

            pygame.display.flip()
            clock.tick(self.FPS)


game = Game()
game.run()
