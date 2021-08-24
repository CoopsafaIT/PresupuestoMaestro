from django import forms


class InvestmentCUForm(forms.Form):
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
    account = forms.IntegerField(
        required=True,
        error_messages={'required': 'Por favor seleccione cuenta contable'},
    )
    investment = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor seleccione inversion'},
    )
    number = forms.IntegerField(
        required=True,
        error_messages={'required': 'Por favor ingrese cantidad'},
    )
    unit_amount = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor ingrese monto unitario'},
    )

    justification = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor ingrese justificacion'}
    )

    class Meta:
        fields = '__all__'
