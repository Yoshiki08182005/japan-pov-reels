# アウトライヤー・フック・ライブラリ（outlier hook library）

初版：2026-11-16。機械可読版は `marketing/hook_library.json`（同内容）。毎日の PDCA で更新する（strategy.md「定常リサーチ：アウトライヤー・フック収集」参照）。

## 手法（method）
1万人フォロワー級の実践として紹介された手法（2026-11-16 ユーザー共有のマーケティングチュートリアルより採用）：
1. 同ジャンルの競合アカウントを10以上スキャンする。
2. **アウトライヤー**＝再生数（Views）がそのアカウントのフォロワー数の **5倍以上** のリールを特定する。
3. 各アウトライヤーの**冒頭3秒**（最初のフレーム／動作、最初の画面テキスト、最初の発話行）を「フック」として抽出する。
4. フックをライブラリ化し、今後の台本はこの実証済みフックから作る（ゼロから発明しない）。

## 数値の注記（重要・正直な限界）
- Instagram は他アカウントのリール Views を instagram-cli 経由で公開していない（`posts` はいいね／コメントのみ、`individual-post-insights` は自アカ専用で、競合投稿では media_not_found を確認済み）。そのため strategy.md の既存方針（**Views が取れない間はいいね数で代用**）に従い、本ライブラリの倍率は**いいねベース**。
- Views は常に Likes 以上なので、**Tier A（いいねだけでフォロワー数の5倍以上）は Views 基準でも確実にアウトライヤー**。Tier A' は投稿時点のフォロワー数（strategy.md の 2026-11-15 実測）で計算した確実枠。**Tier B（いいね 0.15〜2.1倍）は「Views では5倍を超えている可能性が高い候補」**であり、Views 自体は未確認。Tier B のフックは「候補」として扱い、確定扱いしない。
- フォロワー数は原則スキャン時点（2026-11-16）。@thejapanlogic はアウトライヤー自身がフォロワーを 3,213 → 20,644 に押し上げたため、現在数で割ると倍率が過小になる。だから Tier A' を併記する。

## スキャン範囲（2026-11-16）
18アカウント、各直近30投稿、動画339本を分析。フォロワー基盤がほぼ無い @japan.tips（15人・投稿0）、@japan.manners（4人）、@tokyo_tipsin60（0人）はランキングから除外。

| アカウント | フォロワー | 備考 |
|---|---|---|
| @thejapanlogic | 21,719 | 手本。POVアニメ。Tier A/A' を3本輩出 |
| @japan_rule | 28,594 | クレイアニメPSA「Japan's Rules」。Tier A 1本 |
| @japantravelbasics | 353,420 | 実写Tips大手。5倍基準では該当なし（母数が大きい） |
| @flipjapanguide | 185,358 | 実写ガイド大手。該当なし |
| @japan.compass | 75,176 | 実写Tips。直近30本中動画2本。該当なし |
| @japan.tips_official | 13,860 | 量産型。該当なし |
| @japantraveltips__ | 9,930 | リスト系インフォグラフィック。Tier B 3本 |
| @japan.explores | 9,502 | 写真中心。Tier B 1本 |
| @living.in.japan | 9,286 | 写真中心（直近30本中動画12本）。該当なし |
| @japan.travel.hacks | 5,144 | 実写ハック。Tier B 2本 |
| @japanhacksforyou | 3,477 | 該当なし |
| @secrets.of.japan | 3,610 | 該当なし |
| @japan_secrets_lab | 2,638 | 該当なし |
| @japan_life_samurai | 1,691 | 該当なし |
| @japan.etiquette | 566 | 写真スライド＋ナレーション。Tier B 5本（小母数のため倍率は出やすい） |

2026-11-17更新：14アカウントを再スキャン（@thejapanlogic は直近30本、他13アカウントは直近10〜12本）。新規の Tier A はなし。@thejapanlogic のフォロワーは 28,844、食券機は 369,985 いいね（12.8x）に成長。最大の動きは税関eゲートPOV（5,258 → 60,665 いいね、2.10x）で、Tier B の先頭（#5）に昇格。

## アウトライヤー一覧（倍率降順）

| # | Tier | アカウント | フォロワー | いいね | 倍率 | 日付 | 題材 | URL |
|---|---|---|---|---|---|---|---|---|
| 1 | A | @thejapanlogic | 28,844 | 369,985 | 12.8x | 2026-11-14 | 食のルール：ラーメン食券機（POV） | https://www.instagram.com/reel/DfvjjmogNRP/ |
| 2 | A | @japan_rule | 28,594 | 321,963 | 11.3x | 2026-06-08 | マナー論争：公共の場での祈り（PSA） | https://www.instagram.com/reel/DZU0aHqTzaN/ |
| 3 | A' | @thejapanlogic | 3,213（投稿時） | 37,781 | 11.8x | 2026-11-13 | 小売・お金：コンビニのトレイ（POV） | https://www.instagram.com/reel/DfscVEHAQWs/ |
| 4 | A' | @thejapanlogic | 3,213（投稿時） | 25,638 | 8.0x | 2026-11-14 | 安全・夜：新宿の客引き（POV） | https://www.instagram.com/reel/DfvBDPOjX0U/ |
| 5 | B | @thejapanlogic | 28,844 | 60,665 | 2.1x | 2026-11-15 | 入国手続き：税関eゲート（POV） | https://www.instagram.com/reel/DfyIb0rGAYg/ |
| 6 | B | @japan.travel.hacks | 5,144 | 7,181 | 1.40x | 2026-08-31 | 買い物：セブンのフリーズドライ味噌汁 | https://www.instagram.com/reel/Dcsm79ihieH/ |
| 7 | B | @japan.etiquette | 566 | 345 | 0.61x | 2026-10-30 | 旅行リスト：江戸の街並み5選 | https://www.instagram.com/reel/DfJbD9iRy2A/ |
| 8 | B | @japan.etiquette | 566 | 305 | 0.54x | 2026-11-03 | 旅行リスト：現存天守5城 | https://www.instagram.com/reel/DfTTC2thQt7/ |
| 9 | B | @japan_rule | 28,594 | 8,965 | 0.31x | 2026-06-02 | マナーPSA：竹への落書き彫り | https://www.instagram.com/reel/DZFN7Ojz-DJ/ |
| 10 | B | @japantraveltips__ | 9,930 | 2,863 | 0.29x | 2026-09-19 | 旅行リスト：大阪の穴場20選 | https://www.instagram.com/reel/DdeMYB8JzYO/ |
| 11 | B | @japantraveltips__ | 9,930 | 2,510 | 0.25x | 2026-09-26 | 買い物リスト：日本の買い物スポット12選 | https://www.instagram.com/reel/Ddv-hnlpOT2/ |
| 12 | B | @japan_rule | 28,594 | 6,869 | 0.24x | 2026-06-22 | マナーPSA：路上トイレ問題 | https://www.instagram.com/reel/DZ4yWokT7ZH/ |
| 13 | B | @japan.etiquette | 566 | 114 | 0.20x | 2026-11-13 | 旅行リスト：絶景列車5選 | https://www.instagram.com/reel/DftkhE6tTIQ/ |
| 14 | B | @japan.etiquette | 566 | 111 | 0.20x | 2026-11-01 | 旅行リスト：庭園5選 | https://www.instagram.com/reel/DfOJ3VshX_g/ |
| 15 | B | @japan.travel.hacks | 5,144 | 997 | 0.19x | 2026-08-21 | 食：大阪駅前ビル地下飲食街 | https://www.instagram.com/reel/DcS3BY7hHvS/ |
| 16 | B | @japan_rule | 28,594 | 4,772 | 0.17x | 2026-07-04 | 交通マナーPSA：新幹線の騒音 | https://www.instagram.com/reel/DaZMAzWzbHI/ |
| 17 | B | @japan.etiquette | 566 | 94 | 0.17x | 2026-11-11 | 旅行リスト：工芸の町5選 | https://www.instagram.com/reel/DfoAb9whj1t/ |
| 18 | B | @japan_rule | 28,594 | 4,490 | 0.16x | 2026-06-06 | 交通マナーPSA：ラッシュ時の巨大スーツケース | https://www.instagram.com/reel/DZRSMgYpA6b/ |
| 19 | B | @japantraveltips__ | 9,930 | 1,545 | 0.16x | 2026-09-12 | 旅行リスト：東京の穴場20選 | https://www.instagram.com/reel/DdL7zKZJenS/ |
| 20 | B | @japan.explores | 9,502 | 1,438 | 0.15x | 2026-11-14 | ホテル紹介：JWマリオット東京 | https://www.instagram.com/reel/DfuWuYdplZf/ |
## フック詳細（冒頭3秒）

### #1 [Tier A] @thejapanlogic — ラーメン食券機（12.8x）
- **冒頭3秒**：フレーム0でタイトルピル「POV: your first ramen shop in Japan」。POVが着席し、店主に直接現金を渡そうとする「間違った行動」が1秒以内に始まる。店主が驚き、全員が凝視。吹き出し＋叫び「先に食券を！」。
- **最初の発話**：「Don't sit down and call for a menu. Buy your ticket first.」（＝ルールそのもの）
- **構成**：間違い（フリーズ／凝視ギャグ）→ WRONG WAY → THE RIGHT WAY やり直し → 叫び → LED解説（THE MACHINE：TICKET / HAND IT OVER / THEN SIT）→ 判子エンドカード。
- 根拠：media-understanding のナレーション＋キャプション1行目＋ COPY_SPEC_ramen.md のビート分解で確認済み。

### #2 [Tier A] @japan_rule — 公共の場での祈り（11.3x、コメント13,175）
- **冒頭3秒**：東京の路上で祈る人々の場面から開始し、大テキスト「If you live in Japan, follow the rules」「Public Prayer — That's not how it works here」。状況説明なしで「問題行為＋禁止」が同時に画面に出る。
- **最初の発話**：「We respect your faith, we understand, but take it home, take it to your room.」
- **構成**：論争シーン → 不満のモンタージュ（給食・税金）→ スローガン → 懇願する群衆で締め。
- **注意**：伸びの主因は論争性（コメント1.3万）。借りるのは「二人称への直接の禁止＋アイデンティティの緊張をフレーム0に置く」という**フックの力学だけ**。排外的な内容そのものは我々の題材にしない（使うのは形式だけ、という既存方針通り）。
- 根拠：media-understanding＋キャプション1行目。

### #3 [Tier A'] @thejapanlogic — コンビニのトレイ（投稿時11.8x）
- **冒頭3秒**：タイトルピル「POV: your first konbini in Japan」の下で、POVが店員（Mio）に現金を直接手渡す間違いが即座に始まり、WRONG WAY スタンプ。
- **最初の発話**：「Cash goes on the little tray, not in the clerk's hand.」
- **構成**：間違い → 巻き戻し → THE RIGHT WAY（買い物→トレイ→お釣り）→ LED解説 → エンドカード。
- 根拠：media-understanding＋キャプション1行目。

### #4 [Tier A'] @thejapanlogic — 新宿の客引き（投稿時8.0x）
- **冒頭3秒**：夜の街POV。客引きがカメラに近づき、**登場人物自身がフックを喋る**：「Hey, my friend! Looking for a bar? Pretty girls, cheap drinks. Just down here」。数秒で路地へ誘導が始まる。ナレーションでなく「自分に話しかけてくる他者」が脅威。
- **構成**：間違い（ついて行く）→ WRONG WAY → リセット → RIGHT WAY（警察の「DON'T FOLLOW TOUTS」看板→自分で店を選ぶ→明朗会計¥930）→ 解説（本当の罠は請求額）→ CASE エンドカード。
- 根拠：media-understanding＋キャプション1行目。

### #5 [Tier B] @thejapanlogic — 税関eゲート（2.1x）
- **冒頭3秒**：飛行機の窓からの富士山＋スカイツリーの美景に「POV: your first landing in Japan」。直後に混雑した税関ホールの長い列と苛立つ旅行者（WRONG WAY）へ。美景→痛点の順。
- **最初の発話**：「POV: your first landing in Japan, and the customs line goes on forever.」
- **構成**：痛点 → 巻き戻し → RIGHT WAY（機内で Visit Japan Web、QR＋パスポート、eゲート）→ 情報カード。
- **教訓（2026-11-17 訂正）**：2026-11-16 時点では最弱級（5,258 いいね）に見えたが、翌日 60,665 いいね（同アカ2位）へ爆発。手続き説明型POVでも遅れてブレイクすることがある。判定は24hではなく48hで行う。フックは「美景→痛点」の順で、痛点（終わらない税関の列）が WRONG WAY として即座に来る。
- 根拠：media-understanding＋キャプション1行目。

### #6 [Tier B] @japan.travel.hacks — フリーズドライ味噌汁（1.40x）
- **冒頭3秒**：フリーズドライ味噌汁ブロック（豆腐・ねぎが見える）を握る手のアップ＋大テキスト「DON'T LEAVE JAPAN WITHOUT BUYING THIS!」。商品・主張・命令がフレーム0に全部ある。
- **構成**：命令＋商品 → 10秒デモ（お湯を注ぐ）→ 4種＋¥108 → 「小さく軽い」スーツケース → 試食リアクション → 自宅で楽しむ締め。
- 根拠：media-understanding（冒頭テキストを明示）＋キャプション1行目。

### #7 [Tier B] @japan.etiquette — 江戸の街並み5選（0.61x）
- **冒頭3秒**：保存された木造商家の街並みの画＋ナレーション第一声の最上級主張「Japan has preserved entire streets that look exactly like they did two centuries ago.」（200年前そのまま、というタイムトラベル約束）。
- **構成**：最上級主張 → 5か所リスト（静止画）→ 書籍プロモ。
- 根拠：ナレーション＋キャプション1行目から一部推定（3秒境界は未分離）。

### #8 [Tier B] @japan.etiquette — 現存天守5城（0.54x）
- **冒頭3秒**：青空の姫路城ワイドショット。第一声は「Most travelers visit Japan's famous temples and shrines. But five original castle keeps…」という「多数派が見逃している」コントラスト。
- **構成**：コントラスト → 5城リスト → 書籍プロモ。
- 根拠：ナレーション＋キャプション1行目から一部推定。

### #9 [Tier B] @japan_rule — 竹への彫り（0.31x）
- **冒頭3秒**：竹林・神社境内にオレンジジャケットの観光客が入場し、ナイフで竹に「HAILEY TOM 24」と彫る**違反行為そのもの**が冒頭のフック。直後に地元民＋マスコットが詰め寄る。
- **最初の発話（キャプション1行目）**：「Did you come all the way to Japan just to carve your name into bamboo?」
- **構成**：違反 → 対峙 → 回想（竹と神社の数百年）→「keep your hands off what isn't yours」→ 恥じた観光客 → 礼儀正しい観光客の締め。
- 根拠：ナレーションは冒頭シークエンスを確認、発話はキャプション由来（一部推定）。

### #10 [Tier B] @japantraveltips__ — 大阪の穴場20選（0.29x）
- **冒頭3秒**：大阪の地図グラフィック＋赤丸＋大見出し「20 BEST Hidden Gems to Discover in OSAKA」。フックは「数（20）＋穴場」のタイトルカード。
- **構成**：地図タイトル → 4カテゴリ（自然／歴史／博物館／遊び）の写真リスト → 保存誘導。
- 根拠：形式＋キャプションから一部推定（音楽主体で発話フックなし）。

### #11 [Tier B] @japantraveltips__ — 買い物スポット12選（0.25x）
- **冒頭3秒**：混雑した横断歩道の映像の上に半透明パネル「The 12 Best Shopping Spots in JAPAN」＋日本国旗。数字リストの約束を象徴的な街映像に重ねる。
- **構成**：タイトル → 12店を4群（ロゴ＋商品3点＋一言）→ お礼エンドカード。
- 根拠：形式＋キャプションから一部推定。

### #12 [Tier B] @japan_rule — 路上トイレ問題（0.24x）
- **冒頭3秒**：赤い星柄パジャマの男がラーメン店街で腹を押さえて悶え、画面テキスト「If you're coming to Japan, use the toilet.」。周囲が凝視する羞恥ギャグ＋直接命令。
- **構成**：恥ずかしい行為 → 実写カット「We don't do that」→ マスコット解説 → 清潔なトイレの締め。
- 根拠：media-understanding（冒頭明示）＋キャプション。

### #13 [Tier B] @japan.etiquette — 絶景列車5選（0.20x）
- **冒頭3秒**：海岸線を走る青い列車の空撮＋命令テキスト「Pick a window seat.」。最高の景色＋小さな指示。
- 根拠：ナレーション＋キャプション1行目から一部推定。

### #14 [Tier B] @japan.etiquette — 庭園5選（0.20x）
- **冒頭3秒**：庭園の景色に「Most tourists photograph the same famous temples in Kyoto and Tokyo. But Japan's greatest gardens are quieter, less crowded…」の「みんなと違う」コントラスト第一声。
- 根拠：ナレーション＋キャプション1行目から一部推定。

### #15 [Tier B] @japan.travel.hacks — 大阪駅前ビル地下飲食街（0.19x）
- **冒頭3秒**：赤いビールケース机の地下バルの手ブレ実写に大テキスト「Most Tourists Visiting Japan Don't Know This! Osaka's HUGE Underground Food District」。無知ギャップの主張＋混沌とした実写。
- **構成**：主張 → 場所説明（大阪駅・4ビル・地図）→ 地下へ → 歩行映像＋料理アップ＋価格 → 「THIS IS EVERYDAY OSAKA」。
- 根拠：media-understanding（冒頭テキスト明示）＋キャプション1行目。

### #16 [Tier B] @japan_rule — 新幹線の騒音（0.17x）
- **冒頭3秒**：東京駅に到着する新幹線アニメ＋日英テキスト「If you come to Japan, follow the rules」。整然と乗車する「正しい世界」を先に見せ、直後に車内で踊る若者たちの実写へ。
- **最初の発話（キャプション1行目）**：「The Shinkansen is not a club. It's not your living room.」
- 根拠：media-understanding（冒頭明示）＋キャプション。

### #17 [Tier B] @japan.etiquette — 工芸の町5選（0.17x）
- **冒頭3秒**：陶器店が並ぶ伝統的な通りの景色＋「持ち帰る物の物語を知ろう」という誘い。第一声は土産の再定義「You can buy a souvenir anywhere. But what if the thing you brought home had centuries of history woven into it?」
- 根拠：ナレーションはオーバーレイ文を言い換えで伝達、発話はキャプション1行目（一部推定）。

### #18 [Tier B] @japan_rule — 巨大スーツケース（0.16x）
- **冒頭3秒**：新宿駅の混雑した電車ドア（「1302」表示）が巨大スーツケースの家族で物理的に塞がれ、画面テキスト「Giant suitcase on the rush hour train.」。ホームのサラリーマンが乗れない。被害が視覚的に即座に伝わる。
- **構成**：ドア封鎖 → 乗り遅れ → 上司に叱られる（「because of you」）→ マスコットがタクシーを提案 → バス車内の迷惑 → 「Think about us for once.」
- 根拠：media-understanding（冒頭明示）＋キャプション。

### #19 [Tier B] @japantraveltips__ — 東京の穴場20選（0.16x）
- **冒頭3秒**：東京中心部の地図アニメ＋赤丸ポップ＋「20 Best Hidden Gems to Discover in TOKYO」。#9 と同じ数字・地図フックの使い回し（＝型として再利用されている証拠）。
- 根拠：形式＋キャプションから一部推定。

### #20 [Tier B] @japan.explores — JWマリオット東京（0.15x）
- **冒頭3秒**：夜の屋内インフィニティプール越しに東京タワーが光る画。テキストも声もなく、環境音楽だけの「純粋な視覚的ラグジュアリー」フック。我々の形式との適合は最弱だが、このアカウントの倍率トップのため記録。
- 根拠：media-understanding（冒頭明示）。

## 使い方（制作への接続）
- **各エピソードの冒頭3秒は、このライブラリのエントリ（原則 Tier A/A'）のフック構造を題材に合わせて適応する**。ゼロから発明しない。使ったエントリはエピソードのメタデータ（spec の pdca / next.json）に `hook_source` として記録する（FORMAT.md「Hook」ルール、daily.md 企画・台本セクション参照）。
- 借りるのはフックの**構造と力学**（例：間違った行動を1秒以内に開始／登場人物自身がフックを喋る／命令形テキスト＋商品アップ／違反行為そのものを見せる）。台本・絵・言い回しの複写はしない。論争系（#2）は内容でなく力学だけ。
- Tier B は題材カテゴリが Tier A に無いときの候補プール。使う場合は「候補」と自覚し、実績が出たら格上げする。
- 更新：日次 PDCA で競合を再スキャンし、新規アウトライヤーを追加、倍率を更新する。Views が取得できる手段が将来できたら倍率を Views ベースに切り替える。
