"""
mufredat_uretici.py
998 Günlük Project Euler Müfredat Üreticisi.
day_XXX/ klasörlerini, src/ alt klasörlerini ve 20 bölümlü
day_XXX_problem_XXX_slug.ipynb notebook'larını oluşturur.
"""

import inspect
import json
import os
import shutil
import sys
import time
from pathlib import Path
import importlib.util

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Generator dizinini import yoluna ekle
sys.path.insert(0, str(Path(__file__).parent))
from sablon_hucreler import uret_20_bolum_hucreleri

# ── Sabitler ─────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
HARITA_DOSYA = ROOT_DIR / "mufredat_haritasi.json"
SORULAR_DOSYA = ROOT_DIR / "sorular.json"
COZUMLER_DOSYA = ROOT_DIR / "cozumler.py"

# Problem ID -> Harici veri dosyası eşlemesi
VERI_DOSYALARI = {
    22: "p022_names.txt",
    42: "p042_words.txt",
    54: "p054_poker.txt",
    59: "p059_cipher.txt",
    67: "p067_triangle.txt",
    79: "p079_keylog.txt",
    81: "p081_matrix.txt",
    82: "p082_matrix.txt",
    83: "p083_matrix.txt",
    89: "p089_roman.txt",
    96: "p096_sudoku.txt",
    98: "p098_words.txt",
    99: "p099_base_exp.txt",
    102: "p102_triangles.txt",
    105: "p105_sets.txt",
    107: "p107_network.txt"
}

_MODUL = None


def modul_yukle():
    """cozumler.py modülünü tek sefer yükler."""
    global _MODUL
    if _MODUL is None and COZUMLER_DOSYA.exists():
        spec = importlib.util.spec_from_file_location("cozumler", COZUMLER_DOSYA)
        _MODUL = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_MODUL)
    return _MODUL


def cozum_al(pid: int):
    """cozumler.py'den ilgili fonksiyonu ve kaynak kodunu döndürür."""
    modul = modul_yukle()
    if not modul:
        return None, f"def coz_{pid:04d}():\n    return None\n"
    
    fonk = getattr(modul, f"coz_{pid:04d}", None)
    if fonk:
        try:
            kaynak = inspect.getsource(fonk)
        except Exception:
            kaynak = f"def coz_{pid:04d}():\n    return None\n"
        return fonk, kaynak
    
    return None, f"def coz_{pid:04d}():\n    # Problem {pid}: Çözüm henüz eklenmedi\n    return None\n"


def day_uret(meta: dict, sorular: dict, hedef_kok: Path = ROOT_DIR) -> bool:
    """Tek bir gün için klasör, src/ ve notebook üretir."""
    pid = meta["project_euler_id"]
    day = meta["day"]
    slug = meta["slug"]

    day_dir = hedef_kok / f"day_{day:03d}"
    src_dir = day_dir / "src"
    day_dir.mkdir(exist_ok=True, parents=True)
    src_dir.mkdir(exist_ok=True)

    # İlgili harici veri dosyası varsa hem src/ içine hem de day_dir içine kopyala
    veri_adi = VERI_DOSYALARI.get(pid)
    if veri_adi:
        ana_veri_yolu = ROOT_DIR / veri_adi
        if ana_veri_yolu.exists():
            shutil.copy(ana_veri_yolu, src_dir / veri_adi)
            shutil.copy(ana_veri_yolu, day_dir / veri_adi)

    # Çözüm ve kaynak kod
    fonk, kaynak_kod = cozum_al(pid)
    cevap = None
    sure_ms = 0.0

    if fonk:
        try:
            t0 = time.perf_counter()
            cevap = fonk()
            sure_ms = (time.perf_counter() - t0) * 1000
        except Exception as e:
            cevap = f"Hata: {e}"

    soru_metni = sorular.get(str(pid), sorular.get(pid, ""))

    # 20 bölüm hücrelerini üret
    hucreler = uret_20_bolum_hucreleri(
        meta=meta,
        soru_metni_ham=soru_metni,
        kaynak_kod=kaynak_kod,
        cevap=cevap,
        sure_ms=sure_ms
    )

    notebook_adi = f"day_{day:03d}_problem_{pid:03d}_{slug}.ipynb"
    notebook_yolu = day_dir / notebook_adi

    nb_json = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            },
            "curriculum": meta
        },
        "cells": hucreler
    }

    try:
        with open(notebook_yolu, "w", encoding="utf-8") as f:
            json.dump(nb_json, f, ensure_ascii=False, indent=1)
        return True
    except Exception as e:
        print(f"[!] Day {day:03d} yazılamadı: {e}", file=sys.stderr)
        return False


def main():
    if not HARITA_DOSYA.exists():
        print("[!] mufredat_haritasi.json bulunamadı!", file=sys.stderr)
        sys.exit(1)

    with open(HARITA_DOSYA, "r", encoding="utf-8") as f:
        harita = json.load(f)

    sorular = {}
    if SORULAR_DOSYA.exists():
        with open(SORULAR_DOSYA, "r", encoding="utf-8") as f:
            sorular = json.load(f)

    # Argüman kontrolü
    if len(sys.argv) == 3:
        p_min = int(sys.argv[1])
        p_max = int(sys.argv[2])
        secilenler = [m for m in harita if p_min <= m["day"] <= p_max]
        print(f"[*] Belirtilen Gün Aralığı: Gün {p_min:03d} – Gün {p_max:03d} ({len(secilenler)} gün)")
    elif len(sys.argv) == 2:
        arg = sys.argv[1].lower()
        if arg == "all":
            secilenler = harita
            print(f"[*] Tüm 998 Gün Üretilecek...")
        else:
            hedef = int(arg)
            secilenler = [m for m in harita if m["day"] == hedef]
            print(f"[*] Tek Hedef Gün: Gün {hedef:03d}")
    else:
        # Varsayılan: P1 - P100
        secilenler = [m for m in harita if m["day"] <= 100]
        print(f"[*] Varsayılan: Gün 001 – Gün 100 ({len(secilenler)} gün üretiliyor...)")

    print("-" * 65)

    basarili = 0
    toplam = len(secilenler)
    t_baslangic = time.perf_counter()

    for i, meta in enumerate(secilenler, 1):
        day = meta["day"]
        pid = meta["project_euler_id"]
        slug = meta["slug"]
        
        ok = day_uret(meta, sorular)
        if ok:
            basarili += 1
        durum = "✅" if ok else "❌"
        
        if toplam <= 100 or i % 50 == 0 or i <= 5:
            print(f"  [{i:>3}/{toplam:>3}] Day {day:03d} (Euler #{pid:03d}) {durum} day_{day:03d}_problem_{pid:03d}_{slug}.ipynb")

    toplam_sure = time.perf_counter() - t_baslangic
    print("-" * 65)
    print(f"\n[✓] Müfredat Tamamlandı! {basarili}/{toplam} gün oluşturuldu. (Süre: {toplam_sure:.2f} sn)")


if __name__ == "__main__":
    main()
