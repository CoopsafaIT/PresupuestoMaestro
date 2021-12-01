from django.core.management.base import BaseCommand
from apps.main.models import Cuentascontables
from apps.master_budget.loan_portfolio import models as loan_models
from apps.master_budget.passives import models as passives_models
from apps.master_budget.non_performing_assets import models as non_performing_models
from utils.initial_data import (
    FINANCIAL_INVESTMENT,
    SAVINGS_LIABILITIES_CATEGORY,
    LIABILITIES_LOANS_CATEGORY,
    NON_PERFORMING_ASSETS_CATEGORY,
    NON_PERFORMING_ASSETS_CATEGORY_PER_ACCOUNTS,
    OTHERS_ASSETS_CATEGORY
)


def _insert_non_performing_assets_category_map_account():
    for item in NON_PERFORMING_ASSETS_CATEGORY_PER_ACCOUNTS:
        if not non_performing_models.NonPerformingAssetsCategoryMapAccounts.objects.filter(
            category_id__identifier=item.get('category_identifier'),
            account_id=item.get('account_id')
        ).exists():
            qs_category = non_performing_models.NonPerformingAssetsCategory.objects.filter(
                identifier=item.get('category_identifier')
            ).first()
            qs_account = Cuentascontables.objects.filter(pk=item.get('account_id')).first()
            non_performing_models.NonPerformingAssetsCategoryMapAccounts.objects.create(
                category_id=qs_category,
                account_id=qs_account
            )
            print(
                f'Non Perforning Assets Category Map Created, '
                f'identifier: {item.get("category_identifier")}'
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

        for item in NON_PERFORMING_ASSETS_CATEGORY:
            obj, created = non_performing_models.NonPerformingAssetsCategory.objects.update_or_create( # NOQA
                identifier=item.pop('identifier'),
                defaults=item,
            )
            if created:
                print(
                    f'Non Perforning Assets Category Created, identifier: {obj.identifier}'
                )
            else:
                print(
                    f'Non Perforning Assets Category Updated, identifier: {obj.identifier}'
                )
        
        for item in OTHERS_ASSETS_CATEGORY:
            obj, created = non_performing_models.OtherAssetsCategory.objects.update_or_create( # NOQA
                identifier=item.pop('identifier'),
                defaults=item,
            )
            if created:
                print(
                    f'Others Assets Category Created, identifier: {obj.identifier}'
                )
            else:
                print(
                    f'Others Assets Category Updated, identifier: {obj.identifier}'
                )
        
        _insert_non_performing_assets_category_map_account()

        self.stdout.write(self.style.SUCCESS("Command execution ended Successfully!!"))
