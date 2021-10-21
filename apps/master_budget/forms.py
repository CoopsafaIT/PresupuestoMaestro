from django import forms

from apps.main.models import Periodo
from .models import MasterParameters
from utils.constants import STATUS


class MasterParametersForm(forms.ModelForm):
    date_base = forms.DateField(
        label="Fecha Base",
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        )
    )
    is_active = forms.ChoiceField(
        label="Estado",
        required=True,
        choices=STATUS,
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        )
    )
    period_id = forms.ModelChoiceField(
        label="Periodo",
        queryset=Periodo.objects.filter(habilitado=True),
        empty_label="--- Seleccione Periodo ---",
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        )
    )
    comment = forms.CharField(
        label="Comentario",
        widget=forms.Textarea(
            attrs={"rows": 3, "style": 'resize:none', 'class': 'form-control'}
        )
    )

    class Meta:
        model = MasterParameters
        fields = (
            'date_base',
            'period_id',
            'is_active',
            'comment',
        )


class MasterParametersEditForm(forms.ModelForm):
    date_base = forms.DateField(
        label="Fecha Base",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    is_active = forms.ChoiceField(
        label="Estado",
        required=True,
        choices=STATUS,
        widget=forms.Select(
            attrs={'class': 'form-select', 'style': 'width:100%'}
        )
    )
    comment = forms.CharField(
        label="Comentario",
        widget=forms.Textarea(
            attrs={"rows": 3, "style": 'resize:none', 'class': 'form-control'}
        )
    )

    class Meta:
        model = MasterParameters
        fields = (
            'date_base',
            'is_active',
            'comment',
        )
