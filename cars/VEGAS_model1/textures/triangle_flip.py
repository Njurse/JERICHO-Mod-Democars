#!/usr/bin/env python3
"""
wheel_mirror.py - Complete a bisected wheel/texture by reflecting across a
diagonal, then remove the seam by blending or forcing perfect symmetry.

Default behavior (recommended for wheels):
  - Reflect the upper triangle across the anti-diagonal
  - Average with the mirror so the seam disappears completely

Usage:
    python wheel_mirror.py input.png output.png
    python wheel_mirror.py input.png output.png --flip lower
    python wheel_mirror.py input.png output.png --diagonal main
    python wheel_mirror.py input.png output.png --blend 2.5   # thin blend instead of full average
    python wheel_mirror.py input.png output.png --no-blend    # hard cut only (old behavior)
"""

import argparse
import sys
from PIL import Image
import numpy as np


def to_square(img: Image.Image) -> Image.Image:
    """Center-pad to a square."""
    if img.width == img.height:
        return img
    img = img.convert("RGBA")
    side = max(img.width, img.height)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(img, ((side - img.width) // 2, (side - img.height) // 2))
    return canvas


def mirror_and_blend(
    img: Image.Image,
    flip: str = "upper",
    diagonal: str = "anti",
    blend: float | None = 0.0,   # 0.0 = full average (perfect symmetry), None = hard cut, >0 = thin blend width
) -> Image.Image:
    img = to_square(img).convert("RGBA")
    arr = np.array(img).astype(np.float32)
    side = arr.shape[0]

    # Build the mirrored image
    if diagonal == "anti":
        # (x, y) <-> (side-1-y, side-1-x)
        mir = np.empty_like(arr)
        for y in range(side):
            for x in range(side):
                mir[y, x] = arr[side - 1 - x, side - 1 - y]
    else:
        # main diagonal: (x, y) <-> (y, x)
        mir = arr.transpose(1, 0, 2).copy()

    # Decide which half is the source
    ys, xs = np.ogrid[:side, :side]
    if diagonal == "anti":
        if flip == "upper":
            keep = (xs + ys) < (side - 1)
        else:
            keep = (xs + ys) > (side - 1)
    else:
        if flip == "upper":
            keep = xs < ys
        else:
            keep = xs > ys

    # Start with the hard-cut composite
    out = mir.copy()
    out[keep] = arr[keep]

    # Seam removal
    if blend is None:
        # Hard cut only
        pass
    elif blend == 0.0:
        # Perfect symmetry (best for clean wheel textures)
        out = (arr + mir) / 2
    else:
        # Thin blend band around the diagonal
        if diagonal == "anti":
            dist = np.abs(xs + ys - (side - 1))
        else:
            dist = np.abs(xs - ys)
        near = dist <= blend
        out[near] = (arr[near] + mir[near]) / 2

    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("input", help="Input image (PNG recommended)")
    p.add_argument("output", help="Output image")
    p.add_argument("--flip", choices=("upper", "lower"), default="upper",
                   help="Which triangle to treat as the source (default: upper)")
    p.add_argument("--diagonal", choices=("anti", "main"), default="anti",
                   help="Diagonal to reflect across (default: anti)")
    p.add_argument("--blend", type=float, default=0.0,
                   help="Seam blend width in pixels. 0 = perfect symmetry (default), "
                        ">0 = thin blend, omit with --no-blend for hard cut")
    p.add_argument("--no-blend", action="store_true",
                   help="Disable seam removal (hard cut only)")
    args = p.parse_args()

    blend = None if args.no_blend else args.blend

    try:
        with Image.open(args.input) as im:
            result = mirror_and_blend(im, flip=args.flip, diagonal=args.diagonal, blend=blend)
        result.save(args.output)
        mode = "perfect symmetry" if blend == 0.0 else (f"thin blend ({blend}px)" if blend else "hard cut")
        print(f"wrote {args.output}  [{mode}]")
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
