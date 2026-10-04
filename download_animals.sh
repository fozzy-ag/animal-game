#!/data/data/com.termux/files/usr/bin/env bash
# Download animal sounds from wavsource.com
PROJECT="$(cd "$(dirname "$0")" && pwd)"
SOUND_DIR="$PROJECT/sounds"

# Create temporary directory for WAV files
mkdir -p "$SOUND_DIR/wav"

# Download each animal sound
declare -A animals=(
    ["cat"]="cat.wav"
    ["dog"]="dog.wav"
    ["cow"]="cow.wav"
    ["pig"]="pig.wav"
    ["chicken"]="chicken.wav"
    ["bird"]="bird.wav"
    ["frog"]="frog.wav"
    ["lion"]="lion.wav"
    ["monkey"]="monkey.wav"
    ["sheep"]="sheep.wav"
    ["horse"]="horse.wav"
    ["elephant"]="elephant.wav"
)

for animal in "${!animals[@]}"; do
    file="${animals[$animal]}"
    url="https://www.wavsource.com/animals/$file"
    echo "Downloading $animal..."
    if ! curl -fsSL -o "$SOUND_DIR/wav/$file" "$url" 2>/dev/null; then
        echo "  FAILED: HTTP error fetching $file"
        rm -f "$SOUND_DIR/wav/$file"
        continue
    fi

    size=$(stat -c%s "$SOUND_DIR/wav/$file" 2>/dev/null || echo 0)
    if [ "$size" -lt 1000 ]; then
        echo "  FAILED: $file is only $size bytes - likely an error page, not audio"
        rm -f "$SOUND_DIR/wav/$file"
        continue
    fi

    echo "  Downloaded $file: $size bytes"
done

echo ""
echo "Download complete. Files in $SOUND_DIR/wav/"
ls -la "$SOUND_DIR/wav/"
