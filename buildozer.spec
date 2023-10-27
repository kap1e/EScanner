[app]
title = Escanner
package.name = kivymd_test

package.domain = com.heattheatr

source.dir = .


source.include_exts = py,png,jpg,jpeg,ttf

version = 0.0.1


requirements = python3,kivy==2.0.0,pyqt5,sip,pip

orientation = portrait

fullscreen = 1

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

android.api = 28

android.minapi = 21

android.ndk = 17c

android.skip_update = False

android.accept_sdk_license = True

android.arch = armeabi-v7a

[buildozer]
log_level = 2

warn_on_root = 0

build_dir = ./.buildozer

bin_dir = ./bin