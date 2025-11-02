from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode
import re
from enum import Enum
from converter import Converter

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue
            parts = str(node.text).split(delimiter)
            if len(parts) == 1:
                new_nodes.append(node)
                continue
            if len(parts) % 2 == 0:
                raise Exception("Invalid markdown")
            for i, part in enumerate(parts):
                if not part:
                    continue
                ttype = text_type if i % 2 == 1 else TextType.TEXT
                new_nodes.append(TextNode(part, ttype))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
            else:
                remaining = str(node.text)
                while len(extract_markdown_images(remaining)) > 0:
                    alt, url = extract_markdown_images(remaining)[0]
                    snippet = f"![{alt}]({url})"
                    before, after = remaining.split(snippet, 1)    
                    if before:
                        new_nodes.append(TextNode(before, TextType.TEXT))
                    new_nodes.append(TextNode(alt,TextType.IMAGE, url))
                    remaining = after
                if remaining:
                    new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining = str(node.text)
        while extract_markdown_links(remaining):
            alt, url = extract_markdown_links(remaining)[0]
            snippet = f"[{alt}]({url})"
            before, after = remaining.split(snippet, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            remaining = after
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    nodes = split_nodes_image(nodes)

    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):
    if isinstance(markdown,str):
        blocks = markdown.split("\n\n")
        for block in blocks:
            block = block.strip()
            if block == "" or block == "\n":
                blocks.remove(block)
        return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if isinstance(block, str):
        heading_options = ("# ", "## ", "### ", "#### ", "##### ", "###### ")
        if block.startswith(heading_options):
            return BlockType.HEADING
        if block.startswith("```") and block.endswith("```"):
            return BlockType.CODE
        lines = block.splitlines()
        quote = False
        for line in lines:
            if line.startswith(">"):
                quote = True
            else:
                quote = False
                break
        if quote:
            return BlockType.QUOTE
        u_list = False
        for line in lines:
            if line.startswith("- "):
                u_list = True
            else:
                u_list = False
                break
        if u_list:
            return BlockType.UNORDERED_LIST
        o_list = False
        counter = 1
        for line in lines:
            if line.startswith(f"{counter}. "):
                o_list = True
                counter += 1
            else:
                o_list = False
                break
        if o_list:
            return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
