# 起こらなかった経路 制作ノート

トポロジー・ヒルベルト空間・目的因を一本の映像にするための調査メモ（2026-11-12）。

- 全文（図つき）: https://claude.ai/artifact/3EptFoX1Fu1ZK13j6bE32N
- ページのソース: `notes.html`（冒頭の鏡の経路積分の図は同ファイル内の JavaScript）

## 要点

- **主軸は TouchDesigner。** 公式 MCP（TouchDesigner/TDMCP、公開ベータ、TD 2025.33230 以降）と公式スキル（TDMCPSkills）で、ノード作成からエラー取得・画像確認まで Claude から行える。
- **After Effects / Premiere はコミュニティ製 MCP。** Adobe 公式コネクタはデスクトップ版を操作できない。AE は kumoproductions/mcp-aftereffects、Premiere は hetpatel-11/Adobe_Premiere_Pro_MCP。編集は Claude に OTIO を書かせて読み込むのが安定。
- **Notch は本体を操作する MCP がない。** Claude が HLSL の `.fx` を書き、公開パラメータを OSC か TouchDesigner の Notch TOP で動かす。
- **中心ショットは鏡の経路積分。** 経路長 `L(x)`、矢印 `exp(i·k·L)` の総和がコルニュ螺旋になる。既製シェーダーは見つからず、GLSL の雛形を `notes.html` に記載。
- **制作モデル。** `script.json` と `scene_plan.json` を唯一の正とし、朗読を先に作り、静止画を見て直す往復を 1 ショット 3 回までに制限する。

## 未確認

- Instagram の参考リンク 5 本は、セッションのネットワーク設定の都合で閲覧できていない。
- TouchDesigner / After Effects / Notch はこの環境になく、MCP 接続とプロンプトの下書きは未検証。
