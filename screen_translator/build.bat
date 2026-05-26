@echo off
title Mindslator — Build .exe

:: Pindah ke direktori tempat build.bat ini berada
cd /d "%~dp0"

echo ============================================
echo   Mindslator - Build Tool
echo   Direktori: %~dp0
echo ============================================
echo.

:: Cek apakah Python tersedia
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo Silakan install Python dari https://python.org
    echo Pastikan centang "Add Python to PATH" saat instalasi.
    pause
    exit /b 1
)

echo [OK] Python ditemukan:
python --version
echo.

:: Install PyInstaller dan Pillow dulu
echo [1/5] Menginstall PyInstaller dan Pillow...
pip install pyinstaller pillow --quiet
echo       Siap.
echo.

:: Install semua library dari requirements.txt
echo [2/5] Menginstall library dari requirements.txt...
pip install -r requirements.txt --quiet
echo       Semua library siap.
echo.

:: Konversi icon.jpeg / icon.jpg / icon.png ke icon.ico
echo [3/5] Menyiapkan ikon aplikasi...
set ICON_FLAG=

:: Cek apakah ada file icon gambar
if exist "icon.jpeg" (
    python convert_icon.py
    if exist "icon.ico" set ICON_FLAG=--icon="icon.ico"
) else if exist "icon.jpg" (
    python convert_icon.py
    if exist "icon.ico" set ICON_FLAG=--icon="icon.ico"
) else if exist "icon.png" (
    python convert_icon.py
    if exist "icon.ico" set ICON_FLAG=--icon="icon.ico"
) else if exist "icon.ico" (
    echo [Icon] Menggunakan icon.ico yang sudah ada.
    set ICON_FLAG=--icon="icon.ico"
) else (
    echo [Icon] Tidak ada file icon ditemukan, build tanpa ikon kustom.
)
echo.

:: Hapus hasil build lama
if exist "dist\Mindslator.exe" (
    echo [INFO] Menghapus build lama...
    del /f /q "dist\Mindslator.exe"
)

:: Jalankan PyInstaller
echo [4/5] Membangun file .exe (ini bisa memakan 2-5 menit)...
echo.

python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name="Mindslator" ^
    %ICON_FLAG% ^
    --hidden-import=customtkinter ^
    --hidden-import=PIL._tkinter_finder ^
    --hidden-import=pystray._win32 ^
    --collect-all customtkinter ^
    --collect-all deep_translator ^
    main.py

echo.

:: Cek hasil build
echo [5/5] Memeriksa hasil build...
if exist "dist\Mindslator.exe" (
    echo.
    echo ============================================
    echo   [BERHASIL] File .exe siap digunakan!
    echo   Lokasi: %~dp0dist\Mindslator.exe
    echo ============================================
    echo.
    echo Membuka folder dist...
    explorer "%~dp0dist"
) else (
    echo.
    echo [ERROR] Build GAGAL. Lihat pesan error di atas.
)

echo.
pause
