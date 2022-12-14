from django.urls import path
from apps.security.views import (
    login,
    logout,
    users,
    user,
    user_reset_pwd,
    roles,
    role,
    users_cost_centers,
    user_cost_centers
)

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('users/', users, name="users"),
    path('user/<int:id>/', user, name="user"),
    path('user/reset-password/<int:id>/', user_reset_pwd, name="user_reset_pwd"),
    path('roles/', roles, name="roles"),
    path('role/<int:id>/', role, name="role"),
    path('users-cost-centers/', users_cost_centers, name="users_cost_centers"),
    path('user-cost-centers/<int:id>/', user_cost_centers, name="user_cost_centers"),
]
