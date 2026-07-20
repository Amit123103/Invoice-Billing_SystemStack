from dataclasses import dataclass

@dataclass
class Customer:
    id: int
    name: str
    phone: str
    email: str
    gst_number: str
    address: str
