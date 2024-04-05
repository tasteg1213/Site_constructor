import re


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text):
    return re.findall(r"^\[(.*?)\]\((.*?)\)",text) + re.findall(r"[^!]\[(.*?)\]\((.*?)\)",text)

def extract_title(markdown):
    regex_exp = r"(?<=^# ).+"
    header = re.search(regex_exp, markdown, re.MULTILINE)
    if header:
        h1 = header.group(0)
    return h1