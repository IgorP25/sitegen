import os
import shutil
from textnode import TextNode, TextType
from block_markdown import markdown_to_html_node, extract_title


def main():
    new_tn = TextNode("test", TextType.TEXT, "http://localhost:8888")
    print(new_tn)
    delete_and_copy("static", "public")
    generate_pages_recursive("content", "template.html", "public")


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


def generate_page(from_path, template_path, dest_path):
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
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    with open(dest_path, "w") as f:
        f.write(generated)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception("dir_path_content does not exist")
    for path in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, path)
        if os.path.isfile(full_path):
            if str(os.path.basename(path)).endswith(".md"):
                generate_page(full_path, template_path, os.path.join(dest_dir_path, path.removesuffix(".md") + ".html"))
            continue
        generate_pages_recursive(full_path, template_path, os.path.join(dest_dir_path, path))


if __name__ == "__main__":
    main()