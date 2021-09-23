from django import forms
from apps.main.models import (
    Cuentascontables,
    Inversiones,
    Puestos
)
from utils.constants import STATUS


class CuentascontablesForm(forms.ModelForm):
    desccuentacontable = forms.CharField(
        label="Nombre Cuenta Contable",
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'max_length': '150'}
        )
    )
    habilitado = forms.ChoiceField(
        label='Estado',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        choices=STATUS
    )

    class Meta:
        model = Cuentascontables
        fields = (
            'desccuentacontable',
            'habilitado'
        )


class InversionesForm(forms.ModelForm):
    descinversion = forms.CharField(
        label="Nombre Inversión",
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'max_length': '150'}
        )
    )
    meses_depreciacion = forms.IntegerField(
        label="Meses de Depreciación",
        required=True,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'min': '1'}
        )
    )
    codcuentacontable = forms.ModelChoiceField(
        label='Cuenta Contable',
        queryset=Cuentascontables.objects.filter(codtipocuenta=2, habilitado=True),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='-- Seleccione Cuenta Contable --',
        required=True
    )

    Habilitado = forms.ChoiceField(
        label='Estado',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        choices=STATUS
    )

    class Meta:
        model = Inversiones
        fields = (
            'codcuentacontable',
            'descinversion',
            'meses_depreciacion',
            'Habilitado'
        )


class PuestosForm(forms.ModelForm):
    descpuesto = forms.CharField(
        label="Nombre Puesto",
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'max_length': '100'}
        )
    )

    sueldopermanente = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        required=True,
        label="Sueldo Permanente",
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    sueldotemporal = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        required=True,
        label="Sueldo Temporal",
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    puestoestado = forms.ChoiceField(
        label='Estado',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        choices=STATUS
    )

    class Meta:
        model = Puestos
        fields = (
            'descpuesto',
            'sueldopermanente',
            'sueldotemporal',
            'puestoestado',
        )
