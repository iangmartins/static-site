import os, shutil
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
            
def generate_page(from_path, template_path, dest_path):
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
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
        
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    entries = os.listdir(dir_path_content)
    
    for entry in entries:
        from_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(from_path) and entry.endswith(".md"):
            dest_name = entry.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, dest_name)
            generate_page(from_path, template_path, dest_path)
        elif os.path.isdir(from_path):
            new_dest_dir = os.path.join(dest_dir_path, entry)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(from_path, template_path, new_dest_dir)

def main():
    source_dir = "static"
    dest_dir = "public"
    content_dir = "content"
    template_file = "template.html"
    
    print("Initiating static copy process...")
    clean_and_copy_directory(source_dir, dest_dir)
    
    #print("Generating HTML pages...")
    #generate_page("content/index.md", "template.html", "public/index.html")
    
    print("\nInitiating recursive HTML page generation...")
    generate_pages_recursive(content_dir, template_file, dest_dir)
    
    print("Copy finished successfully!")
    
if __name__ == "__main__":
    main()