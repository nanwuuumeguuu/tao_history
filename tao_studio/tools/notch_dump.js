// Notch プロジェクトのノードグラフを、ログにテキストとして書き出す。
//
// 使い方（Notch Builder）:
//   1. 調べたい .dfx を開く（元ファイルを守るため、複製を開くこと）。
//   2. Resources パネルで右クリック → Import Resource → Script → JavaScript でこのファイルを読み込む。
//   3. JavaScript ノードを作り、このスクリプトを割り当てる。再生すると1回だけ書き出す。
//   4. View → Log Window で「TAO|END」が出たら完了。ログは Documents/Notch/Logs にある。
//   5. python tools/notch_log_to_graph.py <ログファイル> --course <コース名> --project <名前>
//   6. 保存せずに閉じる。
//
// 使っている関数はすべて Notch 2026.2 マニュアルの JavaScript リファレンスに載っているもの。
// Notch 上での動作は未検証。値を読むだけで、ノードの作成・変更・削除はしない。

// 2回目以降に値も読みたいとき、ノードの種類ごとにプロパティ名を足す。
// 名前はマニュアルのノードリファレンスで確かめること。例:
//   "Cameras::Orbit Camera": ["Attributes.Zoom", "Transform.Position X"]
var TAO_PROPS = {};

var taoDone = false;

function taoId(node) {
    var p = [0, 0];
    try { p = node.GetNodeGraphPosition(); } catch (e) {}
    if (!p || p.length < 2) p = [0, 0];   // 位置を返さないノードがある
    return node.GetName() + "@" + Math.round(p[0]) + "," + Math.round(p[1]);
}

function taoLinks(node, countFn, getFn) {
    var out = [];
    try {
        var n = node[countFn]();
        for (var i = 0; i < n; i++) {
            var other = node[getFn](i);
            if (other) out.push(taoId(other));
        }
    } catch (e) {}
    return out;
}

// そのオブジェクトで呼べる関数名を全部書き出す。マニュアルに載っていない
// 関数（入力接続やプロパティの一覧など）が無いかを調べるため。
function taoApi(label, obj) {
    var names = [];
    try { for (var k in obj) names.push(k); } catch (e) {}
    try {
        var p = Object.getPrototypeOf(obj), depth = 0;
        while (p && depth < 6) {
            var own = Object.getOwnPropertyNames(p);
            for (var i = 0; i < own.length; i++) names.push(own[i]);
            p = Object.getPrototypeOf(p); depth++;
        }
    } catch (e) {}
    try { Log("TAO|API|" + JSON.stringify({ object: label, names: names })); } catch (e) {}
}

function taoDump() {
    Log("TAO|BEGIN|" + JSON.stringify({ version: GetNotchVersion() }));
    try {
        taoApi("global", (function () { return this; })());
        taoApi("Document", Document);
        taoApi("UpdateContext", UpdateContext);
        var l0 = Document.GetLayer(0);
        taoApi("Layer", l0);
        taoApi("Node", l0.GetNodes()[0]);
    } catch (e) { Log("TAO|APIERR|" + e); }
    var numLayers = Document.GetNumLayers();
    for (var l = 0; l < numLayers; l++) {
        var layer = Document.GetLayer(l);
        if (!layer) continue;
        Log("TAO|LAYER|" + JSON.stringify({
            index: l, name: layer.GetName(),
            start: layer.GetStartTime(), end: layer.GetEndTime()
        }));
        var nodes = layer.GetNodes();
        for (var i = 0; i < nodes.length; i++) {
            var node = nodes[i];
            if (!node) continue;
            try {
            var rec = { layer: l, id: taoId(node), name: node.GetName() };
            try { rec.type = node.GetCategoryAndType(); } catch (e) { rec.type = "?"; }
            try { rec.pos = node.GetNodeGraphPosition(); } catch (e) {}
            try { rec.visible = node.GetVisible(); } catch (e) {}
            try { rec.start = node.GetStartTime(); rec.end = node.GetEndTime(); } catch (e) {}
            rec.children = taoLinks(node, "GetNumChildren", "GetChild");
            rec.parents = taoLinks(node, "GetNumParents", "GetParent");
            rec.embeds = taoLinks(node, "GetNumEmbeds", "GetEmbed");
            var names = TAO_PROPS[rec.type];
            if (names) {
                rec.props = {};
                for (var k = 0; k < names.length; k++) {
                    try { rec.props[names[k]] = node.GetFloat(names[k]); } catch (e) {}
                }
            }
            Log("TAO|NODE|" + JSON.stringify(rec));
            } catch (e) { Log("TAO|SKIP|" + JSON.stringify({ layer: l, index: i, error: "" + e })); }
        }
    }
    Log("TAO|END|");
}

function Update() {
    if (taoDone) return;
    taoDone = true;
    taoDump();
}
