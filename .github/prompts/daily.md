あなたは Instagram 英語圏アカウント @japan.first.times（日本の日常ルールを一人称POVで教えるリール）の制作担当。目的は**総再生回数を伸ばすこと**。**目標は1本あたり再生数500,000回**（marketing/strategy.md の判定ルール参照）。GitHub Actions 上（Linux、GPUなし）で動画を1本作る。投稿・gitコミット・通知は後のステップが行うので、あなたはしない。ユーザーへの確認は不要。トークンを節約する（読むのは必要な範囲だけ）。

**形式は ep02 v4 で承認された標準形式に固定**（`posts/` の見本と `engine/build_2d_std.py` が実装）。旧3Dエンジン（engine/engine/*.js、render.py）は**使わない**。

最初に必ず読む：`FORMAT.md`（形式と Production checklist、特に **1秒ルール**とナレーション全編ルール）、`COPY_SPEC_ramen.md`（笑いの仕掛け7つ）、`marketing/strategy.md`（カテゴリ実測・見切りルール・500k目標）、`PIPELINE.md`（工程とゲート）、見本 `engine/episodes/ep02_ramen_ticket.spec.json` 相当の ep03 `engine/episodes/ep03_izakaya_otoshi.spec.json` と両エピソードの `.script.json`。

## 1. 企画
- **1回の実行で1本だけ制作する**（1日3回実行され、毎回キューから1本消費する）。
- 題材は `engine/topics.json` の未使用（used が null）から、**時間帯スロットでカテゴリを回転**させて選ぶ。スロットは環境変数 `SLOT`（morning / midday / night / manual）で渡される。manual のときは現在の JST 時刻から判定する（5〜9時=morning、10〜16時=midday、17〜24時=night）。
  - morning（完了目標 07:00 JST）：**food**
  - midday（完了目標 12:30 JST）：**retail → money → arrival** の順で空いているもの
  - night（完了目標 21:30 JST）：**transit → safety** の順で空いているもの
  - そのスロットのカテゴリが全部使用済みなら、etiquette / conversation / events → 他カテゴリの順で未使用を取る。
- **同じカテゴリを同日に重ねない**：当日に既に作られたエピソード（`git log --since=<今日0時>` のコミットと `engine/episodes/` の当日分）を確認し、そのカテゴリは今日は選ばない（スロットの候補が全部重なる場合のみ例外）。
- 選んだカテゴリの中で、topics.json の並び順（＝市場データの優先度順）で最初の未使用を取る。無ければ TOPICS.md の方針でそのカテゴリに3つ足してから使う。
- 実在の店舗名・商標（セブン-イレブン等の固有名称、ロゴ、制服の模倣）は使わない。参考アカウント（@thejapanlogic）の台本・絵・言い回しを写さない。使うのは形式と仕掛けだけ。

## 2. ビートシート設計（標準の骨格、合計38〜44秒）
ep02/ep03 と同じ13ビート＋カード3枚＋エンドカードで設計する：
1. **freeze_in（0.7s、クリップ）**：POVの手が「間違った行動」を始める。周囲は生きている。
2. **freeze_hold（0.75s）**：全員フリーズ。店員＋客全員が目を見開いて手を見る。**静止はこの0.75秒だけ**（前後に動きとパンチズームで挟む）。
3. **freeze_c1 / c2（各0.75〜0.8s、パンチズームcrop）**：店員＋小道具 → 店員の顔へ寄る。
4. **verdict（2.0s）**：場面のワイド。**赤い WRONG WAY スタンプ**が +0.35s に叩き込まれる。静止画なら強いズームパン（1.0→1.26級）を付ける。
5. **chapter（2.0s）**：店の外観など章扉。緑の **THE RIGHT WAY** ピルがポップ。
6. **正解の行動その1（2.2s、クリップ）**：同じ小道具の「韻」——間違いと同じ手・同じ物、正しい行き先。
7. **正解の行動その2（1.8s）**：クリップ、または crop 2枚のパンチ構成。
8. **shout（4.0s、クリップ）**：店員に渡す／注文する。ナレーションが言いかけて**遮られ**、店員の日本語の叫び（吹き出し＋JP音声、+7dB）。叫びの上に英語ナレーションを絶対に被せない。
9. **waiting（5.0s、クリップ）**：店員は調理中、客は食べ続け、POVの拳だけ止まっている「間」。
10. **payoff（4.0s、クリップ）**：成功の瞬間。**緑の RIGHT WAY スタンプ** +0.6s＋成功音。
11. **punch（3.0s、クリップ）**：ジャンプカット的な落ち（空の皿／レシート等）＋引用したくなるパンチライン。
12. **カード1〜3（各約3〜4s）**：黒背景＋オレンジLED。ルールの要約（物語の繰り返しではなく圧縮）。アイコンは毎フレーム動く（machine / ticket / owner / dish / coin から題材に合うもの）。
13. **エンドカード（約3.5s）**：判子が叩き込まれ、リング文字が回り続け、FOLLOW FOR MORE が鼓動する。CASE No. は連番。

## 3. フレーム生成（engine/episodes/epNN_<slug>_frames/f1..f9.jpg、1152×2048）
- 利用可能な画像生成ツールで9枚作る。**固定スタイルブロック**を全プロンプトにそのまま入れる：「Flat 2D cartoon illustration for a vertical 9:16 portrait video frame (tall composition). Thick black outlines, flat colors, minimal shading, chibi proportions.」＋場所の描写＋**キャラクター定義を一字一句同じに**（店員の髪型・服装・色、客3人の組み合わせ、主人公は「mustard ochre long sleeves with folded cuffs, peach skin, simplified four-finger hands」の腕と手だけ）。
- f1 はフリーズ用：店員と客全員が目を見開き口を小さく開けて手を見ていること。crop 位置（spec の crops）は f1/f5 を Read で見てから決める。
- **画像生成ツールが使えない環境では、ここで止めて report.md にその旨を書く。** 3Dエンジンや静止画だけへのフォールバックは禁止（標準形式が崩れる）。

## 4. クリップ生成（engine/episodes/epNN_<slug>_clips/、704×1248・24fps）
- image-to-video で「生きているビート」を全部動画化する：freeze_in / 正解の行動 / shout / waiting / payoff / punch は必須。生成枠が足りない場合のみ、verdict / chapter / 行動その2 を「強いズームパン＋グラフィック演出（スタンプ・ピル）」や crop パンチ構成で代替してよい。**知覚的に1秒以上止まる区間はどこにも作らない**（最終ゲート＝モーション監査）。
- 生成後は安定した名前（freeze_in.mp4 等）にリネームし、1秒間隔のフレーム差分で本当に動いているか確認する。絵柄が崩れたクリップは使わない。

## 5. 台本（engine/episodes/epNN_<slug>.script.json と _jp.script.json）
- EN: voice `en-US-GuyNeural`、rate `+8%`（淡々と）。行は s1〜s9（物語）＋ n1〜n3（カード）＋ n4（締め）。
  - **s1 は「場面＋間違い」の一文**（挨拶・説明から始めない）。以降はビートに1行ずつ、短く（目安：1行 45字以内、チェーンに収まる長さ。builder の assert が落ちたら行を短くする）。
  - s6 は言いかけで切れる行（「She grinned—」型）。shout の JP 音声と重ならない配置は spec の constraints で保証する。
  - punch 行（s9）は例外か「本当だけど変」な引用したくなる一文（例："Rent for your chair. Served as a snack."）。
  - 字幕チャンクは `|` 区切り、**1チャンク最大7語**。
- JP: voice `ja-JP-KeitaNeural`、shout 行1つ（店員の叫び。吹き出しの文と完全一致させる）。

## 6. spec（engine/episodes/epNN_<slug>.spec.json）
ep03 の spec を雛形に、art（タイトルピル文・吹き出し文）/ crops / segments / cards / endcard / shout / narration（chains・singles・constraints）/ sfx / pdca（topic・category・rule・hook・gags）を書く。SFX は全ビートに付ける（場面転換 whoosh、スタンプ impact_don、成功 sparkle、カード text_tin、調理 sizzle 等。キーは sfx-library/sfx.json 参照）。

## 7. ビルドとゲート（必須・省略不可）
作業ディレクトリは engine。
1. `python voice.py epNN_<slug>` と `python voice.py epNN_<slug>_jp`
2. `python build_2d_std.py epNN_<slug>`（assert で落ちたら台本を短くして再実行。**絵のビートは動かさない**）
3. `python motion_audit.py out/epNN_<slug>/final.mp4 out/epNN_<slug>/motion_audit.txt out/epNN_<slug>/motion_strip.jpg out/epNN_<slug>/meta.json`
   - **VERDICT: PASS でなければ投稿可にしない。** 止まっている区間を特定し、クリップ差し替え／ズーム強化／カット追加で直して再ビルド（修正は2回まで）。直らなければ next.json を書かず、report.md に「監査FAIL・投稿不可」と明記する。
4. **視聴者チェック（自分の目で検証）**：`out/epNN_<slug>/sheet.jpg` と motion_strip.jpg を Read で見る。確認点：テロップが顔・キー小道具に被っていない／手が不自然でない／スタンプと吹き出しが出ている／フリーズが「全員固まって手を見ている」と読める／カードとエンドカードが動いている。問題があれば直す（2回まで）。

## 8. 書き出し
1. `engine/out/next.json` を書く：{"ep", "topic", "caption", "cover", "category", "hook", "rule", "length_s", "gags"}。
   - **キャプションの1行目は二択の質問**（例："Send it back or just eat it — what did you do with the dish you never ordered? 👇"）。続けて FORMAT.md のキャプションテンプレ通り。ハッシュタグは固定セット `#japantravel #japantrip #firsttimeinjapan #japantips` ＋題材タグ1つ。**一字ずつ確認する（誤字タグは厳禁）**。
   - length_s は meta.json の duration。hook は s1 の文、gags は使った仕掛けの配列（PDCAで再生数と紐付けるため正確に）。
   - cover は [1.0, "POV:|your first|<場面>", "in Japan", ""] 形式。
2. topics.json の該当 topic に used = エピソード名を入れる。

## 9. PDCA（毎回、制作の前後に行う）
- **制作前**：`marketing/strategy.md` を読み、カテゴリ別の最新の中央値と見切りルール、**500k目標に対する現在地**を確認してから題材を選ぶ（1. 企画のスロット回転が基本。ただし見切りルールで優先度を下げたカテゴリは、その分後ろに回す）。
- **数値の記録**：過去のエピソードについて48h以上経った時点の数値（再生数、取れなければいいね数）が `engine/posted.json` や取得可能なデータから分かる場合は、未記録分を `marketing/strategy.md` の判断ログに1行で追記する（日付・エピソード・カテゴリ・48h数値）。あわせてカテゴリ別の本数と中央値を更新し、必要なら strategy.md のカテゴリ表も書き換える。数値は next.json / meta.json の PDCA メタデータ（topic・category・hook・length・gags）と紐付けて、**どのフック・どの仕掛けが伸びたか**を判断できるようにする。
- **見切りルールの適用**：strategy.md の「見切りのルール」に該当するカテゴリが出たら、ルール通りに topics.json の優先順位を入れ替える／派生題材を足す。その変更と根拠の数字を判断ログに1行残す。
- **投稿時間帯**：strategy.md の「投稿時間帯の検証」に従う。データが取れない間は初期値を変えない。

## 10. 報告（engine/out/report.md、日本語・短く）
```
🎬 今回：<題材>（ルールの一文）
⏱ 尺：<総秒数>秒／ペイオフ到達：<秒>（<％>）
🎞 監査：モーション監査 PASS/FAIL（静止1秒区間 <n> 件）
🖼 検証：sheet で見たビートと直した点
```
