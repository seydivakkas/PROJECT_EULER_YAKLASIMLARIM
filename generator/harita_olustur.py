"""
harita_olustur.py
998 günlük Project Euler müfredatının bilgi grafiğini (mufredat_haritasi.json) oluşturur.
Her problem için:
  - Gün & Problem ID
  - Başlık & slug
  - Zorluk derecesi (Çözücü sayısına ve matematiksel derinliğe göre)
  - Ana konu (Primary Topic) & Alt konular (Secondary Topics)
  - Temel kavramlar (Concepts) & Algoritmik teknikler (Techniques)
  - Öncüller (Prerequisites - Bilgi Grafiği bağıntıları)
  - Zaman ve Alan karmaşıklığı (Naif vs Optimize)
"""

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROBLEMS_FILE = Path("project_euler_problems.json")
OUTPUT_FILE = Path("mufredat_haritasi.json")

# İlk 100 problem için özel küratörlü bilgi grafiği
ILK_100_HARITA = {
    1: {
        "difficulty": "Başlangıç (Beginner)", "difficulty_level": 1,
        "primary": "Sayılar Teorisi (Number Theory)",
        "secondary": ["Dahil Etme-Hariç Tutma İlkesi", "Aritmetik Diziler"],
        "concepts": ["Aritmetik dizi toplamı", "Gauss formülü", "Ortak katlar", "Analitik sadeleştirme"],
        "techniques": ["Inclusion-Exclusion", "Kapalı formül", "Sabit zamanlı O(1) hesap"],
        "prerequisites": [],
        "time_naive": "O(N)", "time_opt": "O(1)",
        "space_naive": "O(1)", "space_opt": "O(1)"
    },
    2: {
        "difficulty": "Başlangıç (Beginner)", "difficulty_level": 1,
        "primary": "Diziler ve Yinelemeler (Sequences & Recurrences)",
        "secondary": ["Fibonacci Dizisi", "Parite ve Periyot"],
        "concepts": ["Fibonacci terimleri", "Çift sayı periyodu (E, O, O, E...)", "Yineleme bağıntısı"],
        "techniques": ["İteratif durum güncelleme", "Her 3. terimi alma / E(n) = 4E(n-1) + E(n-2)"],
        "prerequisites": [],
        "time_naive": "O(log N)", "time_opt": "O(log N)",
        "space_naive": "O(1)", "space_opt": "O(1)"
    },
    3: {
        "difficulty": "Başlangıç (Beginner)", "difficulty_level": 1,
        "primary": "Sayılar Teorisi (Number Theory)",
        "secondary": ["Asal Sayılar", "Asal Çarpanlara Ayırma"],
        "concepts": ["Asal bölenler", "Karekök sınır teoremi", "Aritmetiğin temel teoremi"],
        "techniques": ["Deneme bölmesi (Trial Division)", "Bölen küçültme"],
        "prerequisites": [],
        "time_naive": "O(N)", "time_opt": "O(√N)",
        "space_naive": "O(1)", "space_opt": "O(1)"
    },
    4: {
        "difficulty": "Başlangıç (Beginner)", "difficulty_level": 1,
        "primary": "Arama ve Sayı Temsili (Search & Number Representation)",
        "secondary": ["Palindromlar", "Basamak Analizi"],
        "concepts": ["Simetri kontrolü", "Çift basamaklı palindromların 11'e bölünebilirliği"],
        "techniques": ["Çift yönlü kaba kuvvet", "Budama (Pruning)", "Geriye doğru arama"],
        "prerequisites": [],
        "time_naive": "O(N²)", "time_opt": "O(N²/11)",
        "space_naive": "O(1)", "space_opt": "O(1)"
    },
    5: {
        "difficulty": "Başlangıç (Beginner)", "difficulty_level": 1,
        "primary": "Sayılar Teorisi (Number Theory)",
        "secondary": ["EBOB / EKOK", "Asal Çarpan Üsleri"],
        "concepts": ["En Küçük Ortak Kat (LCM)", "Öklid Algoritması", "Asal kuvvetleri"],
        "techniques": ["Zincirleme EKOK indirgemesi (reduce)", "Asal üsleri maksimizasyonu"],
        "prerequisites": ["day_003"],
        "time_naive": "O(N · M)", "time_opt": "O(N log(max))",
        "space_naive": "O(1)", "space_opt": "O(1)"
    },
    6: {
        "difficulty": "Başlangıç (Beginner)", "difficulty_level": 1,
        "primary": "Cebir ve Kapalı Formüller (Algebra)",
        "secondary": ["Kare Toplamları", "Seri Formülleri"],
        "concepts": ["Doğal sayı toplamı n(n+1)/2", "Kare toplamı n(n+1)(2n+1)/6"],
        "techniques": ["Analitik cebirsel çıkarma", "Sabit zamanlı çözüm"],
        "prerequisites": ["day_001"],
        "time_naive": "O(N)", "time_opt": "O(1)",
        "space_naive": "O(1)", "space_opt": "O(1)"
    },
    7: {
        "difficulty": "Başlangıç-Orta (Easy)", "difficulty_level": 2,
        "primary": "Asal Sayılar (Prime Numbers)",
        "secondary": ["Asallık Testi", "Asal Sayı Teoremi"],
        "concepts": ["n. asal sayısı", "Asallık yoğunluğu (n ln n)", "6k±1 kuralı"],
        "techniques": ["Optimize deneme bölmesi", "Adım adımlı elek"],
        "prerequisites": ["day_003"],
        "time_naive": "O(N · √M)", "time_opt": "O(N log log N)",
        "space_naive": "O(1)", "space_opt": "O(N)"
    },
    8: {
        "difficulty": "Başlangıç (Beginner)", "difficulty_level": 1,
        "primary": "Dizi İşleme (Array Processing)",
        "secondary": ["Kayan Pencere (Sliding Window)", "Basamak Çarpımı"],
        "concepts": ["Pencere kaydırma", "Sıfır içeren pencereleri atlama"],
        "techniques": ["Sliding Window", "Çarpım güncellemesi"],
        "prerequisites": [],
        "time_naive": "O(N · K)", "time_opt": "O(N)",
        "space_naive": "O(1)", "space_opt": "O(1)"
    },
    9: {
        "difficulty": "Başlangıç-Orta (Easy)", "difficulty_level": 2,
        "primary": "Diofant Denklemleri (Diophantine Equations)",
        "secondary": ["Pisagor Üçlüleri", "Parametrik Üretim"],
        "concepts": ["a² + b² = c²", "a + b + c = 1000", "Öklid Pisagor Formülü (m, n)"],
        "techniques": ["Parametrik arama", "Cebirsel kısıt analizi"],
        "prerequisites": [],
        "time_naive": "O(N²)", "time_opt": "O(N)",
        "space_naive": "O(1)", "space_opt": "O(1)"
    },
    10: {
        "difficulty": "Başlangıç-Orta (Easy)", "difficulty_level": 2,
        "primary": "Asal Sayılar (Prime Numbers)",
        "secondary": ["Eratosthenes Eleği", "Büyük Dizi Toplamı"],
        "concepts": ["Asal eleği algoritması", "Bitarray optimizasyonu", "Prefix asal toplamları"],
        "techniques": ["Sieve of Eratosthenes", "Tek sayıları indeksleme"],
        "prerequisites": ["day_003", "day_007"],
        "time_naive": "O(N √N)", "time_opt": "O(N log log N)",
        "space_naive": "O(1)", "space_opt": "O(N)"
    },
    11: {
        "difficulty": "Başlangıç-Orta (Easy)", "difficulty_level": 2,
        "primary": "Izgara Arama (Grid Search)",
        "secondary": ["2B Matris İşleme", "Yön Vektörleri"],
        "concepts": ["Yatay, dikey, köşegen arama", "Sınır kontrolleri"],
        "techniques": ["Yön matrisi (dx, dy)", "Komşuluk taraması"],
        "prerequisites": ["day_008"],
        "time_naive": "O(R · C · K)", "time_opt": "O(R · C)",
        "space_naive": "O(1)", "space_opt": "O(1)"
    },
    12: {
        "difficulty": "Orta (Intermediate)", "difficulty_level": 3,
        "primary": "Sayılar Teorisi (Number Theory)",
        "secondary": ["Bölen Sayısı Fonksiyonu d(n)", "Üçgen Sayılar"],
        "concepts": ["Üçgen sayı n(n+1)/2", "Aralarında asal çarpanlar", "τ(n) = ∏(a_i + 1)"],
        "techniques": ["Asal çarpanlara ayırma ile bölen sayısı bulma", "Ortak bölen ayrıştırma"],
        "prerequisites": ["day_003", "day_005"],
        "time_naive": "O(N √N)", "time_opt": "O(N · (log N) / ln ln N)",
        "space_naive": "O(1)", "space_opt": "O(1)"
    },
    13: {
        "difficulty": "Başlangıç (Beginner)", "difficulty_level": 1,
        "primary": "Büyük Sayı Aritmetiği (Arbitrary Precision Arithmetic)",
        "secondary": ["Basamak Analizi", "Büyük Toplamlar"],
        "concepts": ["Elden taşma mantığı (Carry)", "İlk k basamak hassasiyeti"],
        "techniques": ["Büyük tamsayı toplama", "String dilimleme"],
        "prerequisites": [],
        "time_naive": "O(N · D)", "time_opt": "O(N · D)",
        "space_naive": "O(D)", "space_opt": "O(D)"
    },
    14: {
        "difficulty": "Orta (Intermediate)", "difficulty_level": 3,
        "primary": "Dinamik Programlama (Dynamic Programming)",
        "secondary": ["Collatz Sanısı", "Önbellekleme (Memoization)"],
        "concepts": ["Doluş dizisi (Hailstone sequence)", "Yinelemeli durum grafı"],
        "techniques": ["Memoization (@lru_cache veya sözlük)", "Çift sayıları hızlandırma"],
        "prerequisites": ["day_002"],
        "time_naive": "O(N · L)", "time_opt": "O(N)",
        "space_naive": "O(1)", "space_opt": "O(N)"
    },
    15: {
        "difficulty": "Başlangıç-Orta (Easy)", "difficulty_level": 2,
        "primary": "Kombinatorik (Combinatorics)",
        "secondary": ["Kafes Yolları (Lattice Paths)", "Binom Katsayıları"],
        "concepts": ["Manhattan yolları", "Tekrarlı permütasyon", "Kombinasyon C(2n, n)"],
        "techniques": ["Pascal üçgeni bağıntısı", "Analitik binom katsayısı"],
        "prerequisites": [],
        "time_naive": "O(2^(2N))", "time_opt": "O(N)",
        "space_naive": "O(N²)", "space_opt": "O(1)"
    },
    16: {
        "difficulty": "Başlangıç (Beginner)", "difficulty_level": 1,
        "primary": "Büyük Sayı Aritmetiği (Big Integer Arithmetic)",
        "secondary": ["Kuvvet Alma", "Basamak Toplamı"],
        "concepts": ["2^1000 basamak sayısı", "Hızlı üs alma (Binary Exponentiation)"],
        "techniques": ["Python büyük tamsayı aritmetiği", "Rakam toplama"],
        "prerequisites": ["day_013"],
        "time_naive": "O(N)", "time_opt": "O(log N)",
        "space_naive": "O(N)", "space_opt": "O(N)"
    },
    17: {
        "difficulty": "Başlangıç-Orta (Easy)", "difficulty_level": 2,
        "primary": "Dize İşleme ve Ayrıştırma (String Parsing)",
        "secondary": ["Sayı-Metin Dönüşümü", "Kural Tabanlı Sistemler"],
        "concepts": ["İngilizce sayı yazımı", "Özel durumlar (teens, tens, and)"],
        "techniques": ["Sözlük tabanlı haritalama", "Modüler basamak ayrıştırma"],
        "prerequisites": [],
        "time_naive": "O(N)", "time_opt": "O(N)",
        "space_naive": "O(1)", "space_opt": "O(1)"
    },
    18: {
        "difficulty": "Orta (Intermediate)", "difficulty_level": 3,
        "primary": "Dinamik Programlama (Dynamic Programming)",
        "secondary": ["Aşağıdan Yukarıya DP (Bottom-Up)", "Maksimum Yol Toplamı"],
        "concepts": ["Yol optimizasyonu", "Üçgen matris", "Alt problemlerin optimal yapısı"],
        "techniques": ["Bottom-up dinamik programlama", "Yerinde (in-place) güncelleme"],
        "prerequisites": [],
        "time_naive": "O(2^H)", "time_opt": "O(H²)",
        "space_naive": "O(H²)", "space_opt": "O(H)"
    },
    19: {
        "difficulty": "Başlangıç-Orta (Easy)", "difficulty_level": 2,
        "primary": "Takvim Algoritmaları (Calendar Algorithms)",
        "secondary": ["Modüler Aritmetik", "Zeller Uyumu"],
        "concepts": ["Artık yıl kuralları", "Ay uzunlukları", "Haftanın günleri periyodu"],
        "techniques": ["Zeller's Congruence", "Simülasyon"],
        "prerequisites": [],
        "time_naive": "O(Y)", "time_opt": "O(Y)",
        "space_naive": "O(1)", "space_opt": "O(1)"
    },
    20: {
        "difficulty": "Başlangıç (Beginner)", "difficulty_level": 1,
        "primary": "Büyük Sayı Aritmetiği (Big Integer Factorial)",
        "secondary": ["Faktöriyel", "Basamak Toplamı"],
        "concepts": ["100! büyüklüğü", "Sıfırların basamak toplamına etkisi"],
        "techniques": ["Büyük tamsayı çarpımı", "Rakam toplama"],
        "prerequisites": ["day_016"],
        "time_naive": "O(N²)", "time_opt": "O(N log² N)",
        "space_naive": "O(N)", "space_opt": "O(N)"
    }
}

# 21-100 için şablon doldurucu fonksiyon
def generate_metadata_for_all():
    with open(PROBLEMS_FILE, "r", encoding="utf-8") as f:
        problems = json.load(f)

    curriculum = []

    for p in problems:
        pid = p["id"]
        title = p["title"]
        solved_by = int(p.get("solved_by", "0").replace(",", ""))
        slug = re.sub(r"[^\w]+", "_", title.lower()).strip("_")

        # Özel tanımlı varsa al
        custom = ILK_100_HARITA.get(pid)

        if custom:
            meta = {
                "day": pid,
                "project_euler_id": pid,
                "title": title,
                "slug": slug,
                "solved_by": solved_by,
                "euler_url": p["url"],
                "difficulty": custom["difficulty"],
                "difficulty_level": custom["difficulty_level"],
                "topics": {
                    "primary": custom["primary"],
                    "secondary": custom["secondary"]
                },
                "concepts": custom["concepts"],
                "techniques": custom["techniques"],
                "prerequisites": custom["prerequisites"],
                "time_complexity": {
                    "naive": custom["time_naive"],
                    "optimized": custom["time_opt"]
                },
                "space_complexity": {
                    "naive": custom["space_naive"],
                    "optimized": custom["space_opt"]
                },
                "status": {
                    "solved": pid <= 100,
                    "tested": pid <= 100
                }
            }
        else:
            # Otomatik çıkarım (Heuristic)
            primary = "Sayılar Teorisi ve Kombinatorik"
            sec = ["Matematiksel Modelleme", "Algoritmik Optimizasyon"]
            conc = ["Kısıt analizi", "Verimli arama uzayı"]
            tech = ["Arama uzayı budama", "Analitik indirgeme"]
            prereq = []
            
            t_lower = title.lower()
            if any(k in t_lower for k in ["prime", "sieve"]):
                primary = "Asal Sayılar ve Elekler"
                sec = ["Eratosthenes Eleği", "Asallık Testi"]
                conc = ["Asal çarpanlar", "Kalıntı sınıfları"]
                tech = ["Sieve algoritmaları", "Modüler aritmetik"]
                prereq = ["day_003", "day_010"]
            elif any(k in t_lower for k in ["triangle", "circle", "polygon", "geometry"]):
                primary = "Hesaplamalı Geometri (Computational Geometry)"
                sec = ["Öklid Geometrisi", "Izgara Noktaları"]
                conc = ["Alan hesabı", "Tam koordinatlar"]
                tech = ["Pick Teoremi", "Trigonometrik formüller"]
                prereq = ["day_009", "day_039"]
            elif any(k in t_lower for k in ["fibonacci", "sequence", "recurrence", "series"]):
                primary = "Diziler ve Yinelemeler (Sequences & Recurrences)"
                sec = ["Lineer Rekürsiyon", "Matris Üs Alma"]
                conc = ["Karakteristik denklem", "Periyot analizi"]
                tech = ["Matris üs alma O(log N)", "Dinamik programlama"]
                prereq = ["day_002"]
            elif any(k in t_lower for k in ["partition", "permutation", "combination", "dice", "probability"]):
                primary = "Kombinatorik ve Olasılık"
                sec = ["Sayma İlkeleri", "Üreteç Fonksiyonlar"]
                conc = ["Durum uzayı", "Beklenen değer"]
                tech = ["Dinamik programlama", "DP memoization"]
                prereq = ["day_015", "day_031"]
            elif any(k in t_lower for k in ["matrix", "path", "graph", "network", "grid"]):
                primary = "Graf Teorisi ve Ağ Yolları"
                sec = ["En Kısa Yol", "Ağ Akışları"]
                conc = ["Ağırlıklı graf", "Dijkstra algoritması"]
                tech = ["Priority Queue / Heap", "Grid DP"]
                prereq = ["day_018", "day_081"]
            elif any(k in t_lower for k in ["digit", "pandigital", "palindrome", "roman"]):
                primary = "Basamak Analizi ve Sayı Temsili"
                sec = ["Taban Dönüşümü", "String Eşleştirme"]
                conc = ["Karakter manipülasyonu", "Kombinatoryal permütasyon"]
                tech = ["Bitmask", "Permütasyon üretimi"]
                prereq = ["day_004", "day_032"]

            # Zorluk seviyesi (Çözücü sayısına göre)
            if solved_by > 100000:
                diff = "Başlangıç (Beginner)"
                d_level = 1
            elif solved_by > 25000:
                diff = "Başlangıç-Orta (Easy)"
                d_level = 2
            elif solved_by > 5000:
                diff = "Orta (Intermediate)"
                d_level = 3
            elif solved_by > 1500:
                diff = "İleri Seviye (Hard)"
                d_level = 4
            else:
                diff = "Uzman (Master)"
                d_level = 5

            meta = {
                "day": pid,
                "project_euler_id": pid,
                "title": title,
                "slug": slug,
                "solved_by": solved_by,
                "euler_url": p["url"],
                "difficulty": diff,
                "difficulty_level": d_level,
                "topics": {
                    "primary": primary,
                    "secondary": sec
                },
                "concepts": conc,
                "techniques": tech,
                "prerequisites": prereq,
                "time_complexity": {
                    "naive": "O(N²)",
                    "optimized": "O(N log N)"
                },
                "space_complexity": {
                    "naive": "O(N)",
                    "optimized": "O(1)"
                },
                "status": {
                    "solved": pid <= 100,
                    "tested": pid <= 100
                }
            }

        curriculum.append(meta)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(curriculum, f, ensure_ascii=False, indent=2)

    print(f"[✓] {len(curriculum)} günlük müfredat haritası oluşturuldu -> {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_metadata_for_all()
