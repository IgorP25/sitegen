import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text nde", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This is a text node", TextType.TEXT, "http://test.com")
        node2 = TextNode("This is a text node", TextType.TEXT, "http://test.com")
        self.assertEqual(node, node2)

    def test_eq5(self):
        node = TextNode("This is a text node", TextType.TEXT, "http://tes.com")
        node2 = TextNode("This is a text node", TextType.TEXT, "http://test.com")
        self.assertNotEqual(node, node2)

    def test_eq6(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT, "http://test.com")
        self.assertNotEqual(node, node2)


class TestText_node_to_html_node(unittest.TestCase):
    def test_text_node_to_html_node(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<b>This is a text node</b>")
        
    def test_text_node_to_html_node2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<i>This is a text node</i>")

    def test_text_node_to_html_node3(self):
        node = TextNode("This is a text node", TextType.CODE)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<code>This is a text node</code>")

    def test_text_node_to_html_node4(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), '<a href="https://www.google.com">This is a text node</a>')

    def test_text_node_to_html_node5(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.google.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), '<img src="https://www.google.com" alt="This is a text node"></img>')
        


if __name__ == "__main__":
    unittest.main()