from typing import Dict, Any


class IndianGSTTaxCalculator:
    """Calculates CGST, SGST, IGST tax breakdown based on seller and customer state jurisdictions."""

    DEFAULT_TAX_RATE = 0.18  # 18% standard GST for electronics & hardware
    MERCHANT_HOME_STATE = "Karnataka"

    @classmethod
    def compute_gst(
        cls,
        taxable_amount: float,
        destination_state: str,
        tax_rate: float = DEFAULT_TAX_RATE
    ) -> Dict[str, Any]:
        total_tax = round(taxable_amount * tax_rate, 2)
        is_interstate = (destination_state.strip().lower() != cls.MERCHANT_HOME_STATE.lower())

        if is_interstate:
            # Interstate transaction -> IGST
            cgst = 0.0
            sgst = 0.0
            igst = total_tax
        else:
            # Intrastate transaction -> 50% CGST + 50% SGST
            cgst = round(total_tax / 2.0, 2)
            sgst = round(total_tax - cgst, 2)
            igst = 0.0

        return {
            'taxable_amount': taxable_amount,
            'tax_rate_percent': round(tax_rate * 100.0, 1),
            'total_tax': total_tax,
            'is_interstate': is_interstate,
            'cgst': cgst,
            'sgst': sgst,
            'igst': igst,
            'final_amount': round(taxable_amount + total_tax, 2)
        }
