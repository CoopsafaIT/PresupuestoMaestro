import ldap
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.models import (
    User,
    Group,
    Permission
)
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib import messages
from django.db.models import Q

from apps.main.models import ResponsablesPorCentrosCostos
from apps.security.forms import UserRegisterForm, UseEditForm
from ppto_safa.settings import (
    VALIDATE_AD,
    LOGIN_REDIRECT_URL,
    LOGOUT_REDIRECT_URL,
    LDAP_LOGIN,
    LDAP_URL
)
from apps.security.forms import ResponsablesPorCentrosCostosForm
from utils.pagination import pagination


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
        return redirect(LOGIN_REDIRECT_URL)

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


@login_required()
@permission_required(
    'security.puede_listar_usuarios', raise_exception=True
)
def users(request):
    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    form = UserRegisterForm()
    if request.method == 'POST':
        if not request.user.has_perm('security.puede_crear_usuarios'):
            raise PermissionDenied
        try:
            form = UserRegisterForm(request.POST)
            if not form.is_valid():
                raise ValidationError(f'{ form.errors.as_text() }')

            user = form.save()
            for group_id in request.POST.getlist('groups[]'):
                group = Group.objects.get(id=group_id)
                group.user_set.add(user)
            messages.success(
                request,
                f'Usuario: {user.username} creado con éxito'
            )
        except ValidationError as e:
            messages.warning(
                request,
                f'Error de validación: {e.__str__()}'
            )
        except Exception as e:
            messages.error(
                request,
                f'Error al crear usuario. {e.__str__()}'
            )
    users = User.objects.filter(
        Q(username__icontains=q) | Q(email__icontains=q) |
        Q(first_name__icontains=q) | Q(last_name__icontains=q)
    )
    groups = Group.objects.all()
    result = pagination(qs=users, page=page)
    ctx = {
        'users': result,
        'groups': groups,
        'form': form,
    }
    return render(request, 'users.html', ctx)


@login_required
def user(request, id):
    user = get_object_or_404(User, pk=id)
    data = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    form = UseEditForm(initial=data)
    if request.method == 'POST':
        if request.POST.get('method') == 'change-status':
            if not request.user.has_perm('security.puede_cambiar_estado_usuarios'):
                raise PermissionDenied
            user.is_active = not user.is_active
            user.save()
            status = 'Activado' if user.is_active else 'Inactivado'
            messages.success(
                request,
                f'Usuario: {user.username} {status} con éxito'
            )
            return redirect('users')

        if request.POST.get('method') == 'update':
            if not request.user.has_perm('security.puede_editar_usuarios'):
                raise PermissionDenied
            try:
                form = UseEditForm(request.POST)
                if not form.is_valid():
                    raise ValidationError(f'{ form.errors.as_text() }')

                if User.objects.filter(
                    username=form.cleaned_data.get('username')
                ).exclude(pk=user.pk).exists():
                    raise ValidationError(
                        f'Ya existe un usuario con este usuario de '
                        f'active directory: {form.cleaned_data.get("username")}'
                    )
                user.username = form.cleaned_data.get('username')
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                user.save()
                user.groups.clear()
                for group_id in request.POST.getlist('groups[]'):
                    group = Group.objects.get(id=group_id)
                    group.user_set.add(user)
                messages.success(
                    request,
                    f'Usuario: {user.username} editado con éxito'
                )
                return redirect('users')
            except ValidationError as e:
                messages.warning(
                    request,
                    f'Error de validación: {e.__str__()}'
                )
            except Exception as e:
                messages.error(
                    request,
                    f'Error no determinado: {e.__str__()}'
                )

    groups = Group.objects.all()
    ctx = {
        'form': form,
        'user': user,
        'groups': groups,
    }
    return render(request, 'user.html', ctx)


@login_required()
@permission_required(
    'security.puede_listar_grupos', raise_exception=True
)
def roles(request):
    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')

    if request.method == 'POST':
        if not request.user.has_perm('security.puede_crear_grupos'):
            raise PermissionDenied
        role = Group()
        role.name = request.POST.get('name')
        role.save()
        for permission_id in request.POST.getlist('permissions[]'):
            permission = Permission.objects.get(id=permission_id)
            role.permissions.add(permission)
        messages.success(
            request,
            'Rol creado con éxito'
        )
    roles = Group.objects.filter(Q(name__icontains=q)).order_by('name')
    result = pagination(qs=roles, page=page)
    permissions = Permission.objects.exclude(
        content_type__app_label__in=['admin', 'auth', 'contenttypes', 'sessions']
    ).order_by('content_type__app_label', 'name')
    ctx = {
        'roles': result,
        'permissions': permissions
    }
    return render(request, 'roles.html', ctx)


@login_required()
@permission_required(
    'security.puede_editar_grupos', raise_exception=True
)
def role(request, id):
    role = get_object_or_404(Group, pk=id)
    if request.method == 'POST':
        if request.POST.get('method') == 'delete':
            role.delete()
            messages.success(
                request,
                'Rol eliminado con éxito!'
            )
            return redirect('roles')

        if request.POST.get('method') == 'update':
            role.name = request.POST.get('name')
            role.save()
            role.permissions.clear()
            for permission_id in request.POST.getlist('permissions[]'):
                permission = Permission.objects.get(id=permission_id)
                role.permissions.add(permission)
            messages.success(
                request,
                'Rol editado con éxito!'
            )
            return redirect('roles')

    permissions = Permission.objects.exclude(
        content_type__app_label__in=['admin', 'auth', 'contenttypes', 'sessions']
    )
    ctx = {
        'role': role,
        'permissions': permissions
    }
    return render(request, 'role.html', ctx)


@login_required
def users_cost_centers(request):
    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    form = ResponsablesPorCentrosCostosForm()
    if request.method == 'POST':
        form = ResponsablesPorCentrosCostosForm(request.POST)
        if not form.is_valid():
            messages.warning(
                request,
                f'Formulario no válido, por favor revisar. {form.errors.as_text()}'
            )
        else:
            form.save()
            messages.success(
                request,
                'Asignación realizada con éxito'
            )
    qs = ResponsablesPorCentrosCostos.objects.filter(
        Q(CodCentroCosto__desccentrocosto__icontains=q) |
        Q(CodUser__username__icontains=q) |
        Q(CodUser__first_name__icontains=q)
    )

    result = pagination(qs=qs, page=page)
    ctx = {
        'qs': result,
        'form': form,
    }
    return render(request, 'users_cost_centers/list.html', ctx)


@login_required
def user_cost_centers(request, id):
    qs = get_object_or_404(ResponsablesPorCentrosCostos, pk=id)
    form = ResponsablesPorCentrosCostosForm(instance=qs)
    if request.method == 'POST':
        form = ResponsablesPorCentrosCostosForm(request.POST, instance=qs)
        if not form.is_valid():
            messages.warning(
                request,
                f'Formulario no válido, por favor revisar. {form.errors.as_text()}'
            )
        else:
            form.save()
            messages.success(
                request,
                'Asignación realizada con éxito'
            )
            return redirect('users_cost_centers')

    ctx = {
        'qs': qs,
        'form': form,
    }
    return render(request, 'users_cost_centers/edit.html', ctx)
