---
id: T-001
name: 鏡の経路積分（全経路の矢印の和）
status: unverified
tools: [TouchDesigner, GLSL]
source: 自作。数式は標準的な波動光学
license: 自作
automation: claude-writes-code
---

## 何ができるか
光源→鏡の各点→検出器の全経路に位相の矢印を割り当て、足し合わせで残る経路だけを光らせる。鏡を削ると端の経路も光る。

## 仕組み
経路長 L(x)=r1+r2、矢印 exp(i·k·L)、k=2π/λ。L'(x)=0 が入射角＝反射角。矢印を順につなぐとコルニュ螺旋。削る条件は cos(k·L−φ0)>0 の点だけ残す。

## 手順
1. GLSL TOP（rgba32float）に下のコードを入れ、検出器 D を画素座標にする。
2. 波長は鏡の長さの 1/30〜1/100 に誇張する。
3. 経路の線は別の TOP で描き、加算合成する。

```glsl
vec2 A = vec2(0.);
float dx = (b - a) / float(N);
for (int j = 0; j < N; j++) {
  float x  = mix(a, b, (float(j) + .5) / float(N));
  float r1 = length(vec2(x - S.x, S.y)), r2 = length(vec2(x - D.x, D.y));
  float L  = r1 + r2, dL = (x - S.x)/r1 + (x - D.x)/r2;
  float z  = .5 * k * dL * dx;
  float w  = dx * (abs(z) < 1e-4 ? 1. : sin(z)/z);
  float keep = scrape ? step(0., cos(k*L - phi0)) : 1.;
  A += keep * w * vec2(cos(k*L - wt), sin(k*L - wt));
}
float I = dot(A, A);
```

## 注意
同じ式はブラウザでは動作確認済み。TouchDesigner 上では未検証。関連する主張：C-0002、C-0003。
