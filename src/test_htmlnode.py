import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_None(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())

    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "github.com"})
        prop_html = ' href="github.com"'
        self.assertEqual(node.props_to_html(), prop_html)

    def test_props_to_html_multi(self):
        node = HTMLNode(props={"href": "github.com", "target": "NoNe", "stuff": "blad asdf wer"})
        prop_html = ' href="github.com" target="NoNe" stuff="blad asdf wer"'
        self.assertEqual(node.props_to_html(), prop_html)

    def test_repr_none(self):
        node = HTMLNode()
        node_repr = "HTMLNode(None, None, None, None)"
        self.assertEqual(node.__repr__(), node_repr)
        
    def test_repr(self):
        node = HTMLNode(tag="<a>", value="Some text", props={"href": "github.com"})
        node_repr = "HTMLNode(<a>, Some text, None, {'href': 'github.com'})"
        self.assertEqual(node.__repr__(), node_repr)

    def test_repr_children(self):
        node = HTMLNode(tag="<a>", value="Some text", children=[HTMLNode(), HTMLNode(value="I'm a child")])
        node_repr = "HTMLNode(<a>, Some text, [HTMLNode(None, None, None, None), HTMLNode(None, I'm a child, None, None)], None)"
        self.assertEqual(node.__repr__(), node_repr)


class TestLeafNode(unittest.TestCase):
    def test_to_html_none_value(self):
        node = LeafNode(None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_tag(self):
        node = LeafNode("Some testing being done")
        node_to_html = "Some testing being done"
        self.assertEqual(node.to_html(), node_to_html)

    def test_to_html_no_tag_with_props(self):
        node = LeafNode("Some testing being done", props={"href": "github.com", "target": "NoNe", "stuff": "blad asdf wer"})
        node_to_html = "Some testing being done"
        self.assertEqual(node.to_html(), node_to_html)

    def test_to_html_tag(self):
        node = LeafNode("Some testing being done", tag="a")
        node_to_html = "<a>Some testing being done</a>"
        self.assertEqual(node.to_html(), node_to_html)

    def test_to_html_full(self):
        node = LeafNode("Some testing being done", tag="a", props={"href": "github.com", "target": "NoNe", "stuff": "blad asdf wer"})
        node_to_html = '<a href="github.com" target="NoNe" stuff="blad asdf wer">Some testing being done</a>'
        self.assertEqual(node.to_html(), node_to_html)
        

class TestParentNode(unittest.TestCase):
    def test_to_html_simple(self):
        node = ParentNode(tag="p", children=[LeafNode("Test")])
        node_html = "<p>Test</p>"
        self.assertEqual(node_html, node.to_html())

    def test_to_html_simple_no_children(self):
        node = ParentNode(tag="p", children=[])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_simple_children_none(self):
        node = ParentNode(tag="p", children=None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_simple_no_tag(self):
        node = ParentNode(tag="", children=[LeafNode("Child_1")])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_simple_none_tag(self):
        node = ParentNode(tag=None, children=[LeafNode("Child_1")])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_multi_children(self):
        node = ParentNode(tag="p", children=[LeafNode("Child_1"), LeafNode("Child_2", tag="a"), LeafNode("Child_3", tag="b", props={"target": "Option_1", "key": "value"})])
        node_html = '<p>Child_1<a>Child_2</a><b target="Option_1" key="value">Child_3</b></p>'
        self.assertEqual(node_html, node.to_html())

    def test_to_html_multi_children_nested(self):
        node = ParentNode(tag="p", children=[LeafNode("Child_1"), LeafNode("Child_2", tag="a"), LeafNode("Child_3", tag="b", props={"target": "Option_1", "key": "value"}),
                                             ParentNode(tag="div", props={"key_1": "value_1", "key_2":"value2"}, children=[LeafNode("Child_4"),
                                                                                                                           ParentNode(tag="body", children=[LeafNode("Child_5", tag="b")])])])
        node_html = '<p>Child_1<a>Child_2</a><b target="Option_1" key="value">Child_3</b><div key_1="value_1" key_2="value2">Child_4<body><b>Child_5</b></body></div></p>'
        self.assertEqual(node_html, node.to_html())


if __name__ == "__main__":
    unittest.main()