from player import Direction, Player
from point import Point


class Snake:
    def __init__(
        self,
        start_pos: Point = Point((0, 0)),
        start_direction: Direction = Direction.DOWN,
        field_size: int = 9
    ) -> None:
        self.player: Player = Player(start_pos)
        self.direction: Direction = start_direction
        self.field_size: int = field_size

