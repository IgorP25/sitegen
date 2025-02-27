import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
    )


class TestSplit_nodes_delimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        answer = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, answer)

    def test_split_nodes_delimiter2(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        answer = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, answer)

    def test_split_nodes_delimiter3(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        answer = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, answer)

    def test_split_nodes_delimiter4(self):
        node = TextNode("This is text with a **bold block****bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        answer = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, answer)

    def test_split_nodes_delimiter5(self):
        node = TextNode("This is text with a `**bold block**` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        answer = [
            TextNode("This is text with a `", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode("` word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, answer)


class TestMarkdown_images(unittest.TestCase):
    def test_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        answer = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), answer)


class TestMarkdown_links(unittest.TestCase):
    def test_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        answer = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), answer)


class TestSplit_nodes_image(unittest.TestCase):
        def test_split_nodes_image(self):
            node = TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.TEXT,)
            new_nodes = split_nodes_image([node])
            answer = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
                ]
            self.assertEqual(new_nodes, answer)

        def test_split_nodes_image2(self):
            node = TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) or is it?",
                TextType.TEXT,)
            new_nodes = split_nodes_image([node])
            answer = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" or is it?", TextType.TEXT)
                    ]
            self.assertEqual(new_nodes, answer)


class TestSplit_nodes_link(unittest.TestCase):
        def test_split_nodes_link(self):
            node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,)
            new_nodes = split_nodes_link([node])
            answer = [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
                    ]
            self.assertEqual(new_nodes, answer)

        def test_split_nodes_link2(self):
            node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) or is it?",
                TextType.TEXT,)
            new_nodes = split_nodes_link([node])
            answer = [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" or is it?", TextType.TEXT)
                    ]
            self.assertEqual(new_nodes, answer)

        def test_split_nodes_link3(self):
            node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)[to google](https://www.google.com) or is it?",
                TextType.TEXT,)
            new_nodes = split_nodes_link([node])
            answer = [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode("to google", TextType.LINK, "https://www.google.com"),
                TextNode(" or is it?", TextType.TEXT)
                    ]
            self.assertEqual(new_nodes, answer)


class TestText_to_textnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        answer = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
            ]
        self.assertEqual(text_to_textnodes(text), answer)



if __name__ == "__main__":
    unittest.main()