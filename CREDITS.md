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