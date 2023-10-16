from typing import List
from point import Point


class Direction:
    LEFT = 0
    DOWN = 1
    UP = 2
    RIGHT = 3


class Player:
    def __init__(self, start_pos: Point) -> None:
        self.body: List[Point] = [start_pos]

    def move(
        self,
        direction: Direction,
        food_collide: bool
    ) -> None:
        match direction:
            case Direction.LEFT:
                self.body.append(Point((self.body[-1].x - 1, self.body[-1].y)))
            case Directcion.DOWN:
                self.body.append(Point((self.body[-1].x, self.body[-1].y + 1)))
            case Direction.UP:
                self.body.append(Point((self.body[-1].x, self.body[-1].y - 1)))
            case Direction.RIGHT:
                self.body.append(Point((self.body[-1],x + 1, self.body[-1].y)))
        if not food_collide:
            self.body.pop()

