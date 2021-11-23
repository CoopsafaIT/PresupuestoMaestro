from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.conf.urls import handler404, handler500, handler403

from apps.main.views import error_500, error_404, error_403

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls')),
    path('administration/', include('apps.administration.urls')),
    path('security/', include('apps.security.urls')),
    path('expenses-budgets/', include('apps.expenses_budgets.urls')),
    path('travel-budgets/', include('apps.travel_budgets.urls')),
    path('investment-budgets/', include('apps.investment_budgets.urls')),
    path('staff-budgets/', include('apps.staff_budgets.urls')),
    path('indirect-budgets/', include('apps.indirect_budgets.urls')),
    path('income-budgets/', include('apps.income_budgets.urls')),
    path('cost-budgets/', include('apps.cost_budgets.urls')),
    path('master-budget/', include('apps.master_budget.urls')),
    path(
        'master-budget/loan-portfolio/',
        include('apps.master_budget.loan_portfolio.urls')
    ),
    path(
        'master-budget/passives/',
        include('apps.master_budget.passives.urls')
    ),
    path(
        'master-budget/non-performing-assets/',
        include('apps.master_budget.non_performing_assets.urls')
    ),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)

handler403 = error_403  # NOQA
handler404 = error_404  # NOQA
handler500 = error_500  # NOQA
