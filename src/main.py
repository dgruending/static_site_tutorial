import pathlib
import shutil
from text_parser import extract_title, markdown_to_html_node

def copy_from_to(src, dest):
    # Preparation steps
    src_path = pathlib.Path(src)
    if not src_path.exists() or not src_path.is_dir():
        raise Exception("Invalid source directory for copy operations")
    # check if dest exists already, to either delete all content or create the full path
    dest_path = pathlib.Path(dest)
    if dest_path.exists():
        shutil.rmtree(dest)
    pathlib.Path(dest).mkdir(parents=True, exist_ok=True)


    for file_dir in src_path.iterdir():
        if file_dir.is_file():
            shutil.copy(file_dir, dest_path)
        elif file_dir.is_dir():
            new_dest_path = dest_path.joinpath(file_dir.name)
            copy_from_to(file_dir, new_dest_path)

def generate_page(from_path, template_path, dest_path):
    from_path = pathlib.Path(from_path)
    if not from_path.exists():
        raise Exception(f"Source file: {from_path} does not exist")
    if not from_path.is_file():
        raise Exception(f"{from_path} is not a file")
    template_path = pathlib.Path(template_path)
    if not template_path.exists():
        raise Exception(f"Source file: {template_path} does not exist")
    if not template_path.is_file():
        raise Exception(f"{template_path} is not a file")

    dest_path = pathlib.Path(dest_path)
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as src_file:
        with open(template_path) as template_file:
            markdown = src_file.read()
            template = template_file.read()
            html_content = markdown_to_html_node(markdown).to_html()
            title = extract_title(markdown)
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html_content)
            
            pathlib.Path(dest_path.parent).mkdir(parents=True, exist_ok=True)
            with open(dest_path, "w") as dest_file:
                dest_file.write(template)

def generate_pages_recursive(content_dir_path, template_path, dest_dir_path):
    content_dir_path = pathlib.Path(content_dir_path)
    dest_dir_path = pathlib.Path(dest_dir_path)
    if content_dir_path.exists() and content_dir_path.is_dir():
        for file_dir in content_dir_path.iterdir():
            if file_dir.is_file():
                generate_page(file_dir, template_path, dest_dir_path.joinpath(file_dir.name).with_suffix(".html"))
            elif file_dir.is_dir():
                generate_pages_recursive(file_dir, template_path, dest_dir_path.joinpath(file_dir.name))


def main():
    copy_from_to("static", "public")
    generate_pages_recursive("content/", "template.html", "public/")

if __name__ == "__main__":
    main()