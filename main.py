#!/usr/bin/env python3

import pygame
import sys
import math

# Inisialisasi pygame
pygame.init()

# Ukuran jendela dan elemen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
MENU_HEIGHT = 75
DRAWING_HEIGHT = SCREEN_HEIGHT - MENU_HEIGHT

# Warna RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
PURPLE = (148, 0, 211)
ORANGE = (255, 140, 0)
PINK = (255, 105, 180)
CYAN = (0, 206, 209)

PALETTE = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK, CYAN]

LIGHT = (240, 240, 240)
DARK = (100, 100, 100)

class PaintBoard:
    def __init__(self):
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Canvas Interaktif - PyDraw")
        
        self.board = pygame.Surface((SCREEN_WIDTH, DRAWING_HEIGHT))
        self.board.fill(WHITE)

        self.mode = "dot"
        self.color = BLACK
        self.dragging = False
        self.anchor = None
        self.buffer = None
        self.path = []

        self.font = pygame.font.SysFont(None, 20)

    def render_menu(self):
        pygame.draw.rect(self.window, LIGHT, (0, 0, SCREEN_WIDTH, MENU_HEIGHT))
        pygame.draw.line(self.window, DARK, (0, MENU_HEIGHT), (SCREEN_WIDTH, MENU_HEIGHT), 2)

        tools = ["Titik", "Garis", "Persegi", "Lingkaran", "Elips"]
        keymap = ["dot", "line", "rect", "circle", "ellipse"]
        px = 10

        for i, name in enumerate(tools):
            box = pygame.Rect(px, 10, 85, 30)
            active = self.mode == keymap[i]
            pygame.draw.rect(self.window, BLUE if active else WHITE, box)
            pygame.draw.rect(self.window, BLACK, box, 2)
            label = self.font.render(name, True, WHITE if active else BLACK)
            self.window.blit(label, label.get_rect(center=box.center))
            px += 95

        for i, col in enumerate(PALETTE):
            colorbox = pygame.Rect(510 + i * 34, 15, 28, 28)
            pygame.draw.rect(self.window, col, colorbox)
            if col == self.color:
                pygame.draw.rect(self.window, WHITE, colorbox, 3)
            pygame.draw.rect(self.window, BLACK, colorbox, 2)

        clr_btn = pygame.Rect(SCREEN_WIDTH - 95, 15, 75, 28)
        pygame.draw.rect(self.window, RED, clr_btn)
        pygame.draw.rect(self.window, BLACK, clr_btn, 2)
        label = self.font.render("Hapus", True, WHITE)
        self.window.blit(label, label.get_rect(center=clr_btn.center))

        info = f"Mode: {self.mode.upper()}"
        self.window.blit(self.font.render(info, True, BLACK), (10, 52))

    def click_event(self, pos, button):
        x, y = pos

        if y < MENU_HEIGHT:
            if 10 <= x < 485 and 10 <= y <= 40:
                index = (x - 10) // 95
                self.mode = ["dot", "line", "rect", "circle", "ellipse"][index]
                self.path.clear()

            elif 510 <= x <= 816 and 15 <= y <= 45:
                idx = (x - 510) // 34
                if 0 <= idx < len(PALETTE):
                    self.color = PALETTE[idx]

            elif SCREEN_WIDTH - 95 <= x <= SCREEN_WIDTH - 20 and 15 <= y <= 45:
                self.board.fill(WHITE)
                self.path.clear()
        else:
            y -= MENU_HEIGHT
            self.canvas_event((x, y), button)

    def canvas_event(self, pos, button):
        if self.mode == "dot":
            if button == 1:
                pygame.draw.circle(self.board, self.color, pos, 3)
                self.path.clear()
            elif button == 3:
                if self.path:
                    pygame.draw.line(self.board, self.color, self.path[-1], pos, 2)
                pygame.draw.circle(self.board, self.color, pos, 3)
                self.path.append(pos)
        elif self.mode in ["line", "rect", "circle", "ellipse"] and button == 1:
            self.dragging = True
            self.anchor = pos
            self.buffer = self.board.copy()

    def mouse_drag(self, pos):
        if not self.dragging or not self.anchor:
            return

        pos = (pos[0], pos[1] - MENU_HEIGHT)
        self.board = self.buffer.copy()

        if self.mode == "line":
            pygame.draw.line(self.board, self.color, self.anchor, pos, 2)
        elif self.mode == "rect":
            rect = pygame.Rect(min(self.anchor[0], pos[0]), min(self.anchor[1], pos[1]), abs(pos[0] - self.anchor[0]), abs(pos[1] - self.anchor[1]))
            pygame.draw.rect(self.board, self.color, rect, 2)
        elif self.mode == "circle":
            radius = int(math.hypot(pos[0] - self.anchor[0], pos[1] - self.anchor[1]))
            if radius > 0:
                pygame.draw.circle(self.board, self.color, self.anchor, radius, 2)
        elif self.mode == "ellipse":
            rect = pygame.Rect(min(self.anchor[0], pos[0]), min(self.anchor[1], pos[1]), abs(pos[0] - self.anchor[0]), abs(pos[1] - self.anchor[1]))
            pygame.draw.ellipse(self.board, self.color, rect, 2)

    def release_mouse(self):
        self.dragging = False
        self.anchor = None
        self.buffer = None

    def start(self):
        clock = pygame.time.Clock()
        active = True

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_event(event.pos, event.button)
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_drag(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.release_mouse()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.board.fill(WHITE)
                        self.path.clear()

            self.window.fill(WHITE)
            self.window.blit(self.board, (0, MENU_HEIGHT))
            self.render_menu()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    PaintBoard().start()
