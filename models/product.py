from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    category: str
    hsn_code: str
    cost_price: float
    selling_price: float
    gst_percentage: float
    stock_quantity: int
    supplier_id: int
