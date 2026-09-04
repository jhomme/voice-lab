# Voice Lab

A Windows CLI tool for tuning eSpeak NG voice variant files and previewing changes through NVDA in real time.

## Requirements

- Python 3.x
- eSpeak NG installed at `C:\Program Files\eSpeak NG\espeak-ng.exe`
- NVDA running and configured to use the eSpeak NG synthesizer

## Usage

```
python voice_lab.py
```

Voice Lab reads your active eSpeak voice from NVDA's config, presents a menu of tunable parameters (pitch, rate, breathiness, etc.), and plays each change immediately so you can hear the result before committing it.

See [docs/voice-lab.md](docs/voice-lab.md) for the full workflow.

## License

MIT — see [LICENSE](LICENSE).
