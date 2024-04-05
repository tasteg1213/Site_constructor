import work_w_files
import shutil
import os


dir_path_static = "static"
dir_path_public = "public"
dir_path_content = "content"
template_path = "template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to public directory...")
    work_w_files.copy_dir(dir_path_static, dir_path_public)

    work_w_files.generate_pages_recursive(dir_path_content, template_path, dir_path_public)
    #stringg = "dsfsdf.md"
    #print(stringg[-3:])


main()