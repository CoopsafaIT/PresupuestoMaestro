from django import forms


class StaffCUForm(forms.Form):
    cost_center = forms.IntegerField(
        required=True,
        error_messages={'required': 'Por favor seleccione centro de costo'}
    )
    period = forms.IntegerField(
        required=True,
        min_value=1,
        error_messages={'required': 'Por favor seleccione periodo'}
    )
    month = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor seleccione mes'}
    )
    month_end = forms.CharField(required=False)
    job_position = forms.IntegerField(
        required=True,
        error_messages={'required': 'Por favor seleccione puesto de trabajo'},
    )
    type_position = forms.IntegerField(
        required=True,
        error_messages={'required': 'Por favor seleccione tipo de posicion'},
    )
    number = forms.IntegerField(
        required=True,
        error_messages={'required': 'Por favor ingrese cantidad'},
    )

    justification = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor ingrese justificacion'}
    )

    class Meta:
        fields = '__all__'

    def clean(self):
        cleaned_data = super(StaffCUForm, self).clean()
        type_position = cleaned_data['type_position']
        if type_position == 1:
            if cleaned_data.get('month_end') == '':
                raise forms.ValidationError(
                    "Para tipo de posicion temporal es necesario una fecha final"
                )
        return cleaned_data
