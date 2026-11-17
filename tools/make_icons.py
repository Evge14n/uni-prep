"""Іконки PWA (PNG) без зовнішніх файлів."""
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "site" / "icons"


def icon(size, pad):
    im = Image.new("RGBA", (size, size), (47, 91, 211, 255))
    d = ImageDraw.Draw(im)
    s = (size - 2 * pad) / 64
    def p(x, y):
        return (pad + x * s, pad + y * s)
    w = max(2, int(5 * s))
    d.line([p(14, 46), p(26, 18), p(38, 46)], fill="white", width=w, joint="curve")
    d.line([p(18, 37), p(34, 37)], fill="white", width=w)
    d.line([p(42, 30), p(52, 30)], fill=(255, 209, 102), width=w)
    d.line([p(47, 25), p(47, 35)], fill=(255, 209, 102), width=w)
    return im


icon(192, 0).save(OUT / "icon-192.png")
icon(512, 0).save(OUT / "icon-512.png")
icon(512, 80).save(OUT / "maskable-512.png")
print("ok")
