import pygame
import random

TILE = 40
COLS, ROWS = 20, 15
WALL, FLOOR, CHEST, KEY, TRAP = 0, 1, 2, 3, 4
SPEED = 3
FPS = 60

WIDTH = COLS * TILE
HEIGHT = ROWS * TILE + 90

COLORS = {
    WALL: (60, 50, 70),
    FLOOR: (200, 190, 170),
    CHEST: (200, 160, 30),
    KEY: (220, 220, 60),
    TRAP: (160, 40, 40),
}


def generate_world():
    grid = [[WALL] * COLS for _ in range(ROWS)]
    rooms = []

    for _ in range(8):
        w = random.randint(3, 6)
        h = random.randint(3, 5)
        x = random.randint(1, COLS - w - 1)
        y = random.randint(1, ROWS - h - 1)
        room = pygame.Rect(x, y, w, h)

        if not any(room.inflate(2, 2).colliderect(r) for r in rooms):
            rooms.append(room)
            for ry in range(y, y + h):
                for rx in range(x, x + w):
                    grid[ry][rx] = FLOOR

    for i in range(len(rooms) - 1):
        ax, ay = rooms[i].centerx, rooms[i].centery
        bx, by = rooms[i + 1].centerx, rooms[i + 1].centery

        cx = ax
        while cx != bx:
            grid[ay][cx] = FLOOR
            cx += 1 if bx > cx else -1

        cy = ay
        while cy != by:
            grid[cy][bx] = FLOOR
            cy += 1 if by > cy else -1

    start = rooms[0] if rooms else None

    if len(rooms) >= 2:
        chest_room = rooms[-1]
        key_room = rooms[-2]
        grid[chest_room.centery][chest_room.centerx] = CHEST
        grid[key_room.centery][key_room.centerx] = KEY

        floor_tiles = []
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == FLOOR:
                    if start and start.collidepoint(c, r):
                        continue
                    floor_tiles.append((r, c))

        random.shuffle(floor_tiles)
        for r, c in floor_tiles[:3]:
            grid[r][c] = TRAP

    return grid, start


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 28)
        self.color = (60, 120, 220)
        self.has_key = False

    def move(self, keys, grid, rows, cols):
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = SPEED
        self._try_move(dx, 0, grid, rows, cols)
        self._try_move(0, dy, grid, rows, cols)

    def _try_move(self, dx, dy, grid, rows, cols):
        new_rect = self.rect.move(dx, dy)
        points = [
            (new_rect.left, new_rect.top),
            (new_rect.right - 1, new_rect.top),
            (new_rect.left, new_rect.bottom - 1),
            (new_rect.right - 1, new_rect.bottom - 1),
        ]

        for px, py in points:
            c, r = px // TILE, py // TILE
            if not (0 <= r < rows and 0 <= c < cols):
                return
            if grid[r][c] == WALL:
                return

        self.rect = new_rect

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
        if self.has_key:
            pygame.draw.circle(
                screen, (255, 230, 50),
                (self.rect.right - 6, self.rect.top + 6), 5
            )


class Guard:
    def __init__(self, start_x, start_y, end_x):
        self.rect = pygame.Rect(
            start_x * TILE + 8, start_y * TILE + 8, 24, 24
        )
        self.start_x = start_x * TILE + 8
        self.end_x = end_x * TILE + 8
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x <= self.start_x:
            self.rect.x = self.start_x
            self.direction = 1
        if self.rect.x >= self.end_x:
            self.rect.x = self.end_x
            self.direction = -1

    def draw(self, screen):
        pygame.draw.rect(screen, (190, 40, 40), self.rect, border_radius=6)
        pygame.draw.circle(screen, (255, 255, 255),
                           (self.rect.x + 7, self.rect.y + 8), 3)
        pygame.draw.circle(screen, (255, 255, 255),
                           (self.rect.x + 17, self.rect.y + 8), 3)


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Treasure Hunt")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20)
        self.big_font = pygame.font.SysFont("monospace", 40, bold=True)
        self.reset()

    def reset(self):
        self.grid, self.start_room = generate_world()

        if self.start_room:
            sx = self.start_room.x * TILE + 6
            sy = self.start_room.y * TILE + 6
        else:
            sx = sy = TILE + 6

        self.start_position = (sx, sy)
        self.player = Player(sx, sy)
        self.won = False
        self.status = "Find the KEY, avoid traps and guard, then reach the CHEST!"

        guard_y, guard_start, guard_end = ROWS // 2, 12, 16
        found = False

        for r in range(ROWS):
            for c in range(1, COLS - 5):
                if all(self.grid[r][c + i] == FLOOR for i in range(4)):
                    guard_y, guard_start, guard_end = r, c, c + 3
                    found = True
                    break
            if found:
                break

        self.guard = Guard(guard_start, guard_y, guard_end)

    def reset_player(self, message):
        self.player.rect.topleft = self.start_position
        self.status = message

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
        return True

    def update(self):
        if self.won:
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys, self.grid, ROWS, COLS)
        self.guard.update()

        if self.player.rect.colliderect(self.guard.rect):
            self.reset_player("GUARD CAUGHT YOU! Returned to START.")
            return

        pr = self.player.rect.centery // TILE
        pc = self.player.rect.centerx // TILE

        if 0 <= pr < ROWS and 0 <= pc < COLS:
            cell = self.grid[pr][pc]

            if cell == TRAP:
                self.reset_player("TRAP ACTIVATED! Returned to START.")
                return

            if cell == KEY:
                self.player.has_key = True
                self.grid[pr][pc] = FLOOR
                self.status = "KEY COLLECTED! Find the CHEST!"

            elif cell == CHEST:
                if self.player.has_key:
                    self.won = True
                    self.status = "TREASURE FOUND!"
                else:
                    self.status = "You need the KEY first!"

    def draw_world(self):
        for r in range(ROWS):
            for c in range(COLS):
                cell = self.grid[r][c]
                rect = pygame.Rect(c * TILE, r * TILE, TILE, TILE)
                pygame.draw.rect(self.screen, COLORS[cell], rect)
                pygame.draw.rect(self.screen, (90, 80, 100), rect, 1)

                if cell == KEY:
                    pygame.draw.circle(
                        self.screen, (255, 240, 60),
                        (c * TILE + TILE // 2, r * TILE + TILE // 2), 10
                    )
                elif cell == CHEST:
                    pygame.draw.rect(
                        self.screen, (180, 120, 20),
                        rect.inflate(-12, -12), border_radius=4
                    )
                elif cell == TRAP:
                    pygame.draw.polygon(
                        self.screen, (220, 70, 70),
                        [
                            (c * TILE + 10, r * TILE + 30),
                            (c * TILE + 20, r * TILE + 10),
                            (c * TILE + 30, r * TILE + 30),
                        ]
                    )

    def draw_minimap(self):
        map_tile = 6
        map_width, map_height = COLS * map_tile, ROWS * map_tile
        x_offset, y_offset = WIDTH - map_width - 10, 10

        pygame.draw.rect(
            self.screen, (15, 15, 25),
            (x_offset - 4, y_offset - 4, map_width + 8, map_height + 8)
        )

        for r in range(ROWS):
            for c in range(COLS):
                color = (35, 35, 45) if self.grid[r][c] == WALL else (170, 170, 150)
                pygame.draw.rect(
                    self.screen, color,
                    (x_offset + c * map_tile, y_offset + r * map_tile,
                     map_tile, map_tile)
                )

        px = self.player.rect.centerx // TILE
        py = self.player.rect.centery // TILE

        pygame.draw.rect(
            self.screen, (50, 120, 255),
            (x_offset + px * map_tile, y_offset + py * map_tile,
             map_tile, map_tile)
        )

    def draw_inventory(self):
        x, y = 10, ROWS * TILE + 10

        pygame.draw.rect(self.screen, (50, 50, 65), (x, y, 50, 50))
        pygame.draw.rect(self.screen, (180, 180, 190), (x, y, 50, 50), 2)

        if self.player.has_key:
            pygame.draw.circle(self.screen, (255, 220, 50), (x + 17, y + 20), 8, 3)
            pygame.draw.rect(self.screen, (255, 220, 50), (x + 23, y + 18, 18, 5))
            pygame.draw.rect(self.screen, (255, 220, 50), (x + 35, y + 23, 5, 7))

        label = self.font.render("INVENTORY", True, (220, 220, 220))
        self.screen.blit(label, (x + 60, y + 15))

    def draw_hud(self):
        hud_y = ROWS * TILE
        pygame.draw.rect(self.screen, (20, 20, 35), (0, hud_y, WIDTH, 90))
        status = self.font.render(self.status, True, (230, 230, 230))
        self.screen.blit(status, (10, hud_y + 65))

    def draw(self):
        self.screen.fill((30, 25, 40))
        self.draw_world()
        self.guard.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_minimap()
        self.draw_inventory()
        self.draw_hud()

        if self.won:
            overlay = pygame.Surface((WIDTH, ROWS * TILE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            message = self.big_font.render("TREASURE FOUND!", True, (220, 180, 30))
            sub = self.font.render("Press R to Play Again", True, (220, 220, 220))

            self.screen.blit(
                message,
                (WIDTH // 2 - message.get_width() // 2,
                 ROWS * TILE // 2 - 30)
            )
            self.screen.blit(
                sub,
                (WIDTH // 2 - sub.get_width() // 2,
                 ROWS * TILE // 2 + 20)
            )

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    GameEngine().run()
