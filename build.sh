#!/bin/bash
set -e

PROJECT="/data/data/com.termux/files/home/animal-game"
ANDROID_JAR="$PROJECT/stubs/android.jar"
BUILD="$PROJECT/build"
JAVA_SRC="$PROJECT/java"
RES_SRC="$PROJECT/res"
ASSETS_SRC="$PROJECT/assets"
MANIFEST="$PROJECT/AndroidManifest.xml"
OUTPUT="$PROJECT/build/animal.apk"
KEYSTORE="$PROJECT/animal.keystore"

echo "=== Cleaning build ==="
rm -rf "$BUILD"/compiled_res "$BUILD"/gen "$BUILD"/classes "$BUILD"/base.apk "$OUTPUT" 2>/dev/null || true
mkdir -p "$BUILD"/{compiled_res,gen,classes}

echo "=== Step 1: Compile resources with aapt2 ==="
find "$RES_SRC" -type f \( -name "*.xml" -o -name "*.png" -o -name "*.jpg" \) | while read f; do
    echo "  Compiling: $(basename $f)"
    aapt2 compile "$f" -o "$BUILD/compiled_res/" 2>&1 || {
        echo "  WARNING: Failed to compile $f, skipping"
    }
done

echo "=== Step 2: Link resources ==="
FLAT_FILES=$(find "$BUILD/compiled_res" -name "*.flat" | tr '\n' ' ')
aapt2 link \
    -o "$BUILD/base.apk" \
    -I "$ANDROID_JAR" \
    --manifest "$MANIFEST" \
    --java "$BUILD/gen" \
    --auto-add-overlay \
    $FLAT_FILES

echo "=== Step 3: Compile Java ==="
GEN_SRC=$(find "$BUILD/gen" -name "*.java" 2>/dev/null)
ALL_JAVA=$(find "$JAVA_SRC" -name "*.java")
ALL_SOURCES="$GEN_SRC $ALL_JAVA"

echo "  Source files:"
echo "$ALL_SOURCES" | tr ' ' '\n' | while read f; do [ -n "$f" ] && echo "    $f"; done

javac \
    -source 11 -target 11 \
    -classpath "$ANDROID_JAR" \
    -d "$BUILD/classes" \
    $ALL_SOURCES

echo "=== Step 4: Convert to DEX ==="
find "$BUILD/classes" -name "*.class" > "$BUILD/classfiles.txt"
d8 \
    --output "$BUILD" \
    --lib "$ANDROID_JAR" \
    --min-api 24 \
    $(cat "$BUILD/classfiles.txt")

echo "=== Step 5: Build final APK ==="
cp "$BUILD/base.apk" "$BUILD/animal-unsigned.apk"
# Add DEX to APK
cd "$BUILD"
zip -j animal-unsigned.apk classes.dex
# Add assets (game.html + sounds) without directory entries
cd "$PROJECT"
zip -r -D "$BUILD/animal-unsigned.apk" assets

echo "=== Step 6: Align APK ==="
python3 "$PROJECT/zipalign.py" "$BUILD/animal-unsigned.apk" "$BUILD/animal-aligned.apk"

echo "=== Step 7: Generate keystore ==="
if [ ! -f "$KEYSTORE" ]; then
    keytool -genkeypair \
        -v \
        -keystore "$KEYSTORE" \
        -keyalg RSA \
        -keysize 2048 \
        -validity 10000 \
        -alias animal \
        -storepass android \
        -keypass android \
        -dname "CN=Animal Game, OU=Personal, O=Open Source, L=Home, ST=Local, C=US"
else
    echo "  Using existing keystore"
fi

echo "=== Step 8: Sign APK (V1+V2+V3) ==="
apksigner sign \
    --ks "$KEYSTORE" \
    --ks-key-alias animal \
    --ks-pass pass:android \
    --key-pass pass:android \
    --v1-signing-enabled true \
    --v2-signing-enabled true \
    --v3-signing-enabled true \
    --out "$OUTPUT" \
    "$BUILD/animal-aligned.apk"

echo "=== Step 9: Verify signing ==="
apksigner verify --print-certs "$OUTPUT"

echo ""
echo "=== BUILD SUCCESS ==="
ls -lh "$OUTPUT"
echo "APK: $OUTPUT"
