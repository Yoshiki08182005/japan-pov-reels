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

2026-11-18更新：13アカウントを再スキャン（@thejapanlogic は直近30本、他12アカウントは2026-11-17以降の投稿）。新規の Tier A はなし。@thejapanlogic のフォロワーは 37,462 にさらに増加。食券機は 384,451 いいね（10.3x）、eゲートは 72,627 いいね（1.94x）に成長。新規ブレイクアウトは Tier B に3本追加（#21〜#23）：温泉POV 59,024 いいね（1.58x）、チップ断りPOV 31,566 いいね（0.84x）、回転寿司POV 18,079 いいね（0.48x、約22hで最速の伸び）。旅館スリッパPOVは300いいねで不発。@japan.explores はユーザー名が解決せず（tokyo.explores のフィードを返したため対象外）、@flipjapanguide／@japantravelbasics は5倍基準が約0.9M／1.8Mいいねと一晩では到達不能のため未再スキャン。

2026-11-19更新：11アカウントを再スキャン（@thejapanlogic は直近30本、他10アカウントは2026-11-17以降の投稿）。新規の Tier A はなし。@thejapanlogic のフォロワーは 42,517 にさらに増加。食券機は 394,212 いいね（9.3x）、eゲートは 77,307 いいね（1.8x）に成長。新規ブレイクアウトは Tier B に1本追加（#24）：改札・残高不足POV 7,693 いいね（0.18x、約22h）。旅館スリッパPOVは 300 → 3,561 いいねに1日で急伸（0.08xで Tier B 基準未満のためライブラリには追加せず、strategy.md の市場メモに記録）。箸立てPOV（2026-11-18）は383いいねと弱い出足で様子見。回転寿司POVは 18,079 → 69,656 いいね（1.64x）に伸長中。他10アカウントに新規アウトライヤーなし。

2026-11-20更新：11アカウントを再スキャン（@thejapanlogic は直近30本、他10アカウントは2026-11-17以降の投稿）。新規の Tier A はなし。@thejapanlogic のフォロワーは 46,868 にさらに増加。食券機は 403,024 いいね（8.6x）、eゲートは 79,377 いいね（1.69x）に成長。新規ブレイクアウトは Tier B に1本追加（#25）：箸立てPOV 383 → 25,956 いいね（0.55x、約1日で急伸）— 遅れてくるブレイクの4例目。自アカの ep16 chopsticks_rice はこのニアコピーで、今朝制作済み・検証PASS。改札・残高不足POVも 7,693 → 35,780 いいね（0.76x）に伸長中。新規POVは2本：公園の空きペットボトルPOV 4,446 いいね（0.095x、Tier B 基準未満のため様子見）、女性専用車両POV 245 いいねで弱い出足。旅館スリッパPOVは 3,561 → 4,618 いいねと緩やかに伸長中。他10アカウントに新規アウトライヤーなし。@japan.etiquette のフォロワーは 612、絶景列車5選は 114 → 129 いいね（#13、0.21x）。

2026-11-21更新：8アカウントを再スキャン（@thejapanlogic 直近30本、@japan_rule 直近10本・最終投稿2026-10-27で新規なし、他6アカウントは2026-11-17以降の投稿）。新規の Tier A はなし。@thejapanlogic のフォロワーは 48,412 にさらに増加。食券機は 407,627 いいね（8.4x）、eゲートは 80,737 いいね（1.67x）に成長。新規ブレイクアウトは Tier B に1本追加（#26）：公園の空きペットボトルPOV 4,446 → 16,034 いいね（0.33x、1日で3.6倍）— 遅れてくるブレイクの5例目。コピー優先ルールにより本日昼枠の次エピソードに指定（topics.json の matsuri_garbage にフックを適応）。箸立てPOVも 25,956 → 28,273 いいね（0.58x）に伸長中。新規POVは2本：新幹線・指定席POV 3,659 いいね（約22h、様子見）、居酒屋「すみません」POV 348 いいねで弱い出足（自アカの未使用 sumimasen と同ルールのため当面見送り）。女性専用車両POVは 245 → 2,148 いいねと1日で8.8倍に急伸中（0.04x、様子見）。旅館スリッパPOVは 4,618 → 5,071 いいねと緩やかに伸長中。他アカウントでは @japan.explores のカツ丼コメディが 4,288 いいね（0.45x）と同アカでは突出しているが、POVルール形式ではなく自アカ形式に適応できないためライブラリには追加せず様子見。

2026-11-22更新：14アカウントを再スキャン（@thejapanlogic 直近30本、他13アカウントは2026-11-17以降の投稿）。新規の Tier A はなし。@thejapanlogic のフォロワーは 51,670 にさらに増加。食券機は 411,860 いいね（8.0x）、eゲートは 82,208 いいね（1.59x）に成長。新規ブレイクアウトは Tier B に2本追加：#27 新幹線・指定席POV 3,659 → 11,853 いいね（0.23x、1日で3.2倍）— 遅れてくるブレイクの6例目、#28 居酒屋「すみません」POV 348 → 38,887 いいね（0.75x、1日で111倍）— 遅れてくるブレイクの7例目で、遅れてくるブレイクの中で最大の1日ジャンプ。昨日の「すみませんは当面見送り」判断は覆った（eゲート／箸立て／公園ゴミと同じ構図）。コピー優先ルールにより #28 を本日昼枠（sumimasen）、#27 を今夜枠（新規トピック shinkansen_seat）に指定。女性専用車両POVは 2,148 → 2,605 いいね（0.05x、Tier B 基準未満のため様子見継続）。新規POVは2本：ストリートゴーカート 388 いいね、奈良の鹿せんべい 2,806 いいね（0.05x、様子見）。旅館スリッパPOVは 5,071 → 5,477 いいねと緩やかに伸長中。@japan.etiquette の旅行リスト「定番5都市しか回らない旅程」が 122 いいね（0.19x）で #29 に追加（ナレーションリストのため自アカ形式には適応不可、記録のみ）。他アカウントに新規アウトライヤーなし。@japan.explores はユーザー名が解決せず対象外（前回と同じ）。

## アウトライヤー一覧（#1〜#20は倍率降順。#21以降は追加順とし、エピソードの hook_source 引用番号を安定させる）

| # | Tier | アカウント | フォロワー | いいね | 倍率 | 日付 | 題材 | URL |
|---|---|---|---|---|---|---|---|---|
| 1 | A | @thejapanlogic | 51,670 | 411,860 | 8.0x | 2026-11-14 | 食のルール：ラーメン食券機（POV） | https://www.instagram.com/reel/DfvjjmogNRP/ |
| 2 | A | @japan_rule | 28,594 | 321,963 | 11.3x | 2026-06-08 | マナー論争：公共の場での祈り（PSA） | https://www.instagram.com/reel/DZU0aHqTzaN/ |
| 3 | A' | @thejapanlogic | 3,213（投稿時） | 53,282 | 16.6x | 2026-11-13 | 小売・お金：コンビニのトレイ（POV） | https://www.instagram.com/reel/DfscVEHAQWs/ |
| 4 | A' | @thejapanlogic | 3,213（投稿時） | 29,836 | 9.3x | 2026-11-14 | 安全・夜：新宿の客引き（POV） | https://www.instagram.com/reel/DfvBDPOjX0U/ |
| 5 | B | @thejapanlogic | 51,670 | 82,208 | 1.59x | 2026-11-15 | 入国手続き：税関eゲート（POV） | https://www.instagram.com/reel/DfyIb0rGAYg/ |
| 6 | B | @japan.travel.hacks | 5,144 | 7,181 | 1.40x | 2026-08-31 | 買い物：セブンのフリーズドライ味噌汁 | https://www.instagram.com/reel/Dcsm79ihieH/ |
| 7 | B | @japan.etiquette | 566 | 345 | 0.61x | 2026-10-30 | 旅行リスト：江戸の街並み5選 | https://www.instagram.com/reel/DfJbD9iRy2A/ |
| 8 | B | @japan.etiquette | 566 | 305 | 0.54x | 2026-11-03 | 旅行リスト：現存天守5城 | https://www.instagram.com/reel/DfTTC2thQt7/ |
| 9 | B | @japan_rule | 28,594 | 8,965 | 0.31x | 2026-06-02 | マナーPSA：竹への落書き彫り | https://www.instagram.com/reel/DZFN7Ojz-DJ/ |
| 10 | B | @japantraveltips__ | 9,930 | 2,863 | 0.29x | 2026-09-19 | 旅行リスト：大阪の穴場20選 | https://www.instagram.com/reel/DdeMYB8JzYO/ |
| 11 | B | @japantraveltips__ | 9,930 | 2,510 | 0.25x | 2026-09-26 | 買い物リスト：日本の買い物スポット12選 | https://www.instagram.com/reel/Ddv-hnlpOT2/ |
| 12 | B | @japan_rule | 28,594 | 6,869 | 0.24x | 2026-06-22 | マナーPSA：路上トイレ問題 | https://www.instagram.com/reel/DZ4yWokT7ZH/ |
| 13 | B | @japan.etiquette | 612 | 129 | 0.21x | 2026-11-13 | 旅行リスト：絶景列車5選 | https://www.instagram.com/reel/DftkhE6tTIQ/ |
| 14 | B | @japan.etiquette | 566 | 111 | 0.20x | 2026-11-01 | 旅行リスト：庭園5選 | https://www.instagram.com/reel/DfOJ3VshX_g/ |
| 15 | B | @japan.travel.hacks | 5,144 | 997 | 0.19x | 2026-08-21 | 食：大阪駅前ビル地下飲食街 | https://www.instagram.com/reel/DcS3BY7hHvS/ |
| 16 | B | @japan_rule | 28,594 | 4,772 | 0.17x | 2026-07-04 | 交通マナーPSA：新幹線の騒音 | https://www.instagram.com/reel/DaZMAzWzbHI/ |
| 17 | B | @japan.etiquette | 566 | 94 | 0.17x | 2026-11-11 | 旅行リスト：工芸の町5選 | https://www.instagram.com/reel/DfoAb9whj1t/ |
| 18 | B | @japan_rule | 28,594 | 4,490 | 0.16x | 2026-06-06 | 交通マナーPSA：ラッシュ時の巨大スーツケース | https://www.instagram.com/reel/DZRSMgYpA6b/ |
| 19 | B | @japantraveltips__ | 9,930 | 1,545 | 0.16x | 2026-09-12 | 旅行リスト：東京の穴場20選 | https://www.instagram.com/reel/DdL7zKZJenS/ |
| 20 | B | @japan.explores | 9,502 | 1,438 | 0.15x | 2026-11-14 | ホテル紹介：JWマリオット東京 | https://www.instagram.com/reel/DfuWuYdplZf/ |
| 21 | B | @thejapanlogic | 51,670 | 84,827 | 1.64x | 2026-11-16 | 入浴マナー：温泉・洗ってから入る（POV） | https://www.instagram.com/reel/Df0vwvcjZt5/ |
| 22 | B | @thejapanlogic | 51,670 | 48,842 | 0.95x | 2026-11-16 | お金：チップ断り・店員が釣りを追いかける（POV） | https://www.instagram.com/reel/Df1BjSgJct-/ |
| 23 | B | @thejapanlogic | 51,670 | 84,755 | 1.64x | 2026-11-17 | 食のルール：回転寿司・皿を戻すな（POV） | https://www.instagram.com/reel/Df2vY8-pdZi/ |
| 24 | B | @thejapanlogic | 51,670 | 40,747 | 0.79x | 2026-11-18 | 交通のルール：改札・残高不足でゲートが閉まる（POV） | https://www.instagram.com/reel/Df5UMUSAcXj/ |
| 25 | B | @thejapanlogic | 51,670 | 30,621 | 0.59x | 2026-11-18 | 食のルール：箸立て・ご飯に箸を立てるな（POV） | https://www.instagram.com/reel/Df52mWtHGWW/ |
| 26 | B | @thejapanlogic | 51,670 | 18,073 | 0.35x | 2026-11-19 | 公共マナー：公園・空きペットボトルを置き去りにするな（POV） | https://www.instagram.com/reel/Df75LLRkq1e/ |
| 27 | B | @thejapanlogic | 51,670 | 11,853 | 0.23x | 2026-11-20 | 交通のルール：新幹線・指定席に座るな（POV） | https://www.instagram.com/reel/Df-d3t9E-af/ |
| 28 | B | @thejapanlogic | 51,670 | 38,887 | 0.75x | 2026-11-20 | 会話のルール：居酒屋・店員を待たずに「すみません」と呼ぶ（POV） | https://www.instagram.com/reel/Df_AUr1kubj/ |
| 29 | B | @japan.etiquette | 629 | 122 | 0.19x | 2026-11-18 | 旅行リスト：定番5都市しか回らない旅程（ナレーション） | https://www.instagram.com/reel/Df5xt4UxDjQ/ |
## フック詳細（冒頭3秒）

### #1 [Tier A] @thejapanlogic — ラーメン食券機（10.3x）
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

### #3 [Tier A'] @thejapanlogic — コンビニのトレイ（投稿時13.9x）
- **冒頭3秒**：タイトルピル「POV: your first konbini in Japan」の下で、POVが店員（Mio）に現金を直接手渡す間違いが即座に始まり、WRONG WAY スタンプ。
- **最初の発話**：「Cash goes on the little tray, not in the clerk's hand.」
- **構成**：間違い → 巻き戻し → THE RIGHT WAY（買い物→トレイ→お釣り）→ LED解説 → エンドカード。
- 根拠：media-understanding＋キャプション1行目。

### #4 [Tier A'] @thejapanlogic — 新宿の客引き（投稿時8.4x）
- **冒頭3秒**：夜の街POV。客引きがカメラに近づき、**登場人物自身がフックを喋る**：「Hey, my friend! Looking for a bar? Pretty girls, cheap drinks. Just down here」。数秒で路地へ誘導が始まる。ナレーションでなく「自分に話しかけてくる他者」が脅威。
- **構成**：間違い（ついて行く）→ WRONG WAY → リセット → RIGHT WAY（警察の「DON'T FOLLOW TOUTS」看板→自分で店を選ぶ→明朗会計¥930）→ 解説（本当の罠は請求額）→ CASE エンドカード。
- 根拠：media-understanding＋キャプション1行目。

### #5 [Tier B] @thejapanlogic — 税関eゲート（1.9x）
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

### #21 [Tier B] @thejapanlogic — 温泉・洗ってから入る（1.58x）
- **冒頭3秒**：タイトルピル「POV: your first onsen in Japan」の下で、POVが走ってきてそのまま湯船に飛び込む間違いが即座に始まる。入浴客が凝視。最初の発話がルールそのもの（「Don't run in and jump straight into the bath. Wash first.」）。
- **最初の発話**：「POV: your first onsen in Japan. Don't run in and jump straight into the bath. Wash first.」
- **構成**：間違い（飛び込み）→ WRONG WAY → THE RIGHT WAY（洗い場の椅子で体を洗ってから入る、タオルは湯に入れない）→ 静かに浸かる締め。
- 根拠：キャプション1行目＋2026-11-18の posts スキャン（冒頭の細部はキャプション構造からの推定。media-understanding 未実施）。

### #22 [Tier B] @thejapanlogic — チップ断り・店員が釣りを追いかける（0.84x）
- **冒頭3秒**：タイトルピル「POV: your first restaurant in Japan」の下で、POVが釣りをチップとして断り、店員が釣り銭を持って通りまで追いかけてくる。間違った行動とその滑稽な帰結が冒頭数秒に両方ある。
- **最初の発話**：「POV: your first restaurant in Japan. You wave off your change as a tip, and the staff chase you down the street with it.」
- **構成**：間違い（釣りを断る）→ WRONG WAY → THE RIGHT WAY（受け取って「ありがとう」、それだけ）→ 締め。
- **備考**：未使用トピック no_tipping と同じルール。このエントリは no_tipping のフック参照として使う。
- 根拠：キャプション1行目＋2026-11-18の posts スキャン（冒頭の細部はキャプション構造からの推定。media-understanding 未実施）。

### #23 [Tier B] @thejapanlogic — 回転寿司・皿を戻すな（1.64x）
- **冒頭3秒**：タイトルピル「POV: your first conveyor sushi in Japan」の下で、POVがレーンから取った皿を戻す間違いが即座に始まる。ベルトと監視カメラが画面内にある。
- **最初の発話**：「POV: your first conveyor sushi in Japan, and you put the plate back.」
- **構成**：間違い（皿をレーンに戻す）→ WRONG WAY → THE RIGHT WAY（取った皿は自分のもの。欲しいものはタッチパネルで注文）→ 締め。
- **備考**：2026-11-18スキャンで最速の伸び（投稿約22hで18,079いいね）。コピー優先ルールにより本日昼枠の次エピソードに指定（topics.json の conveyor_sushi）。2026-11-19時点で 69,656 いいね（1.64x）に伸長中。
- 根拠：キャプション1行目＋2026-11-18の posts スキャン（冒頭の細部はキャプション構造からの推定。media-understanding 未実施）。

### #24 [Tier B] @thejapanlogic — 改札・残高不足でゲートが閉まる（0.18x）
- **冒頭3秒**：タイトルピル「POV: your first ticket gate in Japan」の下で、POVが残高不足のICカードをタップし、ゲートが目の前で閉まる。後ろにはラッシュアワーの列。間違った行動（残高を確認せずにタップ）とその公開の帰結が冒頭数秒に両方ある。
- **最初の発話**：「POV: your first ticket gate in Japan, and your IC card is empty.」
- **構成**：間違い（残高不足でタップ→ゲートが閉まる）→ WRONG WAY → THE RIGHT WAY（先にチャージする：券売機で現金、または Apple Wallet に Suica へ入金。タップは平らに当てて通る）→ 締め。
- **備考**：2026-11-19スキャンの新規ブレイクアウト（投稿約22hで7,693いいね、コメント19）。自アカの ep09（Suica改札・挿すなタップせよ）とは別角度（残高不足）で、ep09が前日比+220と最も伸びている最中でもある。コピー優先ルールにより今夜の夜枠（交通／安全）の次エピソードに指定（topics.json の ic_empty）。
- 根拠：キャプション1行目＋2026-11-19の posts スキャン（冒頭の細部はキャプション構造からの推定。media-understanding 未実施）。

### #25 [Tier B] @thejapanlogic — 箸立て・ご飯に箸を立てるな（0.55x）
- **冒頭3秒**：タイトルピル「POV: your first set meal in Japan」の下で、POVがご飯に箸を立てる間違いが即座に始まり、テーブル全員が凝視。タブー（立てた箸＝葬式の供え物）がパンチライン。
- **最初の発話**：「POV: your first set meal in Japan, and you just stood your chopsticks up in the rice.」
- **構成**：間違い（箸を立てる、フリーズ／凝視、店員の叫び）→ WRONG WAY → THE RIGHT WAY（箸置きに横に置く、茶碗は手に持つ）→ 解説カード → エンドカード。#1/#3 と同じ Tier A テンプレート。
- **備考**：遅れてくるブレイクの4例目。2026-11-19時点では383いいねの弱い出足だったが、翌日 25,956 いいね（0.55x）に急伸。自アカの ep16 chopsticks_rice はこのニアコピーで、2026-11-20朝枠に制作済み・PDCA検証PASS。
- 根拠：キャプション1行目＋2026-11-20の posts スキャン（冒頭の細部はキャプション構造からの推定。media-understanding 未実施）。

### #26 [Tier B] @thejapanlogic — 公園・空きペットボトルを置き去りにするな（0.33x）
- **冒頭3秒**：タイトルピル「POV: your first park in Japan」の下で、POVが空きペットボトルをベンチに置き去りにして立ち去る間違いが即座に始まり、周囲の公園利用者が凝視。ゴミ箱がほとんど無い日本の公共空間という前提がパンチライン。
- **最初の発話**：「POV: your first park in Japan, and you just left your empty bottle on the bench.」
- **構成**：間違い（ボトルを置き去り、凝視）→ WRONG WAY → THE RIGHT WAY（ゴミは持ち帰る。公共のゴミ箱はほとんど無い）→ 締め。#1/#3 と同じ Tier A テンプレート。
- **備考**：遅れてくるブレイクの5例目。2026-11-20時点では4,446いいね（0.095x）で様子見だったが、翌日 16,034 いいね（0.33x）に1日で3.6倍に急伸。コピー優先ルールにより本日昼枠の次エピソードに指定（topics.json の matsuri_garbage にフックを適応）。
- 根拠：キャプション1行目＋2026-11-21の posts スキャン（冒頭の細部はキャプション構造からの推定。media-understanding 未実施）。

### #27 [Tier B] @thejapanlogic — 新幹線・指定席に座るな（0.23x）
- **冒頭3秒**：タイトルピル「POV: your first bullet train in Japan」の下で、POVが指定席に座る間違いが即座に始まり、正規の乗客がやって来て凝視。座席番号を確認しない間違いとその公開の帰結が冒頭数秒に両方ある。
- **最初の発話**：「POV: your first bullet train in Japan, and you just sat in someone's reserved seat.」
- **構成**：間違い（指定席に座る、正規の乗客が来る、凝視）→ WRONG WAY → THE RIGHT WAY（切符の座席番号を確認する。指定がなければ自由席車両へ）→ 締め。#1/#3 と同じ Tier A テンプレート。
- **備考**：遅れてくるブレイクの6例目。2026-11-21時点では3,659いいね（0.08x）で様子見だったが、翌日 11,853 いいね（0.23x）に1日で3.2倍に急伸。コピー優先ルールにより今夜の夜枠の次エピソードに指定（新規トピック shinkansen_seat）— 実験枠として、自アカの交通48h中央値（318回、食の22%）をブレイクアウトのコピーで超えられるか試す。
- 根拠：キャプション1行目＋2026-11-22の posts スキャン（冒頭の細部はキャプション構造からの推定。media-understanding 未実施）。

### #28 [Tier B] @thejapanlogic — 居酒屋・店員を待たずに「すみません」と呼ぶ（0.75x）
- **冒頭3秒**：タイトルピル「POV: your first izakaya in Japan」の下で、POVがテーブルで黙って店員を待つ間違いが即座に始まり、周りの居酒屋は動き続けるのにテーブルだけが止まっている。黙って待つ（自国式）という間違いとその帰結（誰も来ない）が冒頭数秒にある。
- **最初の発話**：「POV: your first izakaya in Japan, and you're still waiting for the server to come over.」
- **構成**：間違い（黙って待つ、誰も来ない）→ WRONG WAY → THE RIGHT WAY（「すみません」と声に出して呼ぶ — 大きく、失礼ではなく仕組み）→ 締め。#1/#3 と同じ Tier A テンプレート。
- **備考**：遅れてくるブレイクの7例目で、遅れてくるブレイクの中で最大の1日ジャンプ。2026-11-21時点では348いいねの弱い出足で「当面見送り」と判断していたが、翌日 38,887 いいね（0.75x）に1日で111倍に急伸。コピー優先ルールにより本日昼枠の次エピソードに指定（自アカの未使用 sumimasen と同じルール）。
- 根拠：キャプション1行目＋2026-11-22の posts スキャン（冒頭の細部はキャプション構造からの推定。media-understanding 未実施）。

### #29 [Tier B] @japan.etiquette — 旅行リスト・定番5都市しか回らない旅程（0.19x）
- **冒頭3秒**：都市モンタージュの上のナレーション — 「Most Japan itineraries hit the same five cities. You get great food and crowds.」リスト形式で、POVの間違い行動のオープニングはない。
- **最初の発話**：「Most Japan itineraries hit the same five cities. You get great food and crowds.」
- **構成**：リストのナレーション（WRONG WAY / RIGHT WAY の構造なし）。同アカのリストリール #7/#8/#13/#14/#17 と同じ型。
- **備考**：@japan.etiquette の新規リストリール（フォロワー629）。倍率では Tier B（0.19x）だがナレーションリストで POV の間違い行動型ではなく、自アカ形式には適応できないため記録のみ、キューには入れない。
- 根拠：キャプション1行目＋2026-11-22の posts スキャン。

## 使い方（制作への接続）
- **各エピソードの冒頭3秒は、このライブラリのエントリ（原則 Tier A/A'）のフック構造を題材に合わせて適応する**。ゼロから発明しない。使ったエントリはエピソードのメタデータ（spec の pdca / next.json）に `hook_source` として記録する（FORMAT.md「Hook」ルール、daily.md 企画・台本セクション参照）。
- 借りるのはフックの**構造と力学**（例：間違った行動を1秒以内に開始／登場人物自身がフックを喋る／命令形テキスト＋商品アップ／違反行為そのものを見せる）。台本・絵・言い回しの複写はしない。論争系（#2）は内容でなく力学だけ。
- Tier B は題材カテゴリが Tier A に無いときの候補プール。使う場合は「候補」と自覚し、実績が出たら格上げする。
- 更新：日次 PDCA で競合を再スキャンし、新規アウトライヤーを追加、倍率を更新する。Views が取得できる手段が将来できたら倍率を Views ベースに切り替える。
