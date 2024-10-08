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

    def test_markdown_to_blocks_single_block(self):
        input = "# This is just a single block"
        result = ["# This is just a single block"]
        self.assertEqual(result, markdown_to_blocks(input))

    def test_markdown_to_blocks_multiple_blocks(self):
        input = """# this is the first block
        
        # Begin a second block
        
        some text for the third block
        
* and a list
* for the fourth block
* the end"""
        result = ["# this is the first block",
                  "# Begin a second block",
                  "some text for the third block",
                  "* and a list\n* for the fourth block\n* the end"]
        self.assertEqual(result, markdown_to_blocks(input))

    def test_markdown_to_blocks_excessive_newlines(self):
        input = """# Start with a heading

        
        text for the second block"""
        result = ["# Start with a heading", "text for the second block"]
        self.assertEqual(result, markdown_to_blocks(input))

    def test_markdown_to_blocks_more_whitespaces_between_blocks(self):
        input = """# Header
        
                        
                    
        text"""
        result = ["# Header", "text"]
        self.assertEqual(result, markdown_to_blocks(input))

    def test_markdown_to_blocks_trailing_leading_whitespaces(self):
        input = """    # First block
        
        # Second block     
        
                * third block
* is a list
* with both leading and trailing whitespace         \n"""
        result = ["# First block", "# Second block", "* third block\n* is a list\n* with both leading and trailing whitespace"]
        self.assertEqual(result, markdown_to_blocks(input))

    def test_block_to_block_type_heading1(self):
        input = "# Simple Header"
        expected = block_type_heading
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_heading2(self):
        input = "## More advanced header\nSome more text"
        expected = block_type_heading
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_heading4(self):
        input = "#### Header 4"
        expected = block_type_heading
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_heading6(self):
        input = "###### Header 6"
        expected = block_type_heading
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_heading7(self):
        input = "####### Wrong header format"
        expected = block_type_paragraph
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_heading_no_space(self):
        input = "#Forgot the space"
        expected = block_type_paragraph
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_code(self):
        input = "```Here could stand your code.\nWrite it now\nGo\ton!```"
        expected = block_type_code
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_code_incorrect(self):
        input = "```Forgot the last backtick``"
        expected = block_type_paragraph
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_quote(self):
        input = "> some quotes\n> from some person\n> have some more"
        expected = block_type_quote
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_quote_missing_symbol(self):
        input = ">Forgetting\nis human\n>isn't it."
        expected = block_type_paragraph
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_unordered_list_star(self):
        input = "* a list\n* of some stuff\n* adding items\n* end"
        expected = block_type_unordered_list
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_unordered_list_dash(self):
        input = "- a list\n- of some stuff\n- adding items\n- end"
        expected = block_type_unordered_list
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_unordered_list_mixed(self):
        input = "* a list\n* of some stuff\n- adding items\n- end"
        expected = block_type_unordered_list
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_unordered_list_incorrect(self):
        input = "* using a wrong symbol\n+ will wreck this list\n* see?"
        expected = block_type_paragraph
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_ordered_list(self):
        input = "1. first item\n2. second item\n3. third item"
        expected = block_type_ordered_list
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_ordered_list_wrong_increment(self):
        input = "1. first item\n3. second item\n4. third item"
        expected = block_type_paragraph
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_ordered_list_wrong_syntax(self):
        input = "1. first item\n2.second item\n3. third item"
        expected = block_type_paragraph
        self.assertEqual(expected, block_to_block_type(input))

    def test_block_to_block_type_paragraph(self):
        input = "Just some text"
        expected = block_type_paragraph
        self.assertEqual(expected, block_to_block_type(input))

    def test_markdown_to_html_node_single_paragraph(self):
        input = "a"
        expected = ParentNode(tag="div", children=[ParentNode(tag="p", children=[LeafNode(value="a")])])
        self.assertEqual(expected.to_html(), markdown_to_html_node(input).to_html())

    def test_markdown_to_html_node_single_paragraph_with_markdown(self):
        input = "This text has a **bold** word, an *italic*`here is some code`."
        expected = "<div><p>This text has a <b>bold</b> word, an <i>italic</i><code>here is some code</code>.</p></div>"
        self.assertEqual(expected, markdown_to_html_node(input).to_html())

    def test_markdown_to_html_node_single_paragraphs_with_image(self):
        input = "![image_text](url)"
        expected = '<div><p><img src="url" alt="image_text"></img></p></div>'
        self.assertEqual(expected, markdown_to_html_node(input).to_html())

    def test_markdown_to_html_node_single_code_block(self):
        input = "```some code here\nanother line\nthe end```"
        expected = "<div><pre><code>some code here\nanother line\nthe end</code></pre></div>"
        self.assertEqual(expected, markdown_to_html_node(input).to_html())

    def test_markdown_to_html_node_single_quote_block(self):
        input = ">some wisdom\n>some more wisdom\n>the end"
        expected = "<div><blockquote>some wisdom\nsome more wisdom\nthe end</blockquote></div>"
        self.assertEqual(expected, markdown_to_html_node(input).to_html())

    def test_markdown_to_html_node_heading_1(self):
        input = "# Title"
        expected = "<div><h1>Title</h1></div>"
        self.assertEqual(expected, markdown_to_html_node(input).to_html())

    def test_markdown_to_html_node_node_heading_6(self):
        input = "###### Subsubsubsubsubtitle"
        expected = "<div><h6>Subsubsubsubsubtitle</h6></div>"
        self.assertEqual(expected, markdown_to_html_node(input).to_html())

    def test_markdown_to_html_node_unordered_list(self):
        input = "* list item 1\n- list item 2\n- list item 3"
        expected = "<div><ul><li>list item 1</li><li>list item 2</li><li>list item 3</li></ul></div>"
        self.assertEqual(expected, markdown_to_html_node(input).to_html())

    def test_markdown_to_html_node_ordered_list(self):
        input = "1. list item 1\n2. list item 2\n3. list item 3"
        expected = "<div><ol><li>list item 1</li><li>list item 2</li><li>list item 3</li></ol></div>"
        self.assertEqual(expected, markdown_to_html_node(input).to_html())

    def test_markdown_to_html_node_multi_blocks(self):
        input = """
# Title

Here is some *intro* text.

## ToDo list

* task 1
* task 2
* **task 3**

## Links

1. [link1](url1)
2. [link2](url2)
"""
        expected = '<div><h1>Title</h1><p>Here is some <i>intro</i> text.</p><h2>ToDo list</h2><ul><li>task 1</li><li>task 2</li><li><b>task 3</b></li></ul><h2>Links</h2><ol><li><a href="url1">link1</a></li><li><a href="url2">link2</a></li></ol></div>'
        self.assertEqual(expected, markdown_to_html_node(input).to_html())

    def test_extract_title(self):
        input = "# Header"
        expected = "Header"
        self.assertEqual(expected, extract_title(input))

    def test_extract_title_front(self):
        input = "# Header\n\n## Subtitle\n\nsome text"
        expected = "Header"
        self.assertEqual(expected, extract_title(input))

    def test_extract_title_h2_front(self):
        input = "##Something in front\n\n# Header"
        expected = "Header"
        self.assertEqual(expected, extract_title(input))

    def test_extract_title_surrounding_whitespaces(self):
        input = "#   \tHeader   \n"
        expected = "Header"
        self.assertEqual(expected, extract_title(input))

    def test_extract_title_no_header(self):
        input = "## Here will be no header\n\njust text"
        self.assertRaises(Exception, extract_title, input)

if __name__ == "__main__":
    unittest.main()