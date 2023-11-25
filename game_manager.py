from map import Map
from FileIO import FileIO
from constants import Consts
from screen_manager import Display
from state import State
from node import Node
from heap_hashtable import MinHeap
import time


class GameManager:
    map: Map
    init_state: State
    display: Display

    def __init__(self):
        self.map, self.init_state = self.parse_map()
        # After parsing map it's time to start pygame
        self.display = Display(self.map)

    def start_search(self, search_type: str) -> (list[State], int, int):
        """Chooses a search between all and returns its result list.
        :param search_type Search algorithm type
        :returns The result of search"""

        result = self.__getattribute__(search_type + "_search")()

        # Putting path to goal in list
        if search_type in ["bd_bfs", "reverse_bfs"]:
            return result
        else:
            result_list = GameManager.extract_path_list(result)
            result_list.pop()
            result_list.reverse()
            return result_list, result.depth, result.path_cost

    def display_states(self, states_list: list[State]) -> None:
        """Gets a list of states and displays it into display object.
        :param states_list List of states to show"""

        if len(states_list) <= 0:
            print("There is no way")
            return

        self.display.update(self.init_state)  # Starting display
        self.display.begin_display()

        for state in states_list:
            time.sleep(Consts.STEP_TIME)
            self.display.update(state)

    def a_star_search(self) -> Node:
        """Performs an A* search from initial state to goal state.
        :returns The node containing the goal state."""

        def euclid_distance(point1: tuple[int, int], point2: tuple[int, int]) -> float:
            """Finds euclid distance between two points."""
            return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

        def manhattan_distance(point1: tuple[int, int], point2: tuple[int, int]) -> int:
            """Finds manhattan distance between to points."""
            d1 = point1[0] - point2[0]
            d2 = point1[1] - point2[1]
            if d1 < 0:
                d1 *= -1
            if d2 < 0:
                d2 *= -1
            return d1 + d2

        def heuristic(state: State) -> int:
            """The heuristic function which evaluates steps from a state to goal.
            :param state The state to evaluate."""

            sum_of_distances = 0
            for point in self.map.points:
                d = manhattan_distance(point, state.person)
                sum_of_distances += d

            return sum_of_distances

        Node.heuristic = heuristic  # Setting all nodes heuristic functions

        heap = MinHeap()  # Beginning of a star search
        visited = set()
        root_node = Node(self.init_state)
        heap.add(root_node)
        while not heap.is_empty():
            node = heap.pop()

            # Checking goal state
            if State.is_goal(node.state, self.map.points):
                return node

            if node.state not in visited:
                visited.add(node.state)
            else:
                continue

            # A* search
            actions = State.successor(node.state, self.map)
            for child in node.expand(actions):
                heap.add(child)

    @staticmethod
    def parse_map() -> (Map, State):
        """Uses map file to create a map object in the game.
        :returns The map object and the initial state"""

        map_array = FileIO.read_line_by_line(Consts.MAP_FILE)
        sizes = map_array.pop(0)
        h, w = int(sizes[0]), int(sizes[1])
        map_object = Map(h, w)
        # Variables to read from map
        points = []
        person = (0, 0)
        for j, row in enumerate(map_array):
            for i, col in enumerate(row):
                if len(col) > 1:  # If there is an object in map
                    if col[1] == "p":
                        points.append((j, i))
                    elif col[1] == "r":
                        person = (j, i)
                    row[i] = col[0]

            map_object.append_row(row)  # Append row to map

        map_object.set_points(points)
        return map_object, State(person)

    @staticmethod
    def extract_path_list(node: Node) -> list[State]:
        result_list = []
        watchdog = 0
        while node is not None:
            watchdog += 1
            if watchdog > 1000:
                raise Exception("Watchdog limit exceeded")
            result_list.append(node.state)
            node = node.parent

        return result_list

    @staticmethod
    def state_in_list_of_nodes(state: State, nodes_list: list[Node]) -> bool:
        for node in nodes_list:
            if node.state == state:
                return True
        return False
