
from PIL import Image
import sys
from pathlib import Path

source = Path(sys.argv[1])
output = source.with_suffix(".txt")

img = Image.open(source).convert("RGBA")
colors = sorted(set(img.getdata()))

with output.open("w", encoding="ascii", newline="\n") as f:
    for r, g, b, a in colors:
        f.write(f"{a:02X}{r:02X}{g:02X}{b:02X}\n")

print(f"Saved {len(colors)} colors to {output}")
