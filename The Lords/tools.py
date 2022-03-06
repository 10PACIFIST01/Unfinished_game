import pygame


def camera_configure(camera, target_rect, size):
    l, t = target_rect
    w, h = camera.width, camera.height
    l, t = -l + size[0] // 2, -t + size[1] // 2

    l = min(0, l)
    l = max(-(camera.width - size[0]), l)
    t = min(0, t)
    t = max(-(camera.height - size[1]), t)

    return pygame.Rect(l, t, w, h)


class Camera:
    def __init__(self, camera_func, width, height, size):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)
        self.size = size

    def apply(self, target_rect):
        return target_rect.move(self.state.topleft)

    def update(self, target_rect):
        self.state = self.camera_func(self.state, target_rect.center, self.size)


class Text:
    def __init__(self, text, font, size, x, y, color, anim=False):
        self.text = text
        #self.font_name = pygame.font.match_font(font)
        self.font = pygame.font.Font(font, size)

        self.image = self.font.render(text, True, color)
        self.width = self.image.get_rect().width
        self.rect = self.image.get_rect()
        self.rect.center = (int(x), int(y))

        if anim:
            self.image = self.font.render(text[0], True, color)

        self.anim = anim
        self.count = 0
        self.new_text = ''
        self.color = color

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        if self.anim and self.count < len(self.text):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.new_text += self.text[self.count]
                self.image = self.font.render(self.new_text, True, self.color)
                self.count += 1
