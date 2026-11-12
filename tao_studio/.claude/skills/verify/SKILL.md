---
name: verify
description: ledger/ の未確認の主張を文献で確かめ、状態を更新する。「確かめて」「検証して」と言われたときに使う。
---

# 確かめる

1. `status: unverified` の主張を一覧にし、どれから確かめるかを示す。
2. 主張ごとに、種類に合った確かめ方をする：
   - FACT / THEORY：教科書、総説、原論文。二次的な記事だけで済ませない。
   - INTERPRETATION：誰の立場か、対立する立場は何か。両方の出典を載せ、`contested` にする。
   - METAPHYSICAL：誰の議論か、前提は何か。
   - FIRST-PERSON：いつの、どの一回か。本人に聞き直す問いを作る（なぜ、ではなく、どのように）。
   - METAPHOR：確かめる対象ではない。たとえの対応と破綻点が書かれているかだけ見る。
3. `evidence_for` / `evidence_against` には出典と**原文の引用**を入れる。原文を開けなかった出典は載せてもよいが、それだけでは `verified` にしない。
4. `source_reliability` と `info_credibility` は別々に付ける。
5. `verified` にしてよいのは、原文つきの証拠があり、`verified_by` `verified_on` `recheck_after` を埋めたときだけ。
6. 開けなかったページ、見つからなかったものは `note` にそのまま書く。
7. 確かめる作業は `verifier` エージェントに任せ、主張の文面は直さない。直しが要るなら提案として返す。
