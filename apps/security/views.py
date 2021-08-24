import ldap
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib import messages
from django.contrib.auth.models import User

from ppto_safa.settings import (
    VALIDATE_AD,
    LOGIN_REDIRECT_URL,
    LOGOUT_REDIRECT_URL,
    LDAP_LOGIN,
    LDAP_URL
)


def login(request):
    def _validate_active_directory(username, password):
        conn = ldap.initialize(LDAP_URL)
        conn.protocol_version = 3
        conn.set_option(ldap.OPT_REFERRALS, 0)
        try:
            conn.simple_bind_s(f'{LDAP_LOGIN}\\{username}', password)
        except ldap.INVALID_CREDENTIALS:
            return {'status': False, 'message': "Invalid credentials"}
        except ldap.SERVER_DOWN:
            return {'status': False, 'message': "Server down"}
        except ldap.LDAPError as e:
            if type(e.message) == dict and e.message.get('desc', None):
                message = e.message.get('desc', None)
                return {'status': False, 'message': f'Other LDAP error: {message}'}
            else:
                return {'status': False, 'message': f'Other LDAP error: {e}'}
        finally:
            conn.unbind_s()
        return {'status': True, 'message': 'Ok'}

    def _authenticate(username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return True
        return False

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        try:
            first_name = request.POST.get("first_name", "")
            request.session['first_name'] = first_name
            password = request.POST.get("password", "")
            user_query = User.objects.get(first_name=first_name)
            username = user_query.username
            if VALIDATE_AD:
                ad_result = _validate_active_directory(username, password)
                if ad_result.get('status') is not True:
                    messages.warning(
                        request,
                        f"Active Directory message: { ad_result.get('message') }"
                    )
                    return render(request, "login.html", {})
                user_query.set_password(password)
                user_query.save()

            if _authenticate(username, password) is not True:
                messages.warning(request, "Credenciales invalidas!")
                return render(request, "login.html", {})

            return redirect(request.GET.get('next', LOGIN_REDIRECT_URL))
        except User.DoesNotExist:
            messages.warning(request, "Usuario no existe!")
        except Exception as e:
            messages.warning(request, f"Error inesperado, intente de nuevo! {e}")
    return render(request, "login.html", {})


def logout(request):
    auth_logout(request)
    return redirect(LOGOUT_REDIRECT_URL)
