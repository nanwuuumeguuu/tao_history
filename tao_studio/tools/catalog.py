"""配布物フォルダの目録を作る。

使い方（Windows の例）:
    python tools/catalog.py "D:\\Notch\\Fundamentals Japan" --course fundamentals-japan
    python tools/catalog.py "D:\\Notch\\Advanced Course"   --course advanced

出力:
    raw/workshop/<course>/catalog.md      ファイル1件1行の目録
    raw/workshop/<course>/sheets/         ビデオと画像の一覧画像（ffmpeg がある場合）

元のファイルは読むだけで、変更も複製もしない。
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path

KINDS = {
    "notch": {".dfx", ".dfxdll"},
    "video": {".mp4", ".mov", ".avi", ".mkv", ".webm", ".mxf"},
    "image": {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".exr", ".hdr", ".tga", ".bmp", ".dds"},
    "lut": {".cube", ".3dl", ".lut"},
    "3d": {".fbx", ".obj", ".abc", ".c4d", ".glb", ".gltf", ".usd", ".usdz", ".ply"},
    "audio": {".wav", ".mp3", ".aif", ".aiff", ".flac", ".ogg"},
    "shader": {".fx", ".hlsl", ".glsl", ".js"},
    "doc": {".pdf", ".txt", ".md", ".docx", ".pptx", ".csv"},
}
SHEETABLE = {".png", ".jpg", ".jpeg", ".tga", ".bmp", ".tif", ".tiff"}


def kind_of(p):
    ext = p.suffix.lower()
    for k, exts in KINDS.items():
        if ext in exts:
            return k
    return "other"


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def probe(p):
    """ffprobe で長さと解像度を取る。無ければ空。"""
    if not shutil.which("ffprobe"):
        return ""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height:format=duration", "-of", "json", str(p)],
            capture_output=True, text=True, timeout=60).stdout
        d = json.loads(out)
        s = (d.get("streams") or [{}])[0]
        dur = float(d.get("format", {}).get("duration", 0) or 0)
        return f"{s.get('width','?')}x{s.get('height','?')} {dur:.1f}s"
    except Exception:
        return ""


def sheet(p, dest, is_video):
    """一覧画像を1枚作る。失敗しても止めない。"""
    if not shutil.which("ffmpeg") or dest.exists():
        return dest.exists()
    vf = "thumbnail=60,scale=320:-1,tile=4x2" if is_video else "scale=320:-1"
    try:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(p), "-vf", vf,
                        "-frames:v", "1", str(dest)], timeout=180, check=True)
        return True
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--course", required=True, help="目録の名前（例: fundamentals-japan）")
    ap.add_argument("--no-sheets", action="store_true", help="一覧画像を作らない")
    a = ap.parse_args()

    src = Path(a.folder)
    if not src.is_dir():
        sys.exit(f"フォルダが見つかりません: {src}")
    out = Path(__file__).resolve().parent.parent / "raw" / "workshop" / a.course
    sheets = out / "sheets"
    sheets.mkdir(parents=True, exist_ok=True)

    rows, totals = [], {}
    files = sorted(p for p in src.rglob("*") if p.is_file())
    for i, p in enumerate(files, 1):
        k = kind_of(p)
        size = p.stat().st_size
        totals[k] = totals.get(k, [0, 0])
        totals[k][0] += 1
        totals[k][1] += size
        info, pic = "", ""
        if k == "video":
            info = probe(p)
        if not a.no_sheets and (k == "video" or p.suffix.lower() in SHEETABLE):
            name = f"{i:04d}_{p.stem[:40]}.jpg"
            if sheet(p, sheets / name, k == "video"):
                pic = f"sheets/{name}"
        rel = p.relative_to(src).as_posix()
        rows.append(f"| {rel} | {k} | {human(size)} | {info} | {pic} |  |  |")
        print(f"\r{i}/{len(files)}", end="", file=sys.stderr)

    lines = [f"# 目録: {a.course}", "",
             f"- 元の場所: `{src}`", f"- ファイル数: {len(files)}",
             "- 利用条件: 明示なし（主催者に確認するまで、公開する作品や再配布には使わない）", "",
             "## 種類ごとの合計", "", "| 種類 | 件数 | 合計 |", "|---|---|---|"]
    lines += [f"| {k} | {c} | {human(s)} |" for k, (c, s) in sorted(totals.items())]
    lines += ["", "## ファイル", "",
              "| 場所 | 種類 | 大きさ | 映像情報 | 一覧画像 | 用途（後で記入） | 技法カード |",
              "|---|---|---|---|---|---|---|"] + rows
    (out / "catalog.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n{out / 'catalog.md'} を書きました（{len(files)} 件）", file=sys.stderr)


if __name__ == "__main__":
    main()
