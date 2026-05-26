"""
overlay.py — Overlay layar penuh semi-transparan untuk memilih area screenshot.
Pengguna klik dan drag untuk membuat kotak seleksi, lalu lepas untuk capture.
"""

import tkinter as tk
from typing import Callable, Optional


class SelectionOverlay:
    """
    Jendela overlay semi-transparan yang menutupi seluruh layar.
    Pengguna bisa drag mouse untuk memilih area yang ingin di-screenshot.
    """

    def __init__(self, on_selection: Callable[[int, int, int, int], None]):
        """
        Args:
            on_selection: Callback yang dipanggil dengan koordinat (x1, y1, x2, y2)
                          setelah pengguna selesai memilih area.
        """
        self.on_selection = on_selection
        self.start_x: Optional[int] = None
        self.start_y: Optional[int] = None
        self.rect_id: Optional[int] = None

        self._build_window()

    def _build_window(self) -> None:
        """Membuat jendela overlay semi-transparan."""
        self.root = tk.Tk()
        self.root.title("Mindslator — Pilih Area")

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_w}x{screen_h}+0+0")

        # Hilangkan border dan buat selalu di atas
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        # Gunakan -alpha untuk transparansi (BUKAN -transparentcolor)
        # Ini memastikan kursor tetap terlihat
        self.root.attributes("-alpha", 0.35)
        self.root.configure(bg="#1a1a2e")   # Biru gelap — bukan hitam

        # Canvas untuk menggambar kotak seleksi
        # cursor="crosshair" akan bekerja karena bg bukan warna transparan
        self.canvas = tk.Canvas(
            self.root,
            width=screen_w,
            height=screen_h,
            bg="#1a1a2e",
            cursor="crosshair",
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        # Teks petunjuk di tengah layar
        # Shadow dulu (offset +1) agar teks terbaca di semua background
        self.canvas.create_text(
            screen_w // 2 + 1,
            screen_h // 2 + 1,
            text="Klik dan drag untuk memilih area  •  ESC untuk batal",
            fill="#000000",
            font=("Segoe UI", 15, "bold"),
        )
        self.canvas.create_text(
            screen_w // 2,
            screen_h // 2,
            text="Klik dan drag untuk memilih area  •  ESC untuk batal",
            fill="#ffffff",
            font=("Segoe UI", 15, "bold"),
        )

        # Bind event mouse
        self.canvas.bind("<ButtonPress-1>",   self._on_mouse_press)
        self.canvas.bind("<B1-Motion>",       self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_release)
        self.root.bind("<Escape>",            self._on_cancel)

        # Paksa fokus ke overlay agar ESC langsung berfungsi
        self.root.focus_force()

    def _on_mouse_press(self, event: tk.Event) -> None:
        """Catat titik awal seleksi."""
        self.start_x = event.x_root
        self.start_y = event.y_root

        # Hapus kotak sebelumnya jika ada
        if self.rect_id:
            self.canvas.delete(self.rect_id)
            self.rect_id = None

    def _on_mouse_drag(self, event: tk.Event) -> None:
        """Gambar kotak seleksi saat mouse digerakkan."""
        if self.start_x is None:
            return

        # Hapus kotak lama
        if self.rect_id:
            self.canvas.delete(self.rect_id)

        # Area yang dipilih: background lebih terang (efek "jendela bersih")
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            event.x_root, event.y_root,
            outline="#00d4ff",   # Border biru cyan
            width=2,
            fill="#ffffff",      # Isi putih
            stipple="gray50",    # Semi-transparan
        )

    def _on_mouse_release(self, event: tk.Event) -> None:
        """Selesai memilih area — tutup overlay dan panggil callback."""
        if self.start_x is None:
            self._close()
            return

        x1, y1 = self.start_x, self.start_y
        x2, y2 = event.x_root, event.y_root

        self._close()

        # Pastikan area cukup besar (minimal 10x10 pixel)
        if abs(x2 - x1) > 10 and abs(y2 - y1) > 10:
            self.on_selection(x1, y1, x2, y2)

    def _on_cancel(self, event: tk.Event = None) -> None:
        """Batalkan seleksi saat ESC ditekan."""
        self._close()

    def _close(self) -> None:
        """Tutup jendela overlay."""
        try:
            self.root.destroy()
        except Exception:
            pass

    def show(self) -> None:
        """Tampilkan overlay dan mulai event loop."""
        self.root.mainloop()
