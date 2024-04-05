import unittest
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
class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks_test(self):
        md = """This is **text** with an *italic* word and a `code block` 
and more text.

* and an ![image](https://i.imgur.com/zjjcJKZ.png) 
* and a [link](https://boot.dev)

# Header
"""
        self.assertEqual(markdown_to_blocks(md),
        ['This is **text** with an *italic* word and a `code block` \nand more text.', '* and an ![image](https://i.imgur.com/zjjcJKZ.png) \n* and a [link](https://boot.dev)', '# Header']
        )

    def test_markdown_to_blocks_with_lines(self):
        md = """
This is **text** with an *italic* word and a `code block` 
and more text.

    
* and an ![image](https://i.imgur.com/zjjcJKZ.png) 
* and a [link](https://boot.dev)


# Header


"""
        self.assertEqual(markdown_to_blocks(md),
        ['This is **text** with an *italic* word and a `code block` \nand more text.', '* and an ![image](https://i.imgur.com/zjjcJKZ.png) \n* and a [link](https://boot.dev)', '# Header']
        )


    def test_block_type(self):
        md1 = "##### Heading5"
        md2 = "``` code work \n more text \n```"
        md3 = "1. numbered list \n2. second"
        md4 = "- unnumbered list \n- next one"
        md5 = "* unnumbered list asterics"
        md6 = "just plain text"
        md7 = "> and a quote"
        self.assertEqual(block_to_block_type(md1), block_type_heading)
        self.assertEqual(block_to_block_type(md2), block_type_code)
        self.assertEqual(block_to_block_type(md3), block_type_olist)
        self.assertEqual(block_to_block_type(md4), block_type_ulist)
        self.assertEqual(block_to_block_type(md5), block_type_ulist)
        self.assertEqual(block_to_block_type(md6), block_type_paragraph)
        self.assertEqual(block_to_block_type(md7), block_type_quote)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)    

if __name__ == "__main__":
    unittest.main()