from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    # Kullanıcı İşlemleri
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profil/', views.profil, name='profil'),
    
    # Halı Saha İşlemleri
    path('sahalar/', views.saha_listesi, name='saha_listesi'),
    path('saha/ekle/', views.saha_ekle, name='saha_ekle'),
    path('saha/<int:saha_id>/duzenle/', views.saha_duzenle, name='saha_duzenle'),
    path('saha/<int:saha_id>/sil/', views.saha_sil, name='saha_sil'),
    path('saha/<int:saha_id>/', views.saha_detay, name='saha_detay'),
    
    # Rezervasyon İşlemleri
    path('rezervasyonlar/', views.rezervasyonlar, name='rezervasyonlar'),
    path('rezervasyonlarim/', views.rezervasyonlarim, name='rezervasyonlarim'),
    path('rezervasyon/<int:rezervasyon_id>/iptal/', views.rezervasyon_iptal, name='rezervasyon_iptal'),
    path('favori/<int:saha_id>/', views.favori_toggle, name='favori_toggle'),
    path('favori-sahalarim/', views.favori_sahalarim, name='favori_sahalarim'),
]