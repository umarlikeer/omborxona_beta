[app]
title = omborxona
package.name = omborxona
package.domain = org.omborxona
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 0.1

# buildozer.spec ichidagi requirements qatorini topib, bunga almashtiring:
requirements = python3.11, kivy==2.3.0, kivymd==1.2.0, plyer

# TUZATILDI: minSdkVersion va ndk_api versiyalari 24 ga ko'tarildi
android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1