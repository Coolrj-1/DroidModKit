"""DroidModKit - a safe, read-only APK inspection starter workbench."""
from __future__ import annotations
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_NAME = "DroidModKit"
APP_VERSION = "0.1.0"

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def inspect_apk(path: Path) -> dict:
    if not path.is_file() or path.suffix.lower() != ".apk":
        raise ValueError("Select an existing .apk file.")
    report = {
        "tool": APP_NAME,
        "tool_version": APP_VERSION,
        "inspected_at_utc": datetime.now(timezone.utc).isoformat(),
        "file": path.name,
        "file_path": str(path.resolve()),
        "file_size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "valid_zip_archive": False,
        "entry_count": 0,
        "entries": [],
        "notes": [
            "APK files are ZIP containers; this version inventories entries only.",
            "Binary AndroidManifest.xml decoding is not yet implemented.",
            "No APK content is executed or modified."
        ],
    }
    with zipfile.ZipFile(path, "r") as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise ValueError(f"Archive integrity check failed at: {bad_member}")
        entries = [{
            "name": item.filename,
            "size_bytes": item.file_size,
            "compressed_size_bytes": item.compress_size,
            "is_directory": item.is_dir(),
        } for item in archive.infolist()]
    report["valid_zip_archive"] = True
    report["entries"] = entries
    report["entry_count"] = len(entries)
    report["has_android_manifest"] = any(x["name"] == "AndroidManifest.xml" for x in entries)
    report["native_libraries"] = [
        x["name"] for x in entries if x["name"].startswith("lib/") and x["name"].endswith(".so")
    ]
    report["dex_files"] = [
        x["name"] for x in entries if x["name"].startswith("classes") and x["name"].endswith(".dex")
    ]
    return report

class DroidModKitApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry("980x650")
        self.minsize(720, 460)
        self.report = None
        self.current_path = None
        self.build_ui()

    def build_ui(self):
        root = ttk.Frame(self, padding=14)
        root.pack(fill="both", expand=True)
        header = ttk.Frame(root)
        header.pack(fill="x")
        ttk.Label(header, text=APP_NAME, font=("Segoe UI", 20, "bold")).pack(side="left")
        ttk.Label(header, text=f"v{APP_VERSION} • Read-only APK inspector").pack(side="right")
        actions = ttk.Frame(root)
        actions.pack(fill="x", pady=(14, 8))
        ttk.Button(actions, text="Open APK…", command=self.open_apk).pack(side="left")
        self.export_button = ttk.Button(actions, text="Export JSON report…",
                                        command=self.export_report, state="disabled")
        self.export_button.pack(side="left", padx=8)
        self.status = tk.StringVar(value="Open an APK you own or are authorized to inspect.")
        ttk.Label(root, textvariable=self.status).pack(anchor="w", pady=(0, 8))
        columns = ("name", "size", "compressed", "kind")
        self.table = ttk.Treeview(root, columns=columns, show="headings")
        for key, label, width in [
            ("name", "Archive path", 560), ("size", "Size (bytes)", 120),
            ("compressed", "Compressed (bytes)", 140), ("kind", "Type", 100)
        ]:
            self.table.heading(key, text=label)
            self.table.column(key, width=width, anchor="w")
        self.table.pack(fill="both", expand=True)
        details = ttk.LabelFrame(root, text="APK details", padding=8)
        details.pack(fill="x", pady=(10, 0))
        self.details = tk.Text(details, height=7, wrap="word", state="disabled")
        self.details.pack(fill="x")
        ttk.Label(root, text="Safety: inspection only. No execution, signature alteration, "
                  "payment bypass, or protection circumvention.",
                  foreground="#8a4b08", wraplength=900).pack(anchor="w", pady=(10, 0))

    def open_apk(self):
        selected = filedialog.askopenfilename(
            title="Select APK", filetypes=[("Android packages", "*.apk"), ("All files", "*.*")]
        )
        if not selected:
            return
        path = Path(selected)
        try:
            report = inspect_apk(path)
        except (OSError, zipfile.BadZipFile, ValueError) as exc:
            messagebox.showerror("Could not inspect APK", str(exc))
            return
        self.current_path, self.report = path, report
        for item in self.table.get_children():
            self.table.delete(item)
        for entry in report["entries"]:
            kind = "Folder" if entry["is_directory"] else Path(entry["name"]).suffix or "File"
            self.table.insert("", "end", values=(entry["name"], entry["size_bytes"],
                                                 entry["compressed_size_bytes"], kind))
        summary = [
            f"File: {report['file']}", f"Size: {report['file_size_bytes']:,} bytes",
            f"SHA-256: {report['sha256']}", f"Entries: {report['entry_count']}",
            f"AndroidManifest.xml present: {'Yes' if report.get('has_android_manifest') else 'No'}",
            f"DEX files: {', '.join(report.get('dex_files', [])) or 'None found'}",
            f"Native libraries: {', '.join(report.get('native_libraries', [])) or 'None found'}",
        ]
        self.details.configure(state="normal")
        self.details.delete("1.0", "end")
        self.details.insert("1.0", "\n".join(summary))
        self.details.configure(state="disabled")
        self.export_button.configure(state="normal")
        self.status.set(f"Inspected {path.name} successfully.")

    def export_report(self):
        if not self.report:
            return
        destination = filedialog.asksaveasfilename(
            title="Save inspection report", defaultextension=".json",
            initialfile=f"{self.current_path.stem}-inspection.json",
            filetypes=[("JSON report", "*.json")]
        )
        if not destination:
            return
        try:
            Path(destination).write_text(json.dumps(self.report, indent=2), encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Could not save report", str(exc))
            return
        self.status.set(f"Report saved to {destination}")

if __name__ == "__main__":
    DroidModKitApp().mainloop()
