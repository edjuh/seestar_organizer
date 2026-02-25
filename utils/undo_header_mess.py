    search_pattern = os.path.join(base_dir, '**/*.py')
    py_files = glob.glob(search_pattern, recursive=True)
    
    fixed_count = 0

    for filepath in py_files:
        if 'venv' in filepath or '.pyenv' in filepath or '__pycache__' in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Check if this file has my specific messy injection
        if any("[TODO: Define the single responsibility" in line for line in lines):
            # My injected header was exactly 7 lines long. We keep everything from line 8 onwards.
            clean_lines = lines[7:]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(clean_lines)
            
            rel_path = os.path.relpath(filepath, base_dir)
            print(f"🧹 Cleaned up: {rel_path}")
            fixed_count += 1

    print(f"\nDone! Reverted {fixed_count} files back to their original state.")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    revert_mess(project_root)
