from block import (
    markdown_to_blocks, 
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_ulist,
    block_type_olist,
)
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
    text_to_textnodes,
)

def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(value = text_node.text)
    elif text_node.text_type == text_type_bold:
        return LeafNode(tag = "b", value = text_node.text)
    elif text_node.text_type == text_type_italic:
        return LeafNode(tag = "i", value = text_node.text)
    elif text_node.text_type == text_type_code:
        return LeafNode(tag = "code", value = text_node.text)
    elif text_node.text_type == text_type_link:
        return LeafNode(tag = "a", value = text_node.text, props = {"href":text_node.url})
    elif text_node.text_type == text_type_image:
        return LeafNode(tag = "img", value = "", props = {"src":text_node.url, "alt":text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")   

class HTMLNode():
    def __init__(self,tag = None, value = None, children = [], props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        html_out = ""
        for x in self.props.items():
            html_out += f' {x[0]}="{x[1]}"'
        return html_out

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("value is empty")
        if self.tag == None or self.tag == "":
            return self.value
        open_tag = f'<{self.tag}{self.props_to_html()}>'
        close_tag = f'</{self.tag}>'
        return f'{open_tag}{self.value}{close_tag}'

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.props == other.props:
            return True

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children = [], props = None):
        super().__init__(tag, None, children, props)

    def __eq__(self, other):
        if self.tag == other.tag and self.children == other.children and self.props == other.props:
            return True

    def to_html(self):
        if self.children is None:
            raise ValueError("HTML ERROR: No children in parent node")
        if self.tag is None:
            raise ValueError("HTML ERROR: No tag in parent node")
        str_repr = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            str_repr += child.to_html()

        str_repr += f"</{self.tag}>"

        return str_repr

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

def markdown_to_html_node(markdown):
    if markdown == "":
        raise ValueError('Для перевода в HTMLnode передана пустая строка')
    children_html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == block_type_paragraph:
            children_html_nodes.append(paragraph_block_to_html_node(block))
        elif block_to_block_type(block) == block_type_code:
            children_html_nodes.append(code_block_to_html_node(block))
        elif block_to_block_type(block) == block_type_heading:
            children_html_nodes.append(heading_block_to_html_node(block))
        elif block_to_block_type(block) == block_type_ulist:
            children_html_nodes.append(unorderedlist_block_to_html_node(block))
        elif block_to_block_type(block) == block_type_olist:
            children_html_nodes.append(orderedlist_block_to_html_node(block))
        elif block_to_block_type(block) == block_type_quote:
            children_html_nodes.append(quote_block_to_html_node(block))
    return ParentNode("div", children_html_nodes)

def paragraph_block_to_html_node(block):
    children = text_to_textnodes(block)
    htmlchildren = []
    for child in children:
        htmlchildren.append(text_node_to_html_node(child))
    return ParentNode("p", htmlchildren)

def code_block_to_html_node(block):
    children = text_to_textnodes(block[3:-3])
    htmlchildren = []
    for child in children:
        htmlchildren.append(text_node_to_html_node(child))
    return ParentNode("pre", [ParentNode("code", htmlchildren)])

def heading_block_to_html_node(block):
    if block[:2] == "# ":
        tag = "h1"
        block = block[2:]
    elif block[:3] == "## ":
        tag = "h2"
        block = block[3:]
    elif block[:4] == "### ":
        tag = "h3"
        block = block[4:]
    elif block[:5] == "#### ":
        tag = "h4"
        block = block[5:]
    elif block[:6] == "##### ":
        tag = "h5"
        block = block[6:]
    elif block[:7] == "###### ":
        tag = "h6"
        block = block[7:]
    children = text_to_textnodes(block)
    htmlchildren = []
    for child in children:
        htmlchildren.append(text_node_to_html_node(child))
    return ParentNode(tag, htmlchildren)

def unorderedlist_block_to_html_node(block):
    children = block.split("\n")
    htmlparent = []
    for child in children:
        if child != "":
            htmlchildren = []
            child = child[2:]
            child_nodes = text_to_textnodes(child)
            for elem in child_nodes:
                htmlchildren.append(text_node_to_html_node(elem))
            htmlparent.append(ParentNode("li", htmlchildren))
    return ParentNode("ul", htmlparent)

def orderedlist_block_to_html_node(block):
    children = block.split("\n")
    htmlparent = []
    i = 0
    for child in children:
        if child != "":
            i += 1
            htmlchildren = []
            child = child[len(str(i)) + 2:]
            child_nodes = text_to_textnodes(child)
            for elem in child_nodes:
                htmlchildren.append(text_node_to_html_node(elem))
            htmlparent.append(ParentNode("li", htmlchildren))
    return ParentNode("ol", htmlparent)

def quote_block_to_html_node(block):
    children = block.split("\n")
    child_lines = ""
    htmlchild = []
    for child in children:
        if child != "":
            child_lines += child[2:] + " "
    child_lines = text_to_textnodes(child_lines)
    for elem in child_lines:
        htmlchild.append(text_node_to_html_node(elem))
    return ParentNode("blockquote", htmlchild)