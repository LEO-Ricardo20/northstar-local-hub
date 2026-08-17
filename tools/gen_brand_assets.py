#!/usr/bin/env python3
"""Deterministically generate LeoDock application and web brand assets."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "static" / "assets"
SIZE = 1254
APP_ICON = ASSETS / "leodock-app-icon.png"
BRAND_MARK = ASSETS / "leodock-brand-mark.png"


def _glow(canvas: Image.Image, box, color, blur: int) -> None:
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(box, fill=color)
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def _monogram(with_glow: bool = True) -> Image.Image:
    mark = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    if with_glow:
        _glow(mark, (230, 210, 820, 1000), (102, 146, 255, 105), 86)
        _glow(mark, (590, 250, 1040, 760), (71, 209, 140, 72), 92)

    draw = ImageDraw.Draw(mark)
    stroke = 86
    draw.line((338, 306, 338, 836), fill=(245, 248, 255, 255), width=stroke)
    draw.line((338, 836, 568, 836), fill=(245, 248, 255, 255), width=stroke)
    draw.line((632, 306, 632, 836), fill=(109, 146, 255, 255), width=stroke)
    draw.arc((370, 306, 932, 836), -90, 90,
             fill=(109, 146, 255, 255), width=stroke)
    draw.ellipse((835, 250, 935, 350), fill=(255, 184, 92, 255))
    draw.ellipse((861, 276, 909, 324), fill=(255, 238, 208, 255))
    return mark


def _app_icon() -> Image.Image:
    icon = Image.new("RGBA", (SIZE, SIZE), (6, 9, 15, 255))
    _glow(icon, (-120, 120, 780, 1120), (74, 112, 255, 110), 130)
    _glow(icon, (650, -180, 1370, 650), (255, 163, 71, 64), 120)

    glass = Image.new("RGBA", icon.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glass)
    panel = (118, 118, SIZE - 118, SIZE - 118)
    draw.rounded_rectangle(
        panel,
        radius=230,
        fill=(12, 18, 29, 224),
        outline=(223, 232, 255, 66),
        width=5,
    )
    draw.line((230, 250, 1010, 170), fill=(255, 255, 255, 25), width=15)
    draw.line((175, 1000, 1035, 865), fill=(109, 146, 255, 25), width=12)
    icon.alpha_composite(glass)
    icon.alpha_composite(_monogram())
    return icon


def resized(source: Image.Image, size: int) -> Image.Image:
    return source.resize((size, size), Image.Resampling.LANCZOS)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    icon = _app_icon()
    mark = _monogram(with_glow=False)
    icon.save(APP_ICON, optimize=True)
    mark.save(BRAND_MARK, optimize=True)
    resized(icon, 32).save(ASSETS / "favicon-32.png", optimize=True)
    icon.save(
        ASSETS / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )
    for path in (APP_ICON, BRAND_MARK, ASSETS / "favicon-32.png",
                 ASSETS / "favicon.ico"):
        print(f"generated {path}")


if __name__ == "__main__":
    main()
