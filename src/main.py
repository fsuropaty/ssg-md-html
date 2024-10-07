import os
import shutil

from markdown_utils import copy_static, generate_page_recursive

dir_source = "./static"
dir_target = "./public"
dir_gen_source = "./content"
dir_templ = "./template.html"
dir_dest_path = "./public"


def main():

    if os.path.exists(dir_target):
        shutil.rmtree(dir_target)

    copy_static(dir_source, dir_target)

    generate_page_recursive(dir_gen_source, dir_templ, dir_dest_path)


main()
