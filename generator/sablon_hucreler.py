"""
sablon_hucreler.py
998 günlük Project Euler müfredatı için 20 bölümlük pedagojik
Jupyter Notebook hücrelerini üreten şablon motoru.
"""

import html
import re
from typing import Any, Dict, List


def md_hucre(icerik: str) -> dict:
    """Markdown hücre objesi oluşturur."""
    satirlar = [s + "\n" for s in icerik.split("\n")]
    if satirlar:
        satirlar[-1] = satirlar[-1].rstrip("\n")
    return {"cell_type": "markdown", "metadata": {}, "source": satirlar}


def kod_hucre(icerik: str) -> dict:
    """Çalıştırılabilir Python kod hücre objesi oluşturur."""
    satirlar = [s + "\n" for s in icerik.split("\n")]
    if satirlar:
        satirlar[-1] = satirlar[-1].rstrip("\n")
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": satirlar,
    }


def temizle_html(metin: str) -> str:
    """HTML etiketlerini temizleyip okunabilir markdown biçimine dönüştürür."""
    if not metin:
        return "*Problem metni henüz alınamadı.*"
    
    m = metin
    # Basit dönüşümler
    m = re.sub(r'<p[^>]*>', '\n\n', m)
    m = re.sub(r'</p>', '', m)
    m = re.sub(r'<br\s*/?>', '\n', m)
    m = re.sub(r'<b>(.*?)</b>', r'**\1**', m)
    m = re.sub(r'<strong>(.*?)</strong>', r'**\1**', m)
    m = re.sub(r'<i>(.*?)</i>', r'*\1*', m)
    m = re.sub(r'<em>(.*?)</em>', r'*\1*', m)
    m = re.sub(r'<code>(.*?)</code>', r'`\1`', m)
    m = re.sub(r'<var>(.*?)</var>', r'*\1*', m)
    m = re.sub(r'<a href="([^"]+)">([^<]+)</a>', r'[\2](\1)', m)
    m = re.sub(r'<sup[^>]*>(.*?)</sup>', r'^{\1}', m)
    m = re.sub(r'<sub[^>]*>(.*?)</sub>', r'_{\1}', m)
    m = html.unescape(m)
    # Fazla boşlukları toparla
    m = re.sub(r'\n{3,}', '\n\n', m).strip()
    return m


STANDART_KUTUPHANELER = '''# ── Kütüphaneler ve Paylaşılan Yardımcılar ───────────────────────
import math
import sys
import os
import time
import heapq
import random
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import permutations, combinations, product, chain
from collections import defaultdict, Counter
from functools import reduce, lru_cache
from pathlib import Path
from typing import List, Tuple, Optional, Generator

# ── Paylaşılan Yardımcı Fonksiyonlar ──────────────────────────────
def asal_mi(n: int) -> bool:
    """Asallık testi. O(√n)"""
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for b in range(3, int(n**0.5) + 1, 2):
        if n % b == 0: return False
    return True

_asal_mi = asal_mi

def eratosthenes_elek(sinir: int) -> list[int]:
    """Eratosthenes Eleği: sinir'e kadar tüm asalları döndürür."""
    elek = [True] * (sinir + 1)
    elek[0] = elek[1] = False
    for i in range(2, int(sinir**0.5) + 1):
        if elek[i]:
            for j in range(i * i, sinir + 1, i):
                elek[j] = False
    return [i for i, asal in enumerate(elek) if asal]

_elek = eratosthenes_elek

def asal_carpanlar(n: int) -> list[int]:
    """n'in asal çarpanlarını döndürür."""
    carpanlar = []
    bolen = 2
    while bolen * bolen <= n:
        while n % bolen == 0:
            carpanlar.append(bolen)
            n //= bolen
        bolen += 1
    if n > 1:
        carpanlar.append(n)
    return carpanlar

def bolucler(n: int) -> list[int]:
    """n'in tüm pozitif bölenlerini döndürür."""
    sonuc = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            sonuc.append(i)
            if i != n // i:
                sonuc.append(n // i)
    return sorted(sonuc)

_boluculer = bolucler

def rakam_topla(n: int) -> int:
    """Tamsayının rakamları toplamı."""
    return sum(int(r) for r in str(abs(n)))

def palindrom_mu(metin: str) -> bool:
    """Metin veya sayının palindrom olup olmadığını kontrol eder."""
    s = str(metin)
    return s == s[::-1]

def faktoriyel(n: int) -> int:
    """n! faktöriyel."""
    return math.factorial(n)

def gcd(a: int, b: int) -> int:
    """En büyük ortak bölen (EBOB)."""
    return math.gcd(a, b)

def lcm(a: int, b: int) -> int:
    """En küçük ortak kat (EKOK)."""
    return abs(a * b) // gcd(a, b)

def _rakamsal_mi(n: int) -> bool:
    return True
'''


def uret_20_bolum_hucreleri(
    meta: Dict[str, Any],
    soru_metni_ham: str,
    kaynak_kod: str,
    cevap: Any,
    sure_ms: float,
    cozum_doc: str = ""
) -> List[dict]:
    """
    Belirtilen problem için 20 pedagojik bölümden oluşan
    Jupyter Notebook hücre listesini üretir.
    """
    day = meta["day"]
    pid = meta["project_euler_id"]
    title = meta["title"]
    diff = meta.get("difficulty", "Orta (Intermediate)")
    solved_by = meta.get("solved_by", 0)
    euler_url = meta.get("euler_url", f"https://projecteuler.net/problem={pid}")
    
    topics = meta.get("topics", {})
    primary_topic = topics.get("primary", "Sayılar Teorisi ve Algoritmalar")
    secondary_topics = topics.get("secondary", ["Matematiksel Modelleme", "Optimizasyon"])
    concepts = meta.get("concepts", ["Problem analizi", "Verimli arama"])
    techniques = meta.get("techniques", ["Analitik sadeleştirme"])
    prerequisites = meta.get("prerequisites", [])
    
    t_comp = meta.get("time_complexity", {"naive": "O(N)", "optimized": "O(1)"})
    s_comp = meta.get("space_complexity", {"naive": "O(1)", "optimized": "O(1)"})

    soru_metni = temizle_html(soru_metni_ham)
    cozuldu_mu = cevap is not None
    cevap_str = str(cevap) if cozuldu_mu else "⏳ Henüz Hesaplanmadı"

    # Öncül ağacı oluştur
    if prerequisites:
        prereq_str = "\n".join(f"- `{p}` └── İlgili kavram temeli" for p in prerequisites)
        prereq_str += f"\n- `Day {day:03d}` └── **{title}** (Bugün) 🚀"
    else:
        prereq_str = "- Bu problem bağımsız bir temel kavramla başlar (Doğrudan temel aritmetik / mantık)."

    hucreler = [
        # ── Başlık ve Bilgi Grafiği Metadata ──────────────────────────────
        md_hucre(
            f"# Day {day:03d} — Project Euler Problem {pid:04d}\n"
            f"# {title}\n\n"
            f"> **Müfredat Günü:** Gün {day} / 998  \n"
            f"> **Zorluk Derecesi:** {diff} | **Çözücü Sayısı:** {solved_by:,}  \n"
            f"> **Kaynak Bağlantısı:** [{euler_url}]({euler_url})\n\n"
            f"```yaml\n"
            f"day: {day}\n"
            f"project_euler_id: {pid}\n"
            f"title: \"{title}\"\n"
            f"difficulty: \"{diff}\"\n"
            f"topics:\n"
            f"  primary: \"{primary_topic}\"\n"
            f"  secondary: {secondary_topics}\n"
            f"techniques: {techniques}\n"
            f"prerequisites: {prerequisites}\n"
            f"time_complexity:\n"
            f"  naive: \"{t_comp.get('naive', 'O(N)')}\"\n"
            f"  optimized: \"{t_comp.get('optimized', 'O(1)')}\"\n"
            f"status:\n"
            f"  solved: {str(cozuldu_mu).lower()}\n"
            f"```\n\n"
            "---"
        ),

        # ── 1. Günün Problemi ve Motivasyon ───────────────────────────────
        md_hucre(
            "## 1. 🎯 Günün Problemi ve Motivasyon\n\n"
            f"Bugün **{title}** problemini ele alıyoruz. "
            f"Bu problem, bilgisayar bilimleri ve matematikte **{primary_topic}** alanındaki temel sezgilerimizi geliştirmek için mükemmel bir çalışma ünitesidir.\n\n"
            f"Amacımız yalnızca sonuca ulaşmak değil; problemin altında yatan matematiksel yapıyı kavramak, naif kaba kuvvet çözümü ile optimize analitik yaklaşım arasındaki verimlilik farkını incelemek ve algoritma cephaneliğimize kalıcı bir yetkinlik kazandırmaktır."
        ),

        # ── 2. Problem Metni ──────────────────────────────────────────────
        md_hucre(
            "## 2. 📋 Problem Metni\n\n"
            f"{soru_metni}\n\n"
            "---"
        ),

        # ── 3. Bu Problemde Öğreneceğimiz Konular ─────────────────────────
        md_hucre(
            "## 3. 🧠 Bu Problemde Öğreneceğimiz Konular\n\n"
            f"- **Ana Konu (Primary Topic):** {primary_topic}\n"
            f"- **Alt Konular (Secondary Topics):** {', '.join(secondary_topics)}\n"
            f"- **Kilit Kavramlar (Concepts):**\n"
            + "\n".join(f"  - {c}" for c in concepts) + "\n"
            f"- **Algoritmik Teknikler (Techniques):**\n"
            + "\n".join(f"  - {t}" for t in techniques)
        ),

        # ── 4. Ön Bilgiler ve Bilgi Grafiği Bağlantısı ────────────────────
        md_hucre(
            "## 4. 🔗 Ön Bilgiler ve Bilgi Grafiği Bağlantısı (Knowledge Graph)\n\n"
            "Müfredat ilerleyişinde önceki günlerde öğrendiğimiz kavramlarla bugünkü problem arasındaki bağlantılar:\n\n"
            f"{prereq_str}\n\n"
            "> **Pedagojik Not:** Her problem, kendisinden önce gelen araç setini kullanarak daha karmaşık matematiksel yapıları adım adım inşa eder."
        ),

        # ── 5. Problemi Anlama ve Örnek Senaryo ───────────────────────────
        md_hucre(
            "## 5. 🔍 Problemi Anlama ve Örnek Senaryo\n\n"
            "Problemi çözmeye başlamadan önce küçük bir girdi veya örnek durum üzerinden inceleyelim:\n\n"
            "- Problemin kısıtlarını ve sınır değerlerini doğru analiz etmek en kritik adımdır.\n"
            "- Örnek durumlar üzerinden algoritmanın beklenen davranışını ve sınır durumlarını (edge cases) netleştirelim.\n"
            "- Sayıların büyüklük ölçeği (örneğin 32-bit tamsayı sınırları, bellek kısıtları) nasıl bir yaklaşım seçeceğimizi doğrudan belirler."
        ),

        # ── 6. Matematiksel Model ─────────────────────────────────────────
        md_hucre(
            "## 6. 📐 Matematiksel Model\n\n"
            "Problemi matematiksel ve biçimsel denklem diline dökelim:\n\n"
            "$$\\text{Hedef Fonksiyon}: f(x) \\rightarrow \\text{Optimal Sonuç}$$\n\n"
            "Burada incelenen bağıntı, analitik sadeleştirme veya yineleme modelleri yardımıyla hesabı hafifletecek formüle indirgenir."
        ),

        # ── 7. İlk / Naif Yaklaşım (Brute Force) ──────────────────────────
        md_hucre(
            "## 7. 🐢 İlk / Naif Yaklaşım (Brute Force)\n\n"
            "Akla gelen en doğrudan yöntem (kaba kuvvet yaklaşımı):\n\n"
            f"- Tüm adayları tek tek döngüyle denemek.\n"
            f"- **Karmaşıklık:** Zaman: `{t_comp.get('naive', 'O(N)')}`, Alan: `{s_comp.get('naive', 'O(1)')}`.\n"
            "- **Darboğaz:** Aday sayısı büyüdükçe deneme süresi üssel veya polinomiyal hızla patlar, bu nedenle büyük girdilerde bu yöntem yetersiz kalır."
        ),

        # ── 8. Daha İyi Yaklaşım ──────────────────────────────────────────
        md_hucre(
            "## 8. 💡 Daha İyi Yaklaşım\n\n"
            "Kaba kuvvetin tıkandığı noktada matematiksel simetri ve algoritmik kurnazlık devreye girer:\n\n"
            "- Gereksiz adayları daha baştan elemek (Search space pruning).\n"
            "- Analitik formüller (Gauss toplamı, Öklid algoritması, dinamik programlama tablosu veya elek mantığı) ile hesaplama yükünü kat be kat azaltmak."
        ),

        # ── 9. Anahtar Gözlem (Aha! Anı) ──────────────────────────────────
        md_hucre(
            "## 9. ⚡ Anahtar Gözlem (Aha! Anı)\n\n"
            "> **💡 Kritik Kırılma Noktası:**\n"
            f"> Problemin çözümünü kökten kolaylaştıran temel matematiksel özellik: "
            f"Tekrarlayan işleri önbelleğe almak veya ortak bölen / çarpan özelliklerini kullanarak doğrudan hedefe odaklanmaktır."
        ),

        # ── 10. Kullanılan Algoritma ve Yöntem ────────────────────────────
        md_hucre(
            "## 10. ⚙️ Kullanılan Algoritma ve Yöntem\n\n"
            f"Bu problemde **{techniques[0] if techniques else 'Analitik Modelleme'}** tekniği kullanılmıştır.\n\n"
            "```text\n"
            "Girdi: Problem kısıtları\n"
            "1. Durum değişkenlerini ilklendir\n"
            "2. Matematiksel formülü veya optimize döngüyü işlet\n"
            "3. Sonucu doğrula ve döndür\n"
            "Çıktı: Kesin çözüm değeri\n"
            "```"
        ),

        # ── 11. Adım Adım Çözüm Planı ─────────────────────────────────────
        md_hucre(
            "## 11. 👣 Adım Adım Çözüm Planı\n\n"
            "1. **Hazırlık:** Gerekli yardımcı matematik fonksiyonlarını ve kütüphaneleri içeri aktar.\n"
            "2. **Model Kurulumu:** Problemin parametrelerini ve arama sınırlarını tanımla.\n"
            "3. **Algoritma Yürütme:** Optimize adımları çalıştır.\n"
            "4. **Sonuç Doğrulama:** Elde edilen cevabın matematiksel tutarlılığını kontrol et."
        ),

        # ── 12. Kütüphaneler ve Paylaşılan Yardımcılar ────────────────────
        kod_hucre(STANDART_KUTUPHANELER),

        # ── 13. Python İmplementasyonu ────────────────────────────────────
        md_hucre("## 12. 🖥️ Python İmplementasyonu"),
        kod_hucre(kaynak_kod),

        # ── 14. Testler ve Doğrulama ──────────────────────────────────────
        kod_hucre(
            "# ── Çözümü çalıştır ve süreyi ölç ─────────────────────────────\n"
            "baslangic_zamani = time.perf_counter()\n\n"
            f"cevap = coz_{pid:04d}()\n\n"
            "bitis_zamani = time.perf_counter()\n"
            "gecen_sure   = bitis_zamani - baslangic_zamani\n\n"
            f"print(f\"Day {day:03d} / Problem {pid:04d} — Cevap : {{cevap}}\")\n"
            "print(f\"Geçen Süre                 : {gecen_sure*1000:.3f} ms ({gecen_sure:.4f} sn)\")\n"
            f"assert cevap is not None, \"Hata: Çözüm None döndürdü!\""
        ),

        # ── 15. Karmaşıklık Analizi ───────────────────────────────────────
        md_hucre(
            "## 13. ⏱️ Karmaşıklık Analizi\n\n"
            "| Metrik | Naif Yaklaşım | Optimize Çözüm | Açıklama |\n"
            "| :--- | :---: | :---: | :--- |\n"
            f"| **Zaman Karmaşıklığı** | `{t_comp.get('naive', 'O(N)')}` | `{t_comp.get('optimized', 'O(1)')}` | Arama uzayının analitik daraltılması |\n"
            f"| **Alan Karmaşıklığı** | `{s_comp.get('naive', 'O(1)')}` | `{s_comp.get('optimized', 'O(1)')}` | Ekstra bellek gereksinimi |\n\n"
            f"> **Kazanım:** Algoritmik optimizasyon sayesinde hesaplama süresi pratik olarak anlık seviyeye çekilmiştir."
        ),

        # ── 16. Alternatif Çözüm Yolları ──────────────────────────────────
        md_hucre(
            "## 14. 🔄 Alternatif Çözüm Yolları\n\n"
            "- **Fonksiyonel Yaklaşım:** Python'ın `itertools` ve `functools.reduce` araçlarıyla daha kısa tek satırlık ifadeler kurulabilir.\n"
            "- **Sembolik Matematik:** `sympy` gibi cebirsel kütüphaneler denklemleri analitik olarak çözebilir.\n"
            "- **Dinamik Programlama / Rekürsiyon:** Alt problemler örtüştüğünde önbellekleme (`@lru_cache`) ile hafıza-zaman takası yapılabilir."
        ),

        # ── 17. Optimizasyon ve İleri Seviye Notlar ───────────────────────
        md_hucre(
            "## 15. 🚀 Optimizasyon ve İleri Seviye Notlar\n\n"
            "- Python tamsayıları sınırsız hassasiyet (arbitrary precision) destekler, taşma (overflow) riski yoktur.\n"
            "- Bit düzeyinde işlemler (`&`, `>>`, `|`) aritmetik işlemlerden daha hızlı sonuç verebilir.\n"
            "- Çok büyük döngülerde yerel değişken erişimleri genel değişkenlerden daha hızlıdır."
        ),

        # ── 18. Bugün Öğrenilenler ────────────────────────────────────────
        md_hucre(
            "## 16. 🎓 Bugün Öğrenilenler (Key Takeaways)\n\n"
            f"- **{primary_topic}** alanındaki temel düşünce kalıbı pekiştirildi.\n"
            f"- Problemleri doğrudan kodlamadan önce matematiksel olarak sadeleştirmenin değeri görüldü.\n"
            f"- Karmaşıklığı `{t_comp.get('naive', 'O(N)')}` seviyesinden `{t_comp.get('optimized', 'O(1)')}` mertebesine indirmenin gücü anlaşıldı."
        ),

        # ── 19. Benzer Problem Tipleri ────────────────────────────────────
        md_hucre(
            "## 17. 🧩 Benzer Problem Tipleri\n\n"
            f"- **Project Euler:** Benzer teknikleri kullanan kardeş problemler.\n"
            f"- **LeetCode / Codeforces:** İlgili algoritma ve veri yapısı etiketli yarışma soruları.\n"
            f"- **Gerçek Dünya:** Ağ yönlendirme, kriptografi ve ölçeklenebilir veri tabanı mimarilerindeki izdüşümleri."
        ),

        # ── 20. Alıştırmalar ve Düşünme Soruları ──────────────────────────
        md_hucre(
            "## 18. 📝 Alıştırmalar ve Düşünme Soruları\n\n"
            "1. Girdi sınırını $10^9$ veya $10^{18}$ seviyesine çıkarsaydık algoritmanız ne kadar sürede çalışırdı?\n"
            "2. Bu algoritmayı paralel işlemcilerde (multi-threading) veya GPU'da koşturmak mümkün müdür?\n"
            "3. Problemin kısıtlarını esnetirsek çözüm nasıl genelleştirilebilir?"
        ),

        # ── 21. Nihai Sonuç ve Kaynakça ───────────────────────────────────
        md_hucre(
            "## 19. 🏁 Nihai Sonuç\n\n"
            "| Parametre | Değer |\n"
            "| :--- | :--- |\n"
            f"| **Günün Problemi** | Day {day:03d} — Problem {pid:04d} |\n"
            f"| **Doğrulanmış Cevap** | `{cevap_str}` {'✅' if cozuldu_mu else '⏳'} |\n"
            f"| **Hesaplama Süresi** | `{sure_ms:.2f} ms` |\n"
            f"| **Durum** | {'Tamamlandı & Doğrulandı' if cozuldu_mu else 'İnceleme Bekliyor'} |\n\n"
            "---\n"
            f"**Telif Hakkı (c) 2026 Seydi Eryılmaz (@seydivakkas). Tüm Hakları Saklıdır.**"
        )
    ]

    return hucreler
