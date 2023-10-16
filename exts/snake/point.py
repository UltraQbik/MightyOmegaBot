from typing import Tuple


class Point:
    def __init__(self, xy: Tuple[int]) -> None:
        self.point: Tuple[int] = xy

    @property
    def x(self) -> int:
        return self.point[x]

    @property
    def y(self) -> int:
        return self.point[y]

