import unittest

from textnode import *
from text_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextParser(unittest.TestCase):
    def test_bold_split(self):
        test_case = [TextNode("This is **bold** text.", text_type_text)]
        expected = [TextNode("This is ", text_type_text), TextNode("bold", text_type_bold), TextNode(" text.", text_type_text)]
        self.assertEqual(expected, split_nodes_delimiter(test_case, "**", text_type_bold))

    def test_italic_split(self):
        test_case = [TextNode("This is *italic* text.", text_type_text)]
        expected = [TextNode("This is ", text_type_text), TextNode("italic", text_type_italic), TextNode(" text.", text_type_text)]
        self.assertEqual(expected, split_nodes_delimiter(test_case, "*", text_type_italic))

    def test_code_split(self):
        test_case = [TextNode("This is `code` text.", text_type_text)]
        expected = [TextNode("This is ", text_type_text), TextNode("code", text_type_code), TextNode(" text.", text_type_text)]
        self.assertEqual(expected, split_nodes_delimiter(test_case, "`", text_type_code))

    def multiple_splits_same_node(self):
        test_case = [TextNode("This is **bold** text. And **this too**.", text_type_text)]
        expected = [TextNode("This is ", text_type_text), TextNode("bold", text_type_bold), TextNode(" text. And ", text_type_text), TextNode("this too", text_type_bold), TextNode(".", text_type_text)]
        self.assertEqual(expected, split_nodes_delimiter(test_case, "**", text_type_bold))

    def multiple_splits_diff_nodes(self):
        test_case = [TextNode("This is **bold** text.", text_type_text), TextNode("And **this too**.", text_type_text)]
        expected = [TextNode("This is ", text_type_text), TextNode("bold", text_type_bold), TextNode(" text.", text_type_text), TextNode("And ", text_type_text), TextNode("this too", text_type_bold), TextNode(".", text_type_text)]
        self.assertEqual(expected, split_nodes_delimiter(test_case, "**", text_type_bold))

    def test_split_beginning(self):
        test_case = [TextNode("**Bold** at front.", text_type_text)]
        expected = [TextNode("Bold", text_type_bold), TextNode(" at front.", text_type_text)]
        self.assertEqual(expected, split_nodes_delimiter(test_case, "**", text_type_bold))

    def test_split_end(self):
        test_case = [TextNode("A **bolded last part.**", text_type_text)]
        expected = [TextNode("A ", text_type_text), TextNode("bolded last part.", text_type_bold)]
        self.assertEqual(expected, split_nodes_delimiter(test_case, "**", text_type_bold))

    def test_other_type_nodes_bold_split(self):
        test_case = [TextNode("**bold**", text_type_bold), TextNode("*italic*", text_type_italic), TextNode("`code`", text_type_code)]
        expected = [TextNode("**bold**", text_type_bold), TextNode("*italic*", text_type_italic), TextNode("`code`", text_type_code)]
        self.assertEqual(expected, split_nodes_delimiter(test_case, "**", text_type_bold))

    def test_other_type_nodes_italic_split(self):
        test_case = [TextNode("**bold**", text_type_bold), TextNode("*italic*", text_type_italic), TextNode("`code`", text_type_code)]
        expected = [TextNode("**bold**", text_type_bold), TextNode("*italic*", text_type_italic), TextNode("`code`", text_type_code)]
        self.assertEqual(expected, split_nodes_delimiter(test_case, "*", text_type_italic))

    def test_other_type_nodes_code_split(self):
        test_case = [TextNode("**bold**", text_type_bold), TextNode("*italic*", text_type_italic), TextNode("`code`", text_type_code)]
        expected = [TextNode("**bold**", text_type_bold), TextNode("*italic*", text_type_italic), TextNode("`code`", text_type_code)]
        self.assertEqual(expected, split_nodes_delimiter(test_case, "`", text_type_code))
        
    def test_wrong_text_type(self):
        test_case = [TextNode("This is really *italic* but will be considered `code`.", text_type_text)]
        expected = [TextNode("This is really ", text_type_text), TextNode("italic", text_type_code), TextNode(" but will be considered `code`.", text_type_text)]
        self.assertEqual(expected, split_nodes_delimiter(test_case, "*", text_type_code))
        
    def test_wrong_syntax(self):
        test_case = [TextNode("This is *bold** text.", text_type_text)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(test_case, "**", text_type_bold)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, extract_markdown_images(text))

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(result, extract_markdown_links(text))

    def test_extract_no_valid_image(self):
        text = "No image here."
        self.assertEqual([], extract_markdown_images(text))

    def test_extract_broken_link(self):
        text = "This is text with a link [to boot dev(https://www.boot.dev)"
        self.assertEqual([], extract_markdown_links(text))


if __name__ == "__main__":
    unittest.main()