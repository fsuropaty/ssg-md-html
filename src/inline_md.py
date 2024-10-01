import re

from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], text_type_text))
            else:
                split_nodes.append(TextNode(parts[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text):
    result = re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    return result


def extract_markdown_links(text):
    result = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

    return result


def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extract_link = extract_markdown_links(old_node.text)

        for name, url in extract_link:
            section = old_node.text.split(f"[{name}]({url})", 1)

            if section[0]:
                new_nodes.append(TextNode(section[0], text_type_text))

            new_nodes.append(TextNode(name, text_type_link, url))

            old_node.text = section[1]

    return new_nodes


def split_nodes_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extract_link = extract_markdown_images(old_node.text)

        for name, url in extract_link:
            section = old_node.text.split(f"![{name}]({url})", 1)

            if section[0]:
                new_nodes.append(TextNode(section[0], text_type_text))

            new_nodes.append(TextNode(name, text_type_image, url))

            old_node.text = section[1]

        if old_node.text:
            new_nodes.append(TextNode(old_node.text, text_type_text))

    return new_nodes
