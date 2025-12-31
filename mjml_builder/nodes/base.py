import importlib
import importlib.util
import shutil


class BaseNode:
    tag_name: str

    attributes: dict[str, str] = {}
    content: str | None = None
    children: list["BaseNode"] = []

    def __init__(
        self,
        tag_name: str,
        content: str | None = None,
        *children: "BaseNode",
        **attributes: str,
    ) -> None:
        self.tag_name = tag_name
        self.attributes = attributes
        self.content = content
        self.children = list(children)

    @property
    def mjml(self):
        node = self
        attribute_list = []
        for name, value in node.attributes.items():
            name = name.replace("_", "-")
            attribute_list.append(f'{name}="{value}"')
        attribute_string = " ".join(attribute_list)

        tag_start = "<" + f"{node.tag_name} {attribute_string}".strip() + ">"
        tag_end = f"</{node.tag_name}>"

        content = ""
        if node.content:
            content += node.content
        else:
            for child in node.children:
                content += child.mjml

        markup = f"{tag_start}{content}{tag_end}"
        return markup


class StemNode(BaseNode):
    def __init__(
        self,
        *children: BaseNode,
        **attributes: str,
    ) -> None:
        self.children = list(children)
        self.attributes = attributes


class LeafNode(BaseNode):
    def __init__(
        self,
        content: str | None = None,
        **attributes: str,
    ) -> None:
        self.content = content
        self.attributes = attributes
