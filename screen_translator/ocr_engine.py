"""
ocr_engine.py — Mengambil screenshot area tertentu dan membaca teksnya via OCR.
Menggunakan Pillow untuk screenshot dan pytesseract untuk OCR.
"""

import re
import pytesseract
from PIL import ImageGrab, Image


def capture_area(x1: int, y1: int, x2: int, y2: int) -> Image.Image:
    """
    Mengambil screenshot dari koordinat (x1, y1) ke (x2, y2).
    Mengembalikan objek PIL Image.
    """
    # Pastikan koordinat selalu dari kiri-atas ke kanan-bawah
    left   = min(x1, x2)
    top    = min(y1, y2)
    right  = max(x1, x2)
    bottom = max(y1, y2)

    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    return screenshot


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Pra-pemrosesan gambar agar OCR lebih akurat:
    - Konversi ke grayscale
    - Perbesar 2x agar teks lebih jelas dibaca Tesseract
    """
    # Konversi ke grayscale
    gray = image.convert("L")

    # Perbesar gambar 2x untuk akurasi OCR yang lebih baik
    width, height = gray.size
    enlarged = gray.resize((width * 2, height * 2), Image.LANCZOS)

    return enlarged


def extract_text(image: Image.Image, lang: str = "eng") -> str:
    """
    Membaca teks dari gambar menggunakan Tesseract OCR.

    Args:
        image: Objek PIL Image yang akan dibaca
        lang:  Kode bahasa Tesseract (default 'eng' untuk Inggris)

    Returns:
        Teks hasil OCR yang sudah dibersihkan menjadi satu paragraf.
    """
    processed = preprocess_image(image)

    # Konfigurasi Tesseract: mode halaman 6 = blok teks seragam
    custom_config = r"--oem 3 --psm 6"

    raw_text = pytesseract.image_to_string(
        processed,
        lang=lang,
        config=custom_config
    )

    return clean_text(raw_text)


def clean_text(text: str) -> str:
    """
    Membersihkan teks OCR:
    - Menghapus baris kosong berlebih
    - Menggabungkan baris yang terpotong menjadi satu paragraf
    - Menghapus karakter aneh hasil OCR yang salah baca
    """
    if not text:
        return ""

    # Pisahkan per baris dan hapus whitespace di tiap ujung
    lines = [line.strip() for line in text.splitlines()]

    # Hapus baris yang kosong atau hanya berisi simbol tidak berguna
    cleaned_lines = []
    for line in lines:
        # Lewati baris kosong
        if not line:
            continue
        # Lewati baris yang hanya berisi karakter non-alfanumerik
        if not re.search(r"[a-zA-Z0-9\u00C0-\u024F\u3040-\u9FFF]", line):
            continue
        cleaned_lines.append(line)

    # Gabungkan semua baris menjadi satu paragraf dengan spasi
    paragraph = " ".join(cleaned_lines)

    # Bersihkan spasi ganda
    paragraph = re.sub(r" {2,}", " ", paragraph)

    return paragraph.strip()
