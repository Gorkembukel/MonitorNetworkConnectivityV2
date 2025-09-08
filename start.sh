#!/bin/bash

run_app() {
    sudo .venv/bin/python -m test.TEST
}

# İlk deneme
output=$(run_app 2>&1)
echo "$output"

# Eğer hata mesajı çıktıysa bağımlılıkları yükle ve tekrar çalıştır
if echo "$output" | grep -q 'qt.qpa.plugin: Could not load the Qt platform plugin "xcb"'; then
    echo "❌ Qt 'xcb' hatası tespit edildi. Gerekli paketler yükleniyor..."
    sudo apt update
    sudo apt install --reinstall -y libxcb-xinerama0
    sudo apt install -y libxcb-xinerama0 libxcb-xinerama0-dev
    sudo apt install -y libxcb1 libxcb1-dev
    sudo apt install -y libxkbcommon-x11-0
    echo "✅ Kurulum tamamlandı. Uygulama tekrar başlatılıyor..."
    
    # Tekrar çalıştır
    run_app
fi

