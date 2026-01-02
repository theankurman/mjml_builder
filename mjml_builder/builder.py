from .components.base import BaseComponent
from .components.containers import Body, Column, Mjml, Section
from .components.elements import Text


class Builder:
    """Used to build an email.

    Attributes:
        sections (list[Section]): A list of ``mj-section`` tags that this builder contains.
    """

    sections: list[Section]

    def __init__(self) -> None:
        self.sections = []

    def add_section(self, *sections: Section, **attributes: str):
        """Add the given sections to the builder.

        If no sections are provided, add an empty section.

        Args:
            *sections: list of :class:`Section` s to add as positional arguments.

                Can be empty to automatically add an empty section.
            **attributes: attributes to add to the generated empty section if no sections have been provided.
        """
        new_sections = list(sections)
        if not new_sections:
            new_sections.append(Section(**attributes))

        self.sections.extend(new_sections)
        return self

    def add_column(self, *columns: Column, **attributes: str):
        """Add a column to the last section in the builder.

        Args:
            *columns: list of :class:`Column` s to add, provided as positional arguments.

                Can be left empty to automatically add an empty column
            **attributes: attributes to add to the automatically generated
                empty column if no columns have been provided.
        """
        # create section if it doesnt exist
        if not self.sections:
            self.add_section()

        new_columns = list(columns)
        if not new_columns:
            new_columns.append(Column(**attributes))

        # add columns to the last section
        self.sections[-1].children.extend(new_columns)
        return self

    def add_content(self, content: BaseComponent | str, **attributes):
        """Add content to the last column in the last section in the builder.

        Args:
            content: The content to add.

                - If an instance of :class:`BaseComponent`, it is added as is.
                - If an instance of :class:`str`, it is wrapped with a :class:`Text`
                    and provided attributes are applied to the :class:`Text` tag.

            **attributes: attributes to apply to the :class:`Text` tag when a string is passed in as content.
        """
        # if content is str, change to text component

        if isinstance(content, str):
            content = Text(content, **attributes)

        # create section and column if not exists
        if not self.sections:
            self.add_section()

        if not self.sections[-1].children:
            self.add_column()

        # add new content to the last column in the last section
        self.sections[-1].children[-1].children.append(content)

        return self

    def build(self):
        """Build the email component."""
        # wrap sections in mjml and body and return component
        return Mjml(Body(*self.sections))
