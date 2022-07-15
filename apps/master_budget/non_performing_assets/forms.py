from decimal import Decimal as dc
from django import forms

from apps.master_budget.models import MasterParameters
from utils.constants import STATUS_SCENARIO
from .models import NonPerformingAssetsScenario, OtherAssetsScenario, OtherAssets


class NonPerformingAssetsScenarioForm(forms.ModelForm):
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
        model = NonPerformingAssetsScenario
        fields = (
            'parameter_id',
            'is_active',
            'comment',
        )


class OthersAssetsScenarioForm(forms.ModelForm):
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
        model = OtherAssetsScenario
        fields = (
            'parameter_id',
            'is_active',
            'comment',
        )


class ScenarioCloneForm(forms.Form):
    parameter_id = forms.ModelChoiceField(
        label="Actualizar Parametro de Proyección",
        required=False,
        queryset=MasterParameters.objects.filter(is_active=True),
        empty_label="--- Seleccione Parametro de Proyección ---",
        widget=forms.Select(
            attrs={
                'class': 'form-select select2-style',
                'style': 'width:100%'
            }
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


class OtherAssetsDefineAmountMonthlyForm(forms.ModelForm):

    def clean(self):
        super(OtherAssetsDefineAmountMonthlyForm, self).clean()
        data = self.cleaned_data
        instance = self.instance

        data['amount_january'] = instance.previous_balance + data['increases_january']
        data['amount_february'] = data['amount_january'] + data['increases_february']
        data['amount_march'] = data['amount_february'] + data['increases_march']
        data['amount_april'] = data['amount_march'] + data['increases_april']
        data['amount_may'] = data['amount_april'] + data['increases_may']
        data['amount_june'] = data['amount_may'] + data['increases_june']
        data['amount_july'] = data['amount_june'] + data['increases_july']
        data['amount_august'] = data['amount_july'] + data['increases_august']
        data['amount_september'] = data['amount_august'] + data['increases_september']
        data['amount_october'] = data['amount_september'] + data['increases_october']
        data['amount_november'] = data['amount_october'] + data['increases_november']
        data['amount_december'] = data['amount_november'] + data['increases_december']
        if round(float(data['amount_december']), 2) > round(instance.new_balance, 2):
            raise forms.ValidationError("Monto a diciembre es mayor al nuevo monto anual esperado")
        return data

    class Meta:
        model = OtherAssets
        fields = (
            'increases_january', 'increases_february', 'increases_march',
            'increases_april', 'increases_may', 'increases_june',
            'increases_july', 'increases_august', 'increases_september',
            'increases_october', 'increases_november', 'increases_december'
        )
