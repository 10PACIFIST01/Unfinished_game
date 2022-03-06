import pygame
import os
import folders


def load_images(name, folder,  num):
    images = []
    for i in range(num):
        name = os.path.join(folder, name)
        image = pygame.image.load(name + str(i) + ".png")
        image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))
        images += [image]

    return images


class Player(pygame.sprite.Sprite):
    def __init__(self, size, pos, env):
        pygame.sprite.Sprite.__init__(self)
        self.plr_fold = folders.friedrich_folder

        self.count = 0
        self.view = "front"
        self.frame_rate = 80
        self.last_update = pygame.time.get_ticks()

        self.front_hero_image = os.path.join(self.plr_fold, "front")
        self.front_hero_images = load_images("hero", self.front_hero_image, 7)
        self.default_front_image = pygame.image.load(os.path.join(self.front_hero_image, "hero.png"))
        self.front_image_size = (self.default_front_image.get_width(), self.default_front_image.get_height())
        self.default_front_image = pygame.transform.scale(self.default_front_image,
                                                          (self.front_image_size[0] * 3, self.front_image_size[1] * 3))

        self.back_hero_image = os.path.join(self.plr_fold, "back")
        self.back_hero_images = load_images("hero", self.back_hero_image, 7)
        self.default_back_image = pygame.image.load(os.path.join(self.back_hero_image, "hero.png"))
        self.back_image_size = (self.default_back_image.get_width(), self.default_back_image.get_height())
        self.default_back_image = pygame.transform.scale(self.default_back_image,
                                                          (self.back_image_size[0] * 3, self.back_image_size[1] * 3))

        self.right_hero_image = os.path.join(self.plr_fold, "right")
        self.right_hero_images = load_images("hero", self.right_hero_image, 7)
        self.default_right_image = pygame.image.load(os.path.join(self.right_hero_image, "hero.png"))
        self.right_image_size = (self.default_right_image.get_width(), self.default_right_image.get_height())
        self.default_right_image = pygame.transform.scale(self.default_right_image,
                                                          (self.right_image_size[0] * 3, self.right_image_size[1] * 3))

        self.left_hero_image = os.path.join(self.plr_fold, "left")
        self.left_hero_images = load_images("hero", self.left_hero_image, 7)
        self.default_left_image = pygame.image.load(os.path.join(self.left_hero_image, "hero.png"))
        self.left_image_size = (self.default_left_image.get_width(), self.default_left_image.get_height())
        self.default_left_image = pygame.transform.scale(self.default_left_image,
                                                          (self.left_image_size[0] * 3, self.left_image_size[1] * 3))

        self.image = self.default_front_image

        self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width() // 1.25, self.image.get_height() // 3)
        self.radius = self.rect.width // 2

        self.field_size = size

        self.dx = 0
        self.dy = 0
        self.speed = 6
        self.env = env

    def update(self):
        self.dx = 0
        self.dy = 0
        self.speed = 6
        now = pygame.time.get_ticks()

        #move
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_d] and not key_state[pygame.K_a]:
            self.dx = self.speed

            if now - self.last_update > self.frame_rate:
                self.view = "right"
                self.last_update = now
                self.count += 1
                self.count = self.count % 7
                self.image = self.right_hero_images[self.count]

        if key_state[pygame.K_a] and not key_state[pygame.K_d]:
            self.dx = -self.speed

            if now - self.last_update > self.frame_rate:
                self.view = "left"
                self.last_update = now
                self.count += 1
                self.count = self.count % 7
                self.image = self.left_hero_images[self.count]

        if key_state[pygame.K_w] and not key_state[pygame.K_s]:
            self.dy = -self.speed

            if now - self.last_update > self.frame_rate:
                self.view = "back"
                self.last_update = now
                self.count += 1
                self.count = self.count % 7
                self.image = self.back_hero_images[self.count]

        if key_state[pygame.K_s] and not key_state[pygame.K_w]:
            self.dy = self.speed

            if now - self.last_update > self.frame_rate:
                self.view = "front"
                self.last_update = now
                self.count += 1
                self.count = self.count % 7
                self.image = self.front_hero_images[self.count]

        #stop animation
        if self.dx == 0 and self.dy == 0:
            if self.view == "front":
                self.image = self.default_front_image
            if self.view == "back":
                self.image = self.default_back_image
            if self.view == "right":
                self.image = self.default_right_image
            if self.view == "left":
                self.image = self.default_left_image

        self.rect.x += self.dx
        self.collide(self.dx, 0, self.env)

        self.rect.y += self.dy
        self.collide(0, self.dy, self.env)

        #collide with end of map
        if self.rect.right > self.field_size[0]:
            self.rect.right = self.field_size[0]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.field_size[1]:
            self.rect.bottom = self.field_size[1]

    def collide(self, x_vel, y_vel, env_sprites):
        for env in env_sprites:
            if pygame.sprite.collide_rect(self, env):
                if x_vel > 0:
                    self.rect.right = env.rect.left

                if x_vel < 0:
                    self.rect.left = env.rect.right

                if y_vel > 0:
                    self.rect.bottom = env.rect.top

                if y_vel < 0:
                    self.rect.top = env.rect.bottom
