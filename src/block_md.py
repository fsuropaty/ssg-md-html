from htmlnode import HTMLNode, ParentNode
from inline_md import text_to_textnodes
from textnode import TextNode, text_node_to_html_node, text_type_text

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "##", "###", "####", "#####", "######")):
        return block_type_heading

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote

    if block.startswith("*"):
        for line in lines:
            if not line.startswith("*"):
                return block_type_paragraph
        return block_type_ulist

    if block.startswith("-"):
        for line in lines:
            if not line.startswith("-"):
                return block_type_paragraph
        return block_type_ulist

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist

    return block_type_paragraph


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == block_type_heading:
            level = get_heading_level(block)
            text = block[level + 1 :]
            head_node = ParentNode(f"h{level}", text_to_children(text))
            children.append(head_node)

        if block_type == block_type_code:
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("Invalid code block")
            text = block[4:-3]
            code_node = ParentNode("code", text_to_children(text))
            pre_node = ParentNode("pre", [code_node])
            children.append(pre_node)

        if block_type == block_type_quote:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("Invalid quote block")
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            quote_node = ParentNode("blockquote", text_to_children(content))
            children.append(quote_node)

        if block_type == block_type_olist:
            items = block.split("\n")
            html_items = []
            for item in items:
                text = item[3:]
                html_items.append(ParentNode("li", text_to_children(text)))
            ol_node = ParentNode("ol", html_items)
            children.append(ol_node)

        if block_type == block_type_ulist:
            items = block.split("\n")
            html_items = []
            for item in items:
                text = item[2:]
                html_items.append(ParentNode("li", text_to_children(text)))
            ul_node = ParentNode("ul", html_items)
            children.append(ul_node)

        if block_type == block_type_paragraph:
            lines = block.split("\n")
            paragraph = " ".join(lines)
            para_node = ParentNode("p", text_to_children(paragraph))
            children.append(para_node)

    return ParentNode("div", children, None)


def get_heading_level(block):
    heading_tag = block.split(" ", 1)
    level = len(heading_tag[0])
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    return level


def text_to_children(text):
    children_node = []
    text_node = text_to_textnodes(text)
    for node in text_node:
        html_node = text_node_to_html_node(node)
        children_node.append(html_node)
    return children_node
