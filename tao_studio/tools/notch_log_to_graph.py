"""notch_dump.js が書いたログを、読めるつなぎ図にする。

使い方:
    python tools/notch_log_to_graph.py "C:\\Users\\<名前>\\Documents\\Notch\\Logs\\<ログ>.txt" ^
        --course fundamentals-japan --project 03_particles

出力: raw/workshop/<course>/graphs/<project>.md と .json
ログに複数回の書き出しがあれば、最後の1回（BEGIN〜END）を使う。
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path


def read_dump(path):
    runs, cur = [], None
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        i = line.find("TAO|")
        if i < 0:
            continue
        parts = line[i:].split("|", 2)
        tag, payload = parts[1], (parts[2] if len(parts) > 2 else "")
        if tag == "BEGIN":
            cur = {"meta": json.loads(payload or "{}"), "layers": [], "nodes": [], "complete": False}
            runs.append(cur)
        elif cur is None:
            continue
        elif tag == "LAYER":
            cur["layers"].append(json.loads(payload))
        elif tag == "NODE":
            try:
                cur["nodes"].append(json.loads(payload))
            except json.JSONDecodeError:
                cur.setdefault("broken", 0)
                cur["broken"] += 1
        elif tag == "API":
            cur.setdefault("api", []).append(json.loads(payload))
        elif tag == "SKIP":
            cur.setdefault("skipped", []).append(json.loads(payload))
        elif tag == "END":
            cur["complete"] = True
    if not runs:
        sys.exit("ログに TAO| の行がありません。スクリプトが実行されたか確かめてください。")
    return runs[-1]


def label(n):
    t = n.get("type", "?")
    short = t.split("::")[-1]
    s = n["name"] if n["name"] == short else f'{n["name"]}  [{t}]'
    if n.get("visible") is False:
        s += "  (非表示)"
    if n.get("props"):
        s += "  (" + ", ".join(f"{k}: {v:g}" if isinstance(v, (int, float)) else f"{k}: {v}"
                               for k, v in n["props"].items()) + ")"
    return s


def tree(nodes):
    by_id = {}
    for n in nodes:
        by_id.setdefault(n["id"], n)
    dup = [k for k, c in Counter(n["id"] for n in nodes).items() if c > 1]
    roots = [n for n in nodes if not n.get("parents")]
    lines, seen = [], set()

    def walk(n, prefix, last, path):
        mark = "" if not prefix and last is None else ("└─ " if last else "├─ ")
        again = n["id"] in seen
        lines.append(prefix + mark + label(n) + ("  ↑上に既出" if again else ""))
        if again or n["id"] in path:
            return
        seen.add(n["id"])
        kids = [by_id[c] for c in n.get("children", []) if c in by_id]
        ext = "" if last is None else ("   " if last else "│  ")
        leaf = Counter(k.get("type") for k in kids if not k.get("children"))
        shown, hidden = [], Counter()
        for k in kids:
            t = k.get("type")
            if not k.get("children") and leaf[t] > 8:
                if hidden[t] >= 3:
                    hidden[t] += 1
                    seen.add(k["id"])
                    continue
                hidden[t] += 1
            shown.append(k)
        more = [f"… ほか {t.split('::')[-1]} ×{c - 3}" for t, c in hidden.items() if c > 3]
        for i, k in enumerate(shown):
            walk(k, prefix + ext, i == len(shown) - 1 and not more, path | {n["id"]})
        for i, m in enumerate(more):
            lines.append(prefix + ext + ("└─ " if i == len(more) - 1 else "├─ ") + m)

    for r in sorted(roots, key=lambda n: (n.get("pos") or [0, 0])[1]):
        walk(r, "", None, frozenset())
    orphans = [n for n in nodes if n["id"] not in seen]
    return lines, orphans, dup


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--course", required=True)
    ap.add_argument("--project", required=True)
    a = ap.parse_args()

    d = read_dump(a.log)
    out = Path(__file__).resolve().parent.parent / "raw" / "workshop" / a.course / "graphs"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{a.project}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

    md = [f"# {a.project}", "", f"- Notch のバージョン: {d['meta'].get('version')}",
          f"- レイヤー数: {len(d['layers'])}　ノード数: {len(d['nodes'])}"]
    if not d["complete"]:
        md.append("- **注意: 書き出しが途中で終わっています（END がありません）。**")
    if d.get("broken"):
        md.append(f"- **注意: 読めなかった行が {d['broken']} 件あります。**")
    md += ["- 含まれるもの: ノード名、種類、親子のつながり、埋め込み、表示状態",
           "- 含まれないもの: パラメータの値（TAO_PROPS に書いた分だけ）、キーフレーム、プロパティへの入力接続", ""]
    for layer in d["layers"]:
        nodes = [n for n in d["nodes"] if n["layer"] == layer["index"]]
        md += [f"## レイヤー {layer['index']}: {layer['name']}（{len(nodes)} ノード）", ""]
        kinds = Counter(n.get("type", "?") for n in nodes)
        md += ["使われているノードの種類: " + "、".join(f"{k} ×{c}" for k, c in kinds.most_common()), ""]
        lines, orphans, dup = tree(nodes)
        md += ["```"] + lines + ["```", ""]
        if orphans:
            md += ["親子の木に入らなかったノード（循環など）: " + "、".join(label(n) for n in orphans), ""]
        if dup:
            md += ["同じ名前・同じ位置で区別できなかったノード: " + "、".join(dup), ""]
        emb = [(n, n["embeds"]) for n in nodes if n.get("embeds")]
        if emb:
            md += ["埋め込み:"] + [f"- {n['name']} ← {', '.join(e.split('@')[0] for e in es)}" for n, es in emb] + [""]
    (out / f"{a.project}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{out / (a.project + '.md')} を書きました（{len(d['nodes'])} ノード）")


if __name__ == "__main__":
    main()
