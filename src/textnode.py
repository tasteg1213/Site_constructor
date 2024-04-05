from inline_markdown import extract_markdown_links, extract_markdown_images

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

type_symbol_dict = {
    "`":"code",
    "**":"bold",
    "*":"italic",
}

class TextNode():

    def __init__(self,text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"




def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if isinstance(old_node, TextNode):
            list_split = old_node.text.split(delimiter)
            splited_nodes = []
            if len(list_split) % 2 == 0:
                raise ValueError(f"Invalid markdown, {text_type} section not closed")
            for i in range(len(list_split)):
                if list_split[i] == "":
                    continue
                if i%2 == 0:
                    splited_nodes.append(TextNode(list_split[i], old_node.text_type))
                else:
                    splited_nodes.append(TextNode(list_split[i], text_type))
            new_nodes.extend(splited_nodes)
        else:
            new_nodes.append(old_node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes =[]
    for old_node in old_nodes:
        extracted_img = extract_markdown_images(old_node.text)
        if len(extracted_img) == 0 and old_node.text != "":
            new_nodes.append(old_node)
            continue
        for image_tup in extracted_img:
            splited_node_text = old_node.text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            if splited_node_text[0] != "":
                new_nodes.append(TextNode(splited_node_text[0], old_node.text_type))
            new_nodes.append(TextNode(image_tup[0], text_type_image, image_tup[1]))
            old_node.text = splited_node_text[1]
        if old_node.text != "":
            new_nodes.append(TextNode(old_node.text, old_node.text_type))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes =[]
    for old_node in old_nodes:
        extracted_links = extract_markdown_links(old_node.text)
        if len(extracted_links) == 0 and old_node.text != "":
            new_nodes.append(old_node)
            continue
        for link_tup in extracted_links:
            splited_node_text = old_node.text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
            if splited_node_text[0] != "":
                new_nodes.append(TextNode(splited_node_text[0], old_node.text_type))
            new_nodes.append(TextNode(link_tup[0], text_type_link, link_tup[1]))
            old_node.text = splited_node_text[1]
        if old_node.text != "":
            new_nodes.append(TextNode(old_node.text, old_node.text_type))
    return new_nodes


def text_to_textnodes(text):
    node = [TextNode(text, text_type_text)]
    node = split_nodes_delimiter(node, "`", text_type_code)
    node = split_nodes_delimiter(node, "**", text_type_bold)
    node = split_nodes_delimiter(node, "*", text_type_italic)
    node = split_nodes_image(node)
    node = split_nodes_links(node)
    return node