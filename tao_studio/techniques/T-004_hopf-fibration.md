---
id: T-004
name: ホップ・ファイブレーション（球面の点を円の束にする）
status: unverified
tools: [TouchDesigner, Blender]
source: Niles Johnson の制作ノート、mwalczyk/hopf（CC BY 4.0）
license: 数式は自由。コードを写すなら出典を表示
automation: claude-writes-code
---

## 何ができるか
球面上の 1 点が、4 次元の球の中の 1 つの円に対応する。どの 2 つの円も必ず 1 回だけ絡む。量子ビット 1 個の状態空間（実 4 次元）を目に見える形にする唯一に近い方法。

## 仕組み
球面の点 (θ, φ) に対する円：q(t) = (cos(θ/2)·e^{i(t+φ)/2}, sin(θ/2)·e^{i(t−φ)/2})、t は 0〜4π。
4 次元の点 (x, y, z, w) を (x, y, z)/(1−w) で 3 次元に投影する。

## 手順
1. Python で円ごとの点列を作る（1 円あたり 128 点ほど）。
2. TouchDesigner なら Geometry COMP の instancing でチューブにする。色相＝球面上の経度。
3. 球面上の点を緯線に沿って動かすと、入れ子のドーナツ面が現れる。
4. 投影の前に xw 面と yz 面の回転をかけると、4 次元の回転が見える。

## 注意
極を通る円は無限遠へ伸びる直線になる。カメラの遠方クリップに注意。関連：glossary「ヒルベルト空間」、C-0008。
