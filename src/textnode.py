from htmlnode import LeafNode

class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    
    def __eq__(self, other: object) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(textnode):
    if textnode.text_type:
        if textnode.text_type.lower() == "text":
            return LeafNode(textnode.text)
        if textnode.text_type.lower() == "bold":
            return LeafNode(textnode.text, tag="b")
        if textnode.text_type.lower() == "italic":
            return LeafNode(textnode.text, tag="i")
        if textnode.text_type.lower() == "code":
            return LeafNode(textnode.text, tag="code")
        if textnode.text_type.lower() == "link":
            return LeafNode(textnode.text, tag="a", props={"href": textnode.url})
        if textnode.text_type.lower() == "image":
            return LeafNode("", tag="img", props={"src": textnode.url, "alt": textnode.text})
        

    raise Exception("Invalid Text Type")