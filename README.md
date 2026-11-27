# DroidModKit

**A read-only Android APK inspection workbench for developers.**

DroidModKit opens APK files as ZIP archives and creates a structured inventory without installing, executing, extracting, or modifying the application.

> Use only with applications you own or are authorized to inspect. DroidModKit does not remove licensing, bypass payment checks, or defeat app protections.

## Current features (v0.2.0)

- Desktop GUI built with Python's Tkinter (standard library).
- APK ZIP integrity check and archive inventory.
- File sizes, compressed sizes, and extension counts.
- SHA-256 hash of the APK.
- Detection of AndroidManifest.xml, DEX files, native libraries, and signature-related files.
- Review indicators for duplicate archive paths, suspicious paths, encrypted entries, and unusually high compression ratios.
- Live archive-path filtering.
- Exportable JSON inspection report.
- Automated unit tests for core inspection behavior.

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

Choose **Open APK…**, select an APK you are authorized to inspect, and use **Export JSON report…** to save the results.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Important limitations

- Android's compiled binary AndroidManifest.xml is detected but not decoded.
- Signature-related files are identified by filename; cryptographic signature verification is not performed.
- Heuristic review indicators are not malware verdicts.
- The tool does not decompile DEX, decode resources, extract files, rebuild packages, or sign APKs.

## Roadmap

- [ ] Binary AndroidManifest.xml decoding and readable permission/component summary
- [ ] Resource and asset browser
- [ ] Smali and DEX inspection integration
- [ ] Native library metadata viewer
- [ ] Optional Apktool integration for authorized workflows
- [ ] Packaged desktop builds

Contributions are welcome. Please open an issue before large feature changes.

## License

MIT. See [LICENSE](LICENSE).
