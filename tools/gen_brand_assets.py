#!/usr/bin/env python3
"""从品牌主图生成 Windows/Web 图标。"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "static" / "assets" / "northstar-app-icon.png"
ASSETS = ROOT / "static" / "assets"


def resized(source: Image.Image, size: int) -> Image.Image:
    return source.resize((size, size), Image.Resampling.LANCZOS)


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"缺少品牌主图：{SOURCE}")
    source = Image.open(SOURCE).convert("RGBA")
    if source.width != source.height:
        raise SystemExit("品牌主图必须是正方形")

    resized(source, 32).save(ASSETS / "favicon-32.png", optimize=True)
    source.save(
        ASSETS / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )
    print(f"已生成 {ASSETS / 'favicon.ico'}")
    print(f"已生成 {ASSETS / 'favicon-32.png'}")


if __name__ == "__main__":
    main()
