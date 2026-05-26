"""
settings_window.py — Jendela pengaturan utama dengan CustomTkinter.
Pengguna bisa mengatur bahasa, ukuran font, warna, dan hotkey.
"""

import os
import sys
import customtkinter as ctk
from tkinter import colorchooser
from config import load_config, save_config, LANGUAGE_MAP, get_language_name


# Tema default: dark mode ala Windows 11
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SettingsWindow(ctk.CTk):
    """Jendela pengaturan utama aplikasi Mindslator."""

    def __init__(self, on_start_listener=None, on_stop_listener=None):
        super().__init__()

        self.on_start_listener = on_start_listener
        self.on_stop_listener  = on_stop_listener
        self.config_data = load_config()
        self.is_running = False

        self._setup_window()
        self._build_ui()

    # ------------------------------------------------------------------ #
    #  Setup Jendela                                                       #
    # ------------------------------------------------------------------ #

    def _setup_window(self) -> None:
        """Konfigurasi dasar jendela."""
        self.title("Mindslator — Pengaturan")
        self.geometry("480x620")
        self.resizable(False, False)

        # Set ikon jendela
        self._set_window_icon()

        # Tombol X → minimize ke tray, bukan tutup
        self.protocol("WM_DELETE_WINDOW", self._minimize_to_tray)

    def _set_window_icon(self) -> None:
        """Set ikon jendela — coba berbagai format yang tersedia."""
        # Tentukan base path (berbeda saat jalan sebagai .exe vs script)
        if getattr(sys, "frozen", False):
            base = sys._MEIPASS
        else:
            base = os.path.dirname(os.path.abspath(__file__))

        for fname in ("icon.ico", "icon.png", "icon.jpeg", "icon.jpg"):
            fpath = os.path.join(base, fname)
            if not os.path.exists(fpath):
                continue
            try:
                if fname.endswith(".ico"):
                    self.iconbitmap(fpath)
                else:
                    from PIL import Image, ImageTk
                    img = Image.open(fpath).resize((32, 32))
                    photo = ImageTk.PhotoImage(img)
                    self.wm_iconphoto(True, photo)
                    self._icon_ref = photo  # Cegah garbage collection
                return
            except Exception:
                continue

    # ------------------------------------------------------------------ #
    #  Bangun UI                                                           #
    # ------------------------------------------------------------------ #

    def _build_ui(self) -> None:
        """Membangun semua komponen UI."""
        self.grid_columnconfigure(0, weight=1)

        self._build_header()

        scroll_frame = ctk.CTkScrollableFrame(self, label_text="")
        scroll_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")
        scroll_frame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        row = 0
        row = self._build_section_label(scroll_frame, "🌐  Terjemahan", row)
        row = self._build_language_selector(scroll_frame, row)
        row = self._build_section_label(scroll_frame, "🎨  Tampilan Hasil", row)
        row = self._build_font_size_slider(scroll_frame, row)
        row = self._build_color_pickers(scroll_frame, row)
        row = self._build_section_label(scroll_frame, "⌨️  Shortcut Keyboard", row)
        row = self._build_hotkey_display(scroll_frame, row)
        row = self._build_section_label(scroll_frame, "👁️  Preview Tampilan", row)
        row = self._build_preview(scroll_frame, row)

        self._build_footer()

    def _build_header(self) -> None:
        """Header dengan judul dan status."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="🖥️  Mindslator",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Terjemahkan teks di layar dengan satu shortcut",
            font=ctk.CTkFont(size=12),
            text_color="gray",
        ).grid(row=1, column=0, sticky="w")

        self.status_label = ctk.CTkLabel(
            header,
            text="⏸  Tidak Aktif",
            font=ctk.CTkFont(size=12),
            text_color="#e74c3c",
        )
        self.status_label.grid(row=0, column=1, rowspan=2, sticky="e")

    def _build_section_label(self, parent, text: str, row: int) -> int:
        ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        ).grid(row=row, column=0, padx=4, pady=(16, 4), sticky="w")
        return row + 1

    def _build_language_selector(self, parent, row: int) -> int:
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=0, padx=0, pady=4, sticky="ew")
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Bahasa Tujuan:", anchor="w", width=140).grid(
            row=0, column=0, padx=12, pady=10, sticky="w"
        )

        current_lang_name = get_language_name(self.config_data.get("target_language", "id"))
        self.lang_var = ctk.StringVar(value=current_lang_name)

        ctk.CTkComboBox(
            frame,
            values=list(LANGUAGE_MAP.keys()),
            variable=self.lang_var,
            state="readonly",
            width=200,
            command=self._on_language_change,
        ).grid(row=0, column=1, padx=12, pady=10, sticky="e")

        return row + 1

    def _build_font_size_slider(self, parent, row: int) -> int:
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=0, padx=0, pady=4, sticky="ew")
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Ukuran Font:", anchor="w", width=140).grid(
            row=0, column=0, padx=12, pady=10, sticky="w"
        )

        slider_frame = ctk.CTkFrame(frame, fg_color="transparent")
        slider_frame.grid(row=0, column=1, padx=12, pady=10, sticky="ew")
        slider_frame.grid_columnconfigure(0, weight=1)

        current_size = int(self.config_data.get("font_size", 16))

        self.font_size_label = ctk.CTkLabel(
            slider_frame,
            text=f"{current_size} px",
            width=55,
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.font_size_label.grid(row=0, column=1, padx=(8, 0))

        self.font_size_double_var = ctk.DoubleVar(value=float(current_size))

        ctk.CTkSlider(
            slider_frame,
            from_=10,
            to=32,
            number_of_steps=22,
            variable=self.font_size_double_var,
            command=self._on_font_size_change,
        ).grid(row=0, column=0, sticky="ew")

        return row + 1

    def _build_color_pickers(self, parent, row: int) -> int:
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=0, padx=0, pady=4, sticky="ew")
        frame.grid_columnconfigure((0, 1), weight=1)

        # Background color
        bg_frame = ctk.CTkFrame(frame, fg_color="transparent")
        bg_frame.grid(row=0, column=0, padx=12, pady=10, sticky="ew")
        ctk.CTkLabel(bg_frame, text="Warna Background:", anchor="w").pack(anchor="w")
        self.bg_preview = ctk.CTkButton(
            bg_frame,
            text=self.config_data.get("bg_color", "#1e1e1e"),
            fg_color=self.config_data.get("bg_color", "#1e1e1e"),
            hover_color=self.config_data.get("bg_color", "#1e1e1e"),
            width=140,
            height=32,
            command=self._pick_bg_color,
        )
        self.bg_preview.pack(pady=(4, 0))

        # Text color
        txt_frame = ctk.CTkFrame(frame, fg_color="transparent")
        txt_frame.grid(row=0, column=1, padx=12, pady=10, sticky="ew")
        ctk.CTkLabel(txt_frame, text="Warna Teks:", anchor="w").pack(anchor="w")
        self.text_preview = ctk.CTkButton(
            txt_frame,
            text=self.config_data.get("text_color", "#ffffff"),
            fg_color=self.config_data.get("text_color", "#ffffff"),
            hover_color=self.config_data.get("text_color", "#ffffff"),
            text_color="#000000" if self.config_data.get("text_color", "#ffffff") == "#ffffff" else "#ffffff",
            width=140,
            height=32,
            command=self._pick_text_color,
        )
        self.text_preview.pack(pady=(4, 0))

        return row + 1

    def _build_hotkey_display(self, parent, row: int) -> int:
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=0, padx=0, pady=4, sticky="ew")
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Shortcut Aktif:", anchor="w", width=140).grid(
            row=0, column=0, padx=12, pady=10, sticky="w"
        )

        hotkey = self.config_data.get("hotkey", "ctrl+alt+z").upper().replace("+", " + ")
        ctk.CTkLabel(
            frame,
            text=f"  {hotkey}  ",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            fg_color="#2d2d2d",
            corner_radius=6,
        ).grid(row=0, column=1, padx=12, pady=10, sticky="w")

        return row + 1

    def _build_preview(self, parent, row: int) -> int:
        self.preview_frame = ctk.CTkFrame(
            parent,
            fg_color=self.config_data.get("bg_color", "#1e1e1e"),
            corner_radius=8,
        )
        self.preview_frame.grid(row=row, column=0, padx=0, pady=4, sticky="ew")

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="Ini adalah contoh tampilan hasil terjemahan Anda.",
            font=ctk.CTkFont(size=int(self.config_data.get("font_size", 16))),
            text_color=self.config_data.get("text_color", "#ffffff"),
            wraplength=380,
            justify="left",
        )
        self.preview_label.pack(padx=16, pady=16)

        return row + 1

    def _build_footer(self) -> None:
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        footer.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(
            footer,
            text="💾  Simpan",
            command=self._save_settings,
            fg_color="#27ae60",
            hover_color="#1e8449",
            height=40,
        ).grid(row=0, column=0, padx=4, sticky="ew")

        self.toggle_btn = ctk.CTkButton(
            footer,
            text="▶  Aktifkan",
            command=self._toggle_listener,
            height=40,
        )
        self.toggle_btn.grid(row=0, column=1, padx=4, sticky="ew")

        ctk.CTkButton(
            footer,
            text="📌  Ke Tray",
            command=self._minimize_to_tray,
            fg_color="#7f8c8d",
            hover_color="#626567",
            height=40,
        ).grid(row=0, column=2, padx=4, sticky="ew")

    # ------------------------------------------------------------------ #
    #  Event Handlers                                                      #
    # ------------------------------------------------------------------ #

    def _on_language_change(self, choice: str) -> None:
        self.config_data["target_language"] = LANGUAGE_MAP.get(choice, "id")

    def _on_font_size_change(self, value) -> None:
        size = round(float(value))
        self.font_size_label.configure(text=f"{size} px")
        self.config_data["font_size"] = size
        self.preview_label.configure(font=ctk.CTkFont(size=size))

    def _pick_bg_color(self) -> None:
        color = colorchooser.askcolor(
            color=self.config_data.get("bg_color", "#1e1e1e"),
            title="Pilih Warna Background",
        )
        if color[1]:
            hex_color = color[1]
            self.config_data["bg_color"] = hex_color
            self.bg_preview.configure(text=hex_color, fg_color=hex_color, hover_color=hex_color)
            self.preview_frame.configure(fg_color=hex_color)
            self.preview_label.configure(fg_color=hex_color)

    def _pick_text_color(self) -> None:
        color = colorchooser.askcolor(
            color=self.config_data.get("text_color", "#ffffff"),
            title="Pilih Warna Teks",
        )
        if color[1]:
            hex_color = color[1]
            self.config_data["text_color"] = hex_color
            btn_text_color = "#000000" if _is_light_color(hex_color) else "#ffffff"
            self.text_preview.configure(
                text=hex_color,
                fg_color=hex_color,
                hover_color=hex_color,
                text_color=btn_text_color,
            )
            self.preview_label.configure(text_color=hex_color)

    def _save_settings(self) -> None:
        save_config(self.config_data)
        self.after(0, self._show_save_feedback)

    def _show_save_feedback(self) -> None:
        self.title("Mindslator — ✓ Pengaturan Tersimpan!")
        self.after(2000, lambda: self.title("Mindslator — Pengaturan"))

    def _toggle_listener(self) -> None:
        if not self.is_running:
            self._save_settings()
            self.is_running = True
            self.toggle_btn.configure(
                text="⏹  Hentikan",
                fg_color="#e74c3c",
                hover_color="#c0392b",
            )
            self.status_label.configure(text="▶  Aktif", text_color="#27ae60")
            if self.on_start_listener:
                self.on_start_listener()
        else:
            self.is_running = False
            self.toggle_btn.configure(
                text="▶  Aktifkan",
                fg_color=("#3B8ED0", "#1F6AA5"),
                hover_color=("#36719F", "#144870"),
            )
            self.status_label.configure(text="⏸  Tidak Aktif", text_color="#e74c3c")
            if self.on_stop_listener:
                self.on_stop_listener()

    def _minimize_to_tray(self) -> None:
        """Sembunyikan jendela ke system tray."""
        self.withdraw()


# ------------------------------------------------------------------ #
#  Helper                                                              #
# ------------------------------------------------------------------ #

def _is_light_color(hex_color: str) -> bool:
    """Cek apakah warna hex termasuk terang."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return luminance > 0.5
