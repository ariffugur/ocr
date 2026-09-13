import sqlite3

from config import DATABASE_PATH


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_urunler():
    """
    Veritabanindaki tum 'sorgu' degerlerini kucuk harfe cevirip
    kume (set) olarak dondurur. Android tarafindaki whitelist mantiginin
    aynisi: OCR'dan cikan metinler sadece bu listeyle karsilastirilacak.
    """
    conn = get_connection()
    cur = conn.execute("SELECT DISTINCT sorgu FROM VeriSetii")
    urunler = set()
    for row in cur.fetchall():
        sorgu = row["sorgu"]
        if sorgu:
            urunler.add(sorgu.strip().lower())
    conn.close()
    return urunler


def get_product(sorgu):
    """
    Verilen 'sorgu' degerine (kucuk harfe cevrilmis urun anahtar kelimesi)
    karsilik gelen tek satiri dondurur. Bulunamazsa None doner.
    """
    conn = get_connection()
    cur = conn.execute(
        "SELECT urunAdi, kalori, protein, veg, gluten, gramaj, sorgu "
        "FROM VeriSetii WHERE sorgu = ? LIMIT 1",
        (sorgu.strip().lower(),),
    )
    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)
