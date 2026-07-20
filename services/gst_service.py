"""
File: gst_service.py

Purpose:
Centralizes all Goods and Services Tax (GST) mathematical calculations.

Dependencies:
- None

"""

# This class isolates tax calculations.
# It exists because tax laws can be complex and change over time. By keeping the math here,
# we prevent having to update tax logic in 20 different places if the law changes.
# Its responsibility is taking an amount and rate, and returning the exact tax split.
class GSTService:
    """
    Service class executing tax mathematics.
    """
    
    # Purpose:
    # Calculates the total tax on an amount and splits it appropriately.
    # We use @staticmethod because this function doesn't require access to `self` (no internal class state).
    #
    # Parameters:
    # amount (float): The base price of the item.
    # gst_percentage (float): The tax bracket rate (e.g., 18.0).
    #
    # Returns:
    # dict: A dictionary containing the exact tax breakdown.
    @staticmethod
    def calculate_gst(amount, gst_percentage):
        """
        Calculates GST breakdown from a base amount and percentage.

        Args:
            amount (float): The base pre-tax amount.
            gst_percentage (float): The applicable tax rate percentage.

        Returns:
            dict: Breakdowns containing 'cgst', 'sgst', 'igst', and 'total'.
        """
        # Calculate the absolute total tax amount by standard percentage math
        tax = (amount * gst_percentage) / 100
        
        # In this basic implementation, we assume all sales are Intra-State.
        # Therefore, the total tax is split evenly 50/50 between Central GST and State GST.
        return {
            "cgst": tax / 2,
            "sgst": tax / 2,
            "igst": 0,
            "total": tax
        }
