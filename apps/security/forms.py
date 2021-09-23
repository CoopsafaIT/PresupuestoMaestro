from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
