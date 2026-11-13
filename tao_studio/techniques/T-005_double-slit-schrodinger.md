---
id: T-005
name: 二重スリットの干渉縞（シュレーディンガー方程式を解く）
status: unverified
tools: [TouchDesigner, GLSL, Python]
source: qmsolve（BSD-3）、double-slit-2d-schrodinger（MIT）、解説 davidar.io/post/quantum-glsl
license: 上記のとおり
automation: claude-writes-code
---

## 何ができるか
波束が 2 つの隙間を同時に抜け、向こう側に縞ができるまでを計算で見せる。色相＝位相、明るさ＝確率。

## 仕組み
波動関数を実部 R と虚部 I に分け、半歩ずらして交互に更新する（Visscher の方法。FFT が要らないので GLSL TOP と Feedback TOP で組める）。
- R ← R + dt·(−½∇²I + V·I)
- I ← I − dt·(−½∇²R + V·R)
∇² は上下左右 4 点との差。壁は V を大きくする。dt は格子間隔の 2 乗の 1/4 より小さく。

## 手順
1. まず Python（qmsolve）で同じ設定を動かし、縞の間隔を記録する。これが正解になる。
2. GLSL TOP 2 枚（R 用、I 用）を rgba32float で作り、Feedback TOP で往復させる。
3. 初期状態はガウス波束 exp(−|r|²/σ²)·exp(i·k·x)。
4. 表示用の TOP で hue=atan(I,R)、value=R²+I² にする。
5. 1 の結果と縞の間隔を比べる。合えば verified。

## 発展
粒子を v = Im(∇ψ/ψ) で流すとボーム軌道（交わらない流線）。光源側と検出器側から別々に解いて掛け合わせると「終わりから来る波」。

## 注意
未検証。更新式は標準的だが、このカードの形では動かしていない。端での反射を消すには、縁で振幅を少しずつ減らす。
