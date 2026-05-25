[app]
title = Omborxona
package.name = omborxona
package.domain = org.omborxona
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,db
version = 0.1

requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,plyer,sqlite3

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
