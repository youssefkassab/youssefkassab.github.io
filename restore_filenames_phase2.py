#!/usr/bin/env python3
"""
Enhanced Rosetta Stone - Phase 2: Disambiguate by File Size
"""

import os
import re
from pathlib import Path
from PIL import Image

IMAGE_DIR = r"d:\Youssef\Programing\Projects\youssefkassab.github.io\projects screenshots\man ahyaha"

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
    """Extract dimensions from target filename"""
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

def get_file_size(filepath):
    """Get file size in bytes"""
    try:
        return os.path.getsize(filepath)
    except:
        return None

def get_current_img_files():
    """Get all current img_x.* files"""
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
    print("PHASE 2: DISAMBIGUATION BY FILE SIZE")
    print("=" * 70)
    print()
    
    # Get current unmatched img files
    current_files = get_current_img_files()
    
    # Build target lookup by dimensions + extension
    # Map: (dimensions, ext) -> list of targets
    targets_by_dim_and_ext = {}
    for target in TARGET_FILENAMES:
        dims = extract_dimensions(target)
        ext = Path(target).suffix.lower()
        if dims:
            key = (dims, ext)
            if key not in targets_by_dim_and_ext:
                targets_by_dim_and_ext[key] = []
            targets_by_dim_and_ext[key].append(target)
    
    matched_count = 0
    
    for img_file in current_files:
        filepath = os.path.join(IMAGE_DIR, img_file)
        actual_dims = get_image_dimensions(filepath)
        
        if not actual_dims:
            print(f"✗ {img_file}: Could not read dimensions")
            continue
        
        # Already exists (successfully renamed in phase 1)?
        if not os.path.exists(filepath):
            continue
        
        ext = Path(img_file).suffix.lower()
        key = (actual_dims, ext)
        
        # Try matching by dimensions + extension
        if key in targets_by_dim_and_ext:
            targets = targets_by_dim_and_ext[key]
            
            if len(targets) == 1:
                target = targets[0]
                new_path = os.path.join(IMAGE_DIR, target)
                if not os.path.exists(new_path):
                    try:
                        os.rename(filepath, new_path)
                        print(f"✓ {img_file} ({actual_dims}, ext={ext}) → {target}")
                        matched_count += 1
                    except Exception as e:
                        print(f"✗ {img_file}: Rename failed: {e}")
                else:
                    print(f"⚠ {img_file}: Target exists, skipping")
            else:
                # Multiple matches - use file size as secondary key
                img_size = get_file_size(filepath)
                
                print(f"\n{img_file} ({actual_dims}, {img_size} bytes, ext={ext}):")
                print(f"  Candidates ({len(targets)}):")
                
                # Build size map for targets
                size_map = {}
                for target in targets:
                    # Try to find existing similar file or estimate
                    target_path = os.path.join(IMAGE_DIR, target)
                    if os.path.exists(target_path):
                        tsize = os.path.getsize(target_path)
                        size_map[target] = tsize
                        print(f"    ✓ {target} ({tsize} bytes)")
                    else:
                        print(f"    ? {target} (not found)")
                
                # If we have a matching size, rename
                exact_match = None
                for target, tsize in size_map.items():
                    if tsize == img_size:
                        exact_match = target
                        break
                
                if exact_match:
                    new_path = os.path.join(IMAGE_DIR, exact_match)
                    try:
                        os.rename(filepath, new_path)
                        print(f"  → Matched by SIZE: {exact_match}")
                        matched_count += 1
                    except Exception as e:
                        print(f"  ✗ Rename failed: {e}")
                else:
                    # Suggest best match (closest size)
                    if size_map:
                        closest = min(size_map.items(), key=lambda x: abs(x[1] - img_size))
                        print(f"  → MANUAL REVIEW NEEDED (closest by size: {closest[0]}, {closest[1]} bytes)")
                    else:
                        print(f"  → MANUAL REVIEW NEEDED (no existing targets found)")
    
    print()
    print("=" * 70)
    print(f"PHASE 2 SUMMARY: {matched_count} additional files matched by extension")
    print("=" * 70)

if __name__ == "__main__":
    main()
