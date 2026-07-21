import os
import ast

PROJECT_DIR = r"c:\Users\amita\myprojects\invoice_billing"

TEAM_MEMBER_INFO = {
    1: {
        "name": "Team Member 1",
        "module": "Authentication & Dashboard",
        "responsibilities": ["Login Authentication", "Dashboard", "User Management", "Settings"],
        "files": ["login_page.py", "dashboard.py", "settings_page.py", "auth.py"]
    },
    2: {
        "name": "Team Member 2",
        "module": "Inventory Management",
        "responsibilities": ["Product CRUD", "Inventory", "Categories", "Supplier Management"],
        "files": ["inventory_page.py", "product.py", "supplier.py", "inventory_service.py", "qr_service.py"]
    },
    3: {
        "name": "Team Member 3",
        "module": "Customer & Billing",
        "responsibilities": ["Customer CRUD", "Billing", "Cart", "GST", "Discount"],
        "files": ["customer_page.py", "customer.py", "payment.py", "billing_service.py", "gst_service.py"]
    },
    4: {
        "name": "Team Member 4",
        "module": "Invoice & Reports",
        "responsibilities": ["Invoice Generation", "Reports", "Analytics", "PDF Export"],
        "files": ["invoice_page.py", "reports_page.py", "invoice.py", "company.py", "report_service.py"]
    },
    5: {
        "name": "Team Member 5",
        "module": "Database & Integration",
        "responsibilities": ["SQLite", "CRUD Operations", "Database Integration", "Validation", "Testing"],
        "files": ["connection.py", "queries.py", "schema.py", "audit_service.py", "backup_service.py", "main.py", "__init__.py"]
    }
}

def get_member_info(filename):
    basename = os.path.basename(filename)
    for member_id, info in TEAM_MEMBER_INFO.items():
        if basename in info["files"]:
            return member_id, info
    # Default to Member 5
    return 5, TEAM_MEMBER_INFO[5]

def create_file_header(filename, info):
    basename = os.path.basename(filename)
    resp_lines = "\n".join([f"# - {r}" for r in info["responsibilities"]])
    return f"""############################################################
# Project : Smart ERP Billing System
#
# File    : {basename}
#
# Team Member :
# {info['name']}
#
# Module :
# {info['module']}
#
# Responsibilities :
{resp_lines}
#
# Developed By :
# {info['name']}
############################################################
"""

def create_module_header(info):
    resp_lines = "\n".join([f"# - {r}" for r in info["responsibilities"]])
    return f"""###########################################################
# {info['name']}
# Module: {info['module']}
# Completed:
{resp_lines}
###########################################################
"""

def create_function_header(info, func_name, purpose_lines):
    if not purpose_lines:
        purpose_lines = ["Handles logic for " + func_name.replace('_', ' ')]
    purpose_str = "\n".join([f"# {p}" for p in purpose_lines])
    return f"""# ---------------------------------------------
# {info['name']}
# Function: {func_name}
# Purpose:
{purpose_str}
# ---------------------------------------------
"""

def create_class_header(info, class_name, purpose_lines):
    if not purpose_lines:
        purpose_lines = ["Handles logic for " + class_name]
    purpose_str = "\n".join([f"# {p}" for p in purpose_lines])
    return f"""# ---------------------------------------------
# {info['name']}
# Class: {class_name}
# Purpose:
{purpose_str}
# ---------------------------------------------
"""

def get_purpose_from_docstring(docstring):
    if not docstring:
        return []
    lines = docstring.strip().split('\n')
    purpose_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.lower().startswith(('args:', 'returns:', 'yields:', 'raises:')):
            purpose_lines.append(line)
    return purpose_lines[:3] # keep it short

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    # Don't process script itself
    if os.path.basename(filepath) == 'add_comments.py':
        return

    try:
        tree = ast.parse(content)
    except Exception as e:
        print(f"Syntax error in {filepath}: {e}")
        return

    lines = content.split('\n')
    
    member_id, info = get_member_info(filepath)
    
    # We will collect insertions: dict of line_number (0-indexed) -> text_to_insert_BEFORE_that_line
    insertions = {}
    
    # Insert file header at the very beginning (line 0)
    insertions[0] = create_file_header(filepath, info)
    
    # Insert module header before the first import or class/function definition
    module_header_inserted = False
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.ClassDef, ast.FunctionDef)):
            line_idx = node.lineno - 1
            insertions[line_idx] = insertions.get(line_idx, "") + create_module_header(info)
            module_header_inserted = True
            break
    if not module_header_inserted and tree.body:
         line_idx = tree.body[0].lineno - 1
         insertions[line_idx] = insertions.get(line_idx, "") + create_module_header(info)

    # Walk the tree to find classes and functions
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            docstring = ast.get_docstring(node)
            purpose = get_purpose_from_docstring(docstring)
            header = create_class_header(info, node.name, purpose)
            
            # Find the decorator line if it exists
            start_line = node.lineno
            if node.decorator_list:
                start_line = node.decorator_list[0].lineno
                
            line_idx = start_line - 1
            # Maintain indentation
            indent = " " * node.col_offset
            indented_header = "\n".join([(indent + line if line else line) for line in header.split('\n')])
            insertions[line_idx] = insertions.get(line_idx, "") + indented_header

        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            # Skip very short or magic methods unless they are __init__
            if node.name.startswith('__') and node.name != '__init__':
                continue
                
            docstring = ast.get_docstring(node)
            purpose = get_purpose_from_docstring(docstring)
            header = create_function_header(info, node.name, purpose)
            
            start_line = node.lineno
            if node.decorator_list:
                start_line = node.decorator_list[0].lineno
                
            line_idx = start_line - 1
            indent = " " * node.col_offset
            indented_header = "\n".join([(indent + line if line else line) for line in header.split('\n')])
            insertions[line_idx] = insertions.get(line_idx, "") + indented_header

    # Reconstruct the file with insertions
    new_lines = []
    for i, line in enumerate(lines):
        if i in insertions:
            new_lines.append(insertions[i].rstrip())
        new_lines.append(line)
        
    # Write back the modified content
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f"Processed {filepath}")
    except Exception as e:
        print(f"Error writing {filepath}: {e}")

if __name__ == "__main__":
    for root, dirs, files in os.walk(PROJECT_DIR):
        if '.git' in root or '__pycache__' in root or '.pytest_cache' in root:
            continue
        for file in files:
            if file.endswith('.py') and file != 'add_comments.py':
                process_file(os.path.join(root, file))
