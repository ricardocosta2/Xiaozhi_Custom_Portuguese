#!/usr/bin/env python3
"""Verifica se os assets e a documentacao estao sincronizados com os configs.

Para cada Devices/Modular/*.yaml:
  - o ficheiro esta listado em README.md e README_PT.md?
  - os !include locais (core, hw, clocks) existem?
  - existem as 9 imagens do modelo escolhido em images/<modelo>/<imagewidth>x<imageheight>/?
  - existe o wallpaper escolhido em images/Other/<screenwidth>x<screenheight>/?
  - existem images/Other/error-no-ha.png e error-no-wifi.png?

Falha (exit 1) apenas para ficheiros em falta ou PNGs invalidos. Dimensoes
diferentes das esperadas sao avisos, porque algum legado (Steve/Brian/BumbleBee
240x240) tem arte 283x283 que o ESPHome redimensiona no build.

Uso: python tools/check_assets.py
"""

from __future__ import annotations

import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULAR = ROOT / "Devices" / "Modular"
IMAGES = ROOT / "images"
READMES = [ROOT / "README.md", ROOT / "README_PT.md"]

STATES = [
    "error",
    "idle",
    "listening",
    "loading",
    "mute",
    "playing",
    "replying",
    "thinking",
    "timer_finished",
]

REQUIRED_SUBS = [
    "imagewidth",
    "imageheight",
    "screenwidth",
    "screenheight",
    "imagemodel",
    "clock_background_image",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def parse_subs(text: str) -> dict[str, str]:
    """Le as substituicoes simples (chave: valor) do topo do YAML."""
    subs: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        m = re.match(r"^  ([a-z0-9_]+):\s*(.+)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        subs.setdefault(key, value)
    return subs


def find_include(text: str, key: str, base: Path) -> Path | None:
    m = re.search(rf"^\s*{key}:\s*!include\s+(\S+)\s*$", text, re.MULTILINE)
    if not m:
        return None
    return (base / m.group(1)).resolve()


def png_size(path: Path) -> tuple[int, int] | None:
    head = path.read_bytes()[:24]
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    configs = sorted(p for p in MODULAR.glob("*.yaml") if not p.name.startswith("secrets"))
    if not configs:
        print("ERRO: nenhum config encontrado em Devices/Modular")
        return 1

    docs = {p.name: read_text(p) for p in READMES}

    for cfg in configs:
        name = cfg.name
        text = read_text(cfg)
        subs = parse_subs(text)

        for readme, content in docs.items():
            if name not in content:
                failures.append(f"{readme.name}: '{name}' nao esta documentado")

        missing = [k for k in REQUIRED_SUBS if k not in subs]
        if missing:
            failures.append(f"{name}: substituicoes em falta: {', '.join(missing)}")
            continue

        core = find_include(text, "core", MODULAR)
        hw = find_include(text, "hw", MODULAR)
        if core is None or not core.exists():
            failures.append(f"{name}: core !include nao encontrado ({core})")
        if hw is None or not hw.exists():
            failures.append(f"{name}: hw !include nao encontrado ({hw})")
            continue

        hw_text = read_text(hw)
        clocks = find_include(hw_text, "clocks", hw.parent)
        if clocks is None or not clocks.exists():
            failures.append(f"{name}: clocks !include nao encontrado ({clocks})")

        w, h = subs["imagewidth"], subs["imageheight"]
        sw, sh = subs["screenwidth"], subs["screenheight"]
        model = subs["imagemodel"]
        clock = subs["clock_background_image"]

        art_dir = IMAGES / model / f"{w}x{h}"
        for state in STATES:
            f = art_dir / f"{state}.png"
            if not f.exists():
                failures.append(f"{name}: falta {f.relative_to(ROOT)}")
                continue
            size = png_size(f)
            if size is None:
                failures.append(f"{name}: {f.relative_to(ROOT)} nao e um PNG valido")
            elif size != (int(w), int(h)):
                warnings.append(
                    f"{name}: {f.relative_to(ROOT)} e {size[0]}x{size[1]} (esperado {w}x{h})"
                )

        wallpaper = IMAGES / "Other" / f"{sw}x{sh}" / f"{clock}.png"
        if not wallpaper.exists():
            failures.append(f"{name}: falta wallpaper {wallpaper.relative_to(ROOT)}")
        else:
            size = png_size(wallpaper)
            if size is None:
                failures.append(f"{name}: {wallpaper.relative_to(ROOT)} nao e um PNG valido")
            elif size != (int(sw), int(sh)):
                warnings.append(
                    f"{name}: {wallpaper.relative_to(ROOT)} e {size[0]}x{size[1]} "
                    f"(esperado {sw}x{sh})"
                )

        print(f"OK  {name:<32} {w}x{h} ({model}), wallpaper {sw}x{sh}/{clock}.png")

    for err in ("error-no-ha.png", "error-no-wifi.png"):
        f = IMAGES / "Other" / err
        if not f.exists():
            failures.append(f"falta images/Other/{err}")
        elif png_size(f) is None:
            failures.append(f"images/Other/{err} nao e um PNG valido")

    print()
    print(f"{len(configs)} configs verificados")
    if warnings:
        print(f"{len(warnings)} aviso(s):")
        for wmsg in warnings:
            print(f"  AVISO {wmsg}")
    if failures:
        print(f"{len(failures)} erro(s):")
        for err in failures:
            print(f"  ERRO  {err}")
        return 1
    print("Tudo sincronizado: configs, docs, imagens e wallpapers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
