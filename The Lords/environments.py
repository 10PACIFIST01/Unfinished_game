import pygame
import math
import folders
import tools
import os


class Environment(pygame.sprite.Sprite):

    def __init__(self, images, scale, position, screen, parts=False):
        pygame.sprite.Sprite.__init__(self)

        self.front_hero_image = os.path.join(folders.friedrich_folder, "front")
        self.plr_image = pygame.image.load(os.path.join(self.front_hero_image, "hero.png"))
        self.plr_rect = self.plr_image.get_rect()

        self.parts = parts
        self.screen = screen

        if type(images) == list:
            if not parts:
                self.animation = True
                self.images = []
                self.frame = 0
                self.frame_rate = 50
                self.last_update = pygame.time.get_ticks()

                for image in images:
                    img = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
                    self.images += [img]

                self.image = self.images[self.frame]
            if parts:
                self.animation = False
                self.images = []
                for image in images:
                    img = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
                    self.images += [img]

                self.image = self.images[0]
                self.rect = pygame.Rect(position[0], position[1], self.image.get_width() - 10,
                                        self.image.get_height() - self.plr_image.get_height() * 2)
                self.image2 = self.images[1]
                self.rect2 = self.image2.get_rect()
                self.rect2.bottom = self.rect.top
                self.rect2.centerx = self.rect.centerx

        else:
            self.animation = False
            self.image = images
            self.image = pygame.transform.scale(self.image,
                                                (int(self.image.get_width() * scale),
                                                 int(self.image.get_height() * scale)))
            self.rect = pygame.Rect(position[0], position[1], self.image.get_width() - 10,
                                    self.image.get_height() - self.plr_image.get_height() * 2)
            self.radius = self.rect.width // 2

    def update(self):
        if self.animation:
            now = pygame.time.get_ticks()

            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                self.frame = self.frame % len(self.images)
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = pygame.Rect(center[0], center[1], self.image.get_width() - 10,
                                        self.image.get_height() - self.plr_image.get_height() // 2)
                self.rect.center = center


class Button:
    def __init__(self, pos):
        self.image = folders.load(folders.env_folder, "e_button", ".png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 1
        self.s = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.rect.y += self.speed
            self.s += math.sqrt(self.speed ** 2)

        if self.s > 8:
            self.s = 0
            self.speed *= -1


class Table(Environment):
    def __init__(self, scale, position, screen, message, camera,
                 images=folders.load(folders.env_folder, "table", ".png")):
        Environment.__init__(self, images, scale, position, screen)
        self.font = "fonts/pixel2.ttf"
        self.size = 15
        self.screen = screen
        self.dst = 0
        self.plr_x, self.plr_y = self.plr_rect.topleft

        info_object = pygame.display.Info()
        self.display_size = (info_object.current_w, info_object.current_h)

        self.message = message
        self.camera = camera
        #self.camera = tools.Camera(tools.camera_configure, map_size[0], map_size[1], camera)
        self.show_message = False
        self.button = Button((self.rect.centerx + 5, self.rect.centery - 55))

        self.text_bar = folders.load(folders.env_folder, "text_bar", ".png")
        self.text_y = self.display_size[1] - self.text_bar.get_height() * 3

        self.color = (0, 0, 0)
        self.text = tools.Text(self.message, self.font, self.size, self.display_size[0] // 2,
                              self.text_y + self.text_bar.get_height() * 1.25, self.color, True)
        self.text_bar = pygame.transform.scale(self.text_bar, (int(self.text.width + 20), 40))
        self.text_x = self.text.rect.x - 10

    def update(self):
        self.button.update()
        Environment.update(self)
        self.plr_x, self.plr_y = self.plr_rect.topleft
        self.dst = math.sqrt((self.plr_x - self.rect.x) ** 2 + (self.plr_y - self.rect.y) ** 2)
        key_state = pygame.key.get_pressed()
        print(self.dst)

        if self.dst < 150:
            if key_state[pygame.K_e]:
                self.show_message = True
            if not self.show_message:
                self.screen.blit(self.button.image, self.camera.apply(self.button.rect))

        else:
            self.show_message = False
            self.text.count = 0
            self.text.new_text = ''
            self.text.image = self.text.font.render(self.message[0], True, self.color)

        if self.show_message:
            self.text.update()
            self.screen.blit(self.text_bar, (self.text_x, self.text_y))
            self.screen.blit(self.text.image, self.text.rect)
