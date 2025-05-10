"""The class for all our Pai Sho tiles"""


class PaiShoTile:
    def __init__(self, tile_type, color, position=None, identifier=None):
        """
        Initialize a Pai Sho tile.

        :param tile_type: The type of tile (e.g., "flower", "water", "bamboo").
        : white is 1 black is 0 geust is black host is white
        :param position: A tuple (row, column) representing the tile’s position on the board (default is None).
        """

        self.tile_type = tile_type
        self.color = color
        self.position = position
        self.identifier = identifier

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
    def __init__(self, flower_type, color, position=None, identifier=None):
        super().__init__(
            tile_type=flower_type, color=color, position=position, identifier=identifier
        )
        self.flower_type = flower_type  # store flower type explicitly (optional)


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
