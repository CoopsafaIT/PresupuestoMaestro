from django import forms

from apps.master_budget.models import MasterParameters
from apps.master_budget.patrimony.models import (
    EquityScenario, Equity, DistributionSurplusCategory,
    SurplusCategory
)

from utils.constants import STATUS_SCENARIO


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


class ScenarioCloneUpdateParameterForm(forms.Form):
    parameter_id = forms.ModelChoiceField(
            label="Parametro de Proyección",
            required=True,
            queryset=MasterParameters.objects.filter(is_active=True),
            empty_label="--- Seleccione Parametro de Proyección ---",
            widget=forms.Select(
                attrs={'class': 'form-select select2-style-clone-update', 'style': 'width:100%'}
            )
        )
    is_active = forms.ChoiceField(
        label="Estado",
        required=True,
        choices=STATUS_SCENARIO,
        widget=forms.Select(
            attrs={'class': 'form-select select2-style-clone-update', 'style': 'width:100%'}
        )
    )
    comment = forms.CharField(
        label="Comentario",
        required=True,
        widget=forms.Textarea(
            attrs={"rows": 3, "style": 'resize:none', 'class': 'form-control'}
        )
    )


class EquityScenarioForm(forms.ModelForm):
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
        model = EquityScenario
        fields = (
            'parameter_id',
            'is_active',
            'comment',
        )


class EquityDefineAmountMonthlyForm(forms.ModelForm):

    def clean(self):
        super(EquityDefineAmountMonthlyForm, self).clean()
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
        if round(float(data['amount_december']), 2) > round(float(instance.new_balance), 2):
            raise forms.ValidationError("Monto a diciembre es mayor al nuevo monto anual esperado")
        return data

    class Meta:
        model = Equity
        fields = (
            'increases_january', 'increases_february', 'increases_march',
            'increases_april', 'increases_may', 'increases_june',
            'increases_july', 'increases_august', 'increases_september',
            'increases_october', 'increases_november', 'increases_december'
        )


class DistributionSurplusCategoryForm(forms.ModelForm):
    id_surplus_category = forms.ModelChoiceField(
        label="Categoria",
        required=True,
        queryset=SurplusCategory.objects.all(),
        empty_label="--- Seleccione Categoria ---",
        widget=forms.Select(
            attrs={'class': 'form-select select2-style-clone-update', 'style': 'width:100%'}
        )
    )
    title = forms.CharField(
        label="Nombre",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    percentage = forms.FloatField(
        label='Porcentaje',
        required=True,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'min': '0', 'max': '1', 'step': 'any'}
        )
    )

    class Meta:
        model = DistributionSurplusCategory
        fields = ('id_surplus_category', 'title', 'percentage')
