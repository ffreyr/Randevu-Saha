from django.db import models
from django.contrib.auth.models import AbstractUser

#Kullanıcı modeli (Standart kullanıcı/Saha sahibi)
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('standard', 'Standart Kullanıcı'),
        ('owner', 'Saha Sahibi'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='standard')
    favorite_sahalar = models.ManyToManyField('Halisaha', related_name='favori_kullanicilar', blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


#Halısaha Modeli
class Halisaha(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to= {'user_type': 'owner'})
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    hourly_price = models.DecimalField(max_digits=6, decimal_places=2)
    location_url = models.URLField(help_text="Google Maps bağlantısı")
    opening_hours = models.CharField(max_length=100, default="09:00 - 23:00", help_text="Örn: 09:00 - 23:00")

    def __str__(self):
        return self.name
    

#Rezervasyon Modeli
class Reservation(models.Model):
    saha = models.ForeignKey(Halisaha, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    hour_range = models.CharField(max_length=20)  # örneğin "13:00 - 14:00"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.saha.name} - {self.date} {self.hour_range} ({self.user.username})"

    