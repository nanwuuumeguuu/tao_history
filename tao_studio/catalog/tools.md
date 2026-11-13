# 道具の目録

## TouchDesigner
| 名前 | 場所 | 何ができるか | 条件・注意 | 確認 |
|---|---|---|---|---|
| TDMCP（Derivative 公式） | github.com/TouchDesigner/TDMCP | ノード作成・配線・パラメータ・DAT・エラー取得・画像確認・Python 実行。26 ツール | 公開ベータ。TD 2025.33230 以降。`execute_code` はシェル同等 | 直 |
| TDMCPSkills（公式スキル 20 本） | github.com/TouchDesigner/TDMCPSkills | `td-general` `td-glsl-shaders` `td-pop-family` など | `td-` 接頭辞は予約 | 直 |
| 8beeeaaat/touchdesigner-mcp | github.com/8beeeaaat/touchdesigner-mcp | 14 ツール。最も普及 | MIT。古い TD 向けの代替 | 直 |
| johnsabath/touchdesigner-mcp | github.com/johnsabath/touchdesigner-mcp | `observe`（PNG/GIF）、`render`（MP4）、`map`（ネットワークのテキスト地図） | MIT。見て直す往復に強い | 直 |
| satoruhiga/claude-touchdesigner | github.com/satoruhiga/claude-touchdesigner | 4 ツール＋`td-guide` スキル | MIT | 直 |
| bottobot/touchdesigner-mcp-server | github.com/bottobot/touchdesigner-mcp-server | 資料検索専用。オペレータ JSON、GLSL の型 16、雛形 | MIT。TD には接続しない | 直 |
| Embody | github.com/dylanroscover/Embody | ネットワークをテキスト（TDXN）に書き出す | MIT。`.toe` を棚に入れる手段 | 直 |

## Notch
| 名前 | 場所 | 何ができるか | 条件・注意 | 確認 |
|---|---|---|---|---|
| Notch マニュアル MCP | manual.notch.one（MCP の節） | マニュアル検索のみ | 本体は操作できない | 直 |
| JavaScript ノード | マニュアルの JavaScript リファレンス | 全ノードの列挙、作成、親子付け、値の読み書き、ログ出力、HTTP | このリポジトリの `tools/notch_dump.js` が実例。Notch 1.0.2.030 で動作確認 | 直 |
| カスタムシェーダー（.fx） | マニュアル「working with custom shaders」 | HLSL を外部で編集、保存で再読込 | Claude が書ける唯一の描画コード | 直 |
| OSC／Notch TOP | マニュアル | 公開パラメータを外から動かす | TD の MCP 経由で間接操作できる | 直 |

## Adobe
| 名前 | 場所 | 何ができるか | 条件・注意 | 確認 |
|---|---|---|---|---|
| Adobe for creativity コネクタ | Claude のコネクタ | 簡易タイムラインのレンダリング（10 分まで）、リサイズ、1 フレーム確認、音声分離、画像編集 | デスクトップ版 AE／Premiere は操作不可 | 直 |
| ローカル MCP 連携（Ps/Ai/Pr/Ae） | Adobe MAX 2026 で予告 | 外部エージェントからデスクトップ版を操作 | 非公開ベータは 2027 年初頭予定。未提供 | 要約 |
| kumoproductions/mcp-aftereffects | github.com/kumoproductions/mcp-aftereffects | AE のコンポ・レイヤー・1 フレーム書き出し。読み取り専用モードあり | 導入 1 行。AE 2024–2026 | 直 |
| Dakkshin/after-effects-mcp | github.com/Dakkshin/after-effects-mcp | AE 操作の元祖 | ScriptUI パネル方式 | 直 |
| Arman-Luthra/aftr | github.com/Arman-Luthra/aftr | 仕様→適用→レンダ→見直しの往復 | CEP パネル | 直 |
| aedev-tools/adobe-agent-skills | github.com/aedev-tools/adobe-agent-skills | MCP なしで ExtendScript を書いて実行 | macOS のみ | 直 |
| hetpatel-11/Adobe_Premiere_Pro_MCP | github.com/hetpatel-11/Adobe_Premiere_Pro_MCP | Premiere 操作 283 ツール | タイトル／テロップは API の制約大 | 直 |
| mikechambers/adb-mcp | github.com/mikechambers/adb-mcp | Ps/Pr/Id/Ae/Ai | 概念実証 | 直 |

AE／Premiere 共通の注意：ダイアログが出ると止まる。ExtendScript は ES3 のみ。呼び出しは直列。作業前に複製。

## そのほか
| 名前 | 場所 | 何ができるか | 条件・注意 | 確認 |
|---|---|---|---|---|
| blender-mcp | github.com/ahujasid/blender-mcp | Python 実行、ビューポート確認、3D 生成の呼び出し | MIT | 直 |
| davinci-resolve-mcp | github.com/samuelgursky/davinci-resolve-mcp | タイムライン操作 | 外部スクリプトは Studio 版が必要 | 直 |
| Remotion スキル | github.com/remotion-dev/skills | React で動画をコード生成 | | 直 |
| HyperFrames | github.com/heygen-com/hyperframes | HTML を決定論的に MP4 化 | Apache-2.0 | 直 |
| video-use | github.com/browser-use/video-use | 実写の粗編集。文字起こしを読んで EDL を書く | ElevenLabs のキーが必要 | 直 |
| OpenMontage | github.com/calesthio/OpenMontage | 台本→場面表→素材→編集の段階と JSON スキーマ | AGPL-3.0。構成の参考に | 直 |
| manim-skill | github.com/Yusuke710/manim-skill | 朗読を先に作り、Manim を音に合わせる | | 直 |
| scroll-world | github.com/oso95/scroll-world | 静止画→つなぎ動画→スクロール再生 | MIT | 直 |
| film-studio-skills | github.com/machina-exm/film-studio-skills | AI 映像のショットカードと一貫性の関門 | ライセンス表記なし | 直 |
| zbrush-mcp | github.com/newsbubbles/zbrush-mcp | ZBrush の周辺操作 | MIT。実験的 | 直 |
| WhisperX | github.com/m-bain/whisperX | 話者と単語時刻つきの文字起こし | BSD-2 | 直 |
| Zotero MCP | github.com/54yyyu/zotero-mcp | 文献管理、撤回通知 | MIT | 直 |
| arXiv MCP | github.com/blazickjp/arxiv-mcp-server | 論文検索、主題の見張り | Apache-2.0 | 直 |
| RefChecker | github.com/markrussinovich/refchecker | 引用の実在確認 | | 直 |
| fabric | github.com/danielmiessler/fabric | `analyze_claims` `dialog_with_socrates` などの指示文 | | 直 |
