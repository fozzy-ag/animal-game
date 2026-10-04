# Credits

Provenance and licensing for the third-party assets packaged in this app.

# Audio credits

Provenance for the sound effects packaged in `assets/sounds/`.

## donkey.mp3

- **Source:** "Donkey Bray" by StarNinjas, from
  <https://opengameart.org/content/donkey-bray>
- **License:** CC0 1.0 Universal (public domain dedication)
- **Original:** `donkey_bray_-_starninjas.ogg`, 1.81 s, 44.1 kHz stereo Ogg Vorbis
- **Edits applied:** gentle compression (`acompressor`, threshold -20 dB,
  ratio 2.5, attack 5 ms, release 120 ms, knee 6 dB) to reduce the source's
  22 dB crest factor, then +6.76 dB gain to bring true peak to -1.5 dB,
  60 ms fade-out, re-encoded to 44.1 kHz mono 96 kbps MP3
  (1.81 s, 22,614 bytes, -19.6 LUFS). No trimming or time-stretching.
- **Note:** this is a human impression of a bray, not a recording of an
  animal. The author states: "This was a donkey bray imitation I did with
  my mouth." Chosen deliberately over two CC0 field recordings of real
  donkeys (Joseph Sardin / BigSoundBank, felix-blume / Wikimedia Commons)
  because the cartoon quality suits the app better.
- **Attribution:** not required under CC0. Recorded anyway.

## Remaining sounds

`cat`, `cow`, `pig`, `chicken`, `bird`, `frog`, `lion`, `monkey`, `sheep`,
`goat`, `horse`, `rabbit`, `elephant`, `duck` were fetched by
`fetch_sounds.sh`, which scrapes the Pixabay search pages for
`cdn.pixabay.com` download links. The Pixabay Content License permits
free use including commercially, but their terms do not strictly require
attribution. The exact source URL for each file was not recorded, so
individual provenance for these 14 files is unknown.

`octopus` and `turtle` have no audio file: they are synthesized at
runtime with the WebAudio API in `playSynthSound()` (`assets/game.html`).

## If re-fetching sounds

`wavsource.com`, used by `download_animals.sh`, now returns 404 for every
animal it lists. `fetch_sounds.sh` scrapes Pixabay HTML and will break
silently if Pixabay changes its markup. Prefer a source with a stable URL
and an explicit license, and record the URL here when adding a sound.

# Artwork credits

Applies to the Android 7-10 build only (`android7-images` branch). The
`main` branch draws its animals with the system emoji font and ships no
artwork.

## assets/img/*.png

- **Source:** Noto Color Emoji, 2D bitmap artwork, from
  <https://github.com/googlefonts/noto-emoji> (`2D/png/512/`)
- **Copyright:** Copyright 2013 Google, Inc.
- **License:** Apache License 2.0. The full license text ships inside the
  app at `assets/THIRD_PARTY_LICENSES.txt`, as section 4(a) requires.
- **Edits applied:** each bitmap was cropped to its alpha bounding box,
  scaled to fit a 512x512 canvas with a 5% margin, and re-centred with
  Lanczos resampling. No other modification. Fetched and normalised by
  `fetch_emoji_images.py`, which pins the codepoint for every animal.
- **Why these codepoints:** `main` uses emoji that Android 7-10 cannot be
  relied on to draw. U+1FACF DONKEY is Unicode 13 (Android 11) and U+1F986
  DUCK is Unicode 9.0, which is marginal on Android 7.0. Since Noto Color
  Emoji *is* the font Android uses, baking its bitmaps into PNGs makes the
  picture on Android 7 identical to the emoji on Android 11+ rather than an
  approximation of it.
- **Normalisation rationale:** Noto positions each glyph at its natural
  place inside the em square, so the artwork is neither centred nor
  consistently scaled. Left as-is, the turtle sat 36px off centre and six
  other animals drifted 14-24px, which made animals visibly jump while
  swiping. After normalisation the worst offset is 0.5px.

An earlier attempt drew all 18 animals procedurally with
`create_animals.py`. That code was removed: it produced recognisable but
plain faces, and the Noto bitmaps are both better looking and smaller per
animal once normalised.