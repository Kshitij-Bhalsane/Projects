import pygame
import math
from queue import PriorityQueue, Queue

pygame.init()

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Visualizer")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self): return self.color == RED
    def is_open(self): return self.color == GREEN
    def is_barrier(self): return self.color == BLACK
    def is_start(self): return self.color == ORANGE
    def is_end(self): return self.color == TURQUOISE

    def reset(self): self.color = WHITE
    def make_start(self): self.color = ORANGE
    def make_closed(self): self.color = RED
    def make_open(self): self.color = GREEN
    def make_barrier(self): self.color = BLACK
    def make_end(self): self.color = TURQUOISE
    def make_path(self): self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other): return False


def h(p1, p2):  # Heuristic for A*
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


# ----- ALGORITHMS -----

def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def bfs(draw, grid, start, end):
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {start}

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.put(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def dfs(draw, grid, start, end):
    stack = [start]
    came_from = {}
    visited = {start}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def dijkstra(draw, grid, start, end):
    distances = {spot: float("inf") for row in grid for spot in row}
    distances[start] = 0
    visited = set()
    pq = PriorityQueue()
    pq.put((0, start))
    came_from = {}

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_distance, current = pq.get()

        if current in visited:
            continue
        visited.add(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            new_dist = distances[current] + 1
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                pq.put((new_dist, neighbor))
                came_from[neighbor] = current
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


# ----- UI + GRID -----

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([Spot(i, j, gap, rows) for j in range(rows)])
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)

    font = pygame.font.SysFont("Arial", 16)
    pygame.display.update()



def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    return y // gap, x // gap


def algorithm_menu(win, width):
    pygame.font.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 32)
    small_font = pygame.font.SysFont("Arial", 20)

    # Color scheme
    WHITE = (245, 245, 245)
    BUTTON_COLOR = (230, 230, 230)
    BUTTON_HOVER = (200, 200, 200)
    TEXT_COLOR = (70, 70, 70)
    BORDER = (180, 180, 180)

    options = ["A*", "BFS", "DFS", "Dijkstra"]
    selected = None

    # Layout settings
    button_width = 180
    button_height = 50
    spacing_x = 40
    spacing_y = 30

    start_y = 320  # Where buttons start vertically

    while selected is None:
        win.fill(WHITE)

        # Title
        title = font.render("Choose an Algorithm", True, TEXT_COLOR)
        win.blit(title, (width // 2 - title.get_width() // 2, 60))

        # Instructions
        instructions = [
            "Click a button below to begin.",
            "ESC during visualization to return here.",
            "",
            "Controls:",
            "LMB: Place Start, End, and Barriers",
            "RMB: Remove Node",
            "SPACE: Start Pathfinding",
            "C: Clear Grid",
            "ESC: Back to Algorithm Menu"
        ]
        for i, line in enumerate(instructions):
            instr_text = small_font.render(line, True, TEXT_COLOR)
            win.blit(instr_text, (width // 2 - instr_text.get_width() // 2, 110 + i * 22))

        mouse_pos = pygame.mouse.get_pos()

        # Draw buttons in 2x2 layout
        for i, option in enumerate(options):
            col = i % 2
            row = i // 2
            total_width = button_width * 2 + spacing_x
            x = width // 2 - total_width // 2 + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)

            rect = pygame.Rect(x, y, button_width, button_height)
            hovered = rect.collidepoint(mouse_pos)

            pygame.draw.rect(win, BUTTON_HOVER if hovered else BUTTON_COLOR, rect, border_radius=12)
            pygame.draw.rect(win, BORDER, rect, 2, border_radius=12)

            text = font.render(option, True, TEXT_COLOR)
            win.blit(text, (x + button_width // 2 - text.get_width() // 2, y + button_height // 2 - text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, option in enumerate(options):
                    col = i % 2
                    row = i // 2
                    total_width = button_width * 2 + spacing_x
                    x = width // 2 - total_width // 2 + col * (button_width + spacing_x)
                    y = start_y + row * (button_height + spacing_y)
                    rect = pygame.Rect(x, y, button_width, button_height)
                    if rect.collidepoint(mouse_pos):
                        selected = option

        pygame.display.update()
        clock.tick(60)

    return selected




def main(win, width):
    algo_name = algorithm_menu(win, width)
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None

    algo_name = algorithm_menu(win, width)

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    if algo_name == "A*":
                        astar(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algo_name == "DFS":
                        dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algo_name == "BFS":
                        bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algo_name == "Dijkstra":
                        dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start, end = None, None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_ESCAPE:
                    # Go back to menu
                    start, end = None, None
                    grid = make_grid(ROWS, width)
                    algo_name = algorithm_menu(win, width)

    pygame.quit()


main(WIN, WIDTH)
