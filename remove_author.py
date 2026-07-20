import os

root_dir = 'c:/Users/amita/myprojects/invoice_billing'

for root, dirs, files in os.walk(root_dir):
    if '.git' in dirs:
        dirs.remove('.git') # don't visit .git directories
        
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            
            # Check if any lines were removed
            if len(lines) != len(new_lines):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"Removed author from {filepath}")
