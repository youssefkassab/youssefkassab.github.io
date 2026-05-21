import os
from PIL import Image

def rename_images_with_dimensions():
    # Get the current folder path
    folder_path = os.getcwd()
    
    # Supported image extensions
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')
    
    print(f"Scanning folder: {folder_path}\n")

    for filename in os.listdir(folder_path):
        # Skip directories and the script itself
        if not os.path.isfile(filename) or filename == "rename_dimensions.py":
            continue
            
        if filename.lower().endswith(valid_extensions):
            try:
                # Open the image to get its width and height
                with Image.open(filename) as img:
                    width, height = img.size
                
                # Split the filename into the name and the extension
                name, ext = os.path.splitext(filename)
                
                # Create the dimension string, e.g., "_1920x1080"
                dimension_suffix = f"_{width}x{height}"
                
                # Check if the file already has the dimensions in its name
                if not name.endswith(dimension_suffix):
                    new_name = f"{name}{dimension_suffix}{ext}"
                    
                    # Rename the file
                    os.rename(filename, new_name)
                    print(f"✅ Renamed: {filename} -> {new_name}")
                else:
                    print(f"⏭️  Skipped (already renamed): {filename}")
                    
            except Exception as e:
                print(f"❌ Error processing '{filename}': {e}")

if __name__ == "__main__":
    rename_images_with_dimensions()
    print("\nDone!")