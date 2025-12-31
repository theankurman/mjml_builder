from .base import StemNode, LeafNode


class Button(LeafNode):
    tag_name = "mj-button"


class Divider(LeafNode):
    tag_name = "mj-divider"


class Image(LeafNode):
    tag_name = "mj-image"

    def __init__(self, src: str, **attributes: str) -> None:
        super().__init__(src=src, **attributes)


class Spacer(LeafNode):
    tag_name = "mj-spacer"

    def __init__(self, height: str = "10px", **attributes: str) -> None:
        super().__init__(height=height, **attributes)


class Text(LeafNode):
    tag_name = "mj-text"
