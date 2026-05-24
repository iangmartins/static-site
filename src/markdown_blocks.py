from enum import Enum
from htmlnode import *
from textnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []

    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            stripped_blocks.append(stripped)

    return stripped_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

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
    text = block[level+1:].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if block.startswith("```"):
        block = block[3:]
    if block.endswith("```"):
        block = block[:-3]
    if block.startswith("\n"):
        block = block[1:]
        
    raw_text_node = TextNode(block, TextType.TEXT) 
    html_text_node = text_node_to_html_node(raw_text_node)
    code_node = ParentNode("code", [html_text_node])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.lstrip(">").strip())
    content = " ".join(cleaned_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line[2:].strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def olist_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        dot_index = line.find(".")
        text = line[dot_index + 1:].strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.ULIST:
            node = ulist_to_html_node(block)
        elif block_type == BlockType.OLIST:
            node = olist_to_html_node(block)
        else:
            raise ValueError(f"Unknown code block: {block_type}")
            
        block_nodes.append(node)
        
    return ParentNode("div", block_nodes)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("The markdown file DOES NOT have a h1 header")