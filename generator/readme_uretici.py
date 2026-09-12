"""
readme_uretici.py
Master README.md dosyasını mufredat_haritasi.json verileriyle otomatik üretir.
İlk 200 günün tablolarını, 20 bölümlük pedagojik mimariyi,
User Flow Mapping akış şemasını ve Özel Lisans kurallarını içerir.
"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
HARITA_DOSYA = ROOT_DIR / "mufredat_haritasi.json"
README_DOSYA = ROOT_DIR / "README.md"

with open(HARITA_DOSYA, "r", encoding="utf-8") as f:
    harita = json.load(f)

toplam_gun = len(harita)
cozulen_gun = sum(1 for m in harita if m["status"]["solved"])

readme_icerik = f"""# 🧮 Project Euler 998 Days Challenge — Progressive CS + Math Curriculum

[![Curriculum](https://img.shields.io/badge/Curriculum-998%20Days-0052CC?style=flat-square)](https://projecteuler.net/)
[![Solved](https://img.shields.io/badge/Solved-{cozulen_gun}%20%2F%20{toplam_gun}-brightgreen?style=flat-square)](#-998-günlük-müfredat-haritası)
[![Language](https://img.shields.io/badge/Language-Python%203.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Interactive Map](https://img.shields.io/badge/Visualizer-HTML5%20Canvas-FF6F00?style=flat-square)](mufredat_haritasi_visualizer.html)
[![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-red?style=flat-square)](#-özel-lisans)

> **"Project Euler arşivini gelişigüzel bir problem koleksiyonu olarak değil; 998 gün boyunca her gün bir kavram inşa eden, bilgi grafiğiyle (Knowledge Graph) birbirine bağlı bir bilgisayar bilimleri & matematik okuluna dönüştürüyoruz."**

---

## 🎯 Projenin Temel Felsefesi

Bu repo, Project Euler problemlerini rastgele seçip çözmek yerine, **1 Günlük = 1 Project Euler Problemi** kuralıyla sıralı ve pedagojik olarak inşa edilen **998 Günlük İlerlemeli Bilgisayar Bilimleri & Matematik Müfredatıdır**.

```text
Project Euler (998 Problem)
         ↓
      998 Gün
         ↓
  1 Problem / Gün
         ↓
  1 Notebook / Gün
         ↓
Progressive CS + Math Curriculum
```

### ⚖️ Değişmez Kurallar (Invariants)
1. **Birebir Eşleşme:** $\\text{{Day }} N \\equiv \\text{{Project Euler Problem }} N$. Sıra asla değiştirilmez.
2. **Tek Odak:** Her gün yalnızca ve yalnızca o güne ait tek problem çözülür ve incelenir.
3. **Bilgi Grafiği (Knowledge Graph):** Her problem, önceki günlerde öğrenilmiş teoremlere ve algoritmalara köprü kurar (`Day 003` Çarpanlar $\\rightarrow$ `Day 010` Asal Eleği gibi).
4. **Türkçe Standart:** Değişken adları, formülasyonlar, docstring'ler ve kavram açıklamaları eksiksiz Türkçe yazılır.
5. **Tam Bağımsızlık (Self-contained):** Harici veri gerektiren problemler için (`p054_poker.txt`, `p096_sudoku.txt`, `p102_triangles.txt`, `p107_network.txt` vb.) veri dosyaları ilgili günün hem `src/` klasörüne hem de çalışma dizinine kopyalanarak notebook'ların harici bağımlılık olmadan bağımsız çalışması sağlanmıştır.

---

## 🗺️ Pedagojik Öğrenme Akışı (Curriculum User Flow)

Her bir günün notebook'u, bir öğrencinin veya algoritma araştırmacısının bir problemi ilk okuduğu andan nihai karmaşıklık analizine kadar takip edeceği 20 adımlık standart bir zihinsel akışa göre tasarlanmıştır:

```mermaid
graph TD
    START(("Başlangıç: Gün N Problemi")) --> MOTIVATION["1. Günün Problemi & Motivasyon"]
    MOTIVATION --> STATEMENT["2. Problem Metni (TR + EN)"]
    STATEMENT --> TOPICS["3. Öğrenilecek Konular & Teknikler"]
    TOPICS --> PREREQ["4. Ön Bilgiler & Bilgi Grafiği"]
    PREREQ --> UNDERSTAND["5. Problemi Anlama & Örnek Senaryo"]
    
    UNDERSTAND --> MODEL["6. Matematiksel Model (LaTeX Formülleri)"]
    MODEL --> NAIVE["7. İlk / Naif Yaklaşım (Brute Force)"]
    NAIVE --> BOTTLENECK{{"Darboğaz Analizi: Süre O(N^2+) Kabul Edilebilir mi?"}}
    
    BOTTLENECK -- "Kabul Edilemez (Zaman Aşımı)" --> AHA["8 & 9. Anahtar Gözlem (Aha! Anı & Analitik İndirgeme)"]
    BOTTLENECK -- "Yeterli" --> ALGO["10. Algoritma & Sözde Kod (Pseudo-code)"]
    AHA --> ALGO
    
    ALGO --> PLAN["11. Adım Adım Çözüm Planı"]
    PLAN --> HELPERS["12. Kütüphaneler & Bağımsız Yardımcılar"]
    HELPERS --> IMPL["13. Python İmplementasyonu (coz_XXXX)"]
    IMPL --> TESTS["14. Testler & Süre Ölçümlü Doğrulama"]
    
    TESTS --> VERIFY{{"Assertion Doğrulandı mı?"}}

    VERIFY -- "Hata / Yanlış Cevap" --> DEBUG["Hata Ayıklama & Sınır Durum Kontrolü"]
    DEBUG --> IMPL
    VERIFY -- "Başarılı" --> COMPLEXITY["15. Karmaşıklık Analizi (Zaman & Alan: Naif vs Opt)"]
    
    COMPLEXITY --> ALT["16. Alternatif Çözüm Yolları"]
    ALT --> ADVANCED["17. Optimizasyon & İleri Seviye Notlar"]
    ADVANCED --> TAKEAWAYS["18. Bugün Öğrenilenler (Key Takeaways)"]
    TAKEAWAYS --> SIMILAR["19. Benzer Problem Tipleri (Euler / LeetCode / ACM)"]
    SIMILAR --> EXERCISES["20. Alıştırmalar & Düşünme Soruları"]
    EXERCISES --> END(("Nihai Kart: Doğrulanmış Çözüm & Süre"))

    style START fill:#0052cc,stroke:#003380,color:#fff
    style AHA fill:#f59e0b,stroke:#b45309,color:#fff
    style IMPL fill:#10b981,stroke:#047857,color:#fff
    style TESTS fill:#8b5cf6,stroke:#6d28d9,color:#fff
    style VERIFY fill:#06b6d4,stroke:#0e7490,color:#fff
    style DEBUG fill:#ef4444,stroke:#b91c1c,color:#fff
    style END fill:#10b981,stroke:#047857,color:#fff
```

---

## 📘 20 Bölümlük Pedagojik Notebook Mimarisi

Her günün notebook'u sıradan bir kod bloğu değil, kendi içinde eksiksiz bir eğitim ünitesidir:

| # | Bölüm Adı | Açıklama |
|---|---|---|
| **1** | **Günün Problemi ve Motivasyon** | Problemin genel bağlamı ve bize kazandıracağı sezgi |
| **2** | **Problem Metni** | Orijinal metin, akıcı Türkçe çeviri, girdi/çıktı kısıtları |
| **3** | **Öğrenilecek Konular** | Primary/Secondary Topics, temel kavramlar ve teknikler |
| **4** | **Ön Bilgiler & Bilgi Grafiği** | Önceki günlerden gelen kavram bağıntıları (Prerequisites) |
| **5** | **Problemi Anlama & Örnek Senaryo** | Küçük sayılarla adım adım senaryo ve edge-case analizi |
| **6** | **Matematiksel Model** | Teoremler, denklemler ve LaTeX formülasyonları |
| **7** | **İlk / Naif Yaklaşım (Brute Force)** | Akla ilk gelen kaba kuvvet mantığı ve darboğazı |
| **8** | **Daha İyi Yaklaşım** | Analitik sadeleştirme veya arama uzayı budaması |
| **9** | **Anahtar Gözlem (Aha! Anı)** | Problemi anında kolaylaştıran kritik matematiksel özellik |
| **10**| **Kullanılan Algoritma / Yöntem** | Veri yapıları, algoritma mantığı ve sözde kod |
| **11**| **Adım Adım Çözüm Planı** | Kodlama öncesi işlem basamakları rehberi |
| **12**| **Kütüphaneler ve Yardımcılar** | Bağımsız çalışmayı sağlayan paylaşılan matematik araçları |
| **13**| **Python İmplementasyonu** | Temiz, tip ipuçlu ve Türkçe değişkenli `coz_XXXX()` kodu |
| **14**| **Testler ve Doğrulama** | Süre ölçümlü, doğrulanmış çalıştırılabilir test hücresi |
| **15**| **Karmaşıklık Analizi** | Zaman ve Alan karmaşıklığı: Naif vs Optimize karşılaştırması |
| **16**| **Alternatif Çözüm Yolları** | Fonksiyonel tek satırlıklar, dinamik programlama vb. |
| **17**| **Optimizasyon ve İpuçları** | Bellek tasarrufu, ön hesaplama, bit düzeyinde hızlandırma |
| **18**| **Bugün Öğrenilenler** | Algoritma cephaneliğimize eklenen anahtar ilkeler |
| **19**| **Benzer Problem Tipleri** | Euler, LeetCode ve ACM yarışmalarındaki kardeş sorular |
| **20**| **Alıştırmalar & Düşünme Soruları**| Ölçeklenebilirlik, genelleştirme ve zihin açıcı sorular |

---

## 📂 Dizin Yapısı

```text
project-euler-998-days/
│
├── README.md                      # Ana müfredat vitrini ve 998 günlük ilerleme tablosu
├── mufredat_haritasi.json         # 998 günün tam Knowledge Graph veritabanı
├── mufredat_haritasi_visualizer.html # İnteraktif HTML5 Canvas bilgi grafiği görselleştirici
├── AGENTS.md                      # 998 Günlük AI Agent çalışma protokolü
├── cozumler.py                    # Doğrulanmış Türkçe çözümler kütüphanesi (P1 - P200)
├── sorular.json                   # 998 sorunun metin veritabanı
│
├── day_001/
│   ├── day_001_problem_001_multiples_of_3_or_5.ipynb
│   └── src/
├── day_054/
│   ├── day_054_problem_054_poker_hands.ipynb
│   ├── p054_poker.txt
│   └── src/
│       └── p054_poker.txt         # Günün harici verisi yerel olarak src/ içinde
├── day_102/
│   ├── day_102_problem_102_triangle_containment.ipynb
│   ├── p102_triangles.txt
│   └── src/
│       └── p102_triangles.txt
...
└── day_998/
    ├── day_998_problem_998_squaring_the_triangle.ipynb
    └── src/
```

---

## 🗺️ 998 Günlük Müfredat Haritası

### 🔹 Blok 1: Temel Matematik, Sayılar Teorisi ve Algoritma Temelleri (Gün 001 – Gün 100)

| Gün | Euler # | Problem Başlığı | Ana Konu | Zorluk | Zaman (Opt) | Durum |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: |
"""

for m in harita[:100]:
    day = m["day"]
    pid = m["project_euler_id"]
    title = m["title"]
    slug = m["slug"]
    topic = m["topics"]["primary"]
    diff = m["difficulty"].split()[0]
    t_opt = m["time_complexity"]["optimized"]
    nb_link = f"[day_{day:03d}](day_{day:03d}/day_{day:03d}_problem_{pid:03d}_{slug}.ipynb)"
    durum = "✅ Çözüldü" if m["status"]["solved"] else "⏳ Hazır"
    readme_icerik += f"| **{day:03d}** | #{pid} | {nb_link} | {topic} | {diff} | `{t_opt}` | {durum} |\n"

readme_icerik += f"""
### 🔹 Blok 2: İleri Sayılar Teorisi, Markov Zincirleri, Graf Teorisi ve Dinamik Programlama (Gün 101 – Gün 200)

| Gün | Euler # | Problem Başlığı | Ana Konu | Zorluk | Zaman (Opt) | Durum |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: |
"""

for m in harita[100:200]:
    day = m["day"]
    pid = m["project_euler_id"]
    title = m["title"]
    slug = m["slug"]
    topic = m["topics"]["primary"]
    diff = m["difficulty"].split()[0]
    t_opt = m["time_complexity"]["optimized"]
    nb_link = f"[day_{day:03d}](day_{day:03d}/day_{day:03d}_problem_{pid:03d}_{slug}.ipynb)"
    durum = "✅ Çözüldü" if m["status"]["solved"] else "⏳ Hazır"
    readme_icerik += f"| **{day:03d}** | #{pid} | {nb_link} | {topic} | {diff} | `{t_opt}` | {durum} |\n"

readme_icerik += f"""
---

## 🚀 Sonraki Bloklar (Gün 201 – Gün 998)

- **Blok 3 (Gün 201–500):** Üreteç Fonksiyonlar, Eliptik Eğriler, Büyük Kombinatorik, Ağ Akışları
- **Blok 4 (Gün 501–998):** İleri Düzey Araştırma Seviyesi Problemler, Simbiyotik Algoritmalar

---

## 📜 Özel Lisans — Tüm Hakları Saklıdır

```
ÖZEL LİSANS — TÜM HAKLAR SAKLIDIR

Telif Hakkı (c) 2026 Seydi Eryılmaz (@seydivakkas)

Bu yazılım ve ilgili tüm dosyalar ("Yazılım") yalnızca görüntüleme ve eğitim
amaçlı olarak paylaşılmıştır.

YASAKLAR:
  1. Kopyalanamaz, çoğaltılamaz, dağıtılamaz veya yeniden yayınlanamaz.
  2. Ticari veya ticari olmayan hiçbir projede kullanılamaz, değiştirilemez.
  3. Alt lisanslanamaz, satılamaz veya devredilemez.
  4. Tersine mühendislik yapılamaz.

İZİN VERİLEN KULLANIM:
  - GitHub üzerinde görüntüleme ve okuma.
  - Kişisel öğrenim amacıyla kodu inceleme (kopyalamadan).

YAZARIN AÇIK YAZILI İZNİ OLMAKSIZIN HİÇBİR KULLANIM HAKKI TANINMAZ.
İzin talepleri için: GitHub @seydivakkas
```
"""

with open(README_DOSYA, "w", encoding="utf-8") as f:
    f.write(readme_icerik)

print(f"[✓] README.md oluşturuldu! ({len(readme_icerik)} karakter, {cozulen_gun} gün çözüldü)")
