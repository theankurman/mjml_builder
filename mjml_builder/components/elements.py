from .containers import Column, Section
from .base import StemComponent, LeafComponent


class AccordionText(LeafComponent):
    tag_name = "mj-accordion-text"


class AccordionTitle(LeafComponent):
    tag_name = "mj-accordion-title"


class AccordionElement(StemComponent):
    tag_name = "mj-accordion-element"

    def __init__(
        self,
        title: str,
        text: str,
        title_attributes: dict[str, str] = {},
        text_attributes: dict[str, str] = {},
        **attributes: str,
    ) -> None:
        super().__init__(
            AccordionTitle(title, **title_attributes),
            AccordionText(text, **text_attributes),
            **attributes,
        )


class Accordion(StemComponent):
    tag_name = "mj-accordion"

    def __init__(self, *children: AccordionElement, **attributes: str) -> None:
        super().__init__(*children, **attributes)


class Button(LeafComponent):
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
    tag_name = "mj-carousel-image"

    def __init__(self, src: str, **attributes: str) -> None:
        super().__init__(None, src=src, **attributes)


class Carousel(StemComponent):
    tag_name = "mj-carousel"

    def __init__(self, *children: CarouselImage, **attributes: str) -> None:
        super().__init__(*children, **attributes)


class Divider(LeafComponent):
    tag_name = "mj-divider"


class Group(StemComponent):
    tag_name = "mj-group"

    def __init__(self, *children: Column, **attributes: str) -> None:
        super().__init__(*children, **attributes)


class Hero(StemComponent):
    tag_name = "mj-hero"


class Image(LeafComponent):
    tag_name = "mj-image"

    def __init__(self, src: str, **attributes: str) -> None:
        super().__init__(src=src, **attributes)


class NavbarLink(LeafComponent):
    tag_name = "mj-navbar-link"


class Navbar(StemComponent):
    tag_name = "mj-navbar"

    def __init__(self, *children: NavbarLink, **attributes: str) -> None:
        super().__init__(*children, **attributes)


class Raw(LeafComponent):
    tag_name = "mj-raw"


class SocialElement(LeafComponent):
    tag_name = "mj-social-element"


class Social(StemComponent):
    tag_name = "mj-social"

    def __init__(self, *children: SocialElement, **attributes: str) -> None:
        super().__init__(*children, **attributes)


class Spacer(LeafComponent):
    tag_name = "mj-spacer"

    def __init__(self, height: str = "10px", **attributes: str) -> None:
        super().__init__(height=height, **attributes)


class Table(LeafComponent):
    tag_name = "mj-table"
    headings: list[str]
    data: list[list]
    header_background: str
    header_foreground: str

    def _create_content(self):
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
    tag_name = "mj-text"


class Wrapper(StemComponent):
    tag_name = "mj-wrapper"

    def __init__(self, *children: Section, **attributes: str) -> None:
        super().__init__(*children, **attributes)
