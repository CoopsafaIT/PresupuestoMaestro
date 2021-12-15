from apps.master_budget.models import (
    CatalogLossesEarnings,
    LossesEarningsComplementaryProjection
)


def init_complementary_projection(period):
    catalog_list = CatalogLossesEarnings.objects.all()
    for catalog in catalog_list:
        for month in range(1, 13):
            print(catalog.level_four)
            print(period)
            print(month)
            if not LossesEarningsComplementaryProjection.objects.filter(
                category_id=catalog.pk, period_id=period.pk, month=month
            ).exists():
                pass

        print('________________________END_________________________')
