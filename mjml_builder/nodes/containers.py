from .base import StemNode


class Mjml(StemNode):
    tag_name = "mjml"


class Body(StemNode):
    tag_name = "mj-body"


class Section(StemNode):
    tag_name = "mj-section"


class Column(StemNode):
    tag_name = "mj-column"
