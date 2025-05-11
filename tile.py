"""The class for all our Pai Sho tiles"""


class PaiShoTile:
    def __init__(self, tile_type, color, position=None, identifier=None):
        """
        Initialize a Pai Sho tile.

        :param tile_type: The type of tile (e.g., "flower", "water", "bamboo").
        : white is 1 red is 0
        :param position: A tuple (row, column) representing the tile’s position on the board (default is None).
        """
        self.tile_type_to_move_distance = {
            "host_boat": 0,
            "guest_boat": 0,
            "host_lotus": 0,
            "guest_lotus": 0,
            "host_orchid": 0,
            "guest_orchid": 0,
            "host_red_three": 3,
            "host_red_four": 4,
            "host_red_five": 5,
            "guest_red_three": 3,
            "guest_red_four": 4,
            "guest_red_five": 5,
            "host_white_three": 3,
            "host_white_four": 4,
            "host_white_five": 5,
            "guest_white_three": 3,
            "guest_white_four": 4,
            "guest_white_five": 5,
        }
        self.tile_type = tile_type
        if "guest" in self.tile_type:
            self.is_guest = 1
        else:
            self.is_guest = 0
        self.color = color
        self.position = position

        self.move_distance = self.tile_type_to_move_distance[self.tile_type]

    def __str__(self):
        return (
            f"PaiShoTile(type={self.tile_type}, color={self.color}, "
            f"position={self.position}, "
            f"id={self.identifier})"
        )

    def __eq__(self, other):
        if type(other) == int:
            return False
        if other.position == self.position:
            if self.tile_type == other.tile_type:
                if self.identifier == other.identifier and self.color == other.color:
                    return True
        return False


class FlowerTile(PaiShoTile):
    def __init__(self, tile_type, color, position=None, identifier=None):
        super().__init__(
            tile_type=tile_type,
            color=color,
            position=position,
            identifier=identifier,
        )
        self.tile_type = tile_type
        self.identifier = (
            color * 10 + self.move_distance
        )  # store flower type explicitly (optional)


class AccentTile(PaiShoTile):
    def __init__(self, color, position=None, identifier=None):
        super().__init__(
            tile_type="flower", color=color, position=position, identifier=identifier
        )


class SpecialTile(PaiShoTile):
    def __init__(self, color, position=None, identifier=None):
        super().__init__(
            tile_type="flower", color=color, position=position, identifier=identifier
        )
