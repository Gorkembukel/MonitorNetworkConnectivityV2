#!/bin/bash


# Sanal ortam oluştur
python3 -m venv .venv
source .venv/bin/activate

# Gereksinimleri yükle
pip install --upgrade pip
pip install -r requirements.txt

# PyInstaller yükle
pip install pyinstaller

# Executable oluştur
pyinstaller --onefile --noconsole test/TEST.py

echo "Kurulum ve derleme tamamlandı ✅"
echo "Oluşturulan dosya: dist/TEST"
