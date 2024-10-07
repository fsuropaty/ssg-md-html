import os
import shutil

from block_md import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found")


def copy_static(source, target):
    if not os.path.exists(target):
        print("make directory :", target)
        os.mkdir(target)

    for file in os.listdir(source):
        spath = os.path.join(source, file)
        tpath = os.path.join(target, file)

        if os.path.isfile(spath):
            print(f"copying file from {spath} to {tpath}")
            shutil.copy(spath, tpath)
        else:
            copy_static(spath, tpath)


def generate_page(from_path, template_path, dest_path):
    print(f"* Generating page {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as md_file:
        read_md = md_file.read()

    with open(template_path, "r") as template_file:
        read_template = template_file.read()

    title = extract_title(read_md)
    content = markdown_to_html_node(read_md).to_html()

    new_template = read_template.replace("{{ Title }}", title)
    new_template = new_template.replace("{{ Content }}", content)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as output_file:
        output_file.write(new_template)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):

    for file in os.listdir(dir_path_content):
        spath = os.path.join(dir_path_content, file)
        dpath = os.path.join(dest_dir_path, file)

        if os.path.isfile(spath):
            if spath.endswith(".md"):
                dpath = dpath.replace(".md", ".html")
            os.makedirs(dest_dir_path, exist_ok=True)
            generate_page(spath, template_path, dpath)
        else:
            generate_page_recursive(spath, template_path, dpath)
