"""
config.py — Manajemen konfigurasi aplikasi.
Menyimpan dan memuat pengaturan dari file config.json.
"""

import json
import os

# Lokasi file konfigurasi di folder yang sama dengan script ini
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

# Nilai default jika config.json belum ada
DEFAULT_CONFIG = {
    "target_language": "id",          # Kode bahasa tujuan (id = Indonesia)
    "font_size": 16,                   # Ukuran font hasil terjemahan
    "bg_color": "#1e1e1e",            # Warna background pop-up hasil
    "text_color": "#ffffff",           # Warna teks hasil terjemahan
    "bg_opacity": 0.92,               # Transparansi background (0.0 - 1.0)
    "hotkey": "ctrl+alt+z",           # Shortcut keyboard
}

# Peta nama bahasa → kode bahasa untuk Google Translate
LANGUAGE_MAP = {
    "Indonesia": "id",
    "English": "en",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Thai": "th",
    "Vietnamese": "vi",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Russian": "ru",
}

# Kebalikan: kode bahasa → nama bahasa
CODE_TO_LANGUAGE = {v: k for k, v in LANGUAGE_MAP.items()}


def load_config() -> dict:
    """Memuat konfigurasi dari config.json. Jika tidak ada, kembalikan default."""
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Gabungkan dengan default agar key baru tidak hilang
        merged = DEFAULT_CONFIG.copy()
        merged.update(data)
        return merged
    except (json.JSONDecodeError, IOError):
        # Jika file rusak, kembalikan default
        return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> None:
    """Menyimpan konfigurasi ke config.json."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"[Config] Gagal menyimpan konfigurasi: {e}")


def get_language_name(code: str) -> str:
    """Mengubah kode bahasa menjadi nama yang bisa dibaca manusia."""
    return CODE_TO_LANGUAGE.get(code, "Indonesia")
