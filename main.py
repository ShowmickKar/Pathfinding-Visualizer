import math
import random
import pygame
from queue import PriorityQueue

HEIGHT, WIDTH = 800, 800
window = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("A* Pathfinding visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
CYAN = (0, 255, 255)


class Node:
    def __init__(self, row, column, width, total_rows):
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * width
        self.color = WHITE
        self.width = width
        self.neighbors = []
        self.total_rows = total_rows

    def getPosition(self):
        return self.row, self.column

    def isCLosed(self):
        return self.color == RED

    def isVisiting(self):
        return self.color == GREEN

    def isObstacle(self):
        return self.color == BLACK

    def isStartNode(self):
        return self.color == ORANGE

    def isEndNode(self):
        return self.color == CYAN

    def resetNode(self):
        self.color = WHITE

    def makeStartNode(self):
        self.color = ORANGE

    def makeEndNode(self):
        self.color = CYAN

    def makeVisited(self):
        self.color = RED

    def makeVisiting(self):
        self.color = GREEN

    def makeObstacle(self):
        self.color = BLACK

    def makePath(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbors(self, grid):
        self.neighbors = []
        if (
            self.row < self.total_rows - 1
            and not grid[self.row + 1][self.column].isObstacle()
        ):
            self.neighbors.append(grid[self.row + 1][self.column])
        if self.row > 0 and not grid[self.row - 1][self.column].isObstacle():
            self.neighbors.append(grid[self.row - 1][self.column])
        if (
            self.column < self.total_rows - 1
            and not grid[self.row][self.column + 1].isObstacle()
        ):
            self.neighbors.append(grid[self.row][self.column + 1])
        if self.column > 0 and not grid[self.row][self.column - 1].isObstacle():
            self.neighbors.append(grid[self.row][self.column - 1])

    def __lt__(self, other):
        return False


def reconstructPath(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.makePath()
        draw()


def aStar(draw, grid, start, end):
    count = 0
    priority_queue = PriorityQueue()
    priority_queue.put((0, count, start))
    came_from = {}
    g_score = {node: math.inf for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: math.inf for row in grid for node in row}
    f_score[start] = huresticFunction(start.getPosition(), end.getPosition())
    open_set = {start}
    while not priority_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = priority_queue.get()[2]
        open_set.remove(current)
        if current == end:
            reconstructPath(came_from, end, draw)
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + huresticFunction(
                    neighbor.getPosition(), end.getPosition()
                )
                if neighbor not in open_set:
                    count += 1
                    priority_queue.put((f_score[neighbor], count, neighbor))
                    open_set.add(neighbor)
                    if neighbor != end:
                        neighbor.makeVisiting()
        draw()
        if current != start:
            current.makeVisited()
    return False


def dijkstra(draw, grid, start, end):
    visited = {node: False for row in grid for node in row}
    distance = {node: math.inf for row in grid for node in row}
    distance[start] = 0
    came_from = {}
    priority_queue = PriorityQueue()
    priority_queue.put((0, start))
    while not priority_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = priority_queue.get()[1]

        if visited[current]:
            continue
        visited[current] = True
        if current == end:
            reconstructPath(came_from, end, draw)
            return True
        if current != start:
            current.makeVisited()
        for neighbor in current.neighbors:
            weight = 1
            if distance[current] + weight < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = distance[current] + weight
                priority_queue.put((distance[neighbor], neighbor))
            if neighbor != end and neighbor != start and not visited[neighbor]:
                neighbor.makeVisiting()
        draw()
    return False


def algorithm(draw, grid, start, end):
    # aStar(draw, grid, start, end)
    dijkstra(draw, grid, start, end)


def huresticFunction(intermediate_node, end_node):
    x1, y1 = intermediate_node
    x2, y2 = end_node
    return abs(x1 - x2) + abs(y1 - y2)


def buildGrid(row, width):
    grid = []
    node_width = width // row
    for i in range(row):
        grid.append([])
        for j in range(row):
            grid[i].append(Node(i, j, node_width, row))
    return grid


def drawGridLines(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(window, GREY, (i * gap, 0), (i * gap, width))


def draw(window, grid, rows, width):
    for row in grid:
        for node in row:
            node.draw(window)
    drawGridLines(window, rows, width)
    pygame.display.update()


def getClickedPosition(position, rows, width):
    gap = width // rows
    x, y = position
    row, column = x // gap, y // gap
    return (row, column)


def main(window, WIDTH):
    ROWS = 50
    grid = buildGrid(ROWS, WIDTH)

    start, end = None, None
    started = False
    run = True

    started = False
    while run:
        draw(window, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, column = getClickedPosition(position, ROWS, WIDTH)
                node = grid[row][column]
                if not start and node != end:
                    start = node
                    start.makeStartNode()
                elif not end and node != start:
                    end = node
                    end.makeEndNode()
                elif node != start and node != end:
                    node.makeObstacle()

            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, column = getClickedPosition(position, ROWS, WIDTH)
                node = grid[row][column]
                node.resetNode()
                if node == start:
                    start = None
                if node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)
                    algorithm(lambda: draw(window, grid, ROWS, WIDTH), grid, start, end)
                    started = False
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = buildGrid(ROWS, WIDTH)
                    draw(window, grid, ROWS, WIDTH)

    pygame.quit()


main(window, WIDTH)
