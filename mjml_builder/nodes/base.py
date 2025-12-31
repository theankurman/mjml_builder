import importlib
import importlib.util
import io
import shutil
import subprocess


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
    def dict(self):
        data = {}
        data["tagName"] = self.tag_name
        data["attributes"] = self.attributes
        if self.content:
            data["content"] = self.content
        else:
            data["children"] = [c.dict for c in self.children]
        return data

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

    @property
    def html(self, force_external=False):
        from .containers import Mjml, Body

        # wrap node with mjml and mj-body tags
        node = self
        if not isinstance(node, Mjml) and not isinstance(node, Body):
            node = Body(node)
        if not isinstance(node, Mjml):
            node = Mjml(node)

        # python implementation
        has_mrml_python = importlib.util.find_spec("mrml") is not None
        has_mjml_python = importlib.util.find_spec("mjml") is not None
        # external implementation
        has_mjml = shutil.which("mjml") is not None
        has_bun = shutil.which("bun") is not None
        has_pnpx = shutil.which("pnpx") is not None
        has_npx = shutil.which("npx") is not None

        if has_mrml_python and not force_external:
            import mrml  # type: ignore

            return mrml.to_html(node.mjml).content
        if has_mjml_python and not force_external:
            import mjml  # type: ignore

            return mjml.mjml_to_html(io.StringIO(node.mjml)).html

        if has_mjml:
            mjml_command = []
        elif has_bun:
            mjml_command = ["bun", "x"]
        elif has_pnpx:
            mjml_command = ["pnpx"]
        elif has_npx:
            mjml_command = ["npx"]
        else:
            raise OSError("mjml command not found")

        mjml_command += ["mjml", "--stdin", "--stdout"]
        output = subprocess.check_output(
            mjml_command,
            input=node.mjml.encode(),
        ).decode()
        return output

    @property
    def text(self):
        text = ""
        if self.content:
            text += self.content
        else:
            for child in self.children:
                text += child.text + "\n"
        return text


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
