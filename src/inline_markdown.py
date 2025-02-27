import re

from itertools import zip_longest
from textnode import TextNode, TextType

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        regex = re.compile(r"\[(.*?)\]\((.*?)\)")
        text = regex.split(node.text)
        splits = list(zip_longest(text[::3], text[1::3], text[2::3]))
        for txt, alt, url in splits:
            if txt is not None and txt != "":
                new_nodes.append(TextNode(txt, node.text_type, node.url))
            if alt is not None and url is not None:
                new_nodes.append(TextNode(alt, TextType.LINK, url))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        regex = re.compile(r"!\[(.*?)\]\((.*?)\)")
        text = regex.split(node.text)
        splits = list(zip_longest(text[::3], text[1::3], text[2::3]))
        for txt, alt, url in splits:
            if txt is not None and txt != "":
                new_nodes.append(TextNode(txt, node.text_type, node.url))
            if alt is not None and url is not None:
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))

    return new_nodes

def extract_markdown_links(text):
    regex = re.compile(r"\[(.*?)\]\((.*?)\)")
    return regex.findall(text)

def extract_markdown_images(text):
    regex = re.compile(r"!\[(.*?)\]\((.*?)\)")
    return regex.findall(text)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        text = node.text.split(delimiter)
        for i in range(0, len(text)):
            if text[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text[i], node.text_type, node.url))
            else:
                new_nodes.append(TextNode(text[i], text_type))

    return new_nodes