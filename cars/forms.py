from django.forms import ModelForm, widgets

from cars.models import Rezerwacja


class RezerwacjaForm(ModelForm):
    class Meta:
        model = Rezerwacja
        fields = ["date_start", "date_end"] #YYYY-MM-DD
        widgets = {
            "date_start": widgets.DateInput(attrs={'type': 'date'}),
            "date_end": widgets.DateInput(attrs={'type': 'date'}),
        }