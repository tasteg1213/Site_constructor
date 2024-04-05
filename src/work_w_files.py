from genericpath import isfile
import os
import shutil
import re
import htmlnode
import pprint
import pathlib
from inline_markdown import extract_title

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_list = os.listdir(dir_path_content)
    for elem in dir_list:
        elem_cont_path = os.path.join(dir_path_content, elem)
        elem_dest_path = os.path.join(dest_dir_path, elem)
        if os.path.isfile(elem_cont_path) and elem[-3:] == ".md":
            elem_dest_path = elem_dest_path.replace(".md", ".html")
            generate_page(elem_cont_path, template_path, elem_dest_path)
        elif os.path.isfile(elem_cont_path) == False:
            create_dir(elem_dest_path)
            generate_pages_recursive(elem_cont_path, template_path, elem_dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    html_text = ""

    file = open(from_path, "r")
    markdown = file.read()
    file.close()

    file = open(template_path, "r")
    template = file.read()
    file.close()

    html_node = htmlnode.markdown_to_html_node(markdown)
    for child in html_node.children:
        html_text += child.to_html()

    h1 = extract_title(markdown)
    template = template.replace("{{ Title }}", h1)
    template = template.replace("{{ Content }}", html_text)


    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as file:
        file.write(template)
        file.close()

def create_dir(path2):
    if os.path.exists(path2):
        shutil.rmtree(path2)
        print(f"удалена директория перед созданием копии: {path2}")

    os.mkdir(path2)
    print(f"создана новая директория для копирования {path2}")

def copy_dir(path1, path2):
    create_dir(path2)
    dir_list = os.listdir(path1)
    for elem in dir_list:
        if os.path.isfile(os.path.join(path1, elem)):
            shutil.copy(os.path.join(path1, elem), os.path.join(path2, elem))
            print(f"скопирован файл {os.path.join(path1, elem)}")
        else:
            os.mkdir(os.path.join(path2, elem))
            print(f"копируем папку {os.path.join(path2, elem)}")
            copy_dir(os.path.join(path1, elem), os.path.join(path2, elem))