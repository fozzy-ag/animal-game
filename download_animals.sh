#!/bin/bash
# Download animal sounds from wavsource.com
SOUND_DIR="/data/data/com.termux/files/home/animal-game/sounds"

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
    curl -L -o "$SOUND_DIR/wav/$file" "$url" 2>/dev/null
    
    # Check if download succeeded
    if [ -f "$SOUND_DIR/wav/$file" ]; then
        size=$(stat -c%s "$SOUND_DIR/wav/$file" 2>/dev/null || echo "0")
        echo "  Downloaded $file: $size bytes"
    else
        echo "  Failed to download $file"
    fi
done

echo ""
echo "Download complete. Files in $SOUND_DIR/wav/"
ls -la "$SOUND_DIR/wav/"
