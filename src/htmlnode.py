class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""

        props_strings = []
        for key, value in self.props.items():
            props_strings.append(f'{key}="{value}"')

        return " " + " ".join(props_strings)

    def __repr__(self) -> str:
        return f"HTMLNode(tag={repr(self.tag)}, value={repr(self.value)}, children={repr(self.children)}, props={repr(self.props)})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag, value, None, props)
        self.value = value

    def to_html(self) -> str:
        if self.tag is None:
            return self.value

        props_str = ""
        if self.props:
            props_str = " " + " ".join(
                [f'{key}="{value}"' for key, value in self.props.items()]
            )

        if self.tag in ["img", "br", "hr"]:
            return f"<{self.tag}{props_str}/>"
        else:
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def text_node_to_html_node(text_node):
        match (text_node.text_type):
            case "text":
                return LeafNode(None, text_node.text)
            case "bold":
                return LeafNode("b", text_node.text)
            case "italic":
                return LeafNode("i", text_node.text)
            case "code":
                return LeafNode("code", text_node.text)
            case "link":
                return LeafNode(
                    "link",
                    text_node.text,
                    {"href": text_node.url, "alt": text_node.alt},
                )
            case "image":
                return LeafNode("img", "", {"src": text_node.url})
            case _:
                raise ValueError(f"Invalid text type: {text_node.text_type}")


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Invalid HTML : no tag")

        if not self.children:
            raise ValueError("Invalid HTML : no children")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
