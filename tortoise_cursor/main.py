import pygame
import math
import sys
import os
import win32api
import win32con
import win32gui
import struct

# --- Constants and Paths ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class TortoiseCursor:
    def __init__(self):
        pygame.init()

        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h

        self.window = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.NOFRAME)
        pygame.display.set_caption("Tortoise Cursor")
        
        # --- Transparency Setup ---
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                              win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 255), 0, win32con.LWA_COLORKEY)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        
        self.window.fill((0, 0, 255))
        pygame.display.flip()
        # -------------------------

        self.tortoise_frames = []
        try:
            for i in range(16):
                frame_path = os.path.join(SCRIPT_DIR, f"tortoise_frame_{i}.png")
                if not os.path.exists(frame_path):
                    raise FileNotFoundError(f"Frame not found: {frame_path}")
                frame = pygame.image.load(frame_path).convert_alpha()
                self.tortoise_frames.append(frame)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading images: {e}", file=sys.stderr)
            print("Please make sure you have run 'python generate_frames.py' first.", file=sys.stderr)
            sys.exit(1)
        
        self.frame_index = 0
        self.angle = 0
        
        # Force hide cursor
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        win32api.ShowCursor(False)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.tortoise_pos = list(pygame.mouse.get_pos())
        self.last_pos = list(self.tortoise_pos)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.sensitivity = 0.5 # Value < 1 slows down, > 1 speeds up

        # --- Stop Button ---
        self.font = pygame.font.SysFont(None, 24)
        self.stop_button_rect = pygame.Rect(self.screen_width - 65, 5, 60, 25)
        self.stop_button_color = (200, 0, 0)
        self.stop_button_text_color = (255, 255, 255)

    def run(self):
        while self.running:
            total_dx = 0
            total_dy = 0
            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.stop_button_rect.collidepoint(self.tortoise_pos):
                        self.running = False
                if event.type == pygame.MOUSEMOTION:
                    # Accumulate scaled hardware movement
                    dx, dy = event.rel
                    total_dx += dx * self.sensitivity
                    total_dy += dy * self.sensitivity

            # --- Position and Angle ---
            # Apply movement to the tortoise position
            self.tortoise_pos[0] += total_dx
            self.tortoise_pos[1] += total_dy

            # Clamp to screen
            self.tortoise_pos[0] = max(0, min(self.screen_width - 1, self.tortoise_pos[0]))
            self.tortoise_pos[1] = max(0, min(self.screen_height - 1, self.tortoise_pos[1]))

            # Lock the visible cursor to this new position
            pygame.mouse.set_pos(self.tortoise_pos)

            dx = self.tortoise_pos[0] - self.last_pos[0]
            dy = self.tortoise_pos[1] - self.last_pos[1]

            if abs(dx) > 0.1 or abs(dy) > 0.1:
                self.angle = math.degrees(math.atan2(-dy, dx))
                now = pygame.time.get_ticks()
                if now - self.last_update > self.frame_rate:
                    self.last_update = now
                    self.frame_index = (self.frame_index + 1) % len(self.tortoise_frames)
            
            self.last_pos = list(self.tortoise_pos)

            # --- Drawing ---
            self.window.fill((0, 0, 255)) 

            image = self.tortoise_frames[self.frame_index]
            rotated_image = pygame.transform.rotate(image, self.angle)
            rect = rotated_image.get_rect(center=self.tortoise_pos)
            self.window.blit(rotated_image, rect)
            
            # Draw Stop Button
            pygame.draw.rect(self.window, self.stop_button_color, self.stop_button_rect)
            text_surf = self.font.render("QUIT", True, self.stop_button_text_color)
            text_rect = text_surf.get_rect(center=self.stop_button_rect.center)
            self.window.blit(text_surf, text_rect)

            pygame.display.flip()
            self.clock.tick(60)

        # --- Cleanup ---
        win32gui.ShowCursor(True)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = TortoiseCursor()
    app.run()