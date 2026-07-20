import pytest
import os
from services.report_service import ReportService

def test_generate_invoice_pdf():
    """
    Test generating a PDF invoice file.
    """
    service = ReportService()
    
    invoice_data = {
        'invoice_number': "TEST-INV-123",
        'total_amount': 500.0
    }
    
    # We pass None for items and qr_path just to test basic file generation
    pdf_path = service.generate_invoice_pdf(invoice_data, [], None)
    
    # Check that the file was created
    assert os.path.exists(pdf_path)
    assert pdf_path.endswith("TEST-INV-123.pdf")
    
    # Clean up the test file
    try:
        os.remove(pdf_path)
    except:
        pass
