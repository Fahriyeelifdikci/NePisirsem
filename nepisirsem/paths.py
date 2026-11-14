"""Proje klasörlerinin mutlak yolları: kod nereden çalıştırılırsa çalıştırılsın doğru dosyayı bulur."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent     # nepisirsem/paths.py → proje kökü
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"