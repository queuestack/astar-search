"""
Start A* search from root node where is (0, 0), the goal is (width - 1, height - 1)
Priority search by using heap queue
Priority is decided by cost, which is backward cost + forward cost
Cost = backward cost + forward cost
Backward cost is the number of step
Backward cost is updated if smaller backward cost is found
Forward cost is the Manhattan distance between current location and destination
Tie breaker uses Euclidean distance
Tie breaker is used when different nodes have same Manhattan distance

Each node has their location(y, x), costs, and parent node.
By following parent node, you can get optimal solution.
"""

import heapq


class Node(object):
    def __init__(self, y, x, back_cost, forward_cost, parent):
        """
        Initialize node
        :param y: <int>, y coordinates 
        :param x: <int>, x coordinates
        :param back_cost: <int>, backward cost
        :param forward_cost: <int>, forward cost
        :param parent: <Node>, parent node
        """
        self.y = y
        self.x = x
        self.back_cost = back_cost
        self.forward_cost = forward_cost
        self.cost = back_cost + forward_cost
        self.parent = parent

    def __lt__(self, other_node):
        """
        Override function for priority comparison 
        :param other_node: <Node>
        :return: <bool>
        """
        return self.cost < other_node.cost

    def __eq__(self, other_node):
        """
        Override function for priority comparison 
        :param other_node: <Node>
        :return: <bool>
        """
        return self.cost == other_node.cost


class AStar(object):
    def __init__(self, cells, y_start, x_start, y_end, x_end):
        """

        :param cells: <list>, 0 is road, and 1 is wall in list
        :param y_start: <int>, 0 in this homework
        :param x_start: <int>, 0 in this homework
        :param y_end: <int>, height - 1 in this homework
        :param x_end: <int>, width - 1 in this homework
        """
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
        self.nodes = [[Node(y, x, 0, self.get_forward_cost(y, x), None) for x in range(width)]
                      for y in range(height)]
        self.queued = []
        self.explored = []

    def search_answer(self):
        """
        Search answer from starting point (0, 0)
        :return: <None>, print the explored node, and optimal path
        """

        # Start from starting point (0, 0)
        start_back_cost = 0
        start_forward_cost = self.get_forward_cost(self.y_start, self.x_start)
        root_node = Node(self.y_start, self.x_start, start_back_cost, start_forward_cost, None)
        heapq.heappush(self.queued, (root_node.cost, self.get_tie_breaker(self.y_start, self.x_start), root_node))

        # Search answer until queue is empty or answer is found
        while len(self.queued) > 0:
            current_node = self.dequeue()

            # End search when the goal is found
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

            # Search adjacent nodes
            self.search_adjacent_nodes(current_node)

    def search_adjacent_nodes(self, current_node):
        """
        Search adjacent nodes and queue if they are reachable
        :param current_node: <Node>
        :return: <None>, queue the adjacent nodes
        """
        if self.is_reachable(current_node, self.LEFT):
            self.enqueue(current_node, self.LEFT)
        if self.is_reachable(current_node, self.RIGHT):
            self.enqueue(current_node, self.RIGHT)
        if self.is_reachable(current_node, self.UP):
            self.enqueue(current_node, self.UP)
        if self.is_reachable(current_node, self.DOWN):
            self.enqueue(current_node, self.DOWN)

    def dequeue(self) -> Node:
        """
        Explore the node based on their priority
        Cost is Manhattan distance
        Tie index is Euclidean distance, which is used for the case the cost is same
        Node is explored node

        Change the boolean table visit cells where the node visited
              
        :return: <Node>, explored Node
        """

        current_cost, current_tie_index, current_node = heapq.heappop(self.queued)
        self.visit_cells[current_node.y][current_node.x] = True
        self.explored.append(str(current_node.y) + " " + str(current_node.x))
        print(str(current_node.y) + " " + str(current_node.x))

        self.y = current_node.y
        self.x = current_node.x
        return current_node

    def enqueue(self, node, direction):
        """
        Calculate cost, and add or update the node
        Change the boolean table queue cells where the node queued

        :param node: <Node>, current node, next node is combined with current node and direction
        :param direction: <int>, LEFT = 0, RIGHT = 1, TOP = 2, BOTTOM = 3
        :return: <None>
        """
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

        old_back_cost = self.nodes[y][x].back_cost
        back_cost = self.get_backward_cost(node)
        forward_cost = self.get_forward_cost(y, x)

        # Update cost by removing old cost node from queue if new explored cost is smaller than old cost
        if (self.is_queued(y, x) or self.is_visited(y, x)) and back_cost < old_back_cost:
            prev_el_set = (self.nodes[y][x].cost, self.get_tie_breaker(y, x), self.nodes[y][x])
            if self.queued.count(prev_el_set) > 0:
                self.queued.remove(prev_el_set)

        # Add new node to queue
        self.nodes[y][x] = Node(y, x, back_cost, forward_cost, node)
        heapq.heappush(self.queued, (self.nodes[y][x].cost, self.get_tie_breaker(y, x), self.nodes[y][x]))
        self.queue_cells[y][x] = True

    def get_backward_cost(self, node):
        """
        Get backward cost by using the number of search
        :param node: <Node>, current node
        :return: <int>, current backward cost + 1
        """
        return node.back_cost + 1

    def get_forward_cost(self, y, x):
        """
        Get forward cost by using Manhattan distance
        :param y: <int>
        :param x: <int>
        :return: <int>, manhattan distance between current node and goal node
        """
        return self.get_manhattan_distance(self.y_end, self.x_end, y, x)

    def get_tie_breaker(self, y, x):
        """
        Get backward cost by using Euclidean distance for tie break when the Manhattan distance is same
        :param y: <int>
        :param x: <int>
        :return: <int>, Euclidean distance between current node and goal node
        """
        return self.get_euclidean_disatnce(self.y_end, self.x_end, y, x)

    def get_manhattan_distance(self, y2, x2, y1, x1):
        return abs(y2 - y1) + abs(x2 - x1)

    def get_euclidean_disatnce(self, y2, x2, y1, x1):
        return (y2 - y1)**2 + (x2 - x1)**2

    def is_reachable(self, node, direction):
        """
        Check out of index error, and the cell is not wall
        If the cell is not in queue and not visited, then return true
        If the cell is in queue or visited, return true when the new cost is smaller than previous cost
        :param node: <Node>, current node
        :param direction: <int>, LEFT = 0, RIGHT = 1, TOP = 2, BOTTOM = 3
        :return: <bool>, True if the next node is reachable
        """
        y = node.y
        x = node.x
        width = len(self.cells[0])
        height = len(self.cells)

        if direction == self.LEFT:
            if (x - 1 >= 0) and (self.cells[y][x-1] != self.WALL):
                if (self.is_visited(y, x-1) is False) and (self.is_queued(y, x - 1) is False):
                    return True
                else:
                    return self.get_backward_cost(node) < self.nodes[y][x-1].back_cost

        elif direction == self.RIGHT:
            if (x + 1 <= width - 1) and (self.cells[y][x+1] != self.WALL):
                if (self.is_visited(y, x+1) is False) and (self.is_queued(y, x+1) is False):
                    return True
                else:
                    return self.get_backward_cost(node) < self.nodes[y][x+1].back_cost

        elif direction == self.UP:
            if (y - 1 >= 0) and (self.cells[y-1][x] != self.WALL):
                if (self.is_visited(y-1, x) is False) and (self.is_queued(y-1, x) is False):
                    return True
                else:
                    return self.get_backward_cost(node) < self.nodes[y-1][x].back_cost

        elif direction == self.DOWN:
            if (y + 1 <= height - 1) and (self.cells[y+1][x] != self.WALL):
                if (self.is_visited(y+1, x) is False) and (self.is_queued(y+1, x) is False):
                    return True
                else:
                    return self.get_backward_cost(node) < self.nodes[y+1][x].back_cost

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

        a_star = AStar(cells, y_start, x_start, y_end, x_end)
        explored, paths = a_star.search_answer()

        for ele in explored:
            output_file.write(str(ele) + "\n")

        for path in paths:
            output_file.write(str(path))
        output_file.write("\n\n")

    output_file.close()
    input_file.close()


if __name__ == '__main__':
    main()
