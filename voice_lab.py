#!/usr/bin/env python3
"""
Voice Lab -- eSpeak NG variant editor for NVDA
Numbered menus with presets. Synthesizes and plays after every change.
"""
import os
import shutil
import subprocess
from pathlib import Path

ESPEAK_EXE = Path(r"C:\Program Files\eSpeak NG\espeak-ng.exe")
DATA_DIR = Path(__file__).parent / "espeak-ng-data"
VARIANTS_DIR = DATA_DIR / "voices" / "!v"
NVDA_VARIANTS = Path(r"C:\Program Files\NVDA\synthDrivers\espeak-ng-data\voices\!v")
NVDA_CONFIG = Path(os.environ["APPDATA"]) / "nvda" / "nvda.ini"
VARIANT_NAME = "_voicelab_temp"
IN_PROGRESS_FILE = Path(__file__).parent / "_voicelab_in_progress"
OUTPUT_WAV = Path(__file__).parent / "test.wav"
TEST_PHRASE = "Hello, this is a test of the custom voice variant. How does it sound?"

PARAMETERS = {
    "klatt": {
        "label": "klatt model",
        "desc": "synthesis engine; higher = more complex",
        "keys": ["klatt"],
        "help": (
            "The Klatt model selects which formant-synthesis algorithm eSpeak uses to generate the voice. "
            "Higher numbers add more synthesis stages, producing a richer but potentially more synthetic sound. "
            "Model 1 is the simplest and cleanest; model 6 is the most elaborate."
        ),
    },
    "voicing": {
        "label": "voicing",
        "desc": "vocal cord vibration; lower = breathier",
        "keys": ["voicing"],
        "help": (
            "Voicing controls how strongly the vocal cords vibrate during speech. "
            "Lower values let more unvoiced air through, creating a breathy or airy quality. "
            "Higher values produce a fuller, more resonant tone."
        ),
    },
    "flutter": {
        "label": "flutter",
        "desc": "natural pitch wavering",
        "keys": ["flutter"],
        "help": (
            "Flutter adds small, random pitch variations over time, mimicking the natural wavering of a real voice. "
            "A value of 0 gives a perfectly steady, robotic tone. "
            "Higher values make the voice sound more organic and human."
        ),
    },
    "roughness": {
        "label": "roughness",
        "desc": "hoarseness / graininess",
        "keys": ["roughness"],
        "help": (
            "Roughness injects irregular noise into the voice signal, simulating hoarseness or graininess. "
            "A value of 0 produces a smooth, clean sound; higher values make the voice increasingly raspy or gravelly. "
            "It is useful for adding texture, age, or grit to a voice."
        ),
    },
    "pitch": {
        "label": "pitch range",
        "desc": "monotone vs. expressive intonation",
        "keys": ["pitch"],
        "help": (
            "Pitch range sets the low and high pitch boundaries eSpeak uses when inflecting speech. "
            "A narrow range produces a flatter, more monotone delivery; a wide range creates expressive, varied intonation. "
            "The two numbers are the bottom and top of the pitch envelope in percent."
        ),
    },
    "consonants": {
        "label": "consonants",
        "desc": "loudness and crispness of consonants",
        "keys": ["consonants"],
        "help": (
            "Consonants controls the amplitude and sharpness of consonant sounds relative to vowels. "
            "The first number sets overall consonant volume; the second controls how crisply they are articulated. "
            "Boosting sharpness improves clarity; reducing it softens the edges of words."
        ),
    },
    "formant1": {
        "label": "formant 1",
        "desc": "vowel darkness/brightness (jaw opening)",
        "keys": ["formant 1"],
        "help": (
            "The first formant is the lowest resonant frequency of the vocal tract, shaped mainly by jaw opening. "
            "Lowering it darkens vowel sounds; raising it brightens them. "
            "It has the strongest single effect on the perceived openness and warmth of the voice."
        ),
    },
    "formant2": {
        "label": "formant 2",
        "desc": "vowel frontness/backness (tongue position)",
        "keys": ["formant 2"],
        "help": (
            "The second formant is shaped by front-to-back tongue position in the mouth. "
            "Lower values push vowels toward the back (darker, rounder); higher values bring them forward (brighter, more nasal). "
            "It most strongly distinguishes vowels like 'ee' from 'oo'."
        ),
    },
    "formant3": {
        "label": "formant 3",
        "desc": "voice timbre and color",
        "keys": ["formant 3"],
        "help": (
            "The third formant contributes to the individual timbre and character of a voice rather than to specific vowel identity. "
            "Adjusting it can make a voice sound warmer, thinner, or more distinctive. "
            "Changes here are subtler than formants 1 and 2 but shape the overall personality of the voice."
        ),
    },
    "formant4": {
        "label": "formant 4",
        "desc": "upper resonance color",
        "keys": ["formant 4"],
        "help": (
            "The fourth formant shapes upper-frequency resonance, adding brightness or ring to the voice. "
            "It contributes to a sense of presence and projection. "
            "Changes are subtle but can make a voice sound more alive or more muffled."
        ),
    },
}

SUBMENUS = {
    "klatt": [
        ("klatt 1", "cleanest, least complex"),
        ("klatt 2", ""),
        ("klatt 3", ""),
        ("klatt 4", ""),
        ("klatt 5", "used by edward"),
        ("klatt 6", "edward2 default, most complex"),
    ],
    "voicing": [
        ("voicing 60",  "breathy"),
        ("voicing 75",  "airy"),
        ("voicing 90",  "moderate"),
        ("voicing 100", "full (edward2 default)"),
        ("voicing 120", "extra"),
        ("voicing 150", "maximum"),
    ],
    "flutter": [
        ("flutter 0", "none -- perfectly steady"),
        ("flutter 1", "very low"),
        ("flutter 2", "low (current setting)"),
        ("flutter 4", "moderate"),
        ("flutter 6", "natural"),
        ("flutter 8", "high"),
    ],
    "roughness": [
        ("roughness 0", "smooth"),
        ("roughness 1", "very low (current setting)"),
        ("roughness 2", "low"),
        ("roughness 4", "moderate"),
        ("roughness 6", "rough"),
        ("roughness 8", "very rough"),
    ],
    "pitch": [
        ("pitch 75 95",  "very narrow -- almost monotone"),
        ("pitch 70 100", "narrow"),
        ("pitch 65 108", "moderate"),
        ("pitch 60 115", "current setting"),
        ("pitch 55 125", "wide"),
        ("pitch 50 135", "very wide -- very expressive"),
    ],
    "consonants": [
        ("consonants 50 65", "soft amplitude, current sharpness"),
        ("consonants 60 65", "moderate amplitude, current sharpness"),
        ("consonants 70 65", "current amplitude, current sharpness"),
        ("consonants 80 65", "loud amplitude, current sharpness"),
        ("consonants 70 50", "current amplitude, smoother"),
        ("consonants 70 55", "current amplitude, slightly smoother"),
        ("consonants 70 75", "current amplitude, crisper"),
        ("consonants 70 85", "current amplitude, sharp"),
    ],
    "formant1": [
        ("formant 1 80 100 100",  "lower frequency -- darker vowels"),
        ("formant 1 86 100 100",  "slightly dark"),
        ("formant 1 92 100 100",  "current setting"),
        ("formant 1 100 100 100", "neutral frequency"),
        ("formant 1 108 100 100", "higher frequency -- brighter vowels"),
        ("formant 1 92 80 100",   "current freq, quieter"),
        ("formant 1 92 120 100",  "current freq, louder"),
        ("formant 1 92 100 75",   "current freq, narrow width -- tighter"),
        ("formant 1 92 100 130",  "current freq, wide width -- throatier"),
    ],
    "formant2": [
        ("formant 2 90 100 80",  "lower frequency"),
        ("formant 2 96 100 80",  "slightly lower"),
        ("formant 2 103 100 80", "current setting"),
        ("formant 2 110 100 80", "slightly higher"),
        ("formant 2 118 100 80", "higher frequency"),
        ("formant 2 103 80 80",  "current freq, quieter"),
        ("formant 2 103 120 80", "current freq, louder"),
        ("formant 2 103 100 60", "current freq, narrow width"),
        ("formant 2 103 100 100","current freq, wider"),
    ],
    "formant3": [
        ("formant 3 90 100 70",  "lower frequency"),
        ("formant 3 96 100 70",  "slightly lower"),
        ("formant 3 103 100 70", "current setting"),
        ("formant 3 110 100 70", "slightly higher"),
        ("formant 3 118 100 70", "higher frequency"),
        ("formant 3 103 80 70",  "current freq, quieter"),
        ("formant 3 103 120 70", "current freq, louder"),
        ("formant 3 103 100 50", "current freq, narrow width"),
        ("formant 3 103 100 90", "current freq, wider"),
    ],
    "formant4": [
        ("formant 4 100 100 60", "lower frequency"),
        ("formant 4 107 100 60", "slightly lower"),
        ("formant 4 114 100 60", "current setting"),
        ("formant 4 121 100 60", "slightly higher"),
        ("formant 4 128 100 60", "higher frequency"),
        ("formant 4 114 80 60",  "current freq, quieter"),
        ("formant 4 114 120 60", "current freq, louder"),
        ("formant 4 114 100 40", "current freq, narrow width"),
        ("formant 4 114 100 80", "current freq, wider"),
    ],
}

MAIN_MENU_ORDER = [
    "klatt", "voicing", "flutter", "roughness",
    "pitch", "consonants",
    "formant1", "formant2", "formant3", "formant4",
]

_current_voice = "en-us"


class Variant:
    def __init__(self, path: Path):
        self.path = path
        self.lines: list[str] = path.read_text(encoding="utf-8").splitlines()

    def _find(self, key: str) -> int:
        for i, line in enumerate(self.lines):
            if line.startswith(key + " ") or line.startswith(key + "\t") or line == key:
                return i
        return -1

    def get_raw(self, key: str) -> str:
        i = self._find(key)
        return self.lines[i].strip() if i >= 0 else "(not set)"

    def set_line(self, key: str, full_line: str):
        i = self._find(key)
        if i >= 0:
            self.lines[i] = full_line
        else:
            self.lines.append(full_line)

    def save(self):
        self.path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")

    def show(self):
        print("\n--- Current variant ---")
        for line in self.lines:
            if line.strip():
                print(f"  {line}")
        print()


def get_leading_key(line: str) -> str:
    parts = line.split()
    if len(parts) >= 2 and parts[0] == "formant":
        return f"formant {parts[1]}"
    return parts[0] if parts else ""


def read_nvda_config():
    """Return (synth, voice, variant) from NVDA's config. variant may be None."""
    if not NVDA_CONFIG.exists():
        return None, None, None
    synth = voice = variant = None
    in_speech = in_espeak = False
    for line in NVDA_CONFIG.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s == "[speech]":
            in_speech, in_espeak = True, False
        elif s.startswith("[") and not s.startswith("[["):
            in_speech, in_espeak = False, False
        elif in_speech:
            if s == "[[espeak]]":
                in_espeak = True
            elif s.startswith("[["):
                in_espeak = False
            elif "=" in s:
                k, _, v = s.partition("=")
                k, v = k.strip(), v.strip()
                if not in_espeak and k == "synth":
                    synth = v
                elif in_espeak and k == "voice":
                    voice = v
                elif in_espeak and k == "variant":
                    variant = v
    return synth, voice, variant


def synthesize_and_play(variant: Variant, voice: str):
    variant.save()
    voice_arg = f"{voice}+{VARIANT_NAME}" if voice else VARIANT_NAME
    cmd = [
        str(ESPEAK_EXE),
        f"--path={DATA_DIR}",
        "-v", voice_arg,
        "-w", str(OUTPUT_WAV),
        TEST_PHRASE,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Synthesis error: {result.stderr.strip()}")
    else:
        os.startfile(str(OUTPUT_WAV))


APP_DESCRIPTION = """\
Voice Lab creates a custom eSpeak NG voice variant for NVDA.

It reads your current eSpeak voice from NVDA's settings, copies it as a
starting point, and lets you adjust parameters like pitch, formants, flutter,
and consonant sharpness through a numbered menu. After each change it
synthesizes a test phrase to a WAV file and plays it so you can hear the
result immediately. When you are satisfied, it installs the finished variant
into NVDA's voice data folder so it appears in the Voice Settings dialog.

To use this app, open NVDA's Voice Settings and switch the synthesizer to
eSpeak NG, then run Voice Lab again.
"""


def show_main_menu(variant: Variant):
    print("\n--- Parameters ---")
    for i, key in enumerate(MAIN_MENU_ORDER, 1):
        label = PARAMETERS[key]["label"]
        desc = PARAMETERS[key]["desc"]
        lookup_keys = PARAMETERS[key]["keys"]
        current = " / ".join(variant.get_raw(k) for k in lookup_keys)
        print(f"  {i:2}. {label:<12}  {desc:<48}  (current: {current})")
    print()
    print("   R. Re-play last WAV")
    print("   S. Show current file")
    print("   I. Install to NVDA and exit")
    print("   Q. Quit")
    print("   ?. Help")
    print()


def show_submenu(param_key: str, variant: Variant):
    label = PARAMETERS[param_key]["label"]
    options = SUBMENUS[param_key]
    lookup_keys = PARAMETERS[param_key]["keys"]
    current = " / ".join(variant.get_raw(k) for k in lookup_keys)

    print(f"\n--- {label} (current: {current}) ---")
    for i, (value, desc) in enumerate(options, 1):
        marker = " <--" if value == current else ""
        suffix = f"  -- {desc}" if desc else ""
        print(f"  {i}. {value}{suffix}{marker}")
    print()
    print("  B. Back without changing")
    print("  ?. What does this parameter do?")
    print()


def run_submenu(param_key: str, variant: Variant):
    options = SUBMENUS[param_key]
    show_submenu(param_key, variant)

    while True:
        choice = input("Choice: ").strip().upper()
        if choice == "B":
            return
        if choice == "?":
            print(f"\n{PARAMETERS[param_key]['help']}\n")
            continue
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                full_line, _ = options[idx]
                key = get_leading_key(full_line)
                variant.set_line(key, full_line)
                print(f"Set: {full_line}")
                synthesize_and_play(variant, _current_voice)
                return
            else:
                print(f"Enter a number between 1 and {len(options)}, or B to go back.")
        except ValueError:
            print("Enter a number or B.")


def install_to_nvda(variant: Variant):
    display = input(f"Display name in NVDA Voice list [{VARIANT_NAME}]: ").strip() or VARIANT_NAME
    file_name = input(f"File name (one word) [{VARIANT_NAME}]: ").strip() or VARIANT_NAME
    variant.set_line("name", f"name {display}")
    variant.save()
    dest = NVDA_VARIANTS / file_name
    try:
        shutil.copy2(variant.path, dest)
        print(f"\nInstalled as '{file_name}'.")
        print(f"Restart NVDA, then open Voice Settings and select '{display}' from the Voice list.")
    except PermissionError:
        print("\nPermission denied. Re-run as Administrator to install to NVDA.")


def main():
    global _current_voice

    synth, voice, source_variant = read_nvda_config()

    if synth != "espeak":
        print("\nNVDA is not currently using the eSpeak NG synthesizer.\n")
        print(APP_DESCRIPTION)
        return

    print("Voice Lab: eSpeak NG Variant Editor for NVDA")
    _current_voice = voice

    variant_path = VARIANTS_DIR / VARIANT_NAME

    # Decide what to start from
    if IN_PROGRESS_FILE.exists():
        print("\nAn in-progress session was found.")
        print("  1. Continue where you left off")
        print("  2. Start fresh from the current NVDA voice")
        while True:
            pick = input("Choice: ").strip()
            if pick == "1":
                shutil.copy2(IN_PROGRESS_FILE, variant_path)
                print("Loaded in-progress session.")
                break
            elif pick == "2":
                IN_PROGRESS_FILE.unlink()
                _seed_from_nvda(variant_path, voice, source_variant)
                break
            else:
                print("Enter 1 or 2.")
    else:
        print(f"\nNVDA voice: {voice}  variant: {source_variant or '(none)'}")
        _seed_from_nvda(variant_path, voice, source_variant)

    try:
        variant = Variant(variant_path)

        print("\nSynthesizing current variant...")
        synthesize_and_play(variant, voice)

        while True:
            show_main_menu(variant)
            choice = input("Choice: ").strip().upper()

            if choice == "Q":
                print("\nSave progress to continue later?")
                print("  1. Yes, save progress")
                print("  2. No, discard and exit")
                while True:
                    pick = input("Choice: ").strip()
                    if pick == "1":
                        shutil.copy2(variant_path, IN_PROGRESS_FILE)
                        print("Progress saved. Run Voice Lab again to continue.")
                        break
                    elif pick == "2":
                        print("Discarding session.")
                        break
                    else:
                        print("Enter 1 or 2.")
                break
            elif choice == "I":
                install_to_nvda(variant)
                if IN_PROGRESS_FILE.exists():
                    IN_PROGRESS_FILE.unlink()
                break
            elif choice == "?":
                print(APP_DESCRIPTION)
            elif choice == "S":
                variant.show()
            elif choice == "R":
                if OUTPUT_WAV.exists():
                    os.startfile(str(OUTPUT_WAV))
                else:
                    print("No WAV yet.")
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(MAIN_MENU_ORDER):
                        run_submenu(MAIN_MENU_ORDER[idx], variant)
                    else:
                        print(f"Enter a number between 1 and {len(MAIN_MENU_ORDER)}, or a letter option.")
                except ValueError:
                    print("Unknown choice.")
    finally:
        if variant_path.exists():
            variant_path.unlink()


def _seed_from_nvda(variant_path: Path, voice: str, source_variant: str | None):
    if source_variant:
        nvda_source = NVDA_VARIANTS / source_variant
        local_source = VARIANTS_DIR / source_variant
        src = nvda_source if nvda_source.exists() else local_source
        shutil.copy2(src, variant_path)
    else:
        variant_path.write_text("language variant\nname _voicelab_temp\n", encoding="utf-8")


if __name__ == "__main__":
    main()
