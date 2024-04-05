import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
import htmlnode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={'href':'https://', 'target':'_blank'})
        test_result = ' href="https://" target="_blank"'
        self.assertEqual(node.props_to_html(), test_result)

        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

        node = LeafNode(value = "without tag")
        self.assertEqual(
            node.to_html(),
            'without tag',
        )
        node = LeafNode(value = "without tag with props", props = {'href':'https://', 'target':'_blank'})
        self.assertEqual(
            node.to_html(),
            'without tag with props',
        )
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )


    def test_parent_exceptions(self):
        node = ParentNode(
            tag = None,
            children = 
            [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ],
            props = {'href':'https://', 'target':'_blank'}
        )
        with self.assertRaises(ValueError) as assert_error:
            node.to_html()


    def test_parent_node2(self):
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
            '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>',
        ) 


    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "a", 
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<p><a><b>Bold text</b>Normal text<i>italic text</i>Normal text</a>Normal text<i>italic text</i>Normal text</p>',
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_header_text_node_to_html_node(self):
        x = "## text234 "
        self.assertEqual(
            htmlnode.heading_block_to_html_node(x),
            ParentNode("h2", [LeafNode(None, "text234 ", None)], None),
        )
        x = "### text234 "
        self.assertEqual(
            htmlnode.heading_block_to_html_node(x),
            ParentNode("h3", [LeafNode(None, "text234 ", None)], None),
        )
        x = "#### text234 "
        self.assertEqual(
            htmlnode.heading_block_to_html_node(x),
            ParentNode("h4", [LeafNode(None, "text234 ", None)], None),
        )
        x = "##### text234 "
        self.assertEqual(
            htmlnode.heading_block_to_html_node(x),
            ParentNode("h5", [LeafNode(None, "text234 ", None)], None),
        )

    
if __name__ == "__main__":
    unittest.main()