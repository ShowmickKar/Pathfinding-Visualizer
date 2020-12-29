import math
import pygame
from queue import PriorityQueue
from node import Node

HEIGHT, WIDTH = 900, 900


def reconstructPath(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.makePath()
        draw()


def huresticFunction(intermediate_node, end_node):
    x1, y1 = intermediate_node
    x2, y2 = end_node
    return abs(x1 - x2) + abs(y1 - y2)


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