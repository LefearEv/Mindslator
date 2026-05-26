"""
result_popup.py — Jendela pop-up frameless untuk menampilkan hasil terjemahan.
Muncul di dekat area yang di-crop, bisa ditutup dengan tombol X.
"""

import tkinter as tk
from config import load_config


# Lebar pop-up dalam pixel — cukup lebar untuk teks panjang
POPUP_WIDTH = 520

# Tinggi maksimum area teks terjemahan (pixel) sebelum scrollbar muncul
MAX_TEXT_HEIGHT = 300


class ResultPopup:
    """
    Pop-up tanpa border (frameless) yang menampilkan teks terjemahan.
    Posisi muncul di dekat area seleksi, bisa di-drag untuk dipindahkan.
    """

    def __init__(
        self,
        translated_text: str,
        original_text: str,
        anchor_x: int,
        anchor_y: int,
    ):
        self.config = load_config()
        self.translated_text = translated_text
        self.original_text = original_text
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

        self._drag_start_x = 0
        self._drag_start_y = 0

        self._build_window()

    # ------------------------------------------------------------------ #
    #  Bangun Jendela                                                      #
    # ------------------------------------------------------------------ #

    def _build_window(self) -> None:
        self.root = tk.Tk()
        self.root.title("Mindslator")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        bg_color   = self.config.get("bg_color",   "#1e1e1e")
        text_color = self.config.get("text_color", "#ffffff")
        font_size  = int(self.config.get("font_size", 16))

        self.root.configure(bg=bg_color)

        # Frame utama dengan border tipis
        main_frame = tk.Frame(
            self.root,
            bg=bg_color,
            highlightbackground="#555555",
            highlightthickness=1,
        )
        main_frame.pack(fill="both", expand=True)

        # ---- Header ----
        self._build_header(main_frame, bg_color)

        # ---- Area teks terjemahan ----
        self._build_translation_area(main_frame, bg_color, text_color, font_size)

        # ---- Toggle teks asli ----
        self._build_original_toggle(main_frame, bg_color)

        # ---- Footer ----
        self._build_footer(main_frame)

        # Posisikan jendela
        self.root.update_idletasks()
        self._set_position()

    def _build_header(self, parent: tk.Frame, bg_color: str) -> None:
        """Header dengan judul dan tombol tutup."""
        header = tk.Frame(parent, bg="#2d2d2d", pady=5)
        header.pack(fill="x")

        title_label = tk.Label(
            header,
            text="  🌐 Mindslator",
            bg="#2d2d2d",
            fg="#aaaaaa",
            font=("Segoe UI", 9),
            anchor="w",
        )
        title_label.pack(side="left", fill="x", expand=True, padx=4)

        close_btn = tk.Button(
            header,
            text="✕",
            bg="#2d2d2d",
            fg="#aaaaaa",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=2,
            command=self._close,
            activebackground="#c0392b",
            activeforeground="#ffffff",
            bd=0,
        )
        close_btn.pack(side="right")

        # Drag via header
        for widget in (header, title_label):
            widget.bind("<ButtonPress-1>", self._on_drag_start)
            widget.bind("<B1-Motion>",     self._on_drag_motion)

    def _build_translation_area(
        self,
        parent: tk.Frame,
        bg_color: str,
        text_color: str,
        font_size: int,
    ) -> None:
        """Area utama: label + text widget dengan scrollbar."""
        outer = tk.Frame(parent, bg=bg_color, padx=14, pady=10)
        outer.pack(fill="both", expand=True)

        tk.Label(
            outer,
            text="Terjemahan:",
            bg=bg_color,
            fg="#888888",
            font=("Segoe UI", 9),
            anchor="w",
        ).pack(fill="x", pady=(0, 4))

        # Frame untuk Text + Scrollbar
        text_container = tk.Frame(outer, bg=bg_color)
        text_container.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            text_container,
            orient="vertical",
            bg="#3a3a3a",
            troughcolor="#2a2a2a",
            activebackground="#555555",
            relief="flat",
            bd=0,
            width=10,
        )

        self.translated_widget = tk.Text(
            text_container,
            bg=bg_color,
            fg=text_color,
            font=("Segoe UI", font_size),
            relief="flat",
            wrap="word",
            cursor="arrow",
            selectbackground="#3d5a80",
            selectforeground="#ffffff",
            padx=4,
            pady=6,
            width=1,                    # width diatur oleh geometry, bukan karakter
            yscrollcommand=scrollbar.set,
            spacing1=2,                 # Spasi antar paragraf atas
            spacing3=2,                 # Spasi antar paragraf bawah
        )

        scrollbar.config(command=self.translated_widget.yview)

        self.translated_widget.insert("1.0", self.translated_text)
        self.translated_widget.configure(state="disabled")

        # Hitung tinggi yang dibutuhkan, batasi MAX_TEXT_HEIGHT
        self.translated_widget.pack(side="left", fill="both", expand=True)
        self.root.update_idletasks()
        self._adjust_text_height(scrollbar)

    def _adjust_text_height(self, scrollbar: tk.Scrollbar) -> None:
        """
        Sesuaikan tinggi text widget:
        - Jika konten muat → tinggi pas konten, tanpa scrollbar
        - Jika konten panjang → tinggi MAX_TEXT_HEIGHT, tampilkan scrollbar
        """
        widget = self.translated_widget
        font_obj = tk.font.Font(font=widget.cget("font"))
        line_height = font_obj.metrics("linespace") + 4   # +4 untuk spacing

        # Hitung jumlah baris yang dibutuhkan (termasuk word-wrap)
        widget.update_idletasks()
        # Paksa lebar widget sesuai POPUP_WIDTH dikurangi padding
        widget.configure(width=1)
        self.root.geometry(f"{POPUP_WIDTH}x1")
        self.root.update_idletasks()

        # Baca jumlah baris setelah word-wrap diterapkan
        total_lines = int(widget.index("end-1c").split(".")[0])
        # Tambah estimasi baris dari wrap (kasar: panjang teks / 60 karakter per baris)
        wrap_lines = max(total_lines, len(self.translated_text) // 55 + 1)

        needed_height = wrap_lines * line_height + 16   # +16 untuk padding

        if needed_height <= MAX_TEXT_HEIGHT:
            # Konten muat — set tinggi pas, sembunyikan scrollbar
            widget.configure(height=wrap_lines + 1)
            scrollbar.pack_forget()
        else:
            # Konten panjang — batasi tinggi dan tampilkan scrollbar
            rows = MAX_TEXT_HEIGHT // line_height
            widget.configure(height=max(rows, 5))
            scrollbar.pack(side="right", fill="y", padx=(2, 0))

    def _build_original_toggle(self, parent: tk.Frame, bg_color: str) -> None:
        """Tombol toggle untuk menampilkan/menyembunyikan teks asli OCR."""
        self.original_frame = tk.Frame(parent, bg="#252525", padx=12, pady=0)

        self.toggle_btn = tk.Button(
            parent,
            text="▶  Lihat teks asli",
            bg=bg_color,
            fg="#666666",
            font=("Segoe UI", 8),
            relief="flat",
            cursor="hand2",
            anchor="w",
            padx=14,
            pady=4,
            bd=0,
            command=self._toggle_original,
            activebackground=bg_color,
            activeforeground="#aaaaaa",
        )
        self.toggle_btn.pack(fill="x")

        # Teks asli (tersembunyi secara default)
        original_widget = tk.Text(
            self.original_frame,
            bg="#252525",
            fg="#777777",
            font=("Segoe UI", 9),
            relief="flat",
            wrap="word",
            cursor="arrow",
            padx=4,
            pady=6,
            height=4,
        )
        original_widget.insert("1.0", self.original_text if self.original_text else "(tidak ada teks asli)")
        original_widget.configure(state="disabled")
        original_widget.pack(fill="both", expand=True, padx=4, pady=(0, 6))

    def _build_footer(self, parent: tk.Frame) -> None:
        """Footer dengan tombol salin."""
        footer = tk.Frame(parent, bg="#252525", pady=8)
        footer.pack(fill="x")

        copy_btn = tk.Button(
            footer,
            text="📋  Salin Terjemahan",
            bg="#3d5a80",
            fg="#ffffff",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=5,
            bd=0,
            command=self._copy_to_clipboard,
            activebackground="#2c4a6e",
            activeforeground="#ffffff",
        )
        copy_btn.pack(side="left", padx=10)

        self.copy_status = tk.Label(
            footer,
            text="",
            bg="#252525",
            fg="#27ae60",
            font=("Segoe UI", 9),
        )
        self.copy_status.pack(side="left")

    # ------------------------------------------------------------------ #
    #  Logika                                                              #
    # ------------------------------------------------------------------ #

    def _toggle_original(self) -> None:
        """Tampilkan/sembunyikan teks asli OCR."""
        if self.original_frame.winfo_ismapped():
            self.original_frame.pack_forget()
            self.toggle_btn.configure(text="▶  Lihat teks asli")
        else:
            self.original_frame.pack(fill="x", before=self.toggle_btn)
            self.toggle_btn.configure(text="▼  Sembunyikan teks asli")

    def _copy_to_clipboard(self) -> None:
        """Salin teks terjemahan ke clipboard."""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.translated_text)
        self.copy_status.configure(text="✓ Tersalin!")
        self.root.after(2000, lambda: self.copy_status.configure(text=""))

    def _set_position(self) -> None:
        """Posisikan pop-up di dekat area seleksi, pastikan tidak keluar layar."""
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        popup_h  = self.root.winfo_reqheight()

        x = self.anchor_x
        y = self.anchor_y + 10

        # Koreksi batas kanan
        if x + POPUP_WIDTH > screen_w - 10:
            x = screen_w - POPUP_WIDTH - 10

        # Koreksi batas bawah
        if y + popup_h > screen_h - 40:
            y = self.anchor_y - popup_h - 10

        x = max(10, x)
        y = max(10, y)

        self.root.geometry(f"{POPUP_WIDTH}x{popup_h}+{x}+{y}")

    def _on_drag_start(self, event: tk.Event) -> None:
        self._drag_start_x = event.x_root - self.root.winfo_x()
        self._drag_start_y = event.y_root - self.root.winfo_y()

    def _on_drag_motion(self, event: tk.Event) -> None:
        x = event.x_root - self._drag_start_x
        y = event.y_root - self._drag_start_y
        self.root.geometry(f"+{x}+{y}")

    def _close(self) -> None:
        try:
            self.root.destroy()
        except Exception:
            pass

    def show(self) -> None:
        self.root.mainloop()
