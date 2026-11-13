"""Notch のログに、どのプロジェクトの書き出しが入っているかを一覧にする。

使い方: python tools/notch_log_summary.py <ログ.txt> [<ログ.txt> ...]
"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notch_log_to_graph import _lines, read_runs, best_per_doc, slug  # noqa: E402


def main():
    for path in sys.argv[1:]:
        opened = []
        for line in _lines(path):
            j = line.find("Opening document: ")
            if j >= 0:
                opened.append(line[j + 18:].strip().replace("\\", "/").split("/")[-1])
        try:
            runs = read_runs(path)
        except SystemExit:
            runs = []
        best = best_per_doc(runs) if runs else {}
        print(f"\n{Path(path).name}: 開いたプロジェクト {len(opened)}、書き出し {len(runs)} 回")
        for doc in dict.fromkeys(opened):
            r = best.get(slug(doc))
            if not r:
                print(f"  × {doc}  書き出しなし")
                continue
            n = len(r["nodes"])
            vals = sum(1 for x in r["nodes"] if x.get("props"))
            state = "完了" if r["complete"] else "途中まで"
            ver = r["meta"].get("script", "旧")
            times = sum(1 for x in runs if x["doc"] == doc)
            print(f"  {'○' if r['complete'] else '△'} {doc}  {state}  版{ver}  レイヤー{len(r['layers'])}  ノード{n}  値あり{vals}  実行{times}回")


if __name__ == "__main__":
    main()
