# ROADMAP.md — Peta Jalan Pengembangan Sistem Agen AI

Dokumen ini mendefinisikan arah, prioritas, dan milestone pengembangan sistem
agen AI beserta ekosistem skill-nya. Roadmap ini bersifat hidup — diperbarui
seiring pembelajaran dan perubahan prioritas.

---

## Visi

Membangun sistem agen AI yang dapat menyelesaikan tugas-tugas kompleks secara
mandiri, konsisten, dan dapat dipercaya — dengan dokumentasi yang cukup baik
sehingga siapa pun dapat memahami, memperluas, dan memeliharanya.

---

## Status Saat Ini

**Fase:** Fondasi  
**Periode:** Q2 2026  
**Fokus:** Membangun struktur skill, dokumentasi standar, dan pola orkestrasi dasar

---

## Fase Pengembangan

### Fase 1 — Fondasi ✅ (Selesai / Berlangsung)

Membangun blok bangunan dasar yang diperlukan sebelum ekspansi.

**Deliverable:**
- Struktur direktori skill yang standar
- Template SKILL.md dan panduan penulisan
- Skill inti: `docx`, `pdf`, `pptx`, `xlsx`, `frontend-design`
- Skill meta: `skill-template`, `skill-creator`, `file-reading`
- Dokumentasi `agent.md` awal

**Kriteria Selesai:**
- Setiap skill memiliki SKILL.md yang valid
- Agen dapat memilih skill yang tepat berdasarkan konteks
- Tidak ada skill yang tumpang tindih tanpa alasan jelas

---

### Fase 2 — Ekspansi Kemampuan 🔄 (Q3 2026)

Memperluas cakupan skill ke domain baru dan meningkatkan kedalaman skill yang ada.

**Deliverable:**

| Skill Baru | Prioritas | Status |
|---|---|---|
| `data-analysis` | Tinggi | Planned |
| `web-scraping` | Tinggi | Planned |
| `email-drafting` | Sedang | Planned |
| `image-generation` | Sedang | Planned |
| `code-review` | Tinggi | Planned |
| `translation` | Rendah | Backlog |

**Peningkatan Skill Existing:**
- Tambah contoh lebih banyak di setiap SKILL.md
- Dokumentasikan edge case yang ditemukan di lapangan
- Standardisasi format output di semua skill dokumen

---

### Fase 3 — Orkestrasi Multi-Agen 📋 (Q4 2026)

Memungkinkan beberapa agen bekerja sama untuk menyelesaikan tugas yang lebih kompleks.

**Deliverable:**
- Pola handoff antar agen (skill `agent-handoff`)
- Skill `orchestrator` untuk koordinasi workflow multi-langkah
- Mekanisme memory dan state sharing antar sesi
- Skill `quality-check` untuk validasi output agen lain

**Prinsip Desain Fase Ini:**
- Setiap agen tetap memiliki tanggung jawab tunggal yang jelas
- Kegagalan satu agen tidak merusak seluruh workflow
- Semua keputusan orkestrasi dapat diaudit

---

### Fase 4 — Optimasi & Skalabilitas 🔮 (Q1 2027)

Meningkatkan kualitas, kecepatan, dan kemampuan sistem di skala besar.

**Area Fokus:**
- Benchmarking performa per skill
- Reduksi prompt token tanpa kehilangan akurasi
- Skill caching dan reuse pattern
- Evaluasi otomatis dengan test suite per skill

---

## Backlog

Item-item yang diidentifikasi tetapi belum dijadwalkan:

- Skill `research` — pencarian web mendalam multi-sumber
- Skill `meeting-summary` — transkripsi dan ringkasan rapat
- Skill `sql-query` — generasi dan validasi query database
- Integrasi dengan tools eksternal (Notion, Linear, Slack)
- Dashboard monitoring penggunaan skill

---

## Prinsip Pengembangan

1. **Dokumentasi dulu, kode kemudian** — setiap skill didokumentasikan sebelum
   diimplementasikan
2. **Satu skill, satu tanggung jawab** — hindari skill yang mencoba melakukan
   segalanya
3. **Gagal dengan jelas** — skill harus mendokumentasikan batasannya secara
   eksplisit
4. **Iterasi berbasis bukti** — perubahan didorong oleh kasus nyata, bukan asumsi

---

## Cara Berkontribusi

1. Identifikasi gap — tugas yang sering dilakukan tetapi tidak ada skillnya
2. Draft SKILL.md menggunakan template standar
3. Ajukan ke review dengan minimal 2 contoh use case nyata
4. Setelah disetujui, tambahkan ke direktori skill dan perbarui roadmap ini

---

## Changelog

| Tanggal | Versi | Perubahan |
|---|---|---|
| Mei 2026 | 1.0 | Dokumen awal dibuat |

---

*Versi: 1.0 | Terakhir diperbarui: Mei 2026 | Pemilik: Tim AI*
