from .containers import Column, Section
from .base import StemComponent, LeafComponent


class AccordionText(LeafComponent):
    """Represents the ``mj-accordion-text`` tag."""

    tag_name = "mj-accordion-text"


class AccordionTitle(LeafComponent):
    """Represents the ``mj-accordion-title`` tag."""

    tag_name = "mj-accordion-title"


class AccordionElement(StemComponent):
    """Represents the ``mj-accordion-element`` tag."""

    tag_name = "mj-accordion-element"

    def __init__(
        self,
        title: str,
        text: str,
        title_attributes: dict[str, str] = {},
        text_attributes: dict[str, str] = {},
        **attributes: str,
    ) -> None:
        """Create an instance of ``mj-accordion-element``.

        Args:
            title: title of the accordion element.
            text: inner html content of the accordion element.
            title_attributes: attributes to apply to the ``mj-accordion-title`` tag. Defaults to {}.
            text_attributes: attributes to apply to the ``mj-accordion-text`` tag. Defaults to {}.
            **attributes: attributes to apply to the ``mj-accordion-element`` tag.
        """
        super().__init__(
            AccordionTitle(title, **title_attributes),
            AccordionText(text, **text_attributes),
            **attributes,
        )


class Accordion(StemComponent):
    """Represents the ``mj-accordion`` tag."""

    tag_name = "mj-accordion"

    def __init__(self, *children: AccordionElement, **attributes: str) -> None:
        """Create an instance of ``mj-accordion``.

        Args:
            *children: list of :class:`AccordionElement` children.
            **attributes: attributes to apply to the mjml tag.
        """
        super().__init__(*children, **attributes)


class Button(LeafComponent):
    """Represents a ``mj-button`` tag."""

    tag_name = "mj-button"

    @property
    def text(self):
        label = self.content
        link = self.attributes.get("href")
        if not link:
            if label:
                return label
            return ""
        return f"[{label}]({link})"


class CarouselImage(LeafComponent):
    """Represents a ``mj-carousel-image`` tag."""

    tag_name = "mj-carousel-image"

    def __init__(self, src: str, **attributes: str) -> None:
        super().__init__(None, src=src, **attributes)


class Carousel(StemComponent):
    """Represents a ``mj-carousel`` tag."""

    tag_name = "mj-carousel"

    def __init__(self, *children: CarouselImage, **attributes: str) -> None:
        """Create an instance of ``mj-carousel`` tag.

        Args:
            *children: list of child :class:`CarouselImage` tags, provided as positional args.
            **attributes: attributes to apply to this mjml tag.
        """
        super().__init__(*children, **attributes)


class Divider(LeafComponent):
    """Represents a ``mj-divider`` tag."""

    tag_name = "mj-divider"


class Group(StemComponent):
    """Represents a ``mj-group`` tag."""

    tag_name = "mj-group"

    def __init__(self, *children: Column, **attributes: str) -> None:
        """Create an instance of a ``mj-group`` tag.

        Args:
            *children: child :class:`Column` tags, provided as positional args.
            **attributes: attributes to add to this mjml tag.
        """
        super().__init__(*children, **attributes)


class Hero(StemComponent):
    """Represents a ``mj-hero`` tag."""

    tag_name = "mj-hero"


class Image(LeafComponent):
    """Represents a ``mj-image`` tag."""

    tag_name = "mj-image"

    def __init__(self, src: str, **attributes: str) -> None:
        """Create an instance of the ``mj-image`` tag.

        Args:
            src: the source url of the image.
            **attributes: attributes to add to this mjml tag.
        """
        super().__init__(src=src, **attributes)


class NavbarLink(LeafComponent):
    """Represents a ``mj-navbar-link`` tag."""

    tag_name = "mj-navbar-link"


class Navbar(StemComponent):
    """Represents a ``mj-navbar`` tag."""

    tag_name = "mj-navbar"

    def __init__(self, *children: NavbarLink, **attributes: str) -> None:
        """Create an instance of a ``mj-navbar`` tag.

        Args:
            *children: child :class:`NavbarLink` tags, provided as positional args.
            **attributes: attributes to add to this mjml tag.
        """
        super().__init__(*children, **attributes)


class Raw(LeafComponent):
    """Represents a ``mj-raw`` tag."""

    tag_name = "mj-raw"


class SocialElement(LeafComponent):
    """Represents a ``mj-social-element`` tag."""

    tag_name = "mj-social-element"


class Social(StemComponent):
    """Represents a ``mj-social`` tag."""

    tag_name = "mj-social"

    def __init__(self, *children: SocialElement, **attributes: str) -> None:
        """Create an instance of a ``mj-navbar`` tag.

        Args:
            *children: child :class:`SocialElement` tags, provided as positional args.
            **attributes: attributes to add to this mjml tag.
        """
        super().__init__(*children, **attributes)


class Spacer(LeafComponent):
    """Represents a ``mj-spacer`` tag."""

    tag_name = "mj-spacer"

    def __init__(self, height: str = "10px", **attributes: str) -> None:
        """Create an instance of a ``mj-spacer`` tag.

        Args:
            height: the height of the spacer. Defaults to "10px".
            **attributes: attributes to add to this mjml tag.
        """
        super().__init__(height=height, **attributes)


class Table(LeafComponent):
    """Represents a ``mj-table`` tag."""

    tag_name = "mj-table"
    headings: list[str]
    data: list[list]
    header_background: str
    header_foreground: str

    def _create_content(self):
        """Helper method to generate the inner html content for this tag."""
        headings_markup = " ".join([f"<th>{h}</th>" for h in self.headings])
        headings_markup = f"""
        <thead style="background: {self.header_background}; color: {self.header_foreground};">
        <tr>{headings_markup}</tr>
        </thead>
        """

        data_markup = ""
        for row in self.data:
            row_markup = " ".join([f"<td>{item}</td>" for item in row])
            row_markup = f'<tr align="center" style="border: 1px solid {self.header_background};">{row_markup}</tr>'
            data_markup += row_markup

        data_markup = f"<tbody>{data_markup}</tbody>"

        markup = f"{headings_markup}{data_markup}"
        return markup

    def __init__(
        self,
        headings: list[str],
        data: list[list],
        header_background: str = "#5e5e5e",
        header_foreground: str = "white",
        **attributes: str,
    ) -> None:
        """Create an instance of the ``mj-table`` tag.
        Args:
            headings: a list of heading names.
            data: a list representing rows of the table. Each row should be a list of values.
            header_background: a html color string to use for the header background.
                Can be hex codes like "#5e5e5e" or color names like "white".
                Defaults to "#5e5e5e".
            header_foreground: a html color string to use for the header background.
                Can be hex codes like "#5e5e5e" or color names like "white".
                Defaults to "white".
            **attributes: attributes to apply to this mjml tag.
        """
        self.headings = headings
        self.data = data
        self.header_background = header_background
        self.header_foreground = header_foreground
        super().__init__(self._create_content(), **attributes)

    @property
    def text(self):
        num_cols = max(len(self.headings), *[len(row) for row in self.data])

        # maps col_index to the length of the longest item in that column
        max_lengths = {
            col_index: max(
                len(str(self.headings[col_index]))
                if col_index < len(self.headings)
                else 0,
                *[
                    len(str(row[col_index])) if col_index < len(row) else 0
                    for row in self.data
                ],
            )
            for col_index in range(num_cols)
        }

        headings_string = "    ".join(
            [
                h.ljust(max_lengths[col_index])
                for col_index, h in enumerate(self.headings)
            ]
        )
        data_string = ""
        for row in self.data:
            row_string = "    ".join(
                [
                    str(item).ljust(max_lengths[col_index])
                    for col_index, item in enumerate(row)
                ]
            )
            data_string += f"{row_string}\n"

        border_string = "=" * len(headings_string)

        final_string = f"{headings_string}\n{border_string}\n{data_string}"

        return final_string


class Text(LeafComponent):
    """Represents a ``mj-text`` tag."""

    tag_name = "mj-text"


class Wrapper(StemComponent):
    """Represents a ``mj-wrapper`` tag."""

    tag_name = "mj-wrapper"

    def __init__(self, *children: Section, **attributes: str) -> None:
        """Create an instance of a ``mj-wrapper`` tag.

        Args:
            *children: child :class:`Section` tags, provided as positional args.
            **attributes: attributes to add to the mjml tag.
        """
        super().__init__(*children, **attributes)
