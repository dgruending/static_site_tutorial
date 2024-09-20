import re

from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 != 1 :
                raise Exception(f"Invalid Markdown syntax: Missing delimiter {delimiter} in {node.text}")
            else:
                for id, text in enumerate(split_text):
                    if text == "":
                        continue
                    if id % 2 == 0:
                        new_nodes.append(TextNode(text, text_type_text))
                    else:
                        new_nodes.append(TextNode(text, text_type))
    return new_nodes


def extract_markdown_images(text):
    # results = []
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    # results = []
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            result.append(node)
            continue
        remainder_text = node.text
        for image_text, link in extract_markdown_images(node.text):
            [before_text, remainder_text] = remainder_text.split(f"![{image_text}]({link})", maxsplit=1)
            if before_text != "":
                result.append(TextNode(before_text, text_type_text))
            result.append(TextNode(image_text, text_type_image, link))
        if remainder_text != "":
            result.append(TextNode(remainder_text, text_type_text))
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            result.append(node)
            continue
        remainder_text = node.text
        for link_text, link in extract_markdown_links(node.text):
            [before_text, remainder_text] = remainder_text.split(f"[{link_text}]({link})", maxsplit=1)
            if before_text != "":
                result.append(TextNode(before_text, text_type_text))
            result.append(TextNode(link_text, text_type_link, link))
        if remainder_text != "":
            result.append(TextNode(remainder_text, text_type_text))
    return result

def text_to_textnodes(text):
    return split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_image(split_nodes_link([TextNode(text, text_type_text)])), "**", text_type_bold), "*", text_type_italic), "`", text_type_code)