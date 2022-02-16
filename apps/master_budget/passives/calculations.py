from decimal import Decimal as dc
import numpy_financial as npf


class LiabilitiesLoansCalculations():
    @staticmethod
    def level_quota(
        amount_initial, amount_growth, rate, term
    ):
        rate = rate / 12 / 100
        pv = amount_initial + amount_growth
        return dc(npf.pmt(rate, term, float(pv)))

    @staticmethod
    def total_interest(
        amount_initial, amount_growth, rate
    ):
        pv = float(amount_initial + amount_growth) / 1
        return dc(pv * (rate*30/36000))


def calculate_interest_generated(amount_initial, new_amount, rate):
    total_amount = (amount_initial + new_amount) / 2
    rate_monthly = (rate/100) / 12
    return total_amount * dc(rate_monthly)
