import os
import re
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def clean_filename(text):
    """
    Cleans the AI text so it can be safely used as a filename.
    Replaces spaces with underscores and removes special characters.
    """
    # Convert to lowercase and replace spaces with underscores
    clean_text = text.lower().strip().replace(' ', '_')
    # Remove any characters that aren't letters, numbers, or underscores
    clean_text = re.sub(r'[^a-z0-9_]', '', clean_text)
    return clean_text

def rename_images_with_ai_descriptions():
    folder_path = os.getcwd()
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')
    
    print("Loading the AI model (this might take a moment on the first run)...\n")
    
    # Load the free BLIP model from Hugging Face
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    print(f"Scanning folder: {folder_path}\n")

    for filename in os.listdir(folder_path):
        if not os.path.isfile(filename) or filename == "rename_descriptions.py":
            continue
            
        if filename.lower().endswith(valid_extensions):
            try:
                # 1. Open the image
                raw_image = Image.open(filename).convert('RGB')
                
                # 2. Ask the AI to generate a description
                inputs = processor(raw_image, return_tensors="pt")
                out = model.generate(**inputs, max_new_tokens=20)
                description = processor.decode(out[0], skip_special_tokens=True)
                
                # 3. Clean up the text for the filename
                safe_description = clean_filename(description)
                
                # 4. Create the new filename
                name, ext = os.path.splitext(filename)
                
                # Prevent adding the description if it's already in the name
                if safe_description not in name:
                    new_name = f"{name}_{safe_description}{ext}"
                    
                    # 5. Rename the file
                    os.rename(filename, new_name)
                    print(f"✅ Renamed: {filename} -> {new_name}")
                else:
                    print(f"⏭️  Skipped: {filename} (Description already exists)")
                    
            except Exception as e:
                print(f"❌ Error processing '{filename}': {e}")

if __name__ == "__main__":
    rename_images_with_ai_descriptions()
    print("\nDone!")