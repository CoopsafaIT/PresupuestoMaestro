
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

    def validate(self, ponderation):
        super(GlobalGoalDetailForm, self).validate(ponderation)
        pon = Goal.object.get(pk=id)
        pon_goal = pon.ponderation
        sum_ponderation = ponderation + pon_goal
        if sum_ponderation > 100:
            self._errors['sum_ponderation'] = self.error_class([
                'La ponderacion sobrepasa el limite'
                ])

        return self.sum_ponderation
