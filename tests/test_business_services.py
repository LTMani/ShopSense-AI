from app.services.business.coupon_engine import CouponEngine
from app.services.business.tax_calculator import IndianGSTTaxCalculator
from app.services.business.invoice_generator import CommercialInvoiceGenerator
from app.services.business.export_service import CatalogExportService
from app.models.product import Product


def test_coupon_engine_application():
    # Valid FIRST10 on first order
    res1 = CouponEngine.apply_coupon('FIRST10', cart_subtotal=10000.0, is_first_order=True)
    assert res1['valid'] is True
    assert res1['discount_amount'] == 1000.0
    assert res1['new_subtotal'] == 9000.0

    # Below minimum subtotal
    res2 = CouponEngine.apply_coupon('FIRST10', cart_subtotal=1500.0, is_first_order=True)
    assert res2['valid'] is False

    # Invalid code
    res3 = CouponEngine.apply_coupon('NONEXISTENT', cart_subtotal=5000.0)
    assert res3['valid'] is False


def test_gst_tax_calculator():
    # Intrastate (Karnataka -> Karnataka)
    intra = IndianGSTTaxCalculator.compute_gst(taxable_amount=10000.0, destination_state='Karnataka')
    assert intra['is_interstate'] is False
    assert intra['cgst'] == 900.0
    assert intra['sgst'] == 900.0
    assert intra['igst'] == 0.0
    assert intra['final_amount'] == 11800.0

    # Interstate (Karnataka -> Maharashtra)
    inter = IndianGSTTaxCalculator.compute_gst(taxable_amount=10000.0, destination_state='Maharashtra')
    assert inter['is_interstate'] is True
    assert inter['cgst'] == 0.0
    assert inter['sgst'] == 0.0
    assert inter['igst'] == 1800.0
    assert inter['final_amount'] == 11800.0


def test_catalog_export_service(app):
    with app.app_context():
        prods = Product.query.limit(5).all()
        csv_output = CatalogExportService.export_products_csv(prods)
        assert 'SKU,Title,Brand' in csv_output
        assert len(csv_output.splitlines()) >= 6
