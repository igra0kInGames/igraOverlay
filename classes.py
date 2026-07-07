import pygame
import time


class Text:
    def __init__(self, text, rect, fontSize=32, textColor=(0, 0, 0)):
        self.x = rect[0]
        self.y = rect[1]
        self.fontSize = fontSize
        self.text = str(text)
        self.font = pygame.font.Font(None, fontSize)
        self.textColor = textColor
        self.textSurfaces = self.font.render(self.text, True, self.textColor)

    def draw(self, screen):
        self.textSurfaces = self.font.render(self.text, True, self.textColor)
        screen.blit(self.textSurfaces, (self.x, self.y))

    def set_text(self, text):
        self.text = text
        self.textSurfaces = self.font.render(self.text, True, self.textColor)


class Timer:
    def __init__(self):
        self.time_of_timer = 0
        self.timering = False

    def start_timer(self):
        self.timering = True
        self.old_time = time.time()

    def update(self):
        if self.timering:
            self.time_of_timer += time.time() - self.old_time
        self.old_time = time.time()

    def stop_timer(self):
        self.timering = False

    def time_int(self):
        return int(self.time_of_timer)


class CheckBox:
    def __init__(self, rect, text):
        self.x, self.y, self.scale_x, self.scale_y = rect
        self.text = Text(text, (self.x, self.y, self.scale_x, self.scale_y),
                         textColor=(255, 255, 255))
        self.enabled = False
        self.cooldawn = 0
        self.cooldawn_restart = 0
        self.restart = False

    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        is_mouse_click = pygame.mouse.get_pressed()[0]
        if self.cooldawn > 0:
            self.cooldawn -= 1
        if is_mouse_click:
            if self.x < mouse_pos[0] < self.x+self.text.font.size(self.text.text)[0]+50 and\
                    self.y < mouse_pos[1] < self.y + self.scale_y:
                if self.cooldawn == 0:
                    if self.enabled:
                        self.enabled = False
                    else:
                        self.enabled = True
                    self.cooldawn = 10

    def draw(self, screen):
        if self.cooldawn_restart > 0:
            self.cooldawn_restart -= 1
        if self.restart:
            self.enabled = False
            self.cooldawn_restart = 10
            self.restart = False
        elif self.cooldawn_restart == 1:
            self.enabled = True
        self.click()
        self.text.draw(screen)
        pygame.draw.rect(screen, [0, 0, 0], (self.x+self.text.font.size(self.text.text)[0]+10,
                                             self.y, 40, self.text.font.size(self.text.text)[1]),
                         border_radius=10)
        if not self.enabled:
            pygame.draw.circle(screen, [48, 48, 48], (self.x+self.text.font.size(self.text.text)[0]+20,
                                                      self.y+self.text.font.size(self.text.text)[1]/2),
                               radius=self.text.font.size(self.text.text)[1]/2-3)
        else:
            pygame.draw.circle(screen, [48, 128, 48], (self.x + self.text.font.size(self.text.text)[0] + 40,
                                                       self.y + self.text.font.size(self.text.text)[1] / 2),
                               radius=self.text.font.size(self.text.text)[1] / 2 - 3)


class Button:
    def __init__(self, rect, text):
        self.x, self.y, self.scale_x, self.scale_y = rect
        self.text = Text(text, (self.x, self.y,
                                self.scale_x-10, self.scale_y-10), fontSize=22,
                         textColor=(255, 255, 255))
        self.text.x = (self.scale_x - self.text.font.size(text)[0]) / 2 + self.x
        self.text.y = (self.scale_y - self.text.font.size(text)[1]) / 2 + self.y
        self.color = [48, 48, 48]
        self.bg_color = [24, 24, 24]

    def is_click(self):
        mouse_pos = pygame.mouse.get_pos()
        is_mouse_click = pygame.mouse.get_pressed()[0]
        if is_mouse_click:
            if self.x < mouse_pos[0] < self.x+self.scale_x and\
                    self.y < mouse_pos[1] < self.y + self.scale_y:
                return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.scale_x, self.scale_y),
                         border_radius=5)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.scale_x, self.scale_y),
                         border_radius=5, width=5)
        self.text.draw(screen)
