import re

from textnode import text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_html_node(markdown):
    top_node = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        top_node.children.append(block_to_html_node(block))
    return top_node

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)

def block_to_block_type(block):
    if block.startswith("#"):
        return block_type_heading
    if block.startswith("```"):
        if block.endswith("```"):
            return block_type_code
    if block.startswith(">"):
        nonquote = list(filter(lambda line: not line.startswith(">"), block.splitlines()))
        if len(nonquote) == 0:
            return block_type_quote
    if block.startswith(("* ", "- ")):
        nonlist = list(filter(lambda line: not line.startswith(("* ", "- ")), block.splitlines()))
        if len(nonlist) == 0:
            return block_type_ulist
    if block.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")):
        nonlist = list(filter(lambda line: re.match(r"\d+?\.", line) is None, block.splitlines()))
        if len(nonlist) == 0:
            return block_type_olist
    return block_type_paragraph

def markdown_to_blocks(markdown):
    return list(filter(lambda x: x != "", map(lambda line: line.strip(), markdown.split(sep="\n\n"))))

def paragraph_to_html_node(block):
    if block == "":
        return
    paragraph = ParentNode("p", [])
    crushed = " ".join(block.strip().splitlines())
    for node in list(map(text_node_to_html_node, text_to_textnodes(crushed))):
        paragraph.children.append(node)
    return paragraph

def heading_to_html_node(block):
    match_tag = re.match(r"(#+)(.*)", block)
    count = len(match_tag.group(1))
    content = match_tag.group(2).strip()
    nodes = list(map(text_node_to_html_node, text_to_textnodes(content)))
    head_node = ParentNode(f"h{count}", [])
    for node in nodes:
        head_node.children.append(node)
    return head_node

def code_to_html_node(block):
    return LeafNode("code", block[3:-3])

def quote_to_html_node(block):
    quote = ParentNode("blockquote", [])
    crushed = " ".join(map(lambda line: line.lstrip(">").strip(), block.strip().splitlines()))
    for node in list(map(text_node_to_html_node, text_to_textnodes(crushed))):
        quote.children.append(node)
    return quote

def olist_to_html_node(block):
    ord_list = ParentNode("ol", [])
    for list_item in block.splitlines():
        clean_list_item = re.match(r"(\d+?\.)(.*)", list_item).group(2).strip()
        ord_list.children.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(clean_list_item)))))
    return ord_list

def ulist_to_html_node(block):
    unord_list = ParentNode("ul", [])
    for list_item in block.splitlines():
        clean_list_item = list_item.lstrip("*-").strip()
        unord_list.children.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(clean_list_item)))))
    return unord_list

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise Exception("No h1 header found")