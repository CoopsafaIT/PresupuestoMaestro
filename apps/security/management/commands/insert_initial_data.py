from django.core.management.base import BaseCommand
from apps.master_budget.loan_portfolio import models as loan_models

FINANCIAL_INVESTMENT = [
    {
        'name': 'Normales',
        'is_active': True,
        'identifier': '0'
    },
    {
        'name': 'FEC',
        'is_active': True,
        'identifier': '1'
    },
]


class Command(BaseCommand):
    help = "Command for INSERT INITIAL DATA for master budget"

    def add_arguments(self, parser):
        parser.add_argument(
            "-r",
            "--reset",
            type=str,
            help=(
                "Define if want reset (Y) or (N) just update and create "
                "if has new content types and permission. Default N"
            )
        )

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

        self.stdout.write(self.style.SUCCESS("Command execution ended Successfully!!"))
