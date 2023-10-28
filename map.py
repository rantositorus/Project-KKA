class map:
    map_array: list[list[str]]
    points: list[tuple[int, int]]

    def __init__(self, height: int, width: int, map_array=[]):
        self.map = map_array
        self.width = width
        self.height = height
        self.points = []
    
    def check_out_of_bounds(self, y: int, x: int) -> bool:
        return x >= self.width or x < 0 or y >= self.height or y < 0
    
    def is_block(self, y: int, x: int):
        return self.map[y][x].lower() == 'x'
    
    def set_points(self, points):
        self.points = points

    def get_treasure(self, y, x) -> str:
        return self.map[y][x]
    
    def append_row(self, row: list[str]) -> None:
        if len(row) != self.width:
            raise ValueError('Ukuran kolom tidak valid:\n', str(row))
        self.map.append(row)