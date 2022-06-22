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


class OtherAssetsDefinePercentageMonthlyForm(forms.ModelForm):
    def clean(self):
        super(OtherAssetsDefinePercentageMonthlyForm, self).clean()
        cleaned_data = self.cleaned_data

        instance = self.instance
        new_balance = float(instance.new_balance)
        values = [month for month in list(cleaned_data.values())]
        sum_values = sum(values)
        if round(sum_values, 2) > 1:
            raise forms.ValidationError("Suma Porcentaje Mensual supera al 100%")
        cleaned_data['amount_january'] = cleaned_data['percentage_january'] * new_balance
        cleaned_data['amount_february'] = cleaned_data['percentage_february'] * new_balance
        cleaned_data['amount_march'] = cleaned_data['percentage_march'] * new_balance
        cleaned_data['amount_april'] = cleaned_data['percentage_april'] * new_balance
        cleaned_data['amount_may'] = cleaned_data['percentage_may'] * new_balance
        cleaned_data['amount_june'] = cleaned_data['percentage_june'] * new_balance
        cleaned_data['amount_july'] = cleaned_data['percentage_july'] * new_balance
        cleaned_data['amount_august'] = cleaned_data['percentage_august'] * new_balance
        cleaned_data['amount_september'] = cleaned_data['percentage_september'] * new_balance
        cleaned_data['amount_october'] = cleaned_data['percentage_october'] * new_balance
        cleaned_data['amount_november'] = cleaned_data['percentage_november'] * new_balance
        cleaned_data['amount_december'] = cleaned_data['percentage_december'] * new_balance
        return cleaned_data

    class Meta:
        model = OtherAssets
        fields = (
            'percentage_january', 'percentage_february', 'percentage_march',
            'percentage_april', 'percentage_may', 'percentage_june',
            'percentage_july', 'percentage_august', 'percentage_september',
            'percentage_october', 'percentage_november', 'percentage_december'
        )


class OtherAssetsDefineAmountMonthlyForm(forms.ModelForm):

    def clean(self):
        super(OtherAssetsDefineAmountMonthlyForm, self).clean()
        cleaned_data = self.cleaned_data

        instance = self.instance
        values = [dc(month) for month in list(cleaned_data.values())]
        sum_values = sum(values)
        if round(sum_values, 2) > round(instance.new_balance, 2):
            raise forms.ValidationError("Suma Monto Mensual supera a Monto Anual")
        cleaned_data['percentage_january'] = cleaned_data['amount_january'] / instance.new_balance
        cleaned_data['percentage_february'] = cleaned_data['amount_february'] / instance.new_balance
        cleaned_data['percentage_march'] = cleaned_data['amount_march'] / instance.new_balance
        cleaned_data['percentage_april'] = cleaned_data['amount_april'] / instance.new_balance
        cleaned_data['percentage_may'] = cleaned_data['amount_may'] / instance.new_balance
        cleaned_data['percentage_june'] = cleaned_data['amount_june'] / instance.new_balance
        cleaned_data['percentage_july'] = cleaned_data['amount_july'] / instance.new_balance
        cleaned_data['percentage_august'] = cleaned_data['amount_august'] / instance.new_balance
        cleaned_data['percentage_september'] = cleaned_data['amount_september'] / instance.new_balance # NOQA
        cleaned_data['percentage_october'] = cleaned_data['amount_october'] / instance.new_balance
        cleaned_data['percentage_november'] = cleaned_data['amount_november'] / instance.new_balance
        cleaned_data['percentage_december'] = cleaned_data['amount_december'] / instance.new_balance
        return cleaned_data

    class Meta:
        model = OtherAssets
        fields = (
            'amount_january', 'amount_february', 'amount_march',
            'amount_april', 'amount_may', 'amount_june',
            'amount_july', 'amount_august', 'amount_september',
            'amount_october', 'amount_november', 'amount_december'
        )
