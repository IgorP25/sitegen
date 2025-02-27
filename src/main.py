import os
import shutil
import sys
from textnode import TextNode, TextType
from block_markdown import markdown_to_html_node, extract_title


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    delete_and_copy("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


def delete_and_copy(src, dest):
    if not os.path.exists(src):
        raise Exception("Source path does not exist.")
    if os.path.exists(dest):    
        shutil.rmtree(dest)
    os.mkdir(dest)
    source_dirs = os.listdir(src)
    for path in source_dirs:
        if os.path.isfile(os.path.join(src, path)):
            print(shutil.copy(os.path.join(src, path), os.path.join(dest, path)))
            continue
        delete_and_copy(os.path.join(src, path), os.path.join(dest, path))


def generate_page(from_path, template_path, dest_path, basepath):
    if not os.path.exists(from_path):
        raise Exception("from_path does not exist")
    if not os.path.exists(template_path):
        raise Exception("template_path does not exist")
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    generated = template.replace(r"{{ Title }}", title).replace(r"{{ Content }}", html)
    generated = generated.replace(r'href="/', f'href="{basepath}').replace(r'src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        path_split = os.path.split(dest_dir)
        paths = [dest_dir]
        while(path_split[0]):
            paths.append(path_split[0])
            path_split = os.path.split(path_split[0])
        paths.reverse()
        for p in paths:
            if not os.path.exists(p):
                os.mkdir(p)
    with open(dest_path, "w") as f:
        f.write(generated)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dir_path_content):
        raise Exception("dir_path_content does not exist")
    for path in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, path)
        if os.path.isfile(full_path):
            if str(os.path.basename(path)).endswith(".md"):
                generate_page(full_path, template_path, os.path.join(dest_dir_path, path.removesuffix(".md") + ".html"), basepath)
            continue
        generate_pages_recursive(full_path, template_path, os.path.join(dest_dir_path, path), basepath)


if __name__ == "__main__":
    main()