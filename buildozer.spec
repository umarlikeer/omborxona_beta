[app]
title = Omborxona
package.name = omborxona
package.domain = org.omborxona
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 0.1

# requirements ichida kivy-ios bo'lmasligi kerak!
requirements = python3, kivy==2.2.1, plyer

# Android API versiyalarini to'g'rilang
android.api = 33
android.minapi = 21
android.ndk = 25b
orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1