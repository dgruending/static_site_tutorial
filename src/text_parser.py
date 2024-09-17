import re

from textnode import TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 != 1 :
                raise Exception(f"Invalid Markdown syntax: Missing delimiter {delimiter} in {node.text}")
            else:
                for id, text in enumerate(split_text):
                    if id % 2 == 0:
                        new_nodes.append(TextNode(text, "text"))
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

if __name__ == "__main__":
    print(extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"))