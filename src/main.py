import os, shutil, sys
from markdown_blocks import extract_title, markdown_to_html_node

def clean_and_copy_directory(source, destination):
    if os.path.exists(destination):
        print(f"Cleaning existing directory: {destination}")
        shutil.rmtree(destination)

    os.mkdir(destination)
    copy_recursive(source, destination)

def copy_recursive(current_source, current_destination):
    items = os.listdir(current_source)
    
    for item in items:
        src_path = os.path.join(current_source, item)
        dst_path = os.path.join(current_destination, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            copy_recursive(src_path, dst_path)
            
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
        
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    title = extract_title(markdown_content)
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_string)
    
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
        
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    entries = os.listdir(dir_path_content)
    
    for entry in entries:
        from_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(from_path) and entry.endswith(".md"):
            dest_name = entry.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, dest_name)
            generate_page(from_path, template_path, dest_path, basepath)
        elif os.path.isdir(from_path):
            new_dest_dir = os.path.join(dest_dir_path, entry)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(from_path, template_path, new_dest_dir, basepath)

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    source_dir = "static"
    dest_dir = "docs"
    content_dir = "content"
    template_file = "template.html"
    
    print("Initiating static copy process...")
    clean_and_copy_directory(source_dir, dest_dir)
    
    print("Generating HTML pages...")
    generate_page("content/index.md", "template.html", "docs/index.html", basepath)
    
    print("\nInitiating recursive HTML page generation...")
    generate_pages_recursive(content_dir, template_file, dest_dir, basepath)
    
    print("Copy finished successfully!")
    
if __name__ == "__main__":
    main()