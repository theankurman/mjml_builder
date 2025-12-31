from .nodes.base import BaseNode
from .nodes.containers import Body, Column, Mjml, Section
from .nodes.elements import Text


class Builder:
    sections: list[Section]

    def __init__(self) -> None:
        self.sections = []

    def add_section(self, *sections: Section, **attributes: str):
        new_sections = list(sections)
        if not new_sections:
            new_sections.append(Section(**attributes))

        self.sections.extend(new_sections)
        return self

    def add_column(self, *columns: Column, **attributes: str):
        # create section if it doesnt exist
        if not self.sections:
            self.add_section()

        new_columns = list(columns)
        if not new_columns:
            new_columns.append(Column(**attributes))

        # add columns to the last section
        self.sections[-1].children.extend(new_columns)
        return self

    def add_content(self, *contents: BaseNode | str, **attributes):
        # if content is str, change to text node
        new_contents = []
        for content in contents:
            if isinstance(content, str):
                content = Text(content, **attributes)
            new_contents.append(content)

        # create section and column if not exists
        if not self.sections:
            self.add_section()

        if not self.sections[-1].children:
            self.add_column()

        # add new content to the last column in the last section
        self.sections[-1].children[-1].children.extend(new_contents)

        return self

    def build(self):
        # wrap sections in mjml and body and return node
        return Mjml(Body(*self.sections))
