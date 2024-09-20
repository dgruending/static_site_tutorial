import unittest

from textnode import *
from text_parser import *

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

    def test_single_link(self):
        nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev)", text_type_text)]
        expected = [TextNode("This is text with a link ", text_type_text), TextNode("to boot dev", text_type_link, "https://www.boot.dev")]
        self.assertEqual(expected, split_nodes_link(nodes))

    def test_single_image(self):
        nodes = [TextNode("This is text with an image ![boot dev logo](https://www.boot.dev/img/bootdev-logo-full-small.webp)", text_type_text)]
        expected = [TextNode("This is text with an image ", text_type_text), TextNode("boot dev logo", text_type_image, "https://www.boot.dev/img/bootdev-logo-full-small.webp")]
        self.assertEqual(expected, split_nodes_image(nodes))

    def test_multiple_links(self):
        nodes = [
            TextNode("Bold first part", text_type_bold),
            TextNode("[first link](http://first.com) and [second link](https://second.de)[third link](https://third.net) *italic ending*", text_type_text)
        ]
        expected = [
            TextNode("Bold first part", text_type=text_type_bold),
            TextNode("first link", text_type=text_type_link, url="http://first.com"),
            TextNode(" and ", text_type=text_type_text),
            TextNode("second link", text_type=text_type_link, url="https://second.de"),
            TextNode("third link", text_type=text_type_link, url="https://third.net"),
            TextNode(" *italic ending*", text_type=text_type_text)
        ]
        self.assertEqual(expected, split_nodes_link(nodes))

    def test_multiple_images(self):
        nodes = [
            TextNode("Bold first part", text_type_bold),
            TextNode("![first image](http://first.com/first.jpg) and ![second image](https://second.de/logo.webp)![third image](https://third.net/image.png) *italic ending*", text_type_text)
        ]
        expected = [
            TextNode("Bold first part", text_type=text_type_bold),
            TextNode("first image", text_type=text_type_image, url="http://first.com/first.jpg"),
            TextNode(" and ", text_type=text_type_text),
            TextNode("second image", text_type=text_type_image, url="https://second.de/logo.webp"),
            TextNode("third image", text_type=text_type_image, url="https://third.net/image.png"),
            TextNode(" *italic ending*", text_type=text_type_text)
        ]
        self.assertEqual(expected, split_nodes_image(nodes))

    def test_broken_link(self):
        nodes = [TextNode("This is [a link](http://bootdev.com", text_type_text)]
        expected = [TextNode("This is [a link](http://bootdev.com", text_type_text)]
        self.assertEqual(expected, split_nodes_link(nodes))

    def test_broken_image(self):
        nodes = [TextNode("This is [an image link](http://bootdev.com/logo.webp)", text_type_text)]
        expected = [TextNode("This is [an image link](http://bootdev.com/logo.webp)", text_type_text)]
        self.assertEqual(expected, split_nodes_image(nodes))

    def test_mixed_images_links(self):
        nodes = [TextNode("[first link_t](first link) ![first image](first image link)![second image](second image link) [second link text](second link)   ![third image](third image link)", text_type_text)]
        expected = [
            TextNode("first link_t", text_type_link, "first link"),
            TextNode(" ", text_type_text),
            TextNode("first image", text_type_image, "first image link"),
            TextNode("second image", text_type_image, "second image link"),
            TextNode(" ", text_type_text),
            TextNode("second link text", text_type_link, "second link"),
            TextNode("   ", text_type_text),
            TextNode("third image", text_type_image, "third image link")
        ]
        self.assertEqual(expected, split_nodes_image(split_nodes_link(nodes)))

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(expected, text_to_textnodes(text))

if __name__ == "__main__":
    unittest.main()