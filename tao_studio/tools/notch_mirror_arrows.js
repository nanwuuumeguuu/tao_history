// 鏡の下の「回る矢印の列」を、正しい位相で動かす。
//
// 光源 → 鏡の上の点 x → 検出器 の経路長 L(x) から位相 k·L(x) を計算し、
// Exposable Array の各要素の位置・回転・色に書き込む。Array Cloner がそれを矢印として並べる。
// 作り方は techniques/T-013_notch-phase-arrows-build.md。
//
// Notch 上では未検証。数式は鏡の図（制作ノートのページ）と同じもの。

var ARRAY_NAME = "Exposable Array";  // 書き込む先のノード名
var N = 81;          // 矢印の本数。Exposable Array の Num Transforms と Array Cloner の Num Clones をこの数以上に
var WIDTH = 10.0;    // 鏡の長さ（x は -WIDTH/2 〜 +WIDTH/2）
var SRC = [-4.0, 3.4];   // 光源の位置（x, 鏡からの高さ）
var DET = [4.0, 3.4];    // 検出器の位置
var LAMBDA = 0.6;    // 波長。見やすいように大きく誇張してある。小さくすると隣どうしの向きの差が大きくなる
                     // （小さくしすぎると、隣との差が半回転を超えて向きの流れが読めなくなる。そのときは N を増やす）
var SPEED = 0.25;    // 1 秒あたりの回転数。0 にすると止まる
var SIZE = 0.15;     // 矢印の大きさ
var ROT_SLOT = 2;    // 位相を入れる回転の成分（0, 1, 2）。画面の中で時計のように回らなければ変えてみる
var USE_DEGREES = false;  // 回転が小さすぎて動いて見えないときは true に
var SCRAPE = false;  // true で「打ち消す部分の鏡を削る」。削られた所の矢印は大きさ 0 になる
var COLOUR = true;   // 位相を色相にして色を書き込む（Array Cloner の Colour Clones を ON に）

var warned = false;

function pathLength(x) {
    var a = x - SRC[0], b = x - DET[0];
    return Math.sqrt(a * a + SRC[1] * SRC[1]) + Math.sqrt(b * b + DET[1] * DET[1]);
}

function hueToRgb(h) {            // h は 0〜1
    var r = Math.abs(h * 6 - 3) - 1, g = 2 - Math.abs(h * 6 - 2), b = 2 - Math.abs(h * 6 - 4);
    return [Math.max(0, Math.min(1, r)), Math.max(0, Math.min(1, g)), Math.max(0, Math.min(1, b))];
}

function Update() {
    var node = UpdateContext.Layer.FindNode(ARRAY_NAME);
    if (!node) {
        if (!warned) { Log("mirror_arrows: 「" + ARRAY_NAME + "」というノードが見つかりません"); warned = true; }
        return;
    }
    var TWO_PI = 6.283185307179586;
    var k = TWO_PI / LAMBDA;
    var t = UpdateContext.LocalTime;
    var phase0 = k * pathLength((SRC[0] + DET[0]) / 2);   // 正反射の点での位相
    for (var i = 0; i < N; i++) {
        var x = -WIDTH / 2 + WIDTH * i / (N - 1);
        var kl = k * pathLength(x);
        var phase = kl - TWO_PI * SPEED * t;
        var turn = phase / TWO_PI; turn = turn - Math.floor(turn);          // 0〜1
        var angle = USE_DEGREES ? turn * 360 : turn * TWO_PI;
        var rot = [0, 0, 0]; rot[ROT_SLOT] = angle;
        var s = (SCRAPE && Math.cos(kl - phase0) <= 0) ? 0 : SIZE;
        node.SetTransformArrayPRS(i, x, 0, 0, rot[0], rot[1], rot[2], s, s, s);
        if (COLOUR) {
            var c = hueToRgb(turn);
            node.SetTransformArrayColour(i, c[0], c[1], c[2], 1);
        }
    }
}
