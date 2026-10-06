# Four Seasons 店内写真 — A1 用紙合わせ

## A1 サイズ（ISO 216）

| 項目 | 値 |
|------|-----|
| 実寸 | **594 × 841 mm**（縦） |
| インチ | 約 23.39 × 33.11 in |
| アスペクト比 | 1 : √2 ≈ **0.7063** |
| 72 dpi | 1684 × 2384 px |
| 150 dpi（大判印刷向け） | 3508 × 4961 px |
| 300 dpi（高精細） | 7016 × 9933 px |

## 出力（単体）

元写真（3024×4032、比率 0.75）を A1 比率に**中央クロップ**し、余白なしで用紙いっぱいに合わせています。

| ファイル | 用途 |
|----------|------|
| `output/FourSeasons_interior_A1.pdf` | **A1 実寸 PDF**（印刷用） |
| `output/FourSeasons_interior_A1_150dpi.jpg` | 150 dpi JPEG |
| `output/FourSeasons_interior_A1_preview.jpg` | プレビュー（1786×2529） |

## 出力（合成）

赤線位置より下にカウンター写真を挿入。カウンターは用紙横幅いっぱい。

| ファイル | 用途 |
|----------|------|
| `output/FourSeasons_composite_A1.pdf` | **A1 実寸 PDF**（印刷用） |
| `output/FourSeasons_composite_A1_150dpi.jpg` | 150 dpi JPEG |
| `output/FourSeasons_composite_A1_preview.jpg` | プレビュー |
| `output/FourSeasons_composite_A1_chat.jpg` | チャット表示用 |

## 再生成

```bash
python3 fit_to_a1.py
python3 compose_a1.py
```
