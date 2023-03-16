import pygame as pg
from heapq import *


def get_circle(x, y):
    return (x * TILE + TILE // 2, y * TILE + TILE // 2), TILE // 4


def get_neighbours(x, y):
    check_neighbour = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]#, [-1, -1], [1, -1], [1, 1], [-1, 1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]


def get_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.circle(sc, pg.Color('red'), *get_circle(grid_x, grid_y))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


def heuristic(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])

def dijkstra(start, goal, graph):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break

        neighbours = graph[cur_node]
        for neighbour in neighbours:
            neigh_cost, neigh_node = neighbour
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node
    return visited


cols, rows = 23, 13
TILE = 70

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()

grid = ['22112222299222222221222',
        '11119222222229911111229',
        '11119991111119111111222',
        '11111199111199111111112',
        '01111111122191111111999',
        '11199111122211111111111',
        '11119111992211119111111',
        '11119911192211299111111',
        '11111911199111291111111',
        '11111111119122991111112',
        '11111111111112911111129',
        '11222111111112921111229',
        '11292111112292111122299']
grid = [[int(char) for char in string ] for string in grid]

graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        graph[(x, y)] = graph.get((x, y), []) + get_neighbours(x, y)

start = (0, 7)
goal = start
queue = []
heappush(queue, (0, start))
visited = {start: None}

bg = pg.image.load('test1.png').convert()
bg = pg.transform.scale(bg, (cols * TILE, rows * TILE))
while True:

    sc.blit(bg, (0, 0))


    mouse_pos = get_click_mouse_pos()
    if mouse_pos:
        visited = dijkstra(start, mouse_pos, graph)
        goal = mouse_pos


    path_head, path_segment = goal, goal
    while path_segment and path_segment in visited:
        pg.draw.circle(sc, pg.Color('black'), *get_circle(*path_segment))
        path_segment = visited[path_segment]
    pg.draw.circle(sc, pg.Color('green'), *get_circle(*start))
    pg.draw.circle(sc, pg.Color('pink'), *get_circle(*path_head))


    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(30)