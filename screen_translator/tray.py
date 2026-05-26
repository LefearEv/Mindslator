"""
tray.py — Ikon system tray agar aplikasi bisa berjalan di background.
Menggunakan library pystray.
"""

import threading
from typing import Callable, Optional

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False


def _create_default_icon() -> "Image.Image":
    """
    Buat ikon sederhana (lingkaran biru) jika file icon.ico tidak tersedia.
    """
    size = 64
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # Lingkaran biru sebagai ikon default
    draw.ellipse([4, 4, size - 4, size - 4], fill="#3B8ED0")
    # Huruf "T" di tengah
    draw.text((22, 18), "T", fill="white")
    return image


class SystemTray:
    """
    Mengelola ikon di system tray Windows.
    Klik kanan ikon → menu untuk membuka pengaturan atau keluar.
    """

    def __init__(
        self,
        on_show_settings: Callable,
        on_quit: Callable,
        icon_path: Optional[str] = None,
    ):
        """
        Args:
            on_show_settings: Callback untuk menampilkan jendela pengaturan
            on_quit:          Callback untuk keluar dari aplikasi
            icon_path:        Path ke file .ico (opsional)
        """
        self.on_show_settings = on_show_settings
        self.on_quit = on_quit
        self.icon_path = icon_path
        self.tray_icon = None
        self._thread = None

    def start(self) -> None:
        """Mulai ikon tray di thread terpisah agar tidak memblokir UI."""
        if not TRAY_AVAILABLE:
            print("[Tray] pystray tidak tersedia. Ikon tray dinonaktifkan.")
            return

        self._thread = threading.Thread(target=self._run_tray, daemon=True)
        self._thread.start()

    def _run_tray(self) -> None:
        """Jalankan ikon tray (berjalan di thread terpisah)."""
        import os, sys

        # Tentukan base path
        if getattr(sys, "frozen", False):
            base = sys._MEIPASS
        else:
            base = os.path.dirname(os.path.abspath(__file__))

        # Muat ikon — coba semua format yang tersedia
        icon_image = None
        for fname in ("icon.ico", "icon.png", "icon.jpeg", "icon.jpg"):
            fpath = os.path.join(base, fname)
            if os.path.exists(fpath):
                try:
                    icon_image = Image.open(fpath).convert("RGBA")
                    icon_image = icon_image.resize((64, 64))
                    break
                except Exception:
                    continue

        if icon_image is None:
            icon_image = _create_default_icon()

        # Buat menu klik kanan
        menu = pystray.Menu(
            pystray.MenuItem(
                "🖥️  Mindslator",
                None,
                enabled=False,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "⚙️  Buka Pengaturan",
                self._handle_show_settings,
                default=True,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "❌  Keluar",
                self._handle_quit,
            ),
        )

        self.tray_icon = pystray.Icon(
            name="mindslator",
            icon=icon_image,
            title="Mindslator",
            menu=menu,
        )

        self.tray_icon.run()

    def _handle_show_settings(self, icon, item) -> None:
        """Tampilkan jendela pengaturan dari tray."""
        if self.on_show_settings:
            self.on_show_settings()

    def _handle_quit(self, icon, item) -> None:
        """Keluar dari aplikasi."""
        if self.tray_icon:
            self.tray_icon.stop()
        if self.on_quit:
            self.on_quit()

    def stop(self) -> None:
        """Hentikan ikon tray."""
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except Exception:
                pass
