import pathlib
import shutil
from textnode import TextNode

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


def main():
    copy_from_to("./static", "./public")

if __name__ == "__main__":
    main()