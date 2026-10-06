#!/usr/bin/env python3
"""提供写真を A1 用紙サイズ（594×841 mm）に合わせて出力する。"""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from reportlab.lib.pagesizes import A1
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "interior_lounge.jpg"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

# ISO 216 A1（縦）
A1_MM = (594, 841)
A1_RATIO = A1_MM[0] / A1_MM[1]  # ≈ 0.7063

# 既存看板ワークと揃えたプレビュー解像度 / 大判印刷用
PREVIEW_PX = (1786, 2529)  # ≈ 72–96 dpi 相当
PRINT_150_PX = (3508, 4961)  # 150 dpi
PRINT_300_PX = (7016, 9933)  # 300 dpi


def cover_crop(im: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """用紙全体を埋めるよう中央クロップしてリサイズ（余白なし）。"""
    src_w, src_h = im.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # 元が横長すぎる → 左右を切る
        new_w = int(round(src_h * target_ratio))
        left = (src_w - new_w) // 2
        box = (left, 0, left + new_w, src_h)
    else:
        # 元が縦長すぎる → 上下を切る
        new_h = int(round(src_w / target_ratio))
        top = (src_h - new_h) // 2
        box = (0, top, src_w, top + new_h)

    cropped = im.crop(box)
    return cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)


def save_jpeg(im: Image.Image, path: Path, dpi: tuple[int, int]) -> None:
    im.convert("RGB").save(
        path,
        "JPEG",
        quality=95,
        optimize=True,
        dpi=dpi,
    )


def save_a1_pdf(im: Image.Image, path: Path) -> None:
    """A1 実寸 PDF（画像フルブリード）。"""
    # PDF埋め込み用に 150dpi 相当へ
    embed = cover_crop(im, *PRINT_150_PX)
    tmp = OUT / "_embed_tmp.jpg"
    save_jpeg(embed, tmp, (150, 150))

    page_w, page_h = A1  # points
    c = canvas.Canvas(str(path), pagesize=A1)
    c.drawImage(str(tmp), 0, 0, width=page_w, height=page_h, preserveAspectRatio=False)
    c.showPage()
    c.save()
    tmp.unlink(missing_ok=True)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"source not found: {SRC}")

    src = Image.open(SRC)
    # EXIF 向きを反映
    try:
        from PIL import ImageOps

        src = ImageOps.exif_transpose(src)
    except Exception:
        pass

    src_w, src_h = src.size
    print(f"source: {src_w}×{src_h} px  ratio={src_w/src_h:.4f}")
    print(f"A1:     {A1_MM[0]}×{A1_MM[1]} mm  ratio={A1_RATIO:.4f}")
    print(f"A1 pt:  {A1[0]:.1f}×{A1[1]:.1f} (72dpi points)")

    preview = cover_crop(src, *PREVIEW_PX)
    print150 = cover_crop(src, *PRINT_150_PX)

    preview_path = OUT / "FourSeasons_interior_A1_preview.jpg"
    print150_path = OUT / "FourSeasons_interior_A1_150dpi.jpg"
    pdf_path = OUT / "FourSeasons_interior_A1.pdf"

    save_jpeg(preview, preview_path, (96, 96))
    save_jpeg(print150, print150_path, (150, 150))
    save_a1_pdf(src, pdf_path)

    print(f"wrote {preview_path.name}  {PREVIEW_PX[0]}×{PREVIEW_PX[1]}")
    print(f"wrote {print150_path.name}  {PRINT_150_PX[0]}×{PRINT_150_PX[1]} @150dpi")
    print(f"wrote {pdf_path.name}  A1 real size ({A1_MM[0]}×{A1_MM[1]} mm)")


if __name__ == "__main__":
    main()
