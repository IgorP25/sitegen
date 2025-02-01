import unittest

from textnode import TextNode, TextType


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
        


if __name__ == "__main__":
    unittest.main()