from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.conf.urls import handler404, handler500

from apps.main.views import error_500, error_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls')),
    path('administration/', include('apps.administration.urls')),
    path('security/', include('apps.security.urls')),
    path('expenses-budgets/', include('apps.expenses_budgets.urls')),
    path('travel-budgets/', include('apps.travel_budgets.urls')),
    path('investment-budgets/', include('apps.investment_budgets.urls')),
    path('staff-budgets/', include('apps.staff_budgets.urls')),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)

handler404 = error_404  # NOQA
handler500 = error_500  # NOQA
