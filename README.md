# 🗓️ Randevu Saha Yönetim Sistemi

Python ve Django kullanılarak geliştirilen bu proje, saha randevularını yönetmek ve takip etmek için web tabanlı bir sistemdir. Kullanıcılar randevu oluşturabilir, sahaları yönetebilir ve sistem üzerinden kolayca takvimlendirme yapabilir.

---

## 🚀 Özellikler

- 👥 Kullanıcı kayıt ve giriş sistemi
- 🏟️ Saha tanımlama ve güncelleme
- 📅 Randevu oluşturma, listeleme ve silme
- 🗂️ Admin paneli ile içerik yönetimi
- 📊 Temiz ve kullanıcı dostu arayüz
- 🔒 Yetkilendirme ve kullanıcıya özel randevular

---

## 🧰 Kullanılan Teknolojiler

- Python 3.x  
- Django 4.x  
- SQLite3 (varsayılan, PostgreSQL uyumlu)  
- Django Rest Framework 
- HTML, CSS 

---

## ⚙️ Kurulum

Aşağıdaki adımları izleyerek projeyi yerel ortamınızda çalıştırabilirsiniz:

### 1. Repozitoyu klonlayın:
```bash
git clone https://github.com/ffreyr/Randevu-Saha.git
cd Randevu-Saha
```
### 2. Sanal ortam oluşturun ve aktif edin:
```bash
python -m venv env
env\Scripts\activate
```
### 3. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```
### 4. Veritabanı işlemleri:
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5. Süper kullanıcı oluşturun (admin paneli için):
```bash
python manage.py createsuperuser
```
### 6. Sunucuyu başlatın:
```bash
python manage.py runserver 
```

---

## 📁 Proje Yapısı
```bash
randevu-saha/
├── .git/                  # Git versiyon kontrol klasörü
├── config/                # Django ayarlarını içeren config uygulaması
├── main/                  # Uygulamanın ana fonksiyonlarını barındıran klasör
│   ├── migrations/        # Veritabanı migration dosyaları
│   ├── static/            # Statik dosyalar (CSS, JS, resimler)
│   ├── templates/         # HTML şablonları
│   ├── admin.py           # Admin arayüz tanımları
│   ├── apps.py            # Uygulama konfigürasyonu
│   ├── forms.py           # Form tanımlamaları
│   ├── models.py          # Veritabanı modelleri
│   ├── serializers.py     # API serializer'ları
│   ├── tests.py           # Test dosyası
│   ├── urls.py            # Uygulama URL yönlendirmeleri
│   └── views.py           # View fonksiyonları
├── manage.py              # Django yönetim komut dosyası
├── requirements.txt       # Proje bağımlılıkları
└── README.md              # Proje tanıtım dosyası
```

## Hazırlayan: Arda Kaya
