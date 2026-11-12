---
id: T-002
name: 連番画像をスクロールで再生するウェブ体験
status: unverified
tools: [web, Vite, canvas]
source: pear.no の観察と、有志の再現コード github.com/oosuhada/pear.no（ライセンスなし・読むだけ）
license: 手法は一般的。再現コードは写さない
automation: claude-writes-code
---

## 何ができるか
動画を連番画像にし、スクロール位置に応じてコマを canvas に描く。3D に見えるが実体は再生。

## 手順
1. 動画（生成でも TouchDesigner の書き出しでも）を WebP の連番にする。
2. 8 コマに 1 コマを先読み用にまとめ、残りを後から読む。
3. 画面幅ごとに解像度を分ける（例：1440 と 768）。
4. スクロール量→コマ番号の対応を作り、場面の継ぎ目は最初と最後のコマをそろえる。

## 自動化
github.com/oso95/scroll-world（MIT）が同様の流れをスキル化している。未検証。
