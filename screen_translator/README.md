# Screen Translator

Aplikasi desktop untuk menerjemahkan teks di layar secara instan menggunakan
shortcut keyboard. Cocok untuk game, manga, atau aplikasi berbahasa asing.

---

## Cara Kerja

```
Ctrl+Alt+Z  →  Pilih Area  →  OCR  →  Google Translate  →  Pop-up Hasil
```

1. Tekan **Ctrl+Alt+Z** saat ada teks asing di layar
2. Drag mouse untuk memilih area yang ingin diterjemahkan
3. Hasil terjemahan muncul sebagai pop-up di dekat area tersebut

---

## Instalasi

### 1. Install Python
Download Python 3.10+ dari [python.org](https://python.org)

### 2. Install Tesseract OCR
Download installer dari:
https://github.com/UB-Mannheim/tesseract/wiki

> **Penting:** Saat instalasi, centang "Add to PATH" agar Python bisa menemukannya.
> Default install path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

### 3. Install library Python

```bash
pip install -r requirements.txt
```

### 4. Jalankan aplikasi

> **Penting:** Jalankan sebagai Administrator agar shortcut keyboard bisa bekerja.

```bash
# Klik kanan terminal → "Run as Administrator", lalu:
python main.py
```

---

## Penggunaan

1. Buka aplikasi → jendela pengaturan muncul
2. Atur **Bahasa Tujuan**, **Ukuran Font**, dan **Warna** sesuai selera
3. Klik **💾 Simpan** lalu **▶ Aktifkan**
4. Klik **📌 Ke Tray** agar aplikasi berjalan di background
5. Tekan **Ctrl+Alt+Z** kapan saja untuk menerjemahkan

---

## Struktur File

```
screen_translator/
├── main.py              # Entry point & orkestrator utama
├── config.py            # Manajemen config.json
├── ocr_engine.py        # Screenshot & pembacaan teks (OCR)
├── translator.py        # Terjemahan via Google Translate
├── overlay.py           # Overlay seleksi area layar
├── result_popup.py      # Pop-up hasil terjemahan
├── settings_window.py   # Jendela pengaturan (CustomTkinter)
├── tray.py              # Ikon system tray
├── requirements.txt     # Daftar library
└── config.json          # Dibuat otomatis saat pertama kali dijalankan
```

---

## Pengaturan (config.json)

| Key | Default | Keterangan |
|---|---|---|
| `target_language` | `"id"` | Kode bahasa tujuan |
| `font_size` | `16` | Ukuran font pop-up (px) |
| `bg_color` | `"#1e1e1e"` | Warna background pop-up |
| `text_color` | `"#ffffff"` | Warna teks pop-up |
| `hotkey` | `"ctrl+alt+z"` | Shortcut keyboard |

---

## Bahasa yang Didukung

| Nama | Kode |
|---|---|
| Indonesia | `id` |
| English | `en` |
| Japanese | `ja` |
| Korean | `ko` |
| Chinese (Simplified) | `zh-CN` |
| Thai | `th` |
| Vietnamese | `vi` |
| + 7 bahasa lainnya | — |

---

## Troubleshooting

**Shortcut tidak berfungsi**
→ Jalankan aplikasi sebagai Administrator

**OCR tidak akurat**
→ Pastikan Tesseract terinstall dan ada di PATH
→ Coba perbesar tampilan game sebelum capture

**Terjemahan gagal**
→ Periksa koneksi internet
→ Google Translate memiliki batas penggunaan gratis

**Pop-up tidak muncul**
→ Pastikan area yang dipilih cukup besar (minimal 10×10 pixel)
→ Pastikan ada teks di area tersebut

---

## Dependensi

| Library | Fungsi |
|---|---|
| `customtkinter` | UI modern dark mode |
| `keyboard` | Shortcut keyboard global |
| `Pillow` | Screenshot & manipulasi gambar |
| `pytesseract` | OCR (baca teks dari gambar) |
| `deep-translator` | Google Translate API |
| `pystray` | Ikon system tray |
