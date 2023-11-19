from map import Map

class State:
    def __init__(self, person: tuple, lever=[]) -> None:
        self.person = person
        self.lever = lever

    def __eq__(self, other):
        return self.lever == other.lever and self.person == other.person
    
    def __str__(self):
        return '"Person at: ' + str(self.person) + 'lever at: ' + str(self.lever) + '"'
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        h = hash(self.person)
        for i in self.lever:
            h += hash(i)
        return h