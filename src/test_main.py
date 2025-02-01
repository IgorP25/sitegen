import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from main import text_node_to_html_node

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