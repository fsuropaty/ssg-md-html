import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.example.com", "target": "_blank"})
        result = node.props_to_html()
        expected = ' href="https://www.example.com" target="_blank"'
        self.assertEqual(result, expected)

    def test_constructor_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)
        # Create an HTMLNode with no arguments
        # Assert that all its attributes are None

    def test_constructor_partial_arguments(self):
        node = HTMLNode(tag="p", value="Hello, World!")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, World!")
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)

    def test_constructor_all_arguments(self):
        children = [HTMLNode(tag="span", value="Child")]
        props = {"class": "test-class"}
        node = HTMLNode(tag="div", value="Parent", children=children, props=props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Parent")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag=p, value=What a strange world, children=None, props={'class': 'primary'})",
        )

    def test_leafnode(self):
        node = LeafNode("p", "Hi Boots", {"style": "primary"})
        result = node.to_html()
        expected = '<p style="primary">Hi Boots</p>'
        self.assertEqual(result, expected)

        # Test a basic leaf node with a tag
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        # Test a leaf node with no tag
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

        # Test a leaf node with props
        node = LeafNode("a", "Click me!", {"href": "https://www.example.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.example.com">Click me!</a>'
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
