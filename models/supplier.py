from dataclasses import dataclass

@dataclass
class Supplier:
    id: int
    name: str
    phone: str
    email: str
    address: str
