---
id: T-003
name: Notch ワークショップの配布物をカードにする手順
status: unverified
tools: [Notch]
source: 自作の手順
license: 配布物ごとに確認して書く
automation: manual
---

## 手順
1. 配布物の一覧を `raw/workshop/catalog.md` に書く（ファイル名、種類、保存場所、利用条件）。
2. `.dfx` の複製を開き、`tools/notch_dump.js` を JavaScript ノードで実行してノードグラフをログに書き出す。`tools/notch_log_to_graph.py` でつなぎ図にする。
   値や入力接続は書き出されないので、要所だけ画面を撮って `raw/workshop/` に置く。
3. ビデオ・テクスチャ・LUT は `tools/catalog.py` で目録と一覧画像にする。
4. Claude に `technique-card` スキルでカードを書かせる。
5. ノード名を Notch のマニュアルで照合する。
6. 自分で Notch 上に再現できたら `status: verified` にする。

## つなぎ方の書き方

```
Root
└─ Particle Root
   ├─ Primitive Emitter   (Emission Rate: 5000)
   ├─ Turbulence Affector (Scale: 0.3)
   └─ Point Renderer      (Size: 0.02, Blend: Additive)
```

上は書式の例で、実在のプロジェクトの写しではない。
