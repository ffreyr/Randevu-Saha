from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Halisaha


from .models import Reservation


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class HalisahaForm(forms.ModelForm):
    class Meta:
        model = Halisaha
        fields = ['name', 'address', 'phone', 'hourly_price', 'location_url']


class ReservationForm(forms.ModelForm):
    HOUR_CHOICES = [
        ('09:00 - 10:00', '09:00 - 10:00'),
        ('10:00 - 11:00', '10:00 - 11:00'),
        ('11:00 - 12:00', '11:00 - 12:00'),
        ('12:00 - 13:00', '12:00 - 13:00'),
        ('13:00 - 14:00', '13:00 - 14:00'),
        ('14:00 - 15:00', '14:00 - 15:00'),
        ('15:00 - 16:00', '15:00 - 16:00'),
        ('16:00 - 17:00', '16:00 - 17:00'),
        ('17:00 - 18:00', '17:00 - 18:00'),
        ('18:00 - 19:00', '18:00 - 19:00'),
        ('19:00 - 20:00', '19:00 - 20:00'),
        ('20:00 - 21:00', '20:00 - 21:00'),
        ('21:00 - 22:00', '21:00 - 22:00'),
        ('22:00 - 23:00', '22:00 - 23:00'),
    ]

    hour_range = forms.ChoiceField(
        choices=HOUR_CHOICES,
        widget=forms.Select(attrs={'class': 'hour-select'})
    )

    class Meta:
        model = Reservation
        fields = ['date', 'hour_range']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
