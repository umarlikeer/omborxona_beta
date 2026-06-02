[app]
title = omborxona_beta
package.name = omborxona_beta
package.domain = org.omborxona_beta
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 0.1

# Python 3.10 va Kivy 2.3.0 barqaror kombinatsiyasi
requirements = python3.10, kivy==2.3.0, kivymd==1.2.0, plyer

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