from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import JsonResponse

from .models import Halisaha, Reservation, CustomUser
from .forms import HalisahaForm, ReservationForm, CustomUserCreationForm
from .serializers import (
    HaliSahaSerializer, 
    UserSerializer, 
    UserRegistrationSerializer,
    ReservationSerializer
)

from django.db.models import Q  # Arama için Q nesnesi

@login_required
def saha_listesi(request):
    if request.user.user_type == 'owner':
        sahalar = Halisaha.objects.filter(owner=request.user)
    else:
        sahalar = Halisaha.objects.all()

    # Sadece isim filtresi
    name = request.GET.get('name')
    if name:
        sahalar = sahalar.filter(name__icontains=name)

    return render(request, 'main/saha_listesi.html', {'sahalar': sahalar})


@login_required
def saha_ekle(request):
    if request.user.user_type != 'owner':
        return redirect('home')
    if request.method == 'POST':
        form = HalisahaForm(request.POST)
        if form.is_valid():
            saha = form.save(commit=False)
            saha.owner = request.user
            saha.save()
            return redirect('saha_listesi')
    else:
        form = HalisahaForm()

    return render(request, 'main/saha_form.html', {'form': form})

@login_required
def saha_duzenle(request, saha_id):
    saha = get_object_or_404(Halisaha, id=saha_id, owner=request.user)

    if request.method == 'POST':
        form = HalisahaForm(request.POST, instance=saha)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saha başarıyla güncellendi.')
            return redirect('saha_listesi')
        else:
            messages.error(request, 'Formda hatalar var, lütfen düzeltin.')
    else:
        form = HalisahaForm(instance=saha)

    # Render the form for both GET and invalid POST requests
    return render(request, 'main/saha_form.html', {'form': form, 'saha': saha})
    

@login_required
def saha_sil(request, saha_id):
    saha = get_object_or_404(Halisaha, id=saha_id, owner=request.user)
    saha.delete()
    return redirect('saha_listesi')


def home(request):
    return render(request, 'main/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = request.POST.get('user_type', 'standard')
            user.save()
            login(request, user)
            messages.success(request, 'Kayıt başarılı! Hoş geldiniz.')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş başarılı!')
            if user.user_type == 'owner':
                return redirect('saha_listesi')
            else:
                return redirect('rezervasyonlarim')
        else:
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
    
    return render(request, 'main/login.html')

@login_required
def saha_detay(request, saha_id):
    saha = get_object_or_404(Halisaha, id=saha_id)

    if request.user.user_type == 'owner':
        # Admin ise sahanın tüm rezervasyonlarını göster
        rezervasyonlar = Reservation.objects.filter(saha=saha).order_by('-date', '-hour_range')
        return render(request, 'main/saha_rezervasyonlari.html', {'saha': saha, 'rezervasyonlar': rezervasyonlar})
    else:
        # Normal kullanıcı ise rezervasyon yapma formunu göster
        form = ReservationForm()

        # Aşama 1: Form gönderildiğinde veriyi session'a kaydet
        if request.method == 'POST' and 'form_submit' in request.POST:
            form = ReservationForm(request.POST)
            if form.is_valid():
                # Seçilen tarih ve saatin müsait olup olmadığını kontrol et
                date = form.cleaned_data['date']
                hour_range = form.cleaned_data['hour_range']
                
                # Aynı tarih ve saatte başka rezervasyon var mı kontrol et
                existing_reservation = Reservation.objects.filter(
                    saha=saha,
                    date=date,
                    hour_range=hour_range
                ).exists()

                if existing_reservation:
                    messages.error(request, "Bu tarih ve saat için rezervasyon zaten yapılmış. Lütfen başka bir tarih veya saat seçin.")
                    return render(request, 'main/saha_detail.html', {
                        'saha': saha,
                        'form': form
                    })

                # Geçmiş tarih kontrolü
                if date < timezone.now().date():
                    messages.error(request, "Geçmiş bir tarih seçemezsiniz.")
                    return render(request, 'main/saha_detail.html', {
                        'saha': saha,
                        'form': form
                    })

                request.session['rez_saha_id'] = saha.id
                request.session['rez_date'] = form.cleaned_data['date'].isoformat()
                request.session['rez_hour_range'] = form.cleaned_data['hour_range']
                return render(request, 'main/saha_detail.html', {
                    'saha': saha,
                    'form': form,
                    'show_payment': True  # Ödeme ekranı gözüksün
                })

        # Aşama 2: Ödeme onaylandıysa rezervasyon kaydı oluştur
        elif request.method == 'POST' and 'odeme_onayla' in request.POST:
            # Session'dan bilgileri al ve rezervasyon oluştur
            saha_id_from_session = request.session.get('rez_saha_id')
            date_from_session = request.session.get('rez_date')
            hour_range_from_session = request.session.get('rez_hour_range')

            if saha_id_from_session and date_from_session and hour_range_from_session:
                 saha_from_session = get_object_or_404(Halisaha, id=saha_id_from_session)
                 Reservation.objects.create(
                    saha=saha_from_session,
                    user=request.user,
                    date=date_from_session,
                    hour_range=hour_range_from_session,
                 )
                 # Session'daki rezervasyon bilgilerini temizle
                 del request.session['rez_saha_id']
                 del request.session['rez_date']
                 del request.session['rez_hour_range']
                 messages.success(request, "Rezervasyon oluşturuldu. Güzel maçlar dileriz! ⚽")
                 return redirect('rezervasyonlarim') # Rezervasyonlarım sayfasına yönlendir
            else:
                 messages.error(request, "Rezervasyon bilgileri eksik.")
                 return redirect('saha_detay', saha_id=saha.id)

        # Aşama 3: İptal edildiyse hiçbir şey kaydetme
        elif request.method == 'POST' and 'iptal_et' in request.POST:
            # Session'daki rezervasyon bilgilerini temizle
            if 'rez_saha_id' in request.session:
                del request.session['rez_saha_id']
            if 'rez_date' in request.session:
                del request.session['rez_date']
            if 'rez_hour_range' in request.session:
                del request.session['rez_hour_range']
            messages.info(request, "Rezervasyon iptal edildi.")
            return redirect('saha_detay', saha_id=saha.id)

        return render(request, 'main/saha_detail.html', {'saha': saha, 'form': form})

@login_required
def rezervasyonlarim(request):
    rezervasyonlar = Reservation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/rezervasyonlarim.html', {'rezervasyonlar': rezervasyonlar})

@login_required
def rezervasyon_iptal(request, rezervasyon_id):
    rezervasyon = get_object_or_404(Reservation, id=rezervasyon_id, user=request.user)
    rezervasyon.delete()
    return redirect('rezervasyonlarim')

@login_required
def rezervasyonlar(request):
    if request.user.user_type != 'owner':
        messages.error(request, "Bu sayfayı görüntüleme izniniz yok.")
        return redirect('home')
    
    # Admin kullanıcının sahalarına ait tüm rezervasyonları çek
    sahalar = Halisaha.objects.filter(owner=request.user)
    rezervasyonlar = Reservation.objects.filter(saha__in=sahalar).order_by('-date', '-hour_range')

    return render(request, 'main/rezervasyonlar.html', {'rezervasyonlar': rezervasyonlar})

# API Views
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Geçersiz kullanıcı adı veya şifre'}, status=status.HTTP_401_UNAUTHORIZED)

class HalisahaViewSet(viewsets.ModelViewSet):
    queryset = Halisaha.objects.all()
    serializer_class = HaliSahaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.user_type == 'owner':
            return Halisaha.objects.filter(owner=self.request.user)
        return Halisaha.objects.all()

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@login_required
def profil(request):
    if request.method == 'POST':
        # Kullanıcı bilgilerini güncelle
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        
        # Şifre değişikliği kontrolü
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password and new_password and confirm_password:
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    messages.success(request, 'Şifreniz başarıyla güncellendi.')
                else:
                    messages.error(request, 'Yeni şifreler eşleşmiyor.')
            else:
                messages.error(request, 'Mevcut şifre yanlış.')
        
        try:
            user.save()
            messages.success(request, 'Profil bilgileriniz güncellendi.')
        except Exception as e:
            messages.error(request, 'Profil güncellenirken bir hata oluştu.')
        
        return redirect('profil')
    
    return render(request, 'main/profil.html')

@login_required
def favori_toggle(request, saha_id):
    saha = get_object_or_404(Halisaha, id=saha_id)
    user = request.user
    if saha in user.favorite_sahalar.all():
        user.favorite_sahalar.remove(saha)
        messages.info(request, f"'{saha.name}' favorilerinizden çıkarıldı.")
    else:
        user.favorite_sahalar.add(saha)
        messages.success(request, f"'{saha.name}' favorilerinize eklendi.")
    return redirect(request.META.get('HTTP_REFERER', 'saha_listesi'))

@login_required
def favori_sahalarim(request):
    favori_sahalar = request.user.favorite_sahalar.all()
    return render(request, 'main/favori_sahalarim.html', {'favori_sahalar': favori_sahalar})
