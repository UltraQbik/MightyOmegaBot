from typing import Tuple


class Point:
    def __init__(self, xy: Tuple[int]) -> None:
        self.point: Tuple[int] = xy

    @property
    def x(self) -> int:
        return self.point[0]

    @property
    def y(self) -> int:
        return self.point[1]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        return self.point == other.point

    def __hash__(self) -> int:
        return self.x**(abs(self.y) + 1)
