# Sistem Agen AI Berbasis Skill

Sistem agen AI modular yang dirancang untuk menyelesaikan tugas-tugas kompleks
secara mandiri — mulai dari pemrosesan dokumen, analisis data, hingga pembuatan
konten — menggunakan ekosistem skill yang terdokumentasi dan dapat diperluas.

---

## Gambaran Umum

Sistem ini memisahkan **kemampuan** (skill) dari **perilaku** (agen), sehingga
setiap bagian dapat dikembangkan, diuji, dan dipelihara secara independen.
Agen membaca deskripsi skill yang tersedia dan memilih pendekatan terbaik
berdasarkan konteks permintaan pengguna.

```
Permintaan Pengguna → Agen → Pilih Skill → Eksekusi → Output
```

---

## Struktur Proyek

```
/
├── AGENT.md          # Identitas, prinsip perilaku, dan batas otonomi agen
├── SKILL.md          # Template standar untuk mendokumentasikan skill baru
├── ROADMAP.md        # Peta jalan dan milestone pengembangan
├── README.md         # Dokumen ini
└── /mnt/skills/      # Direktori semua skill yang tersedia
    └── [kategori]/
        └── [nama-skill]/
            └── SKILL.md
```

---

## Dokumen Inti

| Dokumen | Fungsi |
|---|---|
| `AGENT.md` | Mendefinisikan cara agen berpikir, berkomunikasi, dan mengambil keputusan |
| `SKILL.md` | Kerangka standar untuk membuat dokumentasi skill baru |
| `ROADMAP.md` | Prioritas dan jadwal pengembangan fitur |

---

## Cara Kerja Skill

Setiap skill adalah unit kemampuan yang terdokumentasi dalam format `SKILL.md`.
Agen menggunakan deskripsi skill untuk menentukan kapan dan bagaimana
menggunakannya.

### Anatomi Skill

```yaml
---
name: nama-skill
description: >
  Kondisi trigger dan scope singkat skill ini.
---
```

Diikuti oleh:
- **Tujuan** — masalah yang diselesaikan dan pengguna yang diuntungkan
- **Panduan Penggunaan** — langkah operasional yang dapat ditindaklanjuti
- **Format Output** — tipe dan struktur hasil yang diharapkan
- **Batasan** — hal yang berada di luar cakupan skill

---

## Status Pengembangan

| Fase | Periode | Status |
|---|---|---|
| Fase 1 — Fondasi | Q2 2026 | ✅ Berlangsung |
| Fase 2 — Ekspansi Kemampuan | Q3 2026 | 🔄 Planned |
| Fase 3 — Orkestrasi Multi-Agen | Q4 2026 | 📋 Planned |
| Fase 4 — Optimasi & Skalabilitas | Q1 2027 | 🔮 Future |

Skill yang sedang dikembangkan di Fase 2: `data-analysis`, `web-scraping`,
`code-review`, `email-drafting`, `image-generation`.

Lihat [ROADMAP.md](ROADMAP.md) untuk detail lengkap.

---

## Prinsip Desain

- **Dokumentasi dulu** — setiap skill didokumentasikan sebelum diimplementasikan
- **Satu skill, satu tanggung jawab** — tidak ada skill yang mencoba melakukan segalanya
- **Gagal dengan jelas** — batasan skill didokumentasikan secara eksplisit
- **Iterasi berbasis bukti** — perubahan didorong oleh kasus nyata

---

## Menambahkan Skill Baru

1. Salin template dari `SKILL.md`
2. Isi semua bagian wajib (name, description, tujuan, panduan, output, batasan)
3. Sertakan minimal 2 contoh use case nyata
4. Simpan di `/mnt/skills/[kategori]/[nama-skill]/SKILL.md`
5. Perbarui `ROADMAP.md` untuk mencatat penambahan skill

---

## Prinsip Perilaku Agen

Agen beroperasi berdasarkan lima prinsip inti:

1. **Kejujuran Kapabilitas** — tidak membuat janji yang tidak dapat dipenuhi
2. **Transparansi Proses** — menjelaskan langkah sebelum mengeksekusi tugas besar
3. **Konfirmasi pada Titik Kritis** — meminta persetujuan sebelum tindakan destruktif
4. **Minimal Footprint** — tidak mengambil akses lebih dari yang dibutuhkan
5. **Gagal dengan Anggun** — menjelaskan error dalam bahasa yang dapat dipahami

---

## Bahasa & Model

- **Bahasa Utama:** Indonesia (dapat beralih ke Inggris sesuai konteks)
- **Model Dasar:** Claude Sonnet (Anthropic)

---

*Versi: 1.0 | Terakhir diperbarui: Mei 2026*
