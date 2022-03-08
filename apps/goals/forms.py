from django import forms

from apps.main.models import Periodo
from .models import GlobalGoalPeriod, Goal


class GoalsForm(forms.ModelForm):
    period_id = forms.ModelChoiceField(
        label="Periodo",
        queryset=Periodo.objects.filter(habilitado=True),
        empty_label="--- Seleccione Periodo ---",
        widget=forms.Select(
            attrs={'class': 'form-select select2-style', 'style': 'width:100%'}
        )
    )
    description = forms.CharField(
        label="Descripcion",
        widget=forms.Textarea(
            attrs={"rows": 3, "style": 'resize:none', 'class': 'form-control'}
        )
    )

    class Meta:
        model = GlobalGoalPeriod
        fields = ('period_id', 'description')


class GoalsGlobalForm(forms.ModelForm):
    description = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(
            attrs={"rows": 3, "style": 'resize:none', 'class': 'form-control'}
        )
    )

    class Meta:
        model = Goal
        fields = (
            'description',
        )
