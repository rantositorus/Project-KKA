from map import Map


class State:
    def __init__(self, person: tuple, butters=[]):
        self.person = person
        self.butters = butters

    def __eq__(self, other):
        return self.butters == other.butters and self.person == other.person

    def __str__(self):
        return (
            '"person at: '
            + str(self.person)
            + " Butters at: "
            + str(self.butters)
            + '"'
        )

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        h = hash(self.person)
        for i in self.butters:
            h += hash(i)
        return h

    @staticmethod
    def successor(state: "State", map_object: Map) -> list[tuple["State", tuple, int]]:
        map_array = map_object.map
        points = map_object.points
        w, h = map_object.w, map_object.h
        next_states = []
        person_y, person_x = state.person[0], state.person[1]

        def try_move_person(y: int, x: int):
            """Tries to move person and saves new state in next_states array."""

            # Checking diagonal movement
            if x * y != 0:
                raise Exception("Diagonal moving is not allowed.")

            # Checking bounds
            if map_object.check_out_of_bounds(person_y + y, person_x + x):
                return

            # Checking blocks
            if map_object.is_block(person_y + y, person_x + x):
                return

            # There is no butters around
            next_states.append(
                (
                    State((person_y + y, person_x + x)),
                    (y, x),
                    max(
                        int(map_array[person_y + y][person_x + x]),
                        int(map_array[person_y][person_x]),
                    ),
                )
            )

        try_move_person(1, 0)
        try_move_person(0, 1)
        try_move_person(-1, 0)
        try_move_person(0, -1)

        return next_states

    @staticmethod
    def is_goal(state: "State", points: list[tuple]):
        return state.person in points
