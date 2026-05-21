#!/usr/bin/env python3
"""
Phase 3: Manual Matching Based on HTML References and File Extensions
"""

import os

IMAGE_DIR = r"d:\Youssef\Programing\Projects\youssefkassab.github.io\projects screenshots\man ahyaha"

# Manual mappings based on:
# 1. File extension matching
# 2. HTML references
# 3. Size context
MANUAL_MAPPINGS = {
    "img_1.jpg": "youssef instractor clear image with no obsticals and no youssef_1204x1600_a_group_of_children_sitting_at_a_table_with_laptops.jpg",
    "img_2.jpg": "youssef instractor-1-close imge he is pointing at somthing in the boy screen_1080x1440_a_man_and_a_boy_are_working_on_a_laptop.jpg",
    "img_5.jpg": "youssef instractore image of large number of pepole holding certaficat _1080x1440_a_group_of_people_holding_up_signs.jpg",
    "img_8.jpeg": "youssef instractornear hight qulity image of the class youssef is visable with wider angle than its twin_1080x1440_a_group_of_children_sitting_at_a_table_with_laptops.jpeg",
}

def main():
    print("=" * 70)
    print("PHASE 3: MANUAL MAPPING")
    print("=" * 70)
    print()
    
    matched = 0
    failed = 0
    
    for old_name, new_name in MANUAL_MAPPINGS.items():
        old_path = os.path.join(IMAGE_DIR, old_name)
        new_path = os.path.join(IMAGE_DIR, new_name)
        
        if not os.path.exists(old_path):
            print(f"✗ {old_name}: File not found")
            failed += 1
            continue
        
        if os.path.exists(new_path):
            print(f"⚠ {old_name}: Target already exists, skipping")
            failed += 1
            continue
        
        try:
            os.rename(old_path, new_path)
            print(f"✓ {old_name}")
            print(f"  → {new_name}")
            matched += 1
        except Exception as e:
            print(f"✗ {old_name}: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    print(f"PHASE 3 SUMMARY: {matched} files renamed, {failed} failed")
    print("=" * 70)

if __name__ == "__main__":
    main()
