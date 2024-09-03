import unittest

from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("", "italic", "boot.dev")
        node2 = TextNode("", "italic", "boot.dev")
        self.assertEqual(node, node2)


    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", url="github.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_no_url(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", url="github.com")
        str_repr = "TextNode(This is a text node, bold, github.com)"
        self.assertEqual(node.__repr__(), str_repr)

    def test_text_to_html_raw(self):
        node = TextNode("This is text", "text")
        ref_node = LeafNode("This is text")
        self.assertEqual(ref_node.to_html(), text_node_to_html_node(node).to_html())

    def test_text_to_html_bold_tag_upper(self):
        node = TextNode("This is bold text", "BOLD")
        ref_node = LeafNode("This is bold text", tag="b")
        self.assertEqual(ref_node.to_html(), text_node_to_html_node(node).to_html())

    def test_text_to_html_italic(self):
        node = TextNode("This is italic text", "italic")
        ref_node = LeafNode("This is italic text", tag="i")
        self.assertEqual(ref_node.to_html(), text_node_to_html_node(node).to_html())

    def test_text_to_html_code(self):
        node = TextNode("This is code", "code")
        ref_node = LeafNode("This is code", tag="code")
        self.assertEqual(ref_node.to_html(), text_node_to_html_node(node).to_html())

    def test_text_to_html_link(self):
        node = TextNode("This is a link", "link", url="example.com")
        ref_node = LeafNode("This is a link", tag="a", props={"href": "example.com"})
        self.assertEqual(ref_node.to_html(), text_node_to_html_node(node).to_html())

    def test_text_to_html_image(self):
        node = TextNode("This is an image", "image", url="example.com/img.jpg")
        ref_node = LeafNode("", tag="img", props={"src": "example.com/img.jpg", "alt": "This is an image"})
        self.assertEqual(ref_node.to_html(), text_node_to_html_node(node).to_html())

    def test_text_to_html_none_text_type(self):
        node = TextNode("Some Text", None)
        self.assertRaises(Exception, text_node_to_html_node, node)

    def test_text_to_html_wrong_text_type(self):
        node = TextNode("Some Text", "cursiv")
        self.assertRaises(Exception, text_node_to_html_node, node)

if __name__ == "__main__":
    unittest.main()