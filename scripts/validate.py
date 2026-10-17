"""Validate this skill package without third-party dependencies (Python 3.10+)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import zlib
from pathlib import Path
from urllib.parse import unquote, urlparse

FAMILIES = ("layered", "matrix", "chart", "logic")


def png_dimensions(data: bytes) -> tuple[int, int]:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("invalid PNG signature")
    pos, dims, ended, image_data = 8, None, False, bytearray()
    header = None
    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        end = pos + 8 + length
        if end + 4 > len(data):
            raise ValueError("truncated PNG chunk")
        payload = data[pos + 8:end]
        crc = struct.unpack(">I", data[end:end + 4])[0]
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != crc:
            raise ValueError("invalid PNG CRC")
        if kind == b"IHDR":
            header = struct.unpack(">IIBBBBB", payload)
            dims = header[:2]
        elif kind == b"IDAT":
            image_data.extend(payload)
        elif kind == b"IEND":
            ended = True
            break
        pos = end + 4
    if not ended or header is None or not image_data:
        raise ValueError("incomplete PNG")
    w, h, depth, color, compression, filtering, interlace = header
    if depth != 8 or color not in (2, 6) or compression or filtering or interlace:
        raise ValueError("expected non-interlaced 8-bit RGB/RGBA reference PNG")
    channels = 3 if color == 2 else 4
    raw = zlib.decompress(image_data)
    if len(raw) != h * (1 + w * channels):
        raise ValueError("PNG pixel data length does not match dimensions")
    return dims


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    skill = root / "skills" / "logic-render"
    assets = skill / "assets"

    def require(ok, message):
        if not ok:
            errors.append(message)

    try:
        source = (skill / "SKILL.md").read_text(encoding="utf-8")
        front = re.match(r"\A---\n(.*?)\n---\n", source, re.S)
        require(front is not None, "SKILL.md: missing YAML frontmatter")
        if front:
            fields = dict(re.findall(r"^(name|description|license):\s*(.+)$", front[1], re.M))
            require(fields.get("name") == "logic-render", "skill name differs from directory")
            description = fields.get("description", "")
            require(1 <= len(description) <= 1024, "description must be 1–1024 characters")
            require(fields.get("license") == "MIT", "skill license must be MIT")
        require((skill / "LICENSE").read_bytes() == (root / "LICENSE").read_bytes(), "bundled LICENSE differs from root")
    except (OSError, UnicodeError) as exc:
        errors.append(f"skill entry/license: {exc}")

    for doc in root.rglob("*.md"):
        if ".git" in doc.parts or "node_modules" in doc.parts:
            continue
        content = re.sub(r"```.*?```", "", doc.read_text(encoding="utf-8"), flags=re.S)
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", content):
            target = target.strip("<>")
            parsed = urlparse(target)
            if parsed.scheme or target.startswith("#"):
                continue
            dest = (doc.parent / unquote(parsed.path)).resolve()
            require(dest.is_relative_to(root), f"{doc.relative_to(root)}: link escapes repository: {target}")
            require(dest.exists(), f"{doc.relative_to(root)}: broken local link: {target}")
            if doc.is_relative_to(skill):
                require(dest.is_relative_to(skill), f"{doc.relative_to(root)}: link breaks standalone skill installation: {target}")

    expected = {f"{family}-{number:02d}.png" for family in FAMILIES for number in (1, 2)}
    prefixes = dict(zip(FAMILIES, ("L", "M", "C", "G")))
    positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
    try:
        manifest = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))
        require(manifest["schema_version"] == 1, "unsupported asset manifest version")
        require(manifest["layout"] == {"columns": 2, "rows": 2, "reading_order": "row-major"},
                "contact sheets must use a 2x2 row-major layout")
        entries = manifest["assets"]
        names = [e["file"] for e in entries]
        require(set(names) == expected and len(names) == len(expected),
                "asset manifest must list exactly eight PNG contact sheets")
        actual = {p.name for p in assets.iterdir() if p.is_file()}
        require(actual == expected | {"README.md", "manifest.json"},
                "asset inventory differs from eight PNG sheets and their index files")
        for entry in entries:
            name = entry["file"]
            if name not in expected:
                continue
            family, number = Path(name).stem.rsplit("-", 1)
            try:
                require(entry["family"] == family, f"{name}: wrong family")
                require(entry["license"] == "MIT", f"{name}: missing license")
                data = (assets / name).read_bytes()
                require(hashlib.sha256(data).hexdigest() == entry["sha256"], f"{name}: hash mismatch")
                width, height = png_dimensions(data)
                require([width, height] == [entry["width"], entry["height"]],
                        f"{name}: dimensions differ from manifest")
                require(width > height and width >= 1200 and height >= 800,
                        f"{name}: expected a large landscape contact sheet")
                panels = entry["panels"]
                start = (int(number) - 1) * 4 + 1
                ids = [f"{prefixes[family]}{i:02d}" for i in range(start, start + 4)]
                require([panel["id"] for panel in panels] == ids,
                        f"{name}: panel IDs must be {', '.join(ids)}")
                require([(panel["row"], panel["column"]) for panel in panels] == positions,
                        f"{name}: panel positions must follow row-major order")
                guide = (skill / "references" / f"{family}.md").read_text(encoding="utf-8")
                guide_panels = dict(re.findall(r"^\| ([LMCG]\d{2}) \| ([^|]+?) \|", guide, re.M))
                for panel in panels:
                    require(bool(panel["title"]) and guide_panels.get(panel["id"]) == panel["title"],
                            f"{name}: panel title/index differs from family guide: {panel['id']}")
            except (OSError, ValueError, KeyError, TypeError, struct.error, zlib.error) as exc:
                errors.append(f"{name}: {exc}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"asset manifest: {exc}")

    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    if errors:
        print(f"Validation failed: {len(errors)} issue(s).", file=sys.stderr)
        return 1
    print("PASS: skill metadata, standalone resources, local links, licenses, eight PNG sheets, image integrity, hashes and 32 panel index entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
