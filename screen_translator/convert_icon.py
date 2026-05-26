"""
convert_icon.py — Konversi file gambar (JPEG/PNG) ke format .ico untuk PyInstaller.
Dijalankan otomatis oleh build.bat sebelum proses build dimulai.
"""

import sys
import os
from PIL import Image


def convert_to_ico(input_path: str, output_path: str = "icon.ico") -> bool:
    """
    Konversi file gambar ke .ico dengan multiple size (16, 32, 48, 64, 128, 256px).
    Ukuran ganda membuat ikon terlihat tajam di semua resolusi Windows.

    Returns:
        True jika berhasil, False jika gagal.
    """
    try:
        img = Image.open(input_path)

        # Konversi ke RGBA agar transparan bisa ditangani
        if img.mode != "RGBA":
            img = img.convert("RGBA")

        # Buat versi persegi (crop tengah jika tidak persegi)
        w, h = img.size
        if w != h:
            side = min(w, h)
            left = (w - side) // 2
            top  = (h - side) // 2
            img  = img.crop((left, top, left + side, top + side))

        # Simpan sebagai .ico dengan berbagai ukuran
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(output_path, format="ICO", sizes=sizes)

        print(f"[Icon] Berhasil: {input_path} → {output_path}")
        return True

    except Exception as e:
        print(f"[Icon] Gagal konversi: {e}")
        return False


if __name__ == "__main__":
    # Cari file icon di direktori saat ini
    candidates = []
    for fname in os.listdir("."):
        if fname.lower() in ("icon.jpeg", "icon.jpg", "icon.png"):
            candidates.append(fname)
        elif fname.lower().endswith((".jpeg", ".jpg", ".png")) and "icon" in fname.lower():
            candidates.append(fname)

    if not candidates:
        print("[Icon] Tidak ada file icon ditemukan (icon.jpeg / icon.jpg / icon.png)")
        sys.exit(1)

    # Gunakan yang pertama ditemukan
    source = candidates[0]
    print(f"[Icon] Menggunakan: {source}")
    success = convert_to_ico(source, "icon.ico")
    sys.exit(0 if success else 1)
