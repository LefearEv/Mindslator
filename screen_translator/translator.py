"""
translator.py — Menerjemahkan teks menggunakan Google Translate via deep_translator.
"""

from deep_translator import GoogleTranslator


def translate_text(text: str, target_lang: str = "id", source_lang: str = "auto") -> str:
    """
    Menerjemahkan teks ke bahasa tujuan.

    Args:
        text:        Teks yang akan diterjemahkan
        target_lang: Kode bahasa tujuan (misal: 'id', 'ja', 'ko')
        source_lang: Kode bahasa sumber ('auto' = deteksi otomatis)

    Returns:
        Teks hasil terjemahan, atau pesan error jika gagal.
    """
    if not text or not text.strip():
        return ""

    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        result = translator.translate(text)
        return result if result else text

    except Exception as e:
        error_msg = str(e)

        # Berikan pesan error yang ramah pengguna
        if "connection" in error_msg.lower() or "network" in error_msg.lower():
            return "[Error] Tidak ada koneksi internet. Periksa jaringan Anda."
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            return "[Error] Batas penggunaan Google Translate tercapai. Coba lagi nanti."
        else:
            return f"[Error] Terjemahan gagal: {error_msg}"
