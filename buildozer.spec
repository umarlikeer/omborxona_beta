[app]
title = omborxona
package.name = omborxona
package.domain = org.omborxona
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 0.1

# 1-MUHIM O'ZGARISH: Agar loyihangizda KivyMD ishlatilgan bo'lsa, uni requirements'ga qo'shish shart!
# Agar ishlatilmagan bo'lsa ham, material elementlar xato bermasligi uchun quyidagicha yozing:
requirements = python3, kivy==2.2.1, kivymd, plyer

# 2-MUHIM O'ZGARISH: NDK va API mosligini ta'minlash
# Android API versiyalarini to'g'rilang
android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1