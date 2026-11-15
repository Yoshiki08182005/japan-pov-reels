# COPY SPEC — faithful reproduction of @thejapanlogic's ramen ticket reel (57k likes at analysis, 2026-11-15)

Source deconstruction (browser observation, timings ±2s, total ~38-40s). This is the beat sheet to reproduce. Format/structure/gags are the target; series branding is ours (Japan First Times).

## Why it works (the comedy mechanics — do not lose these)
1. **The freeze is the joke.** Cold open: POV hand offers a ¥1000 bill directly to the owner. Owner AND all 3 customers freeze mid-motion, eyes wide, mouths small black ovals, staring. Held ~3s. No dialogue needed.
2. **The verdict stamp.** A giant red diagonal stamp "WRONG WAY" slams across the whole screen (oversized, cropped by the frame edges). Success later gets the same treatment in green: "RIGHT WAY". Stamp + slam SE = punctuation.
3. **The same-bill rhyme.** The exact same ¥1000 bill: wrong way → handed to the owner; right way → fed into the machine's NOTES slot. Same hand, same bill, different destination.
4. **Silence → shout.** After the ticket is handed over quietly, the owner shouts 「はい、ラーメン一丁！」with a big open mouth. Contrast is the laugh.
5. **The wait.** Owner turns his back and cooks with a big ladle; protagonist waits at an empty counter, fists resting; other customers keep eating unbothered. Held 2-3s.
6. **Instant finish.** Full bowl → jump cut → empty bowl (chopsticks resting on it). No eating shown. The time-skip is the gag.
7. **Deadpan narration + karaoke subtitles.** Calm male EN narration, mostly over the explainer section; subtitles highlight word by word.
8. **Stamp end card.** A circular stamp-style end card brands the episode as one "case" in a series; follow prompt inside the stamp design.

## Beat sheet (target ~40s)
| # | Time | Visual | Text / audio |
|---|------|--------|--------------|
| 1 | 0-3s | Counter POV. Right hand offers ¥1000 bill to owner; left fist on counter. Owner (ladle + bowl in hand) and 3 customers FROZEN, wide eyes, staring at the hand. Slow push-in. | Title pill top: "POV: your first ramen shop in Japan". Short gasp SE. Near-silence. |
| 2 | 3-5s | Wide shot of ticket machine by the door (sign: 食券を先にどうぞ / red band "食券 BUY YOUR TICKET HERE"). Giant red diagonal stamp slams in: WRONG WAY. | Stamp slam SE. |
| 3 | 5-7s | Shop exterior: sign 麺屋 ろじ MENYA ROJI · RAMEN, red lantern ラーメン, noren, OPEN sign. Green pill center: THE RIGHT WAY. POV fists at bottom. | Chapter SE. |
| 4 | 7-11s | Machine close-up. Right hand inserts the SAME ¥1000 bill into NOTES slot; display ¥1000→¥0. Yellow buttons with prices (Ramen ¥850 etc.). Hand takes the ¥850 ticket from the slot. | Machine beeps, ticket print SE. |
| 5 | 11-15s | Inside, seated POV. Hand passes ticket to owner (face close-up). Owner takes it, then SHOUTS. | Speech bubble: 「はい、ラーメン一丁！」+ loud JP voice. |
| 6 | 15-19s | Owner's back, cooking with big ladle. Empty counter in front of POV, both fists waiting. Customers eating. | Near-silence, faint cooking sounds. |
| 7 | 19-23s | Owner places the bowl (blue rim, chashu, half egg, naruto, negi, nori). Green diagonal stamp slams: RIGHT WAY. Right hand picks up chopsticks. | Stamp SE + success tone. |
| 8 | 23-27s | JUMP CUT: empty bowl, chopsticks resting across it, only broth/egg remains. Held. | Small satisfied SE. |
| 9 | 27-31s | Black explainer card 1: orange LED text "THE MACHINE" + simple machine icon. | Narration: "At many ramen shops, the machine by the door is the menu and the cashier." (karaoke subs) |
| 10 | 31-35s | Black card 2: LED "TICKET FIRST". | Narration: "Buy your ticket first, hand it over, then sit." |
| 11 | 35-38s | Black card 3: LED "AT COUNTER" + small owner icon "ORDER HERE". | Narration: "No machine? Order at the counter." |
| 12 | 38-42s | End card: circular stamp design, our branding: "JAPAN FIRST TIMES · CASE No.1 RAMEN TICKET · FOLLOW FOR MORE". | Narration: "That's Japan first times. Follow for more." Light BGM throughout at low volume. |

## Character / art spec (flat 2D illustration, AI-generated frames)
- Thick black outlines, flat colors, minimal shading, chibi proportions (head ~1/3 of body).
- Owner: round head, peach skin, black hair, white hachimaki headband, navy long sleeves, white apron with red trim; eyes = big white circles with small black pupils; freeze face = pupils small, mouth small black oval, brows raised.
- Customers: red sweater man, green top brown-hair person, blue cap person — same line style.
- Protagonist: never seen except forearms + hands, mustard/ochre long sleeves with folded cuffs, peach skin, simplified 4-finger hands. Left hand mostly a fist; right hand does the actions.
- Interior: beige walls, brown wainscot, grey tile floor, hanging lamps, red お品書き MENU sign, vertical menu cards, light wood counter. Machine: red top, white body, navy base, yellow buttons.
- Bowl: blue-rimmed, brown broth.

## Production rules
- Freeze beats are STILLS held full duration (that is the gag). Push-ins are slow (≤5% scale).
- Stamps animate: scale from 3x → 1x with a hard stop + slam SE, slight rotation (-12°).
- Every narration word-highlight subtitle matches the moshimo karaoke style if available in the engine, else word-timed white/bold subs.
- Length 38-44s. Vertical 1080x1920.
