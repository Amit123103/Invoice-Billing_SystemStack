import os
models_dir = 'c:/Users/amita/myprojects/invoice_billing/models'
os.makedirs(models_dir, exist_ok=True)
models = {
    "company.py": "from dataclasses import dataclass\n\n@dataclass\nclass Company:\n    id: int\n    name: str\n    gst_number: str\n    address: str\n    phone: str\n    email: str\n    logo_path: str\n",
    "customer.py": "from dataclasses import dataclass\n\n@dataclass\nclass Customer:\n    id: int\n    name: str\n    phone: str\n    email: str\n    gst_number: str\n    address: str\n",
    "product.py": "from dataclasses import dataclass\n\n@dataclass\nclass Product:\n    id: int\n    name: str\n    category: str\n    hsn_code: str\n    cost_price: float\n    selling_price: float\n    gst_percentage: float\n    stock_quantity: int\n    supplier_id: int\n",
    "supplier.py": "from dataclasses import dataclass\n\n@dataclass\nclass Supplier:\n    id: int\n    name: str\n    phone: str\n    email: str\n    address: str\n",
    "invoice.py": "from dataclasses import dataclass, field\nfrom typing import List\n\n@dataclass\nclass InvoiceItem:\n    product_id: int\n    quantity: int\n    price: float\n    discount: float\n    gst_percentage: float\n    total: float\n\n@dataclass\nclass Invoice:\n    id: int\n    invoice_number: str\n    customer_id: int\n    company_id: int\n    subtotal: float\n    discount: float\n    cgst: float\n    sgst: float\n    igst: float\n    total_tax: float\n    total_amount: float\n    payment_method: str\n    status: str\n    amount_paid: float\n    notes: str\n    created_by: int\n    items: List[InvoiceItem] = field(default_factory=list)\n",
    "payment.py": "from dataclasses import dataclass\n\n@dataclass\nclass Payment:\n    invoice_id: int\n    amount: float\n    method: str\n    date: str\n",
    "__init__.py": ""
}
for name, content in models.items():
    with open(os.path.join(models_dir, name), 'w') as f:
        f.write(content)







