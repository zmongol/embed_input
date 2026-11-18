#!/usr/bin/env python3
"""Generate the Dart encoding tables for the Flutter IME converter.

Reads the Rust lookup tables of the verified desktop converter
(mongol-convert, ~/workspace/mongol-code_convert) and emits:
  - ../embed_ime/lib/encoding/mongol_encoding_tables.dart
      (const Map<String, String> / const Set<int> literals, part of the
       mongol_encoding library)
  - mongol_encoding_tables.json
      (the same data, for the Python mirror used to validate the port
       on this VM where no Dart toolchain exists)

The Dart engine (mongol_encoding_converter.dart) is a line-for-line port
of the Rust translators; these tables are its data, copied mechanically
— no hand edits. To regenerate after a mongol-convert update, run:
  python3 tools/generate_mongol_tables.py
from the repository root (or anywhere; paths are absolute below).

Source files (Rust, read-only):
  crates/mongol-convert/src/tables/generated/{from_z52,to_z52,
    from_menk_letter,to_menk_letter,from_menk_shape,z52_block,
    zvvnmod_block,menk_shape_block}.rs
  crates/mongol-convert/src/tables/z52_punctuation.rs
  crates/mongol-convert/src/tables/zvvnmod_birga.rs (birga maps only)
"""
import json
import os
import re

CONVERT = os.path.expanduser("~/workspace/mongol-code_convert")
GEN = os.path.join(CONVERT, "crates/mongol-convert/src/tables/generated")
TAB = os.path.join(CONVERT, "crates/mongol-convert/src/tables")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DART_OUT = os.path.join(OUT_DIR, "..", "embed_ime", "lib", "encoding",
                        "mongol_encoding_tables.dart")
JSON_OUT = os.path.join(OUT_DIR, "mongol_encoding_tables.json")

# (dart name, rust file, rust static name, kind)
MAP_TABLES = [
    ("fromZ52", "from_z52.rs", "FROM_Z52", "map"),
    ("toZ52", "to_z52.rs", "TO_Z52", "map"),
    ("fromMenkLetter", "from_menk_letter.rs", "FROM_MENK_LETTER", "map"),
    ("fromMenkLetterChagh", "from_menk_letter.rs", "FROM_MENK_LETTER_CHAGH", "map"),
    ("fromMenkLetterHundii", "from_menk_letter.rs", "FROM_MENK_LETTER_HUNDII", "map"),
    ("fromMenkLetterSaarmag", "from_menk_letter.rs", "FROM_MENK_LETTER_SAARMAG", "map"),
    ("fromMenkLetterWWithEhshig", "from_menk_letter.rs",
     "FROM_MENK_LETTER_W_WITH_EHSHIG", "map"),
    ("toMenkLetter", "to_menk_letter.rs", "TO_MENK_LETTER", "map"),
    ("toMenkLetterHundii", "to_menk_letter.rs", "TO_MENK_LETTER_HUNDII", "map"),
    ("toMenkLetterChagh", "to_menk_letter.rs", "TO_MENK_LETTER_CHAGH", "map"),
    ("fromMenkShape", "from_menk_shape.rs", "FROM_MENK_SHAPE", "map"),
    ("z52Codes", "z52_block.rs", "Z52_CODES", "set"),
    ("z52CodePunctuations", "z52_block.rs", "Z52_CODE_PUNCTUATIONS", "set"),
    ("zvvnmodCodes", "zvvnmod_block.rs", "ZVVNMOD_CODES", "set"),
    ("zvvnmodTailCodes", "zvvnmod_block.rs", "ZVVNMOD_TAIL_CODES", "set"),
    ("zvvnmodPunctuations", "zvvnmod_block.rs", "ZVVNMOD_PUNCTUATIONS", "set"),
    ("toZ52Punctuations", "zvvnmod_block.rs", "TO_Z52_PUNCTUATIONS", "set"),
    ("menkShapeNotSupport", "menk_shape_block.rs", "MENK_SHAPE_NOT_SUPPORT", "set"),
]


def rust_unescape(s):
    """Decode a Rust string literal body (no surrounding quotes)."""
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            if n == "u" and i + 2 < len(s) and s[i + 2] == "{":
                j = s.index("}", i + 3)
                out.append(chr(int(s[i + 3:j], 16)))
                i = j + 1
            elif n == "n":
                out.append("\n")
                i += 2
            elif n == "t":
                out.append("\t")
                i += 2
            elif n == "r":
                out.append("\r")
                i += 2
            elif n == "\\":
                out.append("\\")
                i += 2
            elif n == '"':
                out.append('"')
                i += 2
            elif n == "'":
                out.append("'")
                i += 2
            else:
                raise ValueError(f"unsupported Rust escape \\{n} in {s!r}")
        else:
            out.append(c)
            i += 1
    return "".join(out)


def read_static(path, name):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # Find "pub static NAME: ... = &[ ... ];" and capture the bracket body.
    m = re.search(re.escape(name) + r"\b[^=]*=\s*&\[(.*?)\];", text, re.S)
    assert m, f"{name} not found in {path}"
    return m.group(1)


PAIR_RE = re.compile(r'\(\s*"((?:[^"\\]|\\.)*)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*\)')
CHAR_RE = re.compile(r"'((?:[^'\\]|\\.)*)'")


def parse_map(body):
    pairs = PAIR_RE.findall(body)
    assert pairs, "no pairs parsed"
    d = {}
    for k, v in pairs:
        kk, vv = rust_unescape(k), rust_unescape(v)
        assert kk not in d, f"duplicate key {kk!r}"
        d[kk] = vv
    return d


def parse_set(body):
    chars = CHAR_RE.findall(body)
    assert chars, "no chars parsed"
    vals = [ord(rust_unescape(c)) for c in chars]
    assert vals == sorted(set(vals)), "set not sorted-unique"
    return vals


def dart_escape(s):
    """Render a string as a Dart double-quoted literal body."""
    out = []
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "$":
            out.append("\\$")
        elif 0x21 <= o <= 0x7E:
            out.append(ch)
        else:
            out.append("\\u{%x}" % o)
    return "".join(out)


def main():
    tables = {}
    for dart_name, fname, rust_name, kind in MAP_TABLES:
        body = read_static(os.path.join(GEN, fname), rust_name)
        if kind == "map":
            tables[dart_name] = {"kind": "map", "entries": parse_map(body)}
        else:
            tables[dart_name] = {"kind": "set", "entries": parse_set(body)}

    # z52 punctuation: UNICODE_TO_Z52_PUNCTUATION: &[(char, &str)]
    with open(os.path.join(TAB, "z52_punctuation.rs"), encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"UNICODE_TO_Z52_PUNCTUATION[^=]*=\s*&\[(.*?)\];", text, re.S)
    assert m
    pairs = re.findall(
        r"\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*\"((?:[^\"\\]|\\.)*)\"\s*\)", m.group(1))
    assert pairs
    punct = {}
    for k, v in pairs:
        kk = rust_unescape(k)
        assert len(kk) == 1
        punct[kk] = rust_unescape(v)
    tables["unicodeToZ52Punctuation"] = {"kind": "map", "entries": punct}

    # Birga maps (hand-written Rust fns, 4 entries each).
    tables["menkShapeBirgaToZvvnmod"] = {"kind": "map", "entries": {
        "\ue23f": "\U00011660", "\ue240": "\U00011661",
        "\ue241": "\U00011662", "\ue242": "\U00011663"}}
    tables["zvvnmodBirgaToMenkShape"] = {"kind": "map", "entries": {
        "\U00011660": "\ue23f", "\U00011661": "\ue240",
        "\U00011662": "\ue241", "\U00011663": "\ue242"}}
    tables["menkShapeBirgas"] = {"kind": "set",
                                 "entries": [0xE23F, 0xE240, 0xE241, 0xE242]}
    tables["zvvnmodBirgas"] = {"kind": "set",
                               "entries": [0x11660, 0x11661, 0x11662, 0x11663]}

    # Z52 punctuation-gap table (hand-written Rust, punctuation_gap.rs).
    with open(os.path.join(
            CONVERT, "crates/mongol-convert/src/shape/punctuation_gap.rs"),
            encoding="utf-8") as f:
        text = f.read()
    for rust_name, dart_name in (("Z52_SPACED", "z52GapSpaced"),
                                 ("MENK_SHAPE_SPACED", "menkShapeGapSpaced")):
        m = re.search(rust_name + r"[^=]*=\s*&\[(.*?)\];", text, re.S)
        assert m, rust_name
        pairs = re.findall(
            r"\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*Side::(Before|After|Both)\s*\)",
            m.group(1))
        assert pairs, rust_name
        tables[dart_name] = {"kind": "gap", "entries": [
            [ord(rust_unescape(k)), side] for k, side in pairs]}

    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(tables, f, ensure_ascii=True, indent=0)
    print(f"wrote {JSON_OUT}")

    total = 0
    lines = []
    lines.append("// Generated by tools/generate_mongol_tables.py from the")
    lines.append("// verified desktop converter (mongol-convert). DO NOT EDIT")
    lines.append("// by hand; re-run the generator instead. The tables are the")
    lines.append("// dumped Java meco maps; the engine that reads them lives in")
    lines.append("// mongol_encoding_converter.dart (a port of the Rust")
    lines.append("// translators in crates/mongol-convert/src). Imported by")
    lines.append("// mongol_encoding_converter.dart; nothing else needs it.")
    lines.append("")
    for name, spec in tables.items():
        if spec["kind"] == "map":
            entries = spec["entries"]
            total += len(entries)
            lines.append(f"const Map<String, String> {name} = {{")
            for k, v in entries.items():
                lines.append(f'  "{dart_escape(k)}": "{dart_escape(v)}",')
            lines.append("};")
        elif spec["kind"] == "set":
            entries = spec["entries"]
            total += len(entries)
            items = ", ".join(f"0x{v:x}" for v in entries)
            lines.append(f"const Set<int> {name} = {{{items}}};")
        elif spec["kind"] == "gap":
            entries = spec["entries"]
            total += len(entries)
            lines.append("/// (code point, side) — side 0 = before, 1 = after, 2 = both.")
            lines.append(f"const List<(int, int)> {name} = [")
            side_no = {"Before": 0, "After": 1, "Both": 2}
            for cp, side in entries:
                lines.append(f"  (0x{cp:x}, {side_no[side]}),")
            lines.append("];")
        lines.append("")
    with open(DART_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"wrote {DART_OUT} ({total} entries)")
    for name, spec in tables.items():
        print(f"  {name}: {len(spec['entries'])}")


if __name__ == "__main__":
    main()
