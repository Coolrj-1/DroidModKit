import tempfile
import unittest
import zipfile
from pathlib import Path

from app import APP_VERSION, inspect_apk


class InspectApkTests(unittest.TestCase):
    def make_apk(self, directory):
        path = Path(directory) / "sample.apk"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("AndroidManifest.xml", b"manifest-placeholder")
            archive.writestr("classes.dex", b"dex-placeholder")
            archive.writestr("lib/arm64-v8a/libsample.so", b"native")
            archive.writestr("META-INF/CERT.RSA", b"signature-placeholder")
            archive.writestr("assets/readme.txt", b"hello")
        return path

    def test_reports_apk_inventory_and_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            report = inspect_apk(self.make_apk(directory))
        self.assertEqual(report["tool_version"], APP_VERSION)
        self.assertTrue(report["valid_zip_archive"])
        self.assertTrue(report["has_android_manifest"])
        self.assertEqual(report["dex_files"], ["classes.dex"])
        self.assertEqual(report["native_libraries"], ["lib/arm64-v8a/libsample.so"])
        self.assertEqual(report["signature_files"], ["META-INF/CERT.RSA"])
        self.assertEqual(len(report["sha256"]), 64)

    def test_rejects_non_apk(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "notes.txt"
            path.write_text("not an apk")
            with self.assertRaises(ValueError):
                inspect_apk(path)

    def test_rejects_invalid_zip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.apk"
            path.write_text("not a zip")
            with self.assertRaises(zipfile.BadZipFile):
                inspect_apk(path)


if __name__ == "__main__":
    unittest.main()
