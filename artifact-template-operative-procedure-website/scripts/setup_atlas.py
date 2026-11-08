#!/usr/bin/env python3
"""Fetch the pinned Z-Anatomy archive and extract only its Blender scene."""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

REVISION = "bb293be456f6d2245191f37752d14ec76894740d"
URL = f"https://raw.githubusercontent.com/Z-Anatomy/Models-of-human-anatomy/{REVISION}/Z-Anatomy.zip"
ARCHIVE_SHA256 = "e029688545627bd0214b269e1063143abb580aad72b2c2445d6d8a9a0d9da736"
SCENE_MEMBER = "Z-Anatomy/Startup.blend"


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True, help="Directory for the archive and scene.")
    parser.add_argument("--archive", type=Path, help="Use an existing copy of the pinned Z-Anatomy.zip.")
    args = parser.parse_args()
    cache = args.cache.expanduser().resolve()
    cache.mkdir(parents=True, exist_ok=True)
    archive = args.archive.expanduser().resolve() if args.archive else cache / "Z-Anatomy.zip"
    scene = cache / "Startup.blend"
    provenance = cache / "atlas-source.json"

    with tempfile.TemporaryDirectory(dir=cache) as temporary:
        temporary = Path(temporary)
        if not archive.exists() and not args.archive:
            download = temporary / "Z-Anatomy.zip"
            try:
                with urllib.request.urlopen(URL, timeout=120) as response, download.open("wb") as output:
                    shutil.copyfileobj(response, output)
            except urllib.error.URLError as error:
                curl = shutil.which("curl")
                if not curl:
                    parser.error(f"Download failed ({error.reason}). Download the archive and use --archive.")
                # System curl can use the operating system trust store.
                subprocess.run(
                    [curl, "--fail", "--silent", "--show-error", "--location",
                     "--max-time", "180", "--output", str(download), URL],
                    check=True,
                )
            if sha256(download) != ARCHIVE_SHA256:
                parser.error("The downloaded atlas does not match the pinned checksum.")
            download.replace(archive)
        if not archive.is_file() or sha256(archive) != ARCHIVE_SHA256:
            parser.error("The atlas archive does not match the pinned version. Use the upstream URL or a fresh cache.")

        if scene.is_file() and provenance.is_file():
            recorded = json.loads(provenance.read_text())
            if recorded.get("archiveSha256") == ARCHIVE_SHA256 and recorded.get("sceneSha256") == sha256(scene):
                print(json.dumps(recorded, indent=2))
                return
        extracted = temporary / "Startup.blend"
        with zipfile.ZipFile(archive) as source, source.open(SCENE_MEMBER) as stream, extracted.open("wb") as output:
            shutil.copyfileobj(stream, output)
        record = {
            "source": URL,
            "revision": REVISION,
            "archiveSha256": ARCHIVE_SHA256,
            "scene": str(scene),
            "sceneSha256": sha256(extracted),
        }
        extracted.replace(scene)
        metadata = temporary / "atlas-source.json"
        metadata.write_text(json.dumps(record, indent=2) + "\n")
        metadata.replace(provenance)
        print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
