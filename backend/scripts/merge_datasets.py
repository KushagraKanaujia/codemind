"""
Merge all code example datasets into a single file.
"""

import json
from pathlib import Path

def merge_datasets():
    """Merge all JSON files in data/categories into one master dataset."""

    # Paths
    categories_dir = Path(__file__).parent.parent.parent / "data" / "categories"
    output_file = Path(__file__).parent.parent.parent / "data" / "complete_dataset.json"

    print("🔍 Finding dataset files...")

    # Find all JSON files
    json_files = list(categories_dir.glob("*.json"))

    if not json_files:
        print("❌ No JSON files found in data/categories/")
        return

    print(f"📂 Found {len(json_files)} dataset files:")
    for f in json_files:
        print(f"   - {f.name}")

    # Merge all data
    all_examples = []
    stats = {}

    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
            all_examples.extend(data)
            stats[json_file.stem] = len(data)
            print(f"   ✓ {json_file.stem}: {len(data)} examples")

    # Save merged dataset
    with open(output_file, 'w') as f:
        json.dump(all_examples, f, indent=2)

    # Print summary
    print("\n" + "="*50)
    print("✅ MERGE COMPLETE!")
    print("="*50)
    print(f"\n📊 Statistics:")
    for category, count in sorted(stats.items()):
        print(f"   {category:30s}: {count:3d} examples")
    print(f"   {'─'*30}")
    print(f"   {'TOTAL':30s}: {len(all_examples):3d} examples")
    print(f"\n💾 Saved to: {output_file}")
    print(f"📦 File size: {output_file.stat().st_size / 1024:.1f} KB")

    return all_examples

if __name__ == '__main__':
    merge_datasets()
