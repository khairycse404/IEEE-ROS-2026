import heapq
from dataclasses import dataclass, field
from typing import Optional

@dataclass(order=True)
class Node:
    """
    Represents a single cell visited during the A* search.

    Attributes:
        f       : f(n) = g(n) + h(n) — used by the heap for ordering.
        position: (row, col) coordinate on the grid.
        g       : exact cost from the start to this node (number of steps).
        h       : heuristic cost estimate from this node to the goal.
        parent  : reference to the preceding Node, used for path reconstruction.
    """
    f: float                  
    position: tuple = field(compare=False)
    g: float = field(compare=False)
    h: float = field(compare=False)
    parent: Optional["Node"] = field(default=None, compare=False)


class Pathfinding:

    def a_star(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        grid,
    ) -> list[tuple[int, int]] | None:
        """
        Find the shortest path between two grid cells using A*.

        Step-by-step logic:
            1. Create the start Node with g=0 and h=Manhattan distance to goal.
            2. Push it onto the open set (min-heap ordered by f).
            3. While the open set is not empty:
               a. Pop the node with the lowest f value.
               b. If it equals the goal → reconstruct and return the path.
               c. Mark it in the closed set (already evaluated).
               d. For each of its 4 neighbours (up/down/left/right):
                  - Skip if out-of-bounds, in a no-fly zone, or already closed.
                  - Compute tentative g = current.g + 1 (uniform step cost).
                  - If the neighbour is not yet in the open set, or this path
                    is cheaper, add/update it with its new f, g, h, and parent.
            4. Return None if the open set empties without reaching the goal.

        Args:
            start : (row, col) of the starting cell.
            goal  : (row, col) of the target cell.
            grid  : Grid object exposing:
                        is_valid_position(pos) → bool
                        is_no_fly(pos)         → bool

        Returns:
            Ordered list of (row, col) tuples representing the path from start
            to goal (inclusive), or None if no path exists.
        """
        # Guard: trivial case
        if start == goal:
            return [start]

        # Validate start and goal positions
        if not grid.is_valid_position(start):
            raise ValueError(f"Start position {start} is out of bounds or invalid.")
        if not grid.is_valid_position(goal):
            raise ValueError(f"Goal position {goal} is out of bounds or invalid.")
        if grid.is_no_fly(start):
            raise ValueError(f"Start position {start} is inside a no-fly zone.")
        if grid.is_no_fly(goal):
            raise ValueError(f"Goal position {goal} is inside a no-fly zone.")

        # --- Initialise the start node ---
        h_start = self._manhattan(start, goal)
        start_node = Node(f=h_start, position=start, g=0, h=h_start)

        # Open set: min-heap of Nodes, ordered by f(n).
        # Each entry is a Node; Node.__lt__ compares by f automatically.
        open_heap: list[Node] = []
        heapq.heappush(open_heap, start_node)

        # open_positions maps position → best g value seen so far.
        # Allows O(1) duplicate/cheaper-path detection without scanning the heap.
        open_positions: dict[tuple, float] = {start: 0.0}

        # Closed set: positions that have already been fully evaluated.
        closed_set: set[tuple[int, int]] = set()

        # Four cardinal movement directions: up, down, left, right.
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # --- Main A* loop ---
        while open_heap:
            # 3a. Pop the node with the smallest f value.
            current = heapq.heappop(open_heap)

            # Skip stale heap entries (a cheaper path was already found).
            if current.position in closed_set:
                continue

            # 3b. Goal check — reconstruct the path.
            if current.position == goal:
                return self._reconstruct_path(current)

            # 3c. Mark as evaluated.
            closed_set.add(current.position)

            # 3d. Expand neighbours.
            for dr, dc in directions:
                neighbour_pos = (current.position[0] + dr, current.position[1] + dc)

                # Skip invalid, no-fly, or already-closed cells.
                if not grid.is_valid_position(neighbour_pos):
                    continue

                if grid.is_no_fly(neighbour_pos):
                    continue

                if neighbour_pos in closed_set:
                    continue

                # Uniform step cost of 1.
                tentative_g = current.g + 1

                # Only add/update if this path is strictly better than any
                # previously recorded path to this neighbour.
                if tentative_g < open_positions.get(neighbour_pos, float("inf")):
                    h = self._manhattan(neighbour_pos, goal)
                    neighbour_node = Node(
                        f=tentative_g + h,
                        position=neighbour_pos,
                        g=tentative_g,
                        h=h,
                        parent=current,
                    )
                    heapq.heappush(open_heap, neighbour_node)
                    open_positions[neighbour_pos] = tentative_g

        # Open set exhausted — no path exists.
        return None

    @staticmethod
    def _manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
        """
        Calculate the Manhattan distance between two grid cells.

        Manhattan distance is admissible (never overestimates) for grids that
        allow only horizontal/vertical movement, making it the ideal heuristic
        for A* in this context.

        Args:
            a, b: (row, col) tuples.

        Returns:
            Integer Manhattan distance.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def _reconstruct_path(node: Node) -> list[tuple[int, int]]:
        """
        Trace parent references from the goal node back to the start, then
        reverse the list to obtain the path in start→goal order.

        Args:
            node: The goal Node after A* terminates successfully.

        Returns:
            Ordered list of (row, col) positions from start to goal.
        """
        path: list[tuple[int, int]] = []
        current: Optional[Node] = node
        while current is not None:
            path.append(current.position)
            current = current.parent
        path.reverse()
        return path

class _ExampleGrid:
    """Lightweight Grid used only to demonstrate Pathfinding in isolation."""

    def __init__(self, width: int, height: int, no_fly_zones=None):
        self.width = width
        self.height = height
        # no_fly_zones is a set of (row, col) tuples
        self.no_fly_zones: set[tuple[int, int]] = set(no_fly_zones or [])

    def is_valid_position(self, pos: tuple[int, int]) -> bool:
        """Return True if pos is within grid bounds."""
        row, col = pos
        return 0 <= row < self.height and 0 <= col < self.width

    def is_no_fly(self, pos: tuple[int, int]) -> bool:
        """Return True if pos is a registered no-fly zone."""
        return pos in self.no_fly_zones


def main():
    """
    Demonstrates the Pathfinding class on a small 10x10 grid with a
    wall of no-fly zones that forces the path to go around an obstacle.

    Grid layout (rows 0-9, cols 0-9):
      S = start  (0, 0)
      G = goal   (9, 9)
      X = no-fly zone column at col 5, rows 0-7  (forces detour)
    """
    # Build a 10×10 grid with a vertical no-fly wall at column 5, rows 0–7.
    no_fly = {(r, 5) for r in range(8)}
    grid = _ExampleGrid(width=10, height=10, no_fly_zones=no_fly)

    pf = Pathfinding()
    start = (0, 0)
    goal  = (9, 9)

    print("AeroPath — Pathfinding Demo")
    print(f"Grid size : {grid.width} × {grid.height}")
    print(f"No-fly    : column 5, rows 0-7")
    print(f"Start     : {start}")
    print(f"Goal      : {goal}\n")

    path = pf.a_star(start, goal, grid)

    if path is None:
        print("No path found.")
    else:
        print(f"Path found ({len(path)} steps):")
        print(" → ".join(str(p) for p in path))

        # Visual grid printout
        print("\nGrid visualisation  (S=start, G=goal, X=no-fly, .=path, ' '=empty):")
        path_set = set(path)
        for r in range(grid.height):
            row_str = ""
            for c in range(grid.width):
                pos = (r, c)
                if pos == start:
                    row_str += "S "
                elif pos == goal:
                    row_str += "G "
                elif grid.is_no_fly(pos):
                    row_str += "X "
                elif pos in path_set:
                    row_str += ". "
                else:
                    row_str += "  "
            print(row_str)


if __name__ == "__main__":
    main()