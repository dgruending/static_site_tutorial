import re

from textnode import *

block_type_paragraph = "paragraph"
block_type_code = "code"
block_type_quote = "quote"
block_type_ordered_list = "ordered list"
block_type_unordered_list = "unordered list"
block_type_heading = "heading"

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

def markdown_to_blocks(markdown):
    result = []
    blocks = re.split(r"(\r\n|\r|\n)([ \t]*(\r\n|\r|\n))+", markdown)
    for block in blocks:
        block = block.strip()
        if block != "":
            result.append(block)
    return result

def block_to_block_type(markdown_block):
    # check for heading
    if re.match(r"#{1,6} .*", markdown_block):
        return block_type_heading
    # check for code
    if len(markdown_block) >= 6 and markdown_block[:3] == "```" and markdown_block[-3:] == "```":
        return block_type_code
    # for potential reuse
    splited_markdown_block = markdown_block.splitlines()
    # check for quote
    if all(line.startswith(">") for line in splited_markdown_block):
        return block_type_quote
    # check for unordered list
    if all(re.match(r"[*-] ", line) for line in splited_markdown_block):
        return block_type_unordered_list
    # check for ordered list
    expected_number = 1
    for line in splited_markdown_block:
        if len(line) >= 3 and f"{expected_number}. " == line[:3]:
            expected_number += 1
        else:
        # If no other case fits, it is a paragraph. Even if the syntax may be slightly wrong.
        # inside the for loop for simplicity of writing and ordered list is checked last.
            return block_type_paragraph
    return block_type_ordered_list

def markdown_to_html_node(markdown):
    pass