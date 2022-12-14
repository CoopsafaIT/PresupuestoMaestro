from django import forms

from .models import (
    LoanPortfolioScenario,
    LoanPortfolioCategory,
    FinancialInvestmentsScenario,
    FinancialInvestmentsCategory
)
from apps.master_budget.models import MasterParameters
from utils.constants import STATUS_SCENARIO


class LoanPortfolioScenarioForm(forms.ModelForm):
    parameter_id = forms.ModelChoiceField(
        label="Parametro de Proyección",
        required=True,
        queryset=MasterParameters.objects.filter(is_active=True),
        empty_label="--- Seleccione Parametro de Proyección ---",
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        )
    )
    category_id = forms.ModelChoiceField(
        label="Categoria",
        required=True,
        queryset=LoanPortfolioCategory.objects.filter(is_active=True),
        empty_label="--- Seleccione Categoria ---",
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        )
    )
    is_active = forms.ChoiceField(
        label="Estado",
        required=True,
        choices=STATUS_SCENARIO,
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        )
    )
    comment = forms.CharField(
        label="Comentario",
        required=True,
        widget=forms.Textarea(
            attrs={"rows": 3, "style": 'resize:none', 'class': 'form-control'}
        )
    )

    class Meta:
        model = LoanPortfolioScenario
        fields = (
            'parameter_id',
            'category_id',
            'is_active',
            'comment',
        )


class ScenarioCloneUpdateParameterForm(forms.Form):
    parameter_id = forms.ModelChoiceField(
        label="Parametro de Proyección",
        required=True,
        queryset=MasterParameters.objects.filter(is_active=True),
        empty_label="--- Seleccione Parametro de Proyección ---",
        widget=forms.Select(
            attrs={
                'class': 'form-select select2-style-clone-update',
                'style': 'width:100%'
            }
        )
    )
    is_active = forms.ChoiceField(
        label="Estado",
        required=True,
        choices=STATUS_SCENARIO,
        widget=forms.Select(
            attrs={
                'class': 'form-select select2-style-clone-update',
                'style': 'width:100%'
            }
        )
    )
    comment = forms.CharField(
        label="Comentario",
        required=True,
        widget=forms.Textarea(
            attrs={"rows": 3, "style": 'resize:none', 'class': 'form-control'}
        )
    )


class ScenarioCloneForm(forms.Form):
    is_active = forms.ChoiceField(
        label="Estado",
        required=True,
        choices=STATUS_SCENARIO,
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        )
    )
    comment = forms.CharField(
        label="Comentario",
        required=True,
        widget=forms.Textarea(
            attrs={"rows": 3, "style": 'resize:none', 'class': 'form-control'}
        )
    )


class FinancialInvestmentsScenarioForm(forms.ModelForm):
    parameter_id = forms.ModelChoiceField(
        label="Parametro de Proyección",
        required=True,
        queryset=MasterParameters.objects.filter(is_active=True),
        empty_label="--- Seleccione Parametro de Proyección ---",
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        )
    )
    category_id = forms.ModelChoiceField(
        label="Categoria",
        required=True,
        queryset=FinancialInvestmentsCategory.objects.filter(is_active=True),
        empty_label="--- Seleccione Categoria ---",
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        )
    )
    is_active = forms.ChoiceField(
        label="Estado",
        required=True,
        choices=STATUS_SCENARIO,
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        )
    )
    comment = forms.CharField(
        label="Comentario",
        required=True,
        widget=forms.Textarea(
            attrs={"rows": 3, "style": 'resize:none', 'class': 'form-control'}
        )
    )

    class Meta:
        model = FinancialInvestmentsScenario
        fields = (
            'parameter_id',
            'category_id',
            'is_active',
            'comment',
        )


class FinancialInvestmentsScenarioCloneForm(forms.Form):
    is_active = forms.ChoiceField(
        label="Estado",
        required=True,
        choices=STATUS_SCENARIO,
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        )
    )
    comment = forms.CharField(
        label="Comentario",
        required=True,
        widget=forms.Textarea(
            attrs={"rows": 3, "style": 'resize:none', 'class': 'form-control'}
        )
    )
