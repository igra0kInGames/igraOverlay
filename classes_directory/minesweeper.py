import pyautogui
import pygame
from functions import *
from classes import *


class CellForMinesweeper:
    def __init__(self, rect, num, world):
        self.cooldawn_click_face = 0
        self.x = rect[0]
        self.y = rect[1]
        self.scale = 50
        self.color = [0, 0, 0]
        self.bg_color = [255, 255, 255]
        self.is_open = False
        self.num = num
        self.flagged = False
        self.cooldawn_flag = 0
        self.dict_of_color = {
            -1: [0, 0, 0],
            0: [0, 0, 0],
            1: [0, 0, 255],
            2: [0, 128, 0],
            3: [255, 0, 0],
            4: [0, 0, 128],
            5: [128, 0, 0],
            6: [0, 128, 128],
            7: [48, 48, 48],
            8: [96, 96, 96]
        }
        self.text = Text(self.num, (self.x * self.scale + world.x + 12,
                                    self.y * self.scale + world.y + 85),
                         fontSize=64, textColor=self.dict_of_color[num])

    def click(self, world):
        mouse_pos = pyautogui.position()
        mouse_click = pygame.mouse.get_pressed()
        if self.cooldawn_click_face > 0:
            self.cooldawn_click_face -= 1
        if self.cooldawn_click_face == 1:
            world.selected_face = "good_face"
        if mouse_click[0]:
            if self.x * self.scale + world.x < mouse_pos[0] < self.x * self.scale + self.scale + world.x:
                if self.y * self.scale + world.y + 80 < mouse_pos[1] < self.y * self.scale + self.scale + world.y + 80:
                    self.open(world)
                    world.selected_face = "scared_face"
                    self.cooldawn_click_face = 10
                    if self.num == -1:
                        world.defeate()
        if mouse_click[1]:
            if self.x * self.scale + world.x < mouse_pos[0] < self.x * self.scale + self.scale + world.x:
                if self.y * self.scale + world.y + 80 < mouse_pos[1] < self.y * self.scale + self.scale + world.y + 80:
                    patten_finding = [[-1, -1], [0, -1], [1, -1],
                                      [-1, 0], [1, 0],
                                      [-1, 1], [0, 1], [1, 1]]
                    self.is_open = True
                    for i in patten_finding:
                        try:
                            elem = world.dict_of_cells[f"{self.x + i[0]}.{self.y + i[1]}"]
                            if not elem.is_open and not elem.flagged:
                                elem.open(world)
                                if elem.num == -1:
                                    world.defeate()
                        except Exception as e:
                            pass
        if mouse_click[2]:
            if self.x * self.scale + world.x < mouse_pos[0] < self.x * self.scale + self.scale + world.x:
                if self.y * self.scale + world.y + 80 < mouse_pos[1] < self.y * self.scale + self.scale + world.y + 80:
                    if not self.is_open and self.cooldawn_flag == 0:
                        if self.flagged:
                            self.flagged = False
                        else:
                            self.flagged = True
                        self.cooldawn_flag = 10
                    if self.cooldawn_flag > 0:
                        self.cooldawn_flag -= 1
        if mouse_click[0] or mouse_click[1] or mouse_click[2]:
            if world.timer_text.textColor != [0, 0, 0]:
                if self.x * self.scale + world.x < mouse_pos[0] < \
                        self.x * self.scale + self.scale + world.x:
                    if self.y * self.scale + world.y + 80 < mouse_pos[1] < \
                            self.y * self.scale + self.scale + world.y + 80:
                        world.timer.start_timer()
            count_flagged_bomb = 0
            count_flagged = 0
            for i in world.dict_of_cells:
                if world.dict_of_cells[i].num == -1 and world.dict_of_cells[i].flagged:
                    count_flagged_bomb += 1
                if world.dict_of_cells[i].flagged:
                    count_flagged += 1
            if count_flagged_bomb == 10 and count_flagged == 10:
                world.selected_face = "cool_face"
                world.timer.stop_timer()
                world.timer_text.textColor = [0, 0, 0]

    def open(self, world):
        patten_finding = [[-1, -1], [0, -1], [1, -1],
                          [-1, 0], [1, 0],
                          [-1, 1], [0, 1], [1, 1]]
        self.is_open = True
        if self.num == 0:
            for i in patten_finding:
                try:
                    elem = world.dict_of_cells[f"{self.x + i[0]}.{self.y + i[1]}"]
                    if not elem.is_open:
                        elem.open(world)
                except Exception as e:
                    pass
            self.bg_color = [196, 196, 196]

    def draw(self, screen, world):
        self.text.x = self.x * self.scale + world.x + 12
        self.text.y = self.y * self.scale + world.y + 85
        self.click(world)
        pygame.draw.rect(screen, self.bg_color, (self.x * self.scale + world.x,
                                                 self.y * self.scale + world.y + 80,
                                                 self.scale, self.scale))
        pygame.draw.rect(screen, self.color, (self.x * self.scale + world.x,
                                              self.y * self.scale + world.y + 80,
                                              self.scale, self.scale), width=3)
        if self.num == -1 and self.is_open:
            screen.blit(world.bomb_sprite, (self.x * self.scale + world.x + 5,
                                            self.y * self.scale + world.y + 85))
        if self.is_open and self.num > 0:
            self.text.draw(screen)
        if self.flagged and not self.is_open:
            screen.blit(world.flag_sprite, (self.x * self.scale + world.x + 5,
                                            self.y * self.scale + world.y + 85))


class WorldOfMineSweeper:
    def __init__(self, rect):
        self.timer = Timer()
        self.x = rect[0]
        self.y = rect[1]
        self.last_program_pos = import_from_json("last_pos_program.json")
        if not "minesweeper" in self.last_program_pos:
            self.last_program_pos["minesweeper"] = [self.x, self.y]
        else:
            self.x, self.y = self.last_program_pos["minesweeper"]
        self.x_scale = rect[2]
        self.y_scale = rect[3]
        self.cells = []
        self.cooldawn_restart = -1
        self.timer_text = Text(text="0", rect=(self.x + 60, self.y + 38), fontSize=60,
                               textColor=[255, 0, 0])
        self.faces = {
            "cool_face": pygame.transform.scale(pygame.image.load("sprites/minesweeper_cool_face.png"), (50, 50)),
            "good_face": pygame.transform.scale(pygame.image.load("sprites/minesweeper_good_face.png"), (50, 50)),
            "dead_face": pygame.transform.scale(pygame.image.load("sprites/minesweeper_dead_face.png"), (50, 50)),
            "scared_face": pygame.transform.scale(pygame.image.load("sprites/minesweeper_scared_face.png"), (50, 50)),
            "pressed_face": pygame.transform.scale(pygame.image.load("sprites/minesweeper_pressed_face.png"), (50, 50)),
        }
        self.selected_face = "good_face"
        self.bomb_sprite = pygame.transform.scale(pygame.image.load("sprites/minesweepers_bomb.png"), (40, 40))
        self.flag_sprite = pygame.transform.scale(pygame.image.load("sprites/minesweeper_flag.png"), (40, 40))
        self.isVisible = True
        self.isDefeated = False
        self.map_w_bombs = [[0] * 10 for _ in range(10)]
        count_bombs = 0
        while count_bombs < 10:
            current_cell = [random.randint(0, 9), random.randint(0, 9)]
            if self.map_w_bombs[current_cell[0]][current_cell[1]] != -1:
                self.map_w_bombs[current_cell[0]][current_cell[1]] = -1
                count_bombs += 1
        patten_finding = [[-1, -1], [0, -1], [1, -1],
                          [-1, 0], [1, 0],
                          [-1, 1], [0, 1], [1, 1]]
        for x in range(len(self.map_w_bombs)):
            for y in range(len(self.map_w_bombs[0])):
                if self.map_w_bombs[x][y] != -1:
                    count_bombs_around = 0
                    for xy in patten_finding:
                        if x + xy[0] > -1 and y + xy[1] > -1:
                            try:
                                if self.map_w_bombs[x + xy[0]][y + xy[1]] == -1:
                                    count_bombs_around += 1
                            except Exception as e:
                                pass
                    self.map_w_bombs[x][y] = count_bombs_around
        for i in range(self.x_scale):
            for j in range(self.y_scale):
                self.cells.append(CellForMinesweeper([i, j],
                                                     self.map_w_bombs[i][j],
                                                     self))
        self.dict_of_cells = {}
        for elem in self.cells:
            self.dict_of_cells[f"{elem.x}.{elem.y}"] = elem

    def drag_window(self):
        mouse_pos = pyautogui.position()
        is_mouse_click = pygame.mouse.get_pressed()[0]
        if is_mouse_click:
            if self.x < mouse_pos[0] < self.x + self.x_scale * 50 and\
                    self.y < mouse_pos[1] < self.y + 30:
                self.x = mouse_pos[0] - self.x_scale * 50 / 2
                self.y = mouse_pos[1] - 30 / 2
                self.last_program_pos["minesweeper"] = [self.x, self.y]
                dump_to_json(self.last_program_pos, "last_pos_program.json")

    def draw(self, screen, checkbox):
        self.timer.update()
        self.timer_text.text = str(self.timer.time_int())
        self.timer_text.x = self.x + 60
        self.timer_text.y = self.y + 38
        mouse_pos = pyautogui.position()
        is_mouse_click = pygame.mouse.get_pressed()[0]
        if is_mouse_click:
            if self.x < mouse_pos[0] < self.x + 50 and\
                    self.y + 30 < mouse_pos[1] < self.y + 80:
                self.cooldawn_restart = 20
                self.selected_face = "pressed_face"
        if self.cooldawn_restart > 0:
            self.cooldawn_restart -= 1
        if self.cooldawn_restart == 1:
            checkbox.restart = True
        self.drag_window()
        if self.isVisible:
            for elem in self.cells:
                elem.draw(screen, self)
            pygame.draw.rect(screen, [255, 255, 255], (self.x, self.y, self.x_scale*50, 80))
            pygame.draw.rect(screen, [0, 0, 0], (self.x, self.y+26, self.x_scale*50, 4))
        if self.timer_text.textColor != [0, 0, 0]:
            screen.blit(self.faces[self.selected_face], (self.x, self.y + 30))
        else:
            if self.isDefeated:
                screen.blit(self.faces["dead_face"], (self.x, self.y + 30))
            else:
                screen.blit(self.faces["cool_face"], (self.x, self.y + 30))
        self.timer_text.draw(screen)

    def defeate(self):
        for i in self.cells:
            if i.num == -1:
                i.bg_color = [255, 0, 0]
                i.open(self)
        self.selected_face = "dead_face"
        self.timer.stop_timer()
        self.timer_text.textColor = [0, 0, 0]
        self.isDefeated = True