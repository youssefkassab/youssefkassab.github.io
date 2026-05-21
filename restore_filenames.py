#!/usr/bin/env python3
"""
Rosetta Stone Filename Restoration Script
Matches generic img_x files to their target long filenames based on image dimensions
"""

import os
import re
from pathlib import Path
from PIL import Image

# Directory containing the images
IMAGE_DIR = r"d:\Youssef\Programing\Projects\youssefkassab.github.io\projects screenshots\man ahyaha"

# Target filenames (with dimensions embedded)
TARGET_FILENAMES = [
    "527347872_18334327468201460_3483731416238086089_n_1080x1440_a_man_standing_in_front_of_a_projector_screen.webp",
    "527512533_18334327426201460_4904780385459916981_n_1080x1440_a_man_and_a_boy_are_working_on_a_laptop.jpeg",
    "FB_IMG_1754240608376_1080x1440_a_group_of_children_sitting_at_a_table_with_laptops.jpg",
    "hemex ceo_1080x1440_a_man_in_a_white_shirt_and_black_pants_is_dancing.webp",
    "IMG-20250803-WA0050_1204x1600_a_group_of_children_sitting_at_desks_in_a_classroom.jpg",
    "IMG-20250803-WA0051_1204x1600_a_group_of_children_sitting_in_a_classroom.jpg",
    "IMG-20250803-WA0056_1204x1600_a_group_of_children_sitting_at_a_table_with_laptops.jpg",
    "pepole playing with RC robotes_1080x1440_a_group_of_people_sitting_around_a_table.webp",
    "team-new aspect_1080x1108_hex_team_t__shirt_photo.jpg",
    "team_1080x1440_the_team_of_the_team.jpg",
    "youssef instractor clear image with no obsticals and no youssef_1204x1600_a_group_of_children_sitting_at_a_table_with_laptops.jpg",
    "youssef instractor-1-close imge he is pointing at somthing in the boy screen_1080x1440_a_man_and_a_boy_are_working_on_a_laptop.jpg",
    "youssef instractore back image shows the kids not clearly and youssef back_1018x1178_a_group_of_children_sitting_in_a_classroom.jpg",
    "youssef instractore high qulity image from the side view has the class and youssef from his side-back _1204x1398_a_man_standing_in_front_of_a_classroom_with_students.jpg",
    "youssef instractore image of large number of pepole holding certaficat _1080x1440_a_group_of_people_holding_up_signs.jpg",
    "youssef instractore team far view_433x767_a_group_of_children_sitting_in_a_classroom.png",
    "youssef instractore-1 holding laptop in the middel of the fram giving a lecture wile holding his laptop flat straight so anyone could see_1265x620_a_group_of_people_sitting_around_a_table.png",
    "youssef instractornear hight qulity image of the class youssef is not totaly visable_1440x960_a_group_of_children_sitting_around_a_laptop.png",
    "youssef instractornear hight qulity image of the class youssef is visable with wider angle than its twin_1080x1440_a_group_of_children_sitting_at_a_table_with_laptops.jpeg",
]

def extract_dimensions(filename):
    """Extract dimensions from target filename (e.g., '1080x1440')"""
    match = re.search(r'_(\d+x\d+)_', filename)
    if match:
        return match.group(1)
    return None

def get_image_dimensions(filepath):
    """Get actual image dimensions as 'WIDTHxHEIGHT'"""
    try:
        img = Image.open(filepath)
        width, height = img.size
        return f"{width}x{height}"
    except Exception as e:
        print(f"  ⚠ Could not read {filepath}: {e}")
        return None

def build_dimension_map():
    """Build map: dimensions -> [list of target filenames with those dimensions]"""
    dim_map = {}
    for target in TARGET_FILENAMES:
        dims = extract_dimensions(target)
        if dims:
            if dims not in dim_map:
                dim_map[dims] = []
            dim_map[dims].append(target)
    return dim_map

def get_current_img_files():
    """Get all current img_x.* files in the directory"""
    img_files = []
    try:
        for f in os.listdir(IMAGE_DIR):
            if re.match(r'^img_\d+\.\w+$', f):
                img_files.append(f)
    except Exception as e:
        print(f"Error listing directory: {e}")
    return sorted(img_files)

def main():
    print("=" * 70)
    print("ROSETTA STONE FILENAME RESTORATION")
    print("=" * 70)
    print()
    
    # Build dimension map
    dim_map = build_dimension_map()
    print(f"✓ Loaded {len(TARGET_FILENAMES)} target filenames")
    print(f"✓ Found {len(dim_map)} unique dimensions")
    print()
    
    # Get current img files
    current_files = get_current_img_files()
    print(f"✓ Found {len(current_files)} current img_x files")
    print()
    
    if not current_files:
        print("⚠ No img_x files found!")
        return
    
    # Match and rename
    print("MATCHING PROCESS:")
    print("-" * 70)
    
    matched_count = 0
    unmatched = []
    
    for img_file in current_files:
        filepath = os.path.join(IMAGE_DIR, img_file)
        actual_dims = get_image_dimensions(filepath)
        
        if not actual_dims:
            unmatched.append((img_file, "Could not read dimensions"))
            print(f"✗ {img_file}: Could not read dimensions")
            continue
        
        # Find matching target filename(s)
        if actual_dims in dim_map:
            targets = dim_map[actual_dims]
            
            if len(targets) == 1:
                target = targets[0]
                new_path = os.path.join(IMAGE_DIR, target)
                
                # Avoid overwriting existing files
                if not os.path.exists(new_path):
                    try:
                        os.rename(filepath, new_path)
                        print(f"✓ {img_file} ({actual_dims}) → {target}")
                        matched_count += 1
                    except Exception as e:
                        unmatched.append((img_file, f"Rename failed: {e}"))
                        print(f"✗ {img_file}: Rename failed: {e}")
                else:
                    unmatched.append((img_file, "Target already exists"))
                    print(f"⚠ {img_file} ({actual_dims}): Target already exists")
            else:
                # Multiple targets with same dimensions - list them
                print(f"? {img_file} ({actual_dims}): Multiple matches:")
                for t in targets:
                    print(f"    - {t}")
                unmatched.append((img_file, f"Ambiguous: {len(targets)} matches"))
        else:
            unmatched.append((img_file, f"No match for dimensions {actual_dims}"))
            print(f"✗ {img_file} ({actual_dims}): No target found")
    
    print()
    print("=" * 70)
    print(f"SUMMARY: {matched_count}/{len(current_files)} files renamed successfully")
    
    if unmatched:
        print(f"\nUNMATCHED ({len(unmatched)}):")
        for file, reason in unmatched:
            print(f"  - {file}: {reason}")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
