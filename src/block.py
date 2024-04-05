block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    str_list = markdown.split("\n\n")
    for elem in str_list:
        if elem.strip() != "":
            blocks.append(elem.strip())
    
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if (block[:2] == "# "
        or block[:3] == "## "
        or block[:4] == "### "
        or block[:5] == "#### "
        or block[:6] == "##### "
        or block[:7] == "###### "
    ):
        return block_type_heading
    elif block[:3] == "```" and block[-3:] == "```":
        return block_type_code
    elif block[:1] == ">":
        for line in lines:
            if line[:1] != ">":
                return block_type_paragraph
        return block_type_quote
    elif block[:2] == "* ":
        for line in lines:
            if line[:2] != "* ":
                return block_type_paragraph
        return block_type_ulist
    elif block[:2] == "- ":
        for line in lines:
            if line[:2] != "- ":
                return block_type_paragraph
        return block_type_ulist
    elif block[:3] == "1. ":
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    else:
        return block_type_paragraph