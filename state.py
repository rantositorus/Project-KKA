from map import map

class state:
    def __init__(self, person: tuple, treasure=[]) -> None:
        self.person = person
        self.treasure = treasure

    def __eq__(self, other):
        return self.treasure == other.treasure and self.person == other.person
    
    def __str__(self):
        return '"Person at: ' + str(self.person) + 'treasure at: ' + str(self.treasure) + '"'
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        h = hash(self.person)
        for i in self.treasure:
            h += hash(i)
        return h