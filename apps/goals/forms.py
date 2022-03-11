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

    def validate(self, data):
        super(GlobalGoalDetailForm, self).validate(data)
        pon = GlobalGoalDetail.objecst.filter(
            id_global_goal_period=data.id_global_goal_period,
            id_goal=data.id_goal,
            ponderation=data.ponderation
            )
        ponderation = pon.ponderation + data.ponderation
        print(ponderation)
        if ponderation > 100:
            raise forms.ValidationError('La ponderacion sobrepasa el limite')
        return data
