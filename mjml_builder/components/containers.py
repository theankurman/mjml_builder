from .base import StemComponent


class Mjml(StemComponent):
    """The base ``mjml`` tag."""

    tag_name = "mjml"


class Body(StemComponent):
    """The ``mj-body`` tag."""

    tag_name = "mj-body"


class Section(StemComponent):
    """The ``mj-section`` tag."""

    tag_name = "mj-section"


class Column(StemComponent):
    """The ``mj-column`` tag."""

    tag_name = "mj-column"
