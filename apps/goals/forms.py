from django import forms

from apps.main.models import Periodo
from .models import GlobalGoalPeriod, GlobalGoalDetail, Goal


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
    definition = forms.CharField(
        label="Definición",
        widget=forms.TextInput(
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


class GlobalGoalDetailForm(forms.ModelForm):
    class Meta:
        model = GlobalGoalDetail
        fields = '__all__'
        widgets = {
                'ponderation': forms.TextInput(attrs={'class': 'form-control'})
            }

    def clean(self):
        super(GlobalGoalDetailForm, self).clean()
        id_global_goal_period = self.cleaned_data.get('id_global_goal_period')
        ponderation = self.cleaned_data.get('ponderation')
        sum_ponderation_recorded = GlobalGoalDetail.objects.filter(
            id_global_goal_period=id_global_goal_period
        ).extra({
            'sum_ponderation': 'SUM(Ponderacion)'
        }).values('sum_ponderation')
        sum_ponderation_recorded = sum_ponderation_recorded[0].get('sum_ponderation')
        total = sum_ponderation_recorded + ponderation

        if total > 100:
            self._errors['ponderation'] = self.error_class([
                f'Poderación excede el 100% ({total})'])
        return self.cleaned_data
