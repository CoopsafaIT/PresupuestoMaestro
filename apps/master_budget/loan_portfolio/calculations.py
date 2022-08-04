from decimal import Decimal as dc
import numpy_financial as npf


class LoanPortfolioCalculations():

    @staticmethod
    def level_quota(
        amount_initial, amount_growth, rate, term
    ):
        rate = rate / 12 / 100
        pv = amount_initial + amount_growth
        return npf.pmt(rate, term, float(pv))

    @staticmethod
    def total_interest(
        amount_initial, amount_growth, rate
    ):
        pv = float(amount_initial + amount_growth) / 1
        return pv * (rate*30/36000)

    @staticmethod
    def new_amount(amount_initial, amount_growth, principal_payments):
        return float(amount_initial) + float(amount_growth) - float(principal_payments)

    @staticmethod
    def commission_amount(annual_growth_amount, percent_growth, commission_percentage):
        month_growth = annual_growth_amount * (percent_growth/100)
        percentage = commission_percentage / 100
        return month_growth * percentage

    @staticmethod
    def amount_arrears(new_amount, percentage_arrears):
        return dc(new_amount) * dc(percentage_arrears / 100)

    @staticmethod
    def default_interest(amount_arrears, rate):
        amount_arrears = float(amount_arrears)
        return (amount_arrears)*rate*30/36000

    @staticmethod
    def recovery_amount(recovery_percentage, total_interest, default_interest):
        percentage = dc(recovery_percentage / 100)
        return dc(total_interest - default_interest) * percentage

    @staticmethod
    def interest_due_amount(percantage_interest_due, recovery_amount):
        percentage = dc(percantage_interest_due / 100)
        return recovery_amount * percentage
