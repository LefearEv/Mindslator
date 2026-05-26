---
name: skill-template
description: >
  Gunakan skill ini sebagai kerangka dasar untuk mendokumentasikan kemampuan
  agen AI. Trigger ketika pengguna ingin membuat panduan instruksi terstruktur,
  mendefinisikan perilaku spesifik, atau mendokumentasikan workflow untuk sistem
  berbasis AI.
---

# SKILL.md — Panduan Dokumentasi Kemampuan Agen

Dokumen ini adalah kerangka standar untuk mendefinisikan, mendokumentasikan, dan
mengomunikasikan kemampuan (skill) sebuah agen AI secara konsisten dan dapat
direproduksi.

---

## Tujuan

Skill.md berfungsi sebagai "kontrak" antara agen dan pengguna — menjelaskan
dengan tepat apa yang bisa dilakukan, bagaimana melakukannya, dan kapan
menggunakannya.

- **Masalah yang diselesaikan:** Ketidakkonsistenan perilaku agen akibat instruksi
  yang ambigu atau tidak terdokumentasi
- **Pengguna yang diuntungkan:** Developer, prompt engineer, tim produk yang
  membangun sistem berbasis AI
- **Gunakan ketika:** Mendefinisikan kemampuan baru, onboarding agen ke workflow
  baru, atau membakukan perilaku yang sudah berjalan
- **Jangan gunakan ketika:** Kebutuhan hanya berupa catatan informal atau
  dokumentasi teknis kode

---

## Struktur Dokumen

### Bagian Wajib

| Bagian | Isi |
|---|---|
| `name` | Nama skill dalam format kebab-case |
| `description` | Trigger condition dan scope singkat (≤ 3 kalimat) |
| Tujuan | Masalah, pengguna, kapan pakai / tidak pakai |
| Panduan Penggunaan | Langkah-langkah operasional yang jelas |
| Format Output | Tipe, struktur, dan gaya hasil yang diharapkan |
| Batasan | Hal di luar kemampuan skill ini |

### Bagian Opsional

- Konteks & Latar Belakang
- Contoh Input / Output
- Referensi & Sumber Daya

---

## Panduan Penulisan

### Langkah 1 — Tentukan Scope

Jawab tiga pertanyaan sebelum menulis:
1. Apa satu hal utama yang dilakukan skill ini?
2. Apa sinyal yang memicu penggunaan skill ini?
3. Apa yang berada di luar batas skill ini?

### Langkah 2 — Tulis Deskripsi Trigger

Deskripsi adalah bagian paling kritis — digunakan sistem untuk menentukan
kapan skill ini dipanggil. Gunakan pola:

> "Gunakan skill ini ketika [kondisi]. Trigger ketika [sinyal spesifik].
> Jangan gunakan untuk [pengecualian]."

### Langkah 3 — Dokumentasikan Langkah Operasional

Tulis setiap langkah dalam format imperatif yang dapat ditindaklanjuti.
Hindari kata ambigu seperti "mungkin", "bisa jadi", atau "tergantung".

### Langkah 4 — Validasi

Sebuah skill.md yang baik memenuhi kriteria berikut:
- Orang baru dapat mengikuti instruksi tanpa bertanya
- Tidak ada langkah yang mengasumsikan pengetahuan implisit
- Output yang dihasilkan konsisten di antara berbagai agen

---

## Format Output

- **Tipe file:** Markdown (`.md`) dengan frontmatter YAML
- **Panjang:** 100–300 baris; cukup detail, tidak berlebihan
- **Tone:** Teknis, imperatif, presisi tinggi — bukan prosa naratif
- **Lokasi:** `/mnt/skills/[kategori]/[nama-skill]/SKILL.md`

---

## Contoh

### Contoh Deskripsi Trigger yang Baik

> "Gunakan skill ini setiap kali file .xlsx terlibat sebagai input atau output.
> Trigger ketika pengguna menyebut 'spreadsheet', 'Excel', atau file berekstensi
> .xlsx/.csv. Jangan gunakan untuk dokumen Word atau laporan HTML."

### Contoh yang Buruk (terlalu umum)

> "Gunakan untuk file data."

---

## Batasan

- Skill.md bukan pengganti dokumentasi teknis kode atau API
- Tidak mencakup evaluasi performa atau benchmarking (gunakan skill `skill-creator`)
- Tidak menangani versioning otomatis — versi dikelola manual

---

## Referensi

- Skill terkait: `skill-creator`, `skill-template`
- Panduan lanjutan: `agent.md`

---

*Versi: 1.0 | Terakhir diperbarui: Mei 2026*
