from dataclasses import dataclass

@dataclass
class Company:
    id: int
    name: str
    gst_number: str
    address: str
    phone: str
    email: str
    logo_path: str
