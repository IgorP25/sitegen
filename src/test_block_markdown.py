import unittest

from htmlnode import ParentNode, LeafNode
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    extract_title
    )


class TestMarkdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        answer = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ]
        self.assertEqual(markdown_to_blocks(markdown), answer)

    def test_markdown_to_blocks2(self):
        markdown = "# This is a heading\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        answer = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ]
        self.assertEqual(markdown_to_blocks(markdown), answer)


class TestBlock_to_block_type(unittest.TestCase):
    def test_block_to_block_type(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        blocks = markdown_to_blocks(markdown)
        result = []
        for block in blocks:
            result.append(block_to_block_type(block))
        answer = ["heading", "paragraph", "unordered_list"]
        self.assertEqual(result, answer)

    def test_block_to_block_type2(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n1. This.\n2. That\n3. The other.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        blocks = markdown_to_blocks(markdown)
        result = []
        for block in blocks:
            result.append(block_to_block_type(block))
        answer = ["heading", "paragraph", "ordered_list", "unordered_list"]
        self.assertEqual(result, answer)
        

class TestMarkdown_to_html_node(unittest.TestCase):
    def test_markdown_to_html_node(self):
        markdown = "#### This *is* a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n1. This.\n2. That\n3. The other.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        answer = "<div><h4>This <i>is</i> a heading</h4><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ol><li>This.</li><li>That</li><li>The other.</li></ol><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), answer)

    def test_markdown_to_html_node2(self):
        markdown = "#### This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n1. This.\n2. That\n3. The other.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        answer = "<div><h4>This is a heading</h4><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ol><li>This.</li><li>That</li><li>The other.</li></ol><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), answer)

    def test_markdown_to_html_node3(self):
        markdown = "#### This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n1. This.\n2. That\n3. The other.\n\n* This is the first **list item** in a list block\n* This is a list item\n* This is another list item\n"
        answer = "<div><h4>This is a heading</h4><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ol><li>This.</li><li>That</li><li>The other.</li></ol><ul><li>This is the first <b>list item</b> in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), answer)

    def test_markdown_to_html_node4(self):
        markdown = "#### This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n1. This.\n2. That\n3. The other.\n\n```This is some code and stuff **testing**\nAnd another line of code```\n\n* This is the first **list item** in a list block\n* This is a list item\n* This is another list item\n"
        answer = "<div><h4>This is a heading</h4><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ol><li>This.</li><li>That</li><li>The other.</li></ol><code>This is some code and stuff **testing**\nAnd another line of code</code><ul><li>This is the first <b>list item</b> in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>" 
        self.assertEqual(markdown_to_html_node(markdown).to_html(), answer)

    def test_markdown_to_html_node5(self):
        markdown = "#### This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n1. This.\n2. That\n3. The other.\n\n>This is a quote **testing**\n>And another quote\n>Yet again\n\n* This is the first **list item** in a list block\n* This is a list item\n* This is another list item\n"
        answer = "<div><h4>This is a heading</h4><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ol><li>This.</li><li>That</li><li>The other.</li></ol><blockquote>This is a quote <b>testing</b> And another quote Yet again</blockquote><ul><li>This is the first <b>list item</b> in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), answer)


class TestExtract_title(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title2(self):
        with self.assertRaises(Exception):
            extract_title("## Hello")


if __name__ == "__main__":
    unittest.main()