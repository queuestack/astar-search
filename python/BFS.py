"""
BFS uses queue, so first in first out
BFS does not need cost unlike A* search
"""

import queue


class Node(object):
    def __init__(self, y: int, x: int, parent):
        self.y = y
        self.x = x
        self.parent = parent


class BFS(object):
    def __init__(self, cells: list, y_start: int, x_start: int, y_end: int, x_end: int):
        self.LEFT = 0
        self.RIGHT = 1
        self.UP = 2
        self.DOWN = 3

        self.WALL = 1

        self.cells = cells
        self.y_start = y_start
        self.x_start = x_start
        self.y_end = y_end
        self.x_end = x_end
        self.y = y_start
        self.x = x_start

        width = len(cells[0])
        height = len(cells)
        self.queue_cells = [[False for x in range(width)] for y in range(height)]
        self.visit_cells = [[False for x in range(width)] for y in range(height)]
        self.nodes = [[Node(y, x, None) for x in range(width)]
                      for y in range(height)]
        self.q = queue.Queue()
        self.queued = []
        self.explored =[]

    def search_answer(self):
        # Start search from root node where is (0, 0)
        # Breadth First search by using queue
        root_node = Node(self.y_start, self.x_start, None)
        self.q.put(root_node)

        while not self.q.empty():
            current_node = self.dequeue()

            if self.is_arrived(current_node):
                # Print optimal paths
                path_node = current_node
                paths = []
                while path_node.parent is not None:
                    paths.insert(0, (path_node.y, path_node.x))
                    path_node = path_node.parent
                paths.insert(0, (path_node.y, path_node.x))

                for path in paths:
                    print(path, end='')

                print()
                print()

                return self.explored, paths

            if self.is_reachable(current_node, self.LEFT):
                self.enqueue(current_node, self.LEFT)
            if self.is_reachable(current_node, self.RIGHT):
                self.enqueue(current_node, self.RIGHT)
            if self.is_reachable(current_node, self.UP):
                self.enqueue(current_node, self.UP)
            if self.is_reachable(current_node, self.DOWN):
                self.enqueue(current_node, self.DOWN)

    def dequeue(self) -> Node:
        current_node = self.q.get()
        self.visit_cells[current_node.y][current_node.x] = True
        self.explored.append(str(current_node.y) + " " + str(current_node.x))
        print(str(current_node.y) + " " + str(current_node.x))

        self.y = current_node.y
        self.x = current_node.x
        return current_node

    def enqueue(self, node, direction):
        y = node.y
        x = node.x

        if direction == self.LEFT:
            x = x - 1
        elif direction == self.RIGHT:
            x = x + 1
        elif direction == self.UP:
            y = y - 1
        elif direction == self.DOWN:
            y = y + 1

        self.nodes[y][x] = Node(y, x, node)
        self.q.put(self.nodes[y][x])
        self.queue_cells[y][x] = True

    def is_reachable(self, node, direction) -> bool:
        y = node.y
        x = node.x
        width = len(self.cells[0])
        height = len(self.cells)

        # Check out of index error, queued or visited cell, and wall
        if direction == self.LEFT:
            return (x - 1 >= 0) and \
                   (self.is_queued(y, x - 1) == False) and \
                   (self.is_visited(y, x - 1) == False) and \
                   (self.cells[y][x - 1] != self.WALL)
        elif direction == self.RIGHT:
            return (x + 1 <= width - 1) and \
                   (self.is_queued(y, x + 1) == False) and \
                   (self.is_visited(y, x + 1) == False) and \
                   (self.cells[y][x + 1] != self.WALL)
        elif direction == self.UP:
            return (y - 1 >= 0) and \
                   (self.is_queued(y - 1, x) == False) and \
                   (self.is_visited(y - 1, x) == False) and \
                   (self.cells[y - 1][x] != self.WALL)
        elif direction == self.DOWN:
            return (y + 1 <= height - 1) and \
                   (self.is_queued(y + 1, x) == False) and \
                   (self.is_visited(y + 1, x) == False) and \
                   (self.cells[y + 1][x] != self.WALL)

        return False

    def is_queued(self, y, x) -> bool:
        return self.queue_cells[y][x]

    def is_visited(self, y, x) -> bool:
        return self.visit_cells[y][x]

    def is_arrived(self, node) -> bool:
        return (node.y == self.y_end) and (node.x == self.x_end)


def main():
    input_file = open('input.txt', 'r')
    output_file = open("output.txt", "w")
    T = input_file.readline()
    for i in range(int(T)):
        # read maze files T times
        input_file.readline()
        height, width = input_file.readline().split()
        height = int(height)
        width = int(width)

        y_start = 0
        x_start = 0
        y_end = height - 1
        x_end = width - 1

        cells = []
        for h in range(int(height)):
            row = input_file.readline().strip().split(',')
            row = [int(element) for element in row]
            cells.append(row)

        bfs = BFS(cells, y_start, x_start, y_end, x_end)
        explored, paths = bfs.search_answer()

        for ele in explored:
            output_file.write(str(ele) + "\n")

        for path in paths:
            output_file.write(str(path))
        output_file.write("\n\n")

    output_file.close()
    input_file.close()


if __name__ == '__main__':
    main()
