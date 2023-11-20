from map import Map

class State:
    def __init__(self, person: tuple) -> None:
        self.person = person
        # self.lever = lever

    def __eq__(self, other):
        return self.person == other.person
    
    def __str__(self):
        return '"Person at: ' + str(self.person)
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        h = hash(self.person)
        # for i in self.lever:
        #     h += hash(i)
        return h
    
    @staticmethod
    def successor(state: 'State', map_object: Map) -> list[tuple['State', tuple, int]]:
        map_array = map_object.map
        points = map_object.points
        # levers = map_object.levers
        mech_walls = map_object.mech_walls
        w, h = map_object.w, map_object.h
        next_states = []
        person_y, person_x = state.person[0], state.person[1]

        def try_move_person(y: int, x: int):
            if x*y != 0:
                raise Exception("Bergerak secara diagonal tidak diizinkan!")
            
            if map_object.check_out_of_bounds(person_y + y, person_x + x):
                return
            
            if map_object.is_block(person_y + y, person_x + x):
                return
            
            next_states.append((
                State((person_y + y, person_x + x)),
                (y,x),
                max(int(map_object.map[person_y + y][person_x + x]), int(map_object.map[person_y][person_x]))
            ))
        try_move_person(1, 0)
        try_move_person(0, 1)
        try_move_person(-1, 0)
        try_move_person(0, -1)

        return next_states

    @staticmethod
    def predecessor(state: 'State', map_object: Map) -> list[tuple['State', tuple, int]]:
        next_states = []
        person_y, person_x = state.person[0], state.person[1]

        def try_move_person(y: int, x: int):
            if x*y != 0:
                raise Exception("Bergerak secara diagonal tidak diizinkan!")
            
            if map_object.check_out_of_bounds(person_y + y, person_x + x):
                return
            
            if map_object.is_block(person_y + y, person_x + x):
                return
            
            next_states.append((
                State((person_y + y, person_x + x)),
                (y,x),
                max(int(map_object.map[person_y + y][person_x + x]), int(map_object.map[person_y][person_x]))
            ))
        try_move_person(1, 0)
        try_move_person(0, 1)
        try_move_person(-1, 0)
        try_move_person(0, -1)

        return next_states

    @staticmethod
    def is_goal(state: 'State', points: list[tuple]):
        for person in state.person:
            if person not in points:
                return False
        return True