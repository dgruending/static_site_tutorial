import unittest

from textnode import *
from text_parser import split_nodes_delimiter

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
        expected = [TextNode("", text_type_text), TextNode("Bold", text_type_bold), TextNode(" at front.", text_type_text)]
        self.assertEqual(expected, split_nodes_delimiter(test_case, "**", text_type_bold))

    def test_split_end(self):
        test_case = [TextNode("A **bolded last part.**", text_type_text)]
        expected = [TextNode("A ", text_type_text), TextNode("bolded last part.", text_type_bold), TextNode("", text_type_text)]
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


if __name__ == "__main__":
    unittest.main()