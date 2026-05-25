# 📦 Omborxona Ilovasi

Offline rejimda ishlaydigan omborxona boshqaruv ilovasi.
Python + Kivy + KivyMD + SQLite

---

## 🗂 Loyiha tuzilishi

```
omborxona/
├── main.py                    ← Asosiy fayl (shu yerdan ishga tushiriladi)
├── database.py                ← SQLite ma'lumotlar bazasi
├── screens/
│   ├── sotish_screen.py       ← Sotish ekrani
│   ├── ombor_screen.py        ← Ombor ko'rinishi
│   ├── boshqaruv_screen.py    ← Tovar boshqaruvi
│   └── statistika_screen.py   ← Savdo statistikasi
├── requirements.txt
├── buildozer.spec             ← Android APK sozlamalari
└── .github/workflows/
    └── build.yml              ← Avtomatik APK yaratish
```

---

## 💻 VS Code da ishlatish (Windows)

### 1. Kutubxonalarni o'rnatish

```bash
pip install kivy==2.3.0 kivymd==1.1.1 pillow plyer
```

### 2. Ilovani ishga tushirish

```bash
python main.py
```

---

## 📱 Android APK yaratish (GitHub Actions orqali)

> Android Studio kerak emas! GitHub bulutida build qilinadi.

### 1. GitHub'da repository yarating
- github.com → New repository → "omborxona" deb nomlang

### 2. Kodni yuklang
```bash
git init
git add .
git commit -m "Omborxona ilovasi"
git branch -M main
git remote add origin https://github.com/SIZNING_USERNAME/omborxona.git
git push -u origin main
```

### 3. APK ni yuklab oling
- GitHub → Actions → "Build Android APK" → oxirgi ishga tushirish
- Pastdagi "Artifacts" bo'limida → `omborxona-debug-apk` → yuklab oling
- ZIP ichidan `.apk` faylini chiqaring
- Telefoningizga o'tkazing va o'rnating

---

## 📋 Ilovaning imkoniyatlari

| Tab | Nima qiladi |
|-----|-------------|
| 🛒 **Sotish** | Tovarlarni savatga qo'shib, ombordan kamaytiradi |
| 👁 **Ombor** | Qaysi tovardan qancha qolganini ko'rsatadi |
| 📦 **Boshqaruv** | Tovar yaratish, miqdorni tahrirlash |
| 📊 **Statistika** | Dumaloq grafik bilan savdo tahlili |

---

## ❓ Muammo bo'lsa

- `pip install kivy` xato bersa: `pip install kivy[base]` sinab ko'ring
- Android build xato bersa: GitHub Actions log'ini tekshiring
- Savollar bo'lsa — kodni o'qib, izoh qoldirishingiz mumkin
