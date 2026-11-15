"""Post the episode described in engine/out/next.json as an Instagram Reel — JAPAN POV account ONLY.

SAFETY GATES (all must pass, in this order, before anything is uploaded):
  1. env JAPAN_POV_PUBLISH must be exactly "true"   (repo variable vars.JAPAN_POV_PUBLISH — default unset = disabled)
  2. env JAPAN_POV_USERNAME must be set              (repo variable vars.JAPAN_POV_USERNAME — the new account's username)
  3. the IG account behind IG_USER_ID / IG_ACCESS_TOKEN (THIS repo's own secrets — never reuse the
     moshimo-reels secrets) must report username == JAPAN_POV_USERNAME via the Graph API, else abort.
  4. DRY_RUN=1 skips the actual posting.
Uses the Instagram Graph API (system-user token, graph.facebook.com) with a resumable upload.
The cover image is prepended as a 0.2s title card and selected with thumb_offset.
"""
import datetime, json, os, subprocess, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENG = os.path.join(ROOT, "engine")


class ApiError(Exception):
    pass


def http(method, url, data=None, headers=None, raw=None):
    body = raw if raw is not None else (urllib.parse.urlencode(data).encode() if data else None)
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise ApiError(f"HTTP {e.code} {e.read().decode()[:600]}")


def with_cover(video, cover, out):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", "0.2", "-i", cover, "-i", video, "-filter_complex",
                    "[0:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[c];[1:v]setsar=1,fps=30,format=yuv420p[v];"
                    "[c][v]concat=n=2:v=1:a=0[vv];[1:a]adelay=200|200[aa]",
                    "-map", "[vv]", "-map", "[aa]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)


def post_reel(video, caption, api, uid, auth):
    ver = os.environ.get("IG_API_VERSION", "v25.0")
    size = os.path.getsize(video)
    cid = None
    for attempt in range(6):
        try:
            c = http("POST", f"{api}/{uid}/media", {"media_type": "REELS", "upload_type": "resumable", "caption": caption,
                                                    "share_to_feed": "true", "thumb_offset": "100"}, headers=auth)
            cid = c["id"]; print("container", cid)
            up = http("POST", c.get("uri") or f"https://rupload.facebook.com/ig-api-upload/{ver}/{cid}",
                      headers={**auth, "offset": "0", "file_size": str(size), "Content-Type": "application/octet-stream"},
                      raw=open(video, "rb").read())
            print("upload", "ok" if up.get("success") else up)
            st = {}
            for _ in range(80):
                st = http("GET", f"{api}/{cid}?fields=status_code,status", headers=auth)
                print("status", st.get("status_code"), str(st.get("status", ""))[:120])
                if st.get("status_code") in ("FINISHED", "ERROR", "EXPIRED"):
                    break
                time.sleep(15)
            if st.get("status_code") == "FINISHED":
                break
            print("attempt", attempt + 1, "container", st.get("status_code"))
        except ApiError as e:
            print("attempt", attempt + 1, "failed:", e)
        time.sleep([30, 60, 120, 240, 300, 0][attempt])
    else:
        raise SystemExit("resumable upload failed 6 times")
    for attempt in range(3):
        try:
            pub = http("POST", f"{api}/{uid}/media_publish", {"creation_id": cid}, headers=auth); break
        except ApiError as e:
            print("publish attempt", attempt + 1, "failed:", e); time.sleep(20)
    else:
        raise SystemExit("media_publish failed 3 times")
    info = http("GET", f"{api}/{pub['id']}?fields=permalink", headers=auth)
    return info.get("permalink", pub["id"])


def main():
    # ---- gates 1-2: publishing must be explicitly enabled for THIS repo and name its account ----
    if os.environ.get("JAPAN_POV_PUBLISH") != "true":
        raise SystemExit("PUBLISH GATE: vars.JAPAN_POV_PUBLISH is not 'true' — publishing is disabled. Nothing was posted.")
    want_user = (os.environ.get("JAPAN_POV_USERNAME") or "").strip().lstrip("@")
    if not want_user or want_user == "JAPAN_POV_USERNAME":
        raise SystemExit("PUBLISH GATE: vars.JAPAN_POV_USERNAME is not set to the real account username. Nothing was posted.")
    uid = os.environ.get("IG_USER_ID", "")
    tok = "".join(os.environ.get("IG_ACCESS_TOKEN", "").split())
    if not uid or not tok:
        raise SystemExit("PUBLISH GATE: this repo's IG_USER_ID / IG_ACCESS_TOKEN secrets are not set. Nothing was posted.")
    ver = os.environ.get("IG_API_VERSION", "v25.0")
    api = f"https://graph.facebook.com/{ver}"
    auth = {"Authorization": f"OAuth {tok}"}
    # ---- gate 3: the token's account must BE the japan-pov account ----
    me = http("GET", f"{api}/{uid}?fields=username", headers=auth)
    if (me.get("username") or "").lower() != want_user.lower():
        raise SystemExit(f"PUBLISH GATE: token account is @{me.get('username')}, not @{want_user}. Refusing to post.")
    print(f"publish gate OK: posting as @{want_user}")

    nj = os.path.join(ENG, "out", "next.json")
    nxt = json.load(open(nj, encoding="utf-8"))
    ep = nxt["ep"]; out = os.path.join(ENG, "out", ep)
    if not os.path.exists(os.path.join(out, "final.mp4")):
        subprocess.run(["python", "render.py", ep, "full"], cwd=ENG, check=True)
    if not os.path.exists(os.path.join(out, "cover.jpg")):
        t, l1, l2, stamp = nxt.get("cover") or [1.0, "POV:||", "", ""]
        subprocess.run(["python", "render.py", ep, "clean", str(t)], cwd=ENG, check=True)
        subprocess.run(["python", "cover.py", ep, l1, l2, stamp], cwd=ENG, check=True)
    video = os.path.join(out, "upload.mp4")
    with_cover(os.path.join(out, "final.mp4"), os.path.join(out, "cover.jpg"), video)
    print("video", round(os.path.getsize(video) / 1e6, 1), "MB")
    if os.environ.get("DRY_RUN") == "1":
        print("DRY_RUN: skip posting"); return
    url = post_reel(video, nxt["caption"], api, uid, auth)
    print("posted:", url)
    pj = os.path.join(ENG, "posted.json")
    p = json.load(open(pj, encoding="utf-8"))
    p["posts"].append({"date": datetime.date.today().isoformat(), "ep": ep, "topic": nxt.get("topic", ""), "url": url, "via": "cloud"})
    json.dump(p, open(pj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(ENG, "out", "posted_urls.txt"), "a", encoding="utf-8") as f:
        print(f"{nxt.get('topic', ep)}: {url}", file=f)


if __name__ == "__main__":
    main()
