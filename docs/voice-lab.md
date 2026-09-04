# Voice Lab

A CLI tool for editing eSpeak NG voice variant files and previewing them through NVDA in real time.

---

## Requirements

- eSpeak NG installed at `C:\Program Files\eSpeak NG\espeak-ng.exe`
- NVDA installed at `C:\Program Files\NVDA\` and currently running
- NVDA must be configured to use the eSpeak NG synthesizer (set in NVDA's Voice Settings)

---

## How to Run

```
python voice_lab.py
```

On startup Voice Lab reads your current eSpeak voice from `%APPDATA%\nvda\nvda.ini`. If NVDA is not using eSpeak NG, it prints instructions and exits.

---

## Workflow

1. Start or resume a session. If a previous session was saved, you can continue from where you left off or start fresh from your current NVDA voice.
2. Pick a parameter from the numbered main menu.
3. Choose a preset value from the submenu. Voice Lab writes the change to the working variant file, synthesizes a WAV using eSpeak NG, and plays it immediately.
4. Repeat until the voice sounds right.
5. Install the finished variant into NVDA's voice data folder, then restart NVDA and select it from Voice Settings.

Changes are non-destructive: the tool works on a temporary copy (`_voicelab_temp`) and never modifies your original NVDA voice files.

---

## Main Menu Options

- 1–10 — Open the submenu for that parameter
- R — Re-play the last synthesized WAV
- S — Print the current variant file contents
- I — Install the variant to NVDA and exit
- Q — Quit (optionally saving progress to resume later)
- ? — Show general help

---

## Parameters

### 1. Klatt Model

Selects which formant-synthesis algorithm eSpeak uses to generate the voice. Higher numbers add more synthesis stages, producing a richer but potentially more synthetic sound. Model 1 is the simplest and cleanest; model 6 is the most elaborate.

- klatt 1 — Cleanest, least complex
- klatt 2–4 — Intermediate
- klatt 5 — Used by the built-in "edward" variant
- klatt 6 — edward2 default; most complex

---

### 2. Voicing

Controls how strongly the vocal cords vibrate during speech. Lower values let more unvoiced air through, creating a breathy or airy quality. Higher values produce a fuller, more resonant tone.

- voicing 60 — Breathy
- voicing 75 — Airy
- voicing 90 — Moderate
- voicing 100 — Full (edward2 default)
- voicing 120 — Extra
- voicing 150 — Maximum

---

### 3. Flutter

Adds small, random pitch variations over time, mimicking the natural wavering of a real voice. A value of 0 gives a perfectly steady, robotic tone. Higher values make the voice sound more organic and human.

- flutter 0 — None — perfectly steady
- flutter 1 — Very low
- flutter 2 — Low
- flutter 4 — Moderate
- flutter 6 — Natural
- flutter 8 — High

---

### 4. Roughness

Injects irregular noise into the voice signal, simulating hoarseness or graininess. A value of 0 produces a smooth, clean sound; higher values make the voice increasingly raspy or gravelly. Useful for adding texture, age, or grit to a voice.

- roughness 0 — Smooth
- roughness 1 — Very low
- roughness 2 — Low
- roughness 4 — Moderate
- roughness 6 — Rough
- roughness 8 — Very rough

---

### 5. Pitch Range

Sets the low and high pitch boundaries eSpeak uses when inflecting speech. A narrow range produces a flatter, more monotone delivery; a wide range creates expressive, varied intonation. The two numbers are the bottom and top of the pitch envelope in percent.

- pitch 75 95 — Very narrow — almost monotone
- pitch 70 100 — Narrow
- pitch 65 108 — Moderate
- pitch 60 115 — Current setting
- pitch 55 125 — Wide
- pitch 50 135 — Very wide — very expressive

---

### 6. Consonants

Controls the amplitude and sharpness of consonant sounds relative to vowels. The first number sets overall consonant volume; the second controls how crisply they are articulated. Boosting sharpness improves clarity; reducing it softens the edges of words.

Format: `consonants <amplitude> <sharpness>`

---

### 7–10. Formants 1–4

Formants are the resonant frequencies of the vocal tract. Each is set with three numbers: `formant <n> <frequency%> <amplitude%> <width%>`.

- Formant 1 — Vowel darkness/brightness, shaped by jaw opening. Lower = darker; higher = brighter.
- Formant 2 — Vowel frontness/backness, shaped by tongue position. Lower = back/round; higher = front/bright.
- Formant 3 — Voice timbre and individual character. Subtler than F1/F2; shapes the overall personality of the voice.
- Formant 4 — Upper resonance color. Affects presence and projection; changes are subtle.

---

## Session Files

- `espeak-ng-data/voices/!v/_voicelab_temp` — Working copy of the variant (deleted on exit)
- `_voicelab_in_progress` — Saved session state for resuming later
- `test.wav` — Last synthesized preview audio

---

## Installing a Finished Variant

Choose I from the main menu. You will be prompted for:

- Display name — how it appears in NVDA's Voice list
- File name — the filename saved to NVDA's voice data folder (one word, no spaces)

After installing, restart NVDA and open Preferences → Speech to select the new variant from the Voice dropdown.

> If the install fails with a permission error, re-run Voice Lab as Administrator.
