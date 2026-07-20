class GSTService:
    @staticmethod
    def calculate_gst(amount, gst_percentage):
        tax = (amount * gst_percentage) / 100
        return {
            "cgst": tax / 2,
            "sgst": tax / 2,
            "igst": 0,
            "total": tax
        }
