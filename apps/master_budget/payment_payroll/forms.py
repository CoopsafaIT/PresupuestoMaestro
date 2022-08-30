from django import forms
from apps.master_budget.models import MasterParameters
from utils.constants import STATUS_SCENARIO
from .models import PaymentPayrollScenario


class PaymentPayrollScenarioForm(forms.ModelForm):
    parameter_id = forms.ModelChoiceField(
        label="Parametro de Proyección",
        required=True,
        queryset=MasterParameters.objects.filter(is_active=True),
        empty_label="--- Seleccione Parametro de Proyección ---",
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
        model = PaymentPayrollScenario
        fields = (
            'parameter_id',
            'is_active',
            'comment',
        )


class CollateralPaymentScenarioForm(forms.ModelForm):
    holidays = forms.FloatField(
        required=True,
        label="Días de Vacaciones",
        widget=forms.NumberInput(
            attrs={'class': "form-control"}
        )
    )
    percentage_special_bonuses = forms.FloatField(
        required=True,
        label="Porcentaje de Bonificaciones Especiales (%)",
        widget=forms.NumberInput(
            attrs={'class': "form-control"}
        )
    )
    percentage_rap = forms.FloatField(
        required=True,
        label="Porcentaje RAP (%)",
        widget=forms.NumberInput(
            attrs={'class': "form-control"}
        )
    )
    percentage_labor_coverage = forms.FloatField(
        required=True,
        label="Porcentaje Cubertura Laboral (%)",
        widget=forms.NumberInput(
            attrs={'class': "form-control"}
        )
    )
    percentage_plan_sac = forms.FloatField(
        required=True,
        label="Porcentaje Plan SAC (%)",
        widget=forms.NumberInput(
            attrs={'class': "form-control"}
        )
    )
    percentage_social_security = forms.FloatField(
        required=True,
        label="Porcentaje Seguridad Social (%)",
        widget=forms.NumberInput(
            attrs={'class': "form-control"}
        )
    )

    class Meta:
        model = PaymentPayrollScenario
        fields = (
            'holidays',
            'percentage_special_bonuses',
            'percentage_rap',
            'percentage_labor_coverage',
            'percentage_plan_sac',
            'percentage_social_security'
        )
