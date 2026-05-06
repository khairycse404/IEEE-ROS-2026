class Grid:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.no_fly_zones = set()

    def in_bounds(self, position):
        # Error handling: Check if position is a valid tuple
        if not isinstance(position, tuple) or len(position) != 2:
            return False
        row, col = position
        return 0 <= row < self.height and 0 <= col < self.width

    def is_no_fly(self, position):
        return position in self.no_fly_zones

    def is_valid_position(self, position):
        return self.in_bounds(position) and not self.is_no_fly(position)

    def add_no_fly_zone(self, position):
        # Enhanced Error Handling
        if not isinstance(position, tuple) or len(position) != 2:
            raise TypeError(f"Invalid position format: {position}. Must be a tuple (row, col).")
            
        if not self.in_bounds(position):
            raise ValueError(f"Position {position} is outside the {self.width}x{self.height} grid.")

        self.no_fly_zones.add(position)

    def add_no_fly_cluster(self, positions):
        for pos in positions:
            try:
                self.add_no_fly_zone(pos)
            except (ValueError, TypeError) as e:
                # Log the error but continue adding valid positions
                print(f"Skipped invalid zone: {e}")

    def remove_no_fly_zone(self, position):
        # discard removes if present, does nothing if not (safe)
        self.no_fly_zones.discard(position)

    def display(self):
        for r in range(self.height):
            row_str = ""
            for c in range(self.width):
                if (r, c) in self.no_fly_zones:
                    row_str += "X "
                else:
                    row_str += ". "
            print(row_str)