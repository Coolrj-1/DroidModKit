# DroidModKit

**An open-source Android APK inspection workbench for developers.**

DroidModKit is an early, read-only desktop starter project for examining APK package structure. The first release can open an APK, validate its ZIP archive, list packaged files, identify DEX files and native libraries, calculate SHA-256, and export a JSON report.

> Use only with applications you own or are authorized to inspect. DroidModKit does not execute APKs, remove licensing, bypass payment checks, or defeat app protections.

## Current features (v0.1.0)

- Desktop GUI built with Python's Tkinter (no third-party runtime dependencies).
- APK ZIP integrity check and archive inventory.
- File sizes and compressed sizes.
- Detection of `AndroidManifest.xml`, `classes*.dex`, and `lib/**/*.so`.
- SHA-256 hash of the APK.
- Exportable JSON inspection report.

## Requirements

- Python 3.10 or newer
- Tkinter (included with most standard Python installations; some Linux distributions package it separately)

## Run

```bash
python app.py
```

On Windows:

```powershell
py -3 app.py
```

Click **Open APK…**, choose an APK you are authorized to inspect, then click **Export JSON report…** to save the inventory.

## Limitations

This is a starter inspector, not a full APK decompiler or editor. Android's compiled `AndroidManifest.xml` is usually binary XML; this version detects its presence but does not decode it. It does not extract files, modify APKs, rebuild packages, or sign APKs.

## Roadmap

- [ ] Manifest decoding and readable permission/component summary
- [ ] Resource and asset browser
- [ ] Smali and DEX inspection integration
- [ ] Native library metadata viewer
- [ ] Optional Apktool integration for authorized workflows
- [ ] Automated tests and packaged desktop builds

Contributions are welcome. Please open an issue before large feature changes.

## License

MIT. See [LICENSE](LICENSE).
