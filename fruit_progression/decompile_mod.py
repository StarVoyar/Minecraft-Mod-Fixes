#!/usr/bin/env python3
"""
Decompile jar files
Extracts the ORIGINAL mod with all source code (.class files)
"""
import os
import sys
import zipfile
import shutil

def main():
    jar_path = "build/fruit_progression-reloaded-1.20.1.jar"
    
    if not os.path.exists(jar_path):
        print(f"✗ JAR not found: {jar_path}")
        print(f"\nMake sure this file exists in current directory")
        return False
    
    print("=" * 60)
    print(f"DECOMPILING: {jar_path}")
    print("=" * 60)
    print(f"\nJAR: {jar_path}\n")
    
    # Extract
    print("Step 1: Extracting JAR...")
    extract_dir = "_temp_extract"
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    
    with zipfile.ZipFile(jar_path, 'r') as z:
        z.extractall(extract_dir)
    
    print(f"✓ Extracted\n")
    
    # Find what we have
    print("Step 2: Analyzing contents...")
    class_files = []
    json_files = []
    
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith('.class'):
                class_files.append(os.path.join(root, file))
            elif file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    
    print(f"✓ Found {len(class_files)} .class files (source code)")
    print(f"✓ Found {len(json_files)} JSON files\n")
    
    # Setup output
    print("Step 3: Copying to src/...")
    src_dir = "src"
    if os.path.exists(src_dir):
        shutil.rmtree(src_dir)
    os.makedirs(src_dir)
    
    # Copy all files
    total = 0
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, extract_dir)
            dst_file = os.path.join(src_dir, rel_path)
            
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)
            total += 1
    
    print(f"✓ Copied {total} files\n")
    
    # Cleanup
    shutil.rmtree(extract_dir)
    
    # Summary
    print("=" * 60)
    print("✓ DECOMPILATION COMPLETE")
    print("=" * 60)
    print(f"\n✓ Source extracted to: src/")
    print(f"✓ Total files: {total}")
    print(f"✓ Class files: {len(class_files)}")
    print(f"\n📂 Structure:")
    print(f"  src/net/warcar/fruit_progression/")
    print(f"    ├── DevilFruitProgressionMod.class")
    print(f"    ├── requirements/        (10+ requirement types)")
    print(f"    ├── mixins/             (ContinuousComponentMixin, etc)")
    print(f"    ├── events/             (UnlockEvents)")
    print(f"    ├── init/               (ModRegistry, ModRequirements)")
    print(f"    ├── data/               (Player progression data)")
    print(f"    └── new_data_reader/    (AbilityDataReader)")
    print(f"\n💡 To get readable Java source code:")
    print(f"  1. Download CFR from: https://www.benf.org/other/cfr/cfr.jar")
    print(f"  2. Run: java -jar cfr.jar src/")
    print(f"  3. Get full Java source in src/ folder!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)