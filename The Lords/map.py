import pygame
import folders


class Map:
    def __init__(self, screen, map_name):
        self.file = map_name
        self.screen = screen
        self.tile_size = 150
        self.env_folder = folders.env_folder
        self.ground_images = [folders.load(self.env_folder, "grass", ".jpg"),
                              folders.load(folders.image_name(self.env_folder, "sand"), "sand", ".jpg", 6)]
        self.surfaces = []
        self.environment_sprites = []
        for image in self.ground_images:
            if type(image) == list:
                images = []
                for i_image in image:
                    images += [pygame.transform.scale(i_image, (self.tile_size, self.tile_size))]
                self.surfaces += [images]
            else:
                self.surfaces += [pygame.transform.scale(image, (self.tile_size, self.tile_size))]

        with open(self.file, "r") as file:
            self.map_arr = file.readlines()

        self.map_width, self.map_height = self.tile_size * (len(self.map_arr[0]) - 1), self.tile_size * len(self.map_arr)

    def blit_surface(self, x, y):
        count = 0

        for line in self.map_arr:
            for i in range(len(line)):
                tile_x = x + i * self.tile_size
                tile_y = y + count * self.tile_size
                rect = pygame.Rect(tile_x, tile_y, self.tile_size, self.tile_size)

                if line[i] == "=":
                    if line[i - 1] == "." and line[i + 1] == "." and self.map_arr[count - 1][i] != "." \
                            and self.map_arr[count + 1][i] != ".":
                        self.screen.blit(self.surfaces[1][0], rect)
                    elif line[i - 1] == "." and line[i + 1] == "." and self.map_arr[count - 1][i] == ".":
                        self.screen.blit(self.surfaces[1][1], rect)
                    elif line[i - 1] == "." and line[i + 1] == '.' and self.map_arr[count + 1][i] == '.':
                        image = pygame.transform.flip(self.surfaces[1][1], True, False)
                        image = pygame.transform.rotate(image, 180)
                        self.screen.blit(image, rect)
                    elif self.map_arr[count - 1][i] == '.' and self.map_arr[count + 1][i] == '.' and line[i - 1] != '.'\
                            and line[i + 1] != '.':
                        image = pygame.transform.rotate(self.surfaces[1][0], 90)
                        self.screen.blit(image, rect)
                    elif self.map_arr[count - 1][i] == '.' and self.map_arr[count + 1][i] == '.' and line[i - 1] != '.'\
                            and line[i + 1] == '.':
                        image = pygame.transform.flip(self.surfaces[1][1], True, False)
                        image = pygame.transform.rotate(image, 270)
                        self.screen.blit(image, rect)
                    elif self.map_arr[count - 1][i] == '.' and self.map_arr[count + 1][i] == "." and line[i - 1] == '.':
                        image = pygame.transform.rotate(self.surfaces[1][1], 90)
                        self.screen.blit(image, rect)
                    elif self.map_arr[count - 1][i] == '.' and self.map_arr[count + 1][i] != "." and line[i - 1] == "."\
                            and line[i + 1] != ".":
                        self.screen.blit(self.surfaces[1][2], rect)
                    elif self.map_arr[count - 1][i] == "." and self.map_arr[count + 1][i] != "." and line[i - 1] != "."\
                            and line[i + 1] == ".":
                        self.screen.blit(self.surfaces[1][5], rect)
                    elif self.map_arr[count - 1][i] == "=" and self.map_arr[count + 1] == "." or line[i - 1] == "=" and\
                            line[i + 1] == '.':
                        self.screen.blit(self.surfaces[1][4], rect)
                    elif self.map_arr[count - 1][i] == "=" and self.map_arr[count + 1] == "." or line[i - 1] == "."\
                            and line[i + 1] == "=":
                        self.screen.blit(self.surfaces[1][3], rect)
                else:
                    self.screen.blit(self.surfaces[0], rect)
            count += 1
