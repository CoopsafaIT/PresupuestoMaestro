from django import forms

from ppto_safa.constants import TRAVEL_TYPE, TRAVEL_CATEGORY, ZONES


class NacionalTravelBudget(forms.Form):
    category = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor seleccione categoria'},
    )
    filial = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor seleccione filial'}
    )
    cost_center = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor seleccione centro de costo'}
    )
    period = forms.IntegerField(
        required=True,
        min_value=1,
        error_messages={'required': 'Por favor seleccione periodo'}
    )
    travel_type = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor ingrese/seleccione tipo de viatico'}
    )
    number_trips = forms.IntegerField(
        required=True,
        error_messages={'required': 'Por favor ingrese cantidad de viaje'}
    )
    number_days = forms.FloatField(
        required=True,
        error_messages={'required': 'Por favor ingrese cantidad de dias'}
    )
    justification = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor ingrese justificacion'}
    )

    class Meta:
        fields = '__all__'

    def clean_travel_type(self):
        cleaned = self.cleaned_data['travel_type']
        travel_type = TRAVEL_TYPE.get(int(cleaned), None)
        if travel_type is None:
            raise forms.ValidationError("Tipo de viaje no reconocido")
        return cleaned

    def clean_category(self):
        cleaned = self.cleaned_data['category']
        category = TRAVEL_CATEGORY.get(cleaned, None)
        if category is None:
            raise forms.ValidationError("Categoria no reconocida")
        return cleaned


class InternacionalTravelBudget(forms.Form):
    category = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor seleccione categoria'},
    )
    zone = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor seleccione zone'}
    )
    cost_center = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor seleccione centro de costo'}
    )
    period = forms.IntegerField(
        required=True,
        min_value=1,
        error_messages={'required': 'Por favor seleccione periodo'}
    )
    travel_type = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor ingrese/seleccione tipo de viatico'}
    )
    number_trips = forms.IntegerField(
        required=True,
        error_messages={'required': 'Por favor ingrese cantidad de viaje'}
    )
    number_days = forms.FloatField(
        required=True,
        error_messages={'required': 'Por favor ingrese cantidad de dias'}
    )
    justification = forms.CharField(
        required=True,
        error_messages={'required': 'Por favor ingrese justificacion'}
    )

    class Meta:
        fields = '__all__'

    def clean_travel_type(self):
        cleaned = self.cleaned_data['travel_type']
        travel_type = TRAVEL_TYPE.get(int(cleaned), None)
        if travel_type is None:
            raise forms.ValidationError("Tipo de viaje no reconocido")
        return cleaned

    def clean_category(self):
        cleaned = self.cleaned_data['category']
        category = TRAVEL_CATEGORY.get(cleaned, None)
        if category is None:
            raise forms.ValidationError("Categoria no reconocida")
        return cleaned

    def clean_zone(self):
        cleaned = self.cleaned_data['zone']
        zone = ZONES.get(cleaned, None)
        if zone is None:
            raise forms.ValidationError("Zona no reconocida")
        return cleaned
