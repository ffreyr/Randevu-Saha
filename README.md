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
- Bootstrap 5  
- HTML, CSS, JavaScript  

---

## ⚙️ Kurulum

Aşağıdaki adımları izleyerek projeyi yerel ortamınızda çalıştırabilirsiniz:

### 1. Repozitoyu klonlayın:

```bash
git clone https://github.com/ffreyr/Randevu-Saha.git
cd Randevu-Saha

### 2. Sanal ortam oluşturun ve aktif edin:

python -m venv env
env\Scripts\activate

### 3. Gereksinimleri yükleyin:

pip install -r requirements.txt

### 4. Veritabanı işlemleri:

python manage.py makemigrations
python manage.py migrate

### 5. Süper kullanıcı oluşturun (admin paneli için):

python manage.py createsuperuser

### 6. Sunucuyu başlatın:

python manage.py runserver
