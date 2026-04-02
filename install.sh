#!/bin/sh
# سكريبت خالد الاحترافي - إصدار المسار الجذري
# هذا السكريبت يتعامل مع ملف tar.gz يحتوي على المسار الكامل بداخله

URL="https://github.com/KhaledAli65/novaler/raw/refs/heads/main/Vu_Backup_Downloader.tar.gz"
# المسار النهائي الذي سيستقر فيه البلجن بعد فك الضغط
DEST_DIR="/usr/lib/enigma2/python/Plugins/Extensions/Vu_Backup_Downloader"

echo "📥 جاري تحميل الحزمة الجذرية..."
wget --no-check-certificate $URL -O /tmp/Vu_Backup_Downloader.tar.gz

echo "📦 جاري فك الضغط إلى جذور النظام..."
# فك الضغط في الـ Root (/) لأن الملف يحتوي على المسارات بداخله
tar -xzf /tmp/Vu_Backup_Downloader.tar.gz -C /

# --- مرحلة التشفير الذكي لحماية الروابط وحل التعارض ---
if [ -f "$DEST_DIR/plugin.py" ]; then
    echo "⚙️ جاري التشفير الموضعي لضمان التوافق..."
    
    # تنفيذ التشفير باستخدام بايثون الرسيفر
    python -m py_compile "$DEST_DIR/plugin.py"
    
    # معالجة الناتج لصور بايثون 3 (مثل OpenATV 8.0)
    if [ -d "$DEST_DIR/__pycache__" ]; then
        cp $DEST_DIR/__pycache__/plugin.cpython*.pyc $DEST_DIR/plugin.pyc
        rm -rf "$DEST_DIR/__pycache__"
    fi
    
    # التأكد من وجود الملف المشفر قبل حذف المصدر (قفل الحماية)
    if [ -f "$DEST_DIR/plugin.pyc" ] || [ -f "$DEST_DIR/plugin.pyo" ]; then
        rm -f "$DEST_DIR/plugin.py"
        echo "✅ تم التشفير بنجاح وإخفاء الروابط الـ 35."
    else
        echo "⚠️ تنبيه: فشل التشفير، سيبقى الملف مفتوحاً ليعمل البلجن."
    fi
fi

# ضبط التصاريح النهائية للمجلد بالكامل
chmod -R 755 "$DEST_DIR"

echo "♻️ جاري إعادة تشغيل Enigma2..."
killall -9 enigma2

echo "✨ انتهى التنصيب بنجاح يا خالد!"
