from dataclasses import dataclass

@dataclass
class Payment:
    invoice_id: int
    amount: float
    method: str
    date: str
