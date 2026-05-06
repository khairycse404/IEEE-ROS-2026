from __future__ import annotations

from typing import Optional

from AStar_MazeSolver import Pathfinding

class Package:
    """
    Represents a delivery package in the AeroPath system.

    Attributes (public, matching the UML):
        id          : Unique integer identifier for this package.
        weight      : Mass of the package in kilograms (affects battery drain).
        start       : (row, col) grid coordinate where the package originates.
        destination : (row, col) grid coordinate where it must be delivered.

    Internal state (private):
        _assigned_drone_id : ID of the drone carrying this package, or None.
        _delivered         : True once the package has reached its destination.
    """

    def __init__(
        self,
        id: int,
        weight: float,
        start: tuple[int, int],
        destination: tuple[int, int],
    ) -> None:
        """
        Initialise a new Package.

        Args:
            id          : Unique package identifier.
            weight      : Package mass in kg.  Must be > 0.
            start       : Grid cell (row, col) of pickup location.
            destination : Grid cell (row, col) of drop-off location.

        Raises:
            ValueError: If weight is non-positive, or start equals destination.
        """
        if weight <= 0:
            raise ValueError(f"Package weight must be positive, got {weight}.")
        if start == destination:
            raise ValueError("Start and destination must be different positions.")

        self.id: int = id
        self.weight: float = weight
        self.start: tuple[int, int] = start
        self.destination: tuple[int, int] = destination

        # --- Private state ---
        self._assigned_drone_id: Optional[int] = None  # None = unassigned
        self._delivered: bool = False                  # False = pending delivery

    def assign_to(self, drone_id: int) -> None:
        """
        Assign this package to a specific drone.

        Records which drone is responsible for delivering this package.
        A package that has already been delivered cannot be reassigned.

        Args:
            drone_id: The integer ID of the drone taking on this delivery.

        Raises:
            RuntimeError: If the package has already been delivered.
        """
        if self._delivered:
            raise RuntimeError(
                f"Package {self.id} has already been delivered and cannot be reassigned."
            )
        self._assigned_drone_id = drone_id

    def mark_delivered(self) -> None:
        """
        Mark this package as successfully delivered.

        Should be called by the simulation once the assigned drone reaches
        the destination cell.

        Raises:
            RuntimeError: If the package has not been assigned to a drone yet.
            RuntimeError: If the package was already marked as delivered.
        """
        if self._assigned_drone_id is None:
            raise RuntimeError(
                f"Package {self.id} cannot be marked delivered — it has no assigned drone."
            )
        if self._delivered:
            raise RuntimeError(f"Package {self.id} is already delivered.")
        self._delivered = True

    @property
    def is_delivered(self) -> bool:
        """Return True if the package has reached its destination."""
        return self._delivered

    @property
    def assigned_drone_id(self) -> Optional[int]:
        """Return the ID of the drone assigned to this package, or None."""
        return self._assigned_drone_id

    @property
    def is_assigned(self) -> bool:
        """Return True if a drone has been assigned to this package."""
        return self._assigned_drone_id is not None


    def get_path(self, grid) -> Optional[list[tuple[int, int]]]:
        """
        Calculate the optimal A* path from this package's start to its
        destination on the given grid.

        This is a convenience method that delegates entirely to the
        Pathfinding class — no pathfinding logic lives here.

        Args:
            grid: A Grid instance with is_valid_position() and is_no_fly().

        Returns:
            Ordered list of (row, col) positions from start to destination,
            or None if no valid path exists (e.g., completely surrounded by
            no-fly zones).
        """
        pf = Pathfinding()
        return pf.a_star(self.start, self.destination, grid)


    def to_dict(self) -> dict:
        """
        Serialise the package state to a plain dictionary for JSON storage.

        Returns:
            Dict containing all package attributes and internal state.
        """
        return {
            "id": self.id,
            "weight": self.weight,
            "start": list(self.start),
            "destination": list(self.destination),
            "assigned_drone_id": self._assigned_drone_id,
            "delivered": self._delivered,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Package":
        """
        Reconstruct a Package instance from a serialised dictionary.

        Args:
            data: Dictionary produced by to_dict().

        Returns:
            A fully restored Package object.
        """
        pkg = cls(
            id=data["id"],
            weight=data["weight"],
            start=tuple(data["start"]),
            destination=tuple(data["destination"]),
        )
        pkg._assigned_drone_id = data.get("assigned_drone_id")
        pkg._delivered = data.get("delivered", False)
        return pkg

    def __repr__(self) -> str:
        if self._delivered:
            status = "delivered"

        elif self._assigned_drone_id is not None:
            status = f"assigned→drone {self._assigned_drone_id}"

        else:
            status = "unassigned"

        return (
            f"Package(id={self.id}, weight={self.weight}kg, "
            f"start={self.start}, dest={self.destination}, status={status})"
        )


def main():
    """
    Demonstrates the Package class:
      1. Basic creation and attribute access.
      2. Drone assignment and delivery lifecycle.
      3. A* path retrieval via get_path().
      4. Serialisation round-trip.
      5. Error-handling guards.
    """

    # ---- Minimal Grid stub ----
    class _ExampleGrid:
        def __init__(self, width, height, no_fly_zones=None):
            self.width = width
            self.height = height
            self.no_fly_zones = set(no_fly_zones or [])

        def is_valid_position(self, pos):
            r, c = pos
            return 0 <= r < self.height and 0 <= c < self.width

        def is_no_fly(self, pos):
            return pos in self.no_fly_zones

    print("=" * 55)
    print("  AeroPath — Package class demo")
    print("=" * 55)

    # 1. Create a package
    pkg = Package(id=1, weight=2.5, start=(0, 0), destination=(5, 7))
    print(f"\n[Created]  {pkg}")

    # 2. Assign to a drone
    pkg.assign_to(drone_id=42)
    print(f"[Assigned] {pkg}")
    print(f"           is_assigned={pkg.is_assigned}, drone={pkg.assigned_drone_id}")

    # 3. Calculate the A* path on a 10×10 grid with no obstacles
    grid = _ExampleGrid(width=10, height=10)
    path = pkg.get_path(grid)
    print(f"\n[Path]     {len(path)} steps: {path}")

    # 4. Mark as delivered
    pkg.mark_delivered()
    print(f"[Delivered]{pkg}")
    print(f"           is_delivered={pkg.is_delivered}")

    # 5. Serialisation round-trip
    data = pkg.to_dict()
    restored = Package.from_dict(data)
    print(f"\n[Round-trip JSON]")
    print(f"  Original : {pkg}")
    print(f"  Restored : {restored}")
    assert restored.to_dict() == data, "Serialisation mismatch!"
    print("  ✓ Serialisation verified.")

    # 6. Error guards
    print("\n[Error handling]")

    # Cannot reassign after delivery
    try:
        pkg.assign_to(99)
    except RuntimeError as e:
        print(f"  ✓ Caught: {e}")

    # Cannot mark delivered twice
    try:
        pkg.mark_delivered()
    except RuntimeError as e:
        print(f"  ✓ Caught: {e}")

    # Cannot create package with zero weight
    try:
        Package(id=2, weight=0, start=(0, 0), destination=(1, 1))
    except ValueError as e:
        print(f"  ✓ Caught: {e}")

    # Cannot create package where start == destination
    try:
        Package(id=3, weight=1.0, start=(3, 3), destination=(3, 3))
    except ValueError as e:
        print(f"  ✓ Caught: {e}")

    print("\nDemo complete.")


if __name__ == "__main__":
    main()