from typing import List, Tuple, Dict
from random import randint
from exts.snake.player import Direction, Player
from exts.snake.point import Point


class CollisionException(Exception):
    "Raised when snake have collided"
    pass


class Snake:
    def __init__(
        self,
        start_pos: Point = Point((0, 0)),
        start_direction: Direction = Direction.DOWN,
        field_size: int = 9,
        style: Dict[str, str] = {
            "snake": ":black_large_square:",
            "food": ":red_square:",
            "space": ":white_large_square:"
        }
    ) -> None:
        self.player: Player = Player(start_pos)
        self.direction: Direction = start_direction
        self.field_size: int = field_size
        self.style = style
        self.generate_food()

    def generate_food(self) -> None:
        while True:
            food = Point(
                (randint(0, self.field_size - 1), randint(0, self.field_size - 1))
            )
            if food not in self.player:
                break
        self.food = food

    def check_collisions(self) -> None:
        collided_points: set = set(self.player.body + [self.food])
        if len(collided_points) < len(self.player) + 1:
            return True
        for point in self.player:
            for coordinate in point.point:
                if coordinate < 0 or coordinate >= self.field_size:
                    return True
        return False

    def do_tick(self) -> None:
        self.player.move(self.direction)
        if self.check_collisions():
            raise CollisionException

    def __str__(self) -> str:
        out: str = ""
        points_list: List[Tuple[int]] = []
        for point in self.player:
            points_list.append(point.point)
        for y in range(self.field_size):
            for x in range(self.field_size):
                if (x, y) == self.food.point:
                    out += self.style["food"]
                elif (x, y) in points_list:
                    out += self.style["snake"]
                else:
                    out += self.style["space"]
            out += "\n"
        return out[:-1]

