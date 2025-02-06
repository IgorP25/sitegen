import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        node = HTMLNode()
        self.assertEqual(str(node), "tag: None, value: None, children: None, props: None")

    def test_print2(self):
        node = HTMLNode("href")
        self.assertEqual(str(node), "tag: href, value: None, children: None, props: None")
    
    def test_print3(self):
        node = HTMLNode("href", "https://www.google.com")
        self.assertEqual(str(node), "tag: href, value: https://www.google.com, children: None, props: None")
    
    def test_print4(self):
        node = HTMLNode("href", "https://www.google.com", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_print5(self):
        node = HTMLNode("href", "https://www.google.com", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    

class TestLeafNode(unittest.TestCase):
    def test_leaf(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


class TestParentNode(unittest.TestCase):
    def test_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent2(self):
        node = ParentNode("p",
                          [
            ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
                          ]
        )

        self.assertEqual(node.to_html(), "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>")

    def test_parent3(self):
        node = ParentNode("p", [])

        self.assertEqual(node.to_html(), "<p></p>")

    def test_parent4(self):
        node = ParentNode("p", [])
        node.children = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent5(self):
        with self.assertRaises(TypeError):
            node = ParentNode("p")


if __name__ == "__main__":
    unittest.main()          