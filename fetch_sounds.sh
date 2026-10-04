#!/data/data/com.termux/files/usr/bin/env bash
PROJECT="$(cd "$(dirname "$0")" && pwd)"
DIR="$PROJECT/sounds"
UA="Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36"

download_from_pixabay() {
    local animal="$1"
    local query="$2"
    local url="https://pixabay.com/sound-effects/search/${query}/"
    
    echo "=== Fetching: $animal ==="
    
    local page=$(curl -sL -H "User-Agent: $UA" "$url" 2>/dev/null)
    
    local sound_path=$(echo "$page" | grep -oP '/sound-effects/[^"]*-\d+/' | head -1)
    
    if [ -z "$sound_path" ]; then
        echo "  FAILED: No sound effect page found"
        return 1
    fi
    
    local detail_page=$(curl -sL -H "User-Agent: $UA" "https://pixabay.com${sound_path}" 2>/dev/null)
    
    local cdn_url=$(echo "$detail_page" | grep -oP 'https://cdn\.pixabay\.com/download/audio/[^"?]+' | head -1)
    
    if [ -z "$cdn_url" ]; then
        echo "  FAILED: No CDN URL found on detail page"
        return 1
    fi
    
    echo "  Downloading: $cdn_url"

    local tmp="$DIR/${animal}.mp3.part"
    mkdir -p "$DIR"

    curl -sL -H "User-Agent: $UA" -H "Referer: https://pixabay.com/" -o "$tmp" "$cdn_url"

    local size=$(stat -c%s "$tmp" 2>/dev/null || echo 0)

    if [ "$size" -lt 1000 ]; then
        echo "  FAILED: File too small ($size bytes)"
        rm -f "$tmp"
        return 1
    fi

    # Only replace an existing sound once the new one is known to be valid
    mv "$tmp" "$DIR/${animal}.mp3"

    echo "  SUCCESS: ${animal}.mp3 ($size bytes)"
    return 0
}

# NOTE: existing sounds are never deleted up front. Each animal is downloaded to
# a .part file and only moved into place once it has been validated, so a failed
# fetch cannot destroy sounds that were already downloaded successfully.

download_from_pixabay "cat" "cat%20meow"
download_from_pixabay "dog" "dog%20bark"
download_from_pixabay "cow" "cow%20moo"
download_from_pixabay "pig" "pig%20oink"
download_from_pixabay "chicken" "chicken%20cluck"
download_from_pixabay "bird" "bird%20chirp"
download_from_pixabay "frog" "frog%20croak"
download_from_pixabay "lion" "lion%20roar"
download_from_pixabay "monkey" "monkey"
download_from_pixabay "sheep" "sheep%20baa"
download_from_pixabay "horse" "horse%20neigh"
download_from_pixabay "rabbit" "rabbit"
download_from_pixabay "elephant" "elephant%20trumpet"

echo ""
echo "=== RESULTS ==="
ls -lhS "$DIR"/*.mp3 2>/dev/null
