from django.core.management.base import BaseCommand
from apps.master_budget.loan_portfolio import models as loan_models
from apps.master_budget.passives import models as passives_models
from utils.initial_data import (
    FINANCIAL_INVESTMENT,
    SAVINGS_LIABILITIES_CATEGORY,
    LIABILITIES_LOANS_CATEGORY
)


class Command(BaseCommand):
    help = "Command for INSERT INITIAL DATA for master budget"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):

        for item in FINANCIAL_INVESTMENT:
            obj, created = loan_models.FinancialInvestmentsCategory.objects.update_or_create( # NOQA
                identifier=item.pop('identifier'),
                defaults=item,
            )
            if created:
                print(
                    f'Financial Investment Category Created, identifier: {obj.identifier}'
                )
            else:
                print(
                    f'Financial Investment Category Updated, identifier: {obj.identifier}'
                )

        for item in SAVINGS_LIABILITIES_CATEGORY:
            obj, created = passives_models.SavingsLiabilitiesCategory.objects.update_or_create( # NOQA
                identifier=item.pop('identifier'),
                defaults=item,
            )
            if created:
                print(
                    f'Savings Liabilities Category Created, identifier: {obj.identifier}'
                )
            else:
                print(
                    f'Savings Liabilities Category Updated, identifier: {obj.identifier}'
                )

        for item in LIABILITIES_LOANS_CATEGORY:
            obj, created = passives_models.LiabilitiesLoansCategory.objects.update_or_create( # NOQA
                identifier=item.pop('identifier'),
                defaults=item,
            )
            if created:
                print(
                    f'Liabilities Loans Category Created, identifier: {obj.identifier}'
                )
            else:
                print(
                    f'Liabilities Loans Category Updated, identifier: {obj.identifier}'
                )

        self.stdout.write(self.style.SUCCESS("Command execution ended Successfully!!"))
