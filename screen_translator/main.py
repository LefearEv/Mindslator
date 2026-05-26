"""
main.py — Entry point aplikasi Screen Translator.

Alur kerja:
1. Buka jendela pengaturan (CustomTkinter)
2. Saat diaktifkan, dengarkan shortcut Ctrl+Alt+Z di background thread
3. Saat shortcut ditekan → tampilkan overlay seleksi area
4. Setelah area dipilih → OCR → Translate → tampilkan pop-up hasil
"""

import sys
import threading
import time

import keyboard  # pip install keyboard

from config import load_config
from ocr_engine import capture_area, extract_text
from translator import translate_text
from overlay import SelectionOverlay
from result_popup import ResultPopup
from settings_window import SettingsWindow
from tray import SystemTray


class ScreenTranslatorApp:
    """Kelas utama yang mengorkestrasikan semua komponen aplikasi."""

    def __init__(self):
        self.config = load_config()
        self.is_listening = False
        self._hotkey_thread = None
        self._hotkey_registered = False

        # Inisialisasi jendela pengaturan
        self.settings_window = SettingsWindow(
            on_start_listener=self._start_listening,
            on_stop_listener=self._stop_listening,
        )

        # Inisialisasi system tray
        self.tray = SystemTray(
            on_show_settings=self._show_settings,
            on_quit=self._quit_app,
        )

    # ------------------------------------------------------------------ #
    #  Kontrol Listener                                                    #
    # ------------------------------------------------------------------ #

    def _start_listening(self) -> None:
        """Mulai mendengarkan shortcut keyboard di background thread."""
        self.config = load_config()  # Reload config terbaru
        self.is_listening = True

        hotkey = self.config.get("hotkey", "ctrl+alt+z")

        try:
            keyboard.add_hotkey(hotkey, self._on_hotkey_pressed)
            self._hotkey_registered = True
            print(f"[Main] Mendengarkan shortcut: {hotkey.upper()}")
        except Exception as e:
            print(f"[Main] Gagal mendaftarkan hotkey: {e}")

    def _stop_listening(self) -> None:
        """Hentikan listener shortcut keyboard."""
        self.is_listening = False

        if self._hotkey_registered:
            try:
                hotkey = self.config.get("hotkey", "ctrl+alt+z")
                keyboard.remove_hotkey(hotkey)
                self._hotkey_registered = False
                print("[Main] Listener dihentikan.")
            except Exception as e:
                print(f"[Main] Gagal menghapus hotkey: {e}")

    # ------------------------------------------------------------------ #
    #  Alur Utama: Shortcut → Overlay → OCR → Translate → Popup           #
    # ------------------------------------------------------------------ #

    def _on_hotkey_pressed(self) -> None:
        """
        Dipanggil saat shortcut ditekan.
        Jalankan di thread terpisah agar tidak memblokir listener keyboard.
        """
        if not self.is_listening:
            return

        thread = threading.Thread(target=self._run_translation_flow, daemon=True)
        thread.start()

    def _run_translation_flow(self) -> None:
        """
        Alur lengkap: tampilkan overlay → capture → OCR → translate → popup.
        Berjalan di thread terpisah.
        """
        # Reload config untuk mendapatkan pengaturan terbaru
        self.config = load_config()

        # Simpan koordinat seleksi dari overlay
        selection_result = {"coords": None}

        def on_area_selected(x1: int, y1: int, x2: int, y2: int) -> None:
            selection_result["coords"] = (x1, y1, x2, y2)

        # Tampilkan overlay di main thread (tkinter tidak thread-safe)
        self.settings_window.after(0, lambda: self._show_overlay(on_area_selected))

        # Tunggu sampai overlay selesai (max 30 detik)
        timeout = 30
        elapsed = 0
        while selection_result["coords"] is None and elapsed < timeout:
            time.sleep(0.1)
            elapsed += 0.1

        if selection_result["coords"] is None:
            return  # Pengguna membatalkan atau timeout

        x1, y1, x2, y2 = selection_result["coords"]

        # Ambil screenshot area yang dipilih
        print(f"[Main] Capture area: ({x1}, {y1}) → ({x2}, {y2})")
        image = capture_area(x1, y1, x2, y2)

        # Baca teks dengan OCR
        print("[Main] Membaca teks dengan OCR...")
        original_text = extract_text(image)

        if not original_text:
            print("[Main] Tidak ada teks yang terdeteksi di area tersebut.")
            self._show_no_text_popup(x2, y2)
            return

        print(f"[Main] Teks OCR: {original_text[:80]}...")

        # Terjemahkan teks
        target_lang = self.config.get("target_language", "id")
        print(f"[Main] Menerjemahkan ke '{target_lang}'...")
        translated = translate_text(original_text, target_lang=target_lang)

        print(f"[Main] Hasil: {translated[:80]}...")

        # Tampilkan pop-up hasil di main thread
        self.settings_window.after(
            0,
            lambda: self._show_result_popup(translated, original_text, x2, y2),
        )

    def _show_overlay(self, callback) -> None:
        """Tampilkan overlay seleksi area (harus dipanggil dari main thread)."""
        overlay = SelectionOverlay(on_selection=callback)
        overlay.show()

    def _show_result_popup(
        self,
        translated: str,
        original: str,
        anchor_x: int,
        anchor_y: int,
    ) -> None:
        """Tampilkan pop-up hasil terjemahan (harus dipanggil dari main thread)."""
        popup = ResultPopup(
            translated_text=translated,
            original_text=original,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
        )
        popup.show()

    def _show_no_text_popup(self, x: int, y: int) -> None:
        """Tampilkan pesan jika tidak ada teks terdeteksi."""
        self.settings_window.after(
            0,
            lambda: self._show_result_popup(
                "⚠️ Tidak ada teks yang terdeteksi di area tersebut.\n"
                "Coba pilih area yang lebih jelas atau perbesar tampilan game.",
                "",
                x,
                y,
            ),
        )

    # ------------------------------------------------------------------ #
    #  Kontrol Jendela & Tray                                              #
    # ------------------------------------------------------------------ #

    def _show_settings(self) -> None:
        """Tampilkan kembali jendela pengaturan dari tray."""
        self.settings_window.after(0, self.settings_window.deiconify)

    def _quit_app(self) -> None:
        """Keluar dari aplikasi sepenuhnya."""
        self._stop_listening()
        self.tray.stop()
        self.settings_window.after(0, self.settings_window.destroy)

    # ------------------------------------------------------------------ #
    #  Jalankan Aplikasi                                                   #
    # ------------------------------------------------------------------ #

    def run(self) -> None:
        """Mulai aplikasi."""
        print("[Main] Mindslator dimulai.")
        print("[Main] Atur preferensi di jendela pengaturan, lalu klik 'Aktifkan'.")

        # Mulai ikon tray di background
        self.tray.start()

        # Jalankan event loop UI (blocking)
        self.settings_window.mainloop()

        # Cleanup saat jendela ditutup
        self._stop_listening()
        self.tray.stop()
        print("[Main] Aplikasi ditutup.")


# ------------------------------------------------------------------ #
#  Entry Point                                                         #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    # Cek apakah dijalankan sebagai admin (diperlukan library 'keyboard')
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            print(
                "[Peringatan] Library 'keyboard' membutuhkan hak akses Administrator.\n"
                "Klik kanan pada file main.py atau terminal, lalu pilih 'Run as Administrator'."
            )
    except Exception:
        pass  # Bukan Windows atau tidak bisa cek

    app = ScreenTranslatorApp()
    app.run()
