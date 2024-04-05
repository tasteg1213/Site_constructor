import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links

class TestInline(unittest.TestCase):
    def test_link_img(self):
        text = """
        This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png). This is text with a [link](https://www.example.com) and [another](https://www.example.com/another). And sentance with [words in square brackets] and then some usual brackets (with words inside).
        Next line ![image2](https:/ddfsdfsdf) and if we multiline 
        [link3](next line test)
        """
        img = [('image', 'https://i.imgur.com/zjjcJKZ.png'), ('another', 'https://i.imgur.com/dfsdkjfd.png'), ('image2', 'https:/ddfsdfsdf')]
        link = [('link', 'https://www.example.com'), ('another', 'https://www.example.com/another'), ('link3', 'next line test')]
        
        self.assertListEqual(extract_markdown_images(text), img)
        self.assertListEqual(extract_markdown_links(text), link)

        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )
if __name__ == "__main__":
    unittest.main()