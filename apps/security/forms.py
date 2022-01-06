from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from utils.constants import STATUS
from apps.main.models import ResponsablesPorCentrosCostos, Centroscosto


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Usuario Active Directory",
        max_length=30,
        help_text='Usuario con el que se ingresa a la computadora.'
    )
    first_name = forms.CharField(
        label="Nombre",
        max_length=30,
        required=False,
        help_text='Opcional.'
    )
    last_name = forms.CharField(
        label="Apellidos",
        max_length=30,
        required=False,
        help_text='Opcional.'
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        max_length=254,
        help_text='Requerido. Ingrese el correo electrónico institucional.'
    )
    password1 = forms.CharField(
        widget=forms.TextInput(attrs={'type': "hidden", 'value': 'Password1234.'})
    )
    password2 = forms.CharField(
        widget=forms.TextInput(attrs={'type': "hidden", 'value': 'Password1234.'})
    )

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


class UseEditForm(forms.Form):
    username = forms.CharField(
        label="Usuario Active Directory",
        max_length=30,
        help_text='Usuario con el que se ingresa a la computadora.'
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        max_length=254,
        help_text='Requerido. Ingrese el correo electrónico institucional.'
    )
    first_name = forms.CharField(
        label="Nombre",
        max_length=30,
        required=False,
        help_text='Opcional.'
    )
    last_name = forms.CharField(
        label="Apellidos",
        max_length=30,
        required=False,
        help_text='Opcional.'
    )

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UseEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ResponsablesPorCentrosCostosForm(forms.ModelForm):
    CodCentroCosto = forms.ModelChoiceField(
        label='Centro de Costos',
        queryset=Centroscosto.objects.filter(habilitado=True),
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        ),
        empty_label='-- Seleccione Centros de Costos --',
        required=True
    )
    CodUser = forms.ModelChoiceField(
        label='Usuario',
        queryset=User.objects.filter(is_active=True),
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        ),
        empty_label='-- Seleccione Usuario --',
        required=True
    )
    Estado = forms.ChoiceField(
        label='Estado',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        ),
        choices=STATUS
    )
    class Meta:
        model = ResponsablesPorCentrosCostos
        fields = (
            'CodCentroCosto',
            'CodUser',
            'Estado',
        )


class AdminResetPassword(forms.Form):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    required_css_class = 'required'
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password (again)",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        """Save the new password."""
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

    @property
    def changed_data(self):
        data = super().changed_data
        for name in self.fields:
            if name not in data:
                return []
        return ['password']
