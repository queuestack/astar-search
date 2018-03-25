import queue

class Node(object):
    def __init__(self, y: int, x: int, back_cost: int, forward_cost: int, parent):
        self.y = y
        self.x = x
        self.back_cost = back_cost
        self.forward_cost = forward_cost
        self.cost = back_cost + 2 * forward_cost
        self.parent = parent

    def __lt__(self, other_node):
        return self.cost < other_node.cost

    def __eq__(self, other_node):
        return self.cost == other_node.cost

    def set_back_cost(self, back_cost):
        self.back_cost = back_cost
        self.cost = self.back_cost + 2 * self.forward_cost


class Maze(object):
    def __init__(self, cells: list, y_start: int, x_start: int, y_end: int, x_end: int):
        self.LEFT = 0
        self.RIGHT = 1
        self.UP = 2
        self.DOWN = 3

        self.ROAD = 0
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
        self.nodes = [[Node(y, x, 0, self.get_forward_cost(y, x), None) for x in range(width)]
                      for y in range(height)]
        self.q = queue.PriorityQueue()
        self.queued = []

    def update_cost(self):
        for i, (cost, tie, node) in enumerate(self.queued):
            new_backward_cost = self.get_backward_cost(node)
            node.set_back_cost(new_backward_cost)
            self.queued[i] = (node.cost, tie, node)

    def search_answer(self):
        start_back_cost = 0
        start_forward_cost = self.get_forward_cost(self.y_start, self.x_start)
        root_node = Node(self.y_start, self.x_start, start_back_cost, start_forward_cost, None)
        self.q.put((root_node.cost, self.get_tie_breaker(self.y_start, self.x_start), root_node))
        #heapq.heappush(self.queued, (root_node.cost, self.get_tie_breaker(self.y_start, self.x_start), root_node))

        while not self.q.empty():
        #while len(self.queued) > 0:
            current_node = self.dequeue()

            if self.is_arrived(current_node):
                print("Finish")
                return

            if self.is_reachable(current_node, self.LEFT):
                self.enqueue(current_node, self.LEFT)
            if self.is_reachable(current_node, self.RIGHT):
                self.enqueue(current_node, self.RIGHT)
            if self.is_reachable(current_node, self.UP):
                self.enqueue(current_node, self.UP)
            if self.is_reachable(current_node, self.DOWN):
                self.enqueue(current_node, self.DOWN)

    def dequeue(self) -> Node:
        current_cost, current_tie_index, current_node = self.q.get()
        #current_cost, current_tie_index, current_node = heapq.heappop(self.queued)
        self.visit_cells[current_node.y][current_node.x] = True
        print("Move to (" + str(current_node.y) + ", " + str(current_node.x) +
              ") backward cost : " + str(current_node.back_cost) +
              ", forward cost : " + str(current_node.forward_cost) +
              ", total cost: " + str(current_cost))

        self.y = current_node.y
        self.x = current_node.x
        #self.update_cost()
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

        back_cost = self.get_backward_cost(node)
        forward_cost = self.get_forward_cost(y, x)

        self.nodes[y][x] = Node(y, x, back_cost, forward_cost, node)
        self.q.put((self.nodes[y][x].cost, self.get_tie_breaker(y, x), self.nodes[y][x]))
        #heapq.heappush(self.queued, (self.nodes[y][x].cost, self.get_tie_breaker(y, x), self.nodes[y][x]))
        self.queue_cells[y][x] = True
    
    def get_backward_cost(self, node) -> int:
        return node.back_cost + 1
        #return self.get_manhattan_distance(self.y, self.x, y, x)

    def get_forward_cost(self, y, x) -> int:
        # Use Manhattan distance
        return self.get_manhattan_distance(self.y_end, self.x_end, y, x)

    def get_manhattan_distance(self, y2, x2, y1, x1):
        return abs(y2 - y1) + abs(x2 - x1)

    def get_tie_breaker(self, y, x) -> int:
        return self.get_euclidean_disatnce(y, x)
        #return -1 * self.get_adjacent_num(y, x)

    def get_euclidean_disatnce(self, y, x) -> int:
        return (self.y_end - y)**2 + (self.x_end - x)**2

    def get_adjacent_num(self, y, x) -> int:
        num = 0
        width = len(self.cells[0])
        height = len(self.cells)

        if((x - 1 >= 0) and
                (self.is_queued(y, x - 1) == False) and
                (self.is_visited(y, x - 1) == False) and
                (self.cells[y][x-1] != self.WALL)):
            num += 1
        if((x + 1 <= width - 1) and
                (self.is_queued(y, x + 1) == False) and
                (self.is_visited(y, x + 1) == False) and
                (self.cells[y][x+1] != self.WALL)):
            num += 1
        if((y - 1 >= 0) and
                (self.is_queued(y - 1, x) == False) and
                (self.is_visited(y - 1, x) == False) and
                (self.cells[y-1][x] != self.WALL)):
            num += 1
        if((y + 1 <= height - 1) and
                (self.is_queued(y + 1, x) == False) and
                (self.is_visited(y + 1, x) == False) and
                (self.cells[y+1][x] != self.WALL)):
            num += 1

        return num

    def is_reachable(self, node, direction) -> bool:
        y = node.y
        x = node.x
        width = len(self.cells[0])
        height = len(self.cells)

        if direction == self.LEFT:
            return (x - 1 >= 0) and\
                   (self.is_queued(y, x - 1) == False) and\
                   (self.is_visited(y, x - 1) == False) and\
                   (self.cells[y][x-1] != self.WALL)
        elif direction == self.RIGHT:
            return (x + 1 <= width - 1) and \
                   (self.is_queued(y, x + 1) == False) and\
                   (self.is_visited(y, x + 1) == False) and\
                   (self.cells[y][x+1] != self.WALL)
        elif direction == self.UP:
            return (y - 1 >= 0) and \
                   (self.is_queued(y - 1, x) == False) and\
                   (self.is_visited(y - 1, x) == False) and\
                   (self.cells[y-1][x] != self.WALL)
        elif direction == self.DOWN:
            return (y + 1 <= height - 1) and \
                   (self.is_queued(y + 1, x) == False) and\
                   (self.is_visited(y + 1, x) == False) and\
                   (self.cells[y+1][x] != self.WALL)

        return False

    def is_queued(self, y, x) -> bool:
        return self.queue_cells[y][x]

    def is_visited(self, y, x) -> bool:
        return self.visit_cells[y][x]

    def is_arrived(self, node) -> bool:
        return (node.y == self.y_end) and (node.x == self.x_end)


def main():
    file = open('input.txt', 'r')
    T = file.readline()
    for i in range(int(T)):
        # read maze files
        file.readline() # read new line
        height, width = file.readline().split()
        height = int(height)
        width = int(width)

        y_start = 0
        x_start = 0
        y_end = height - 1
        x_end = width - 1

        cells = []
        for h in range(int(height)):
            row = file.readline().strip().split(',')
            row = [int(element) for element in row]
            cells.append(row)

        maze = Maze(cells, y_start, x_start, y_end, x_end)
        maze.search_answer()

    file.close()


if __name__ == '__main__':
    main()
