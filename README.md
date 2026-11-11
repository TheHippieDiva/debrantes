# debrantes.com: static site (PREVIEW, 11 Nov 2026)

A plain HTML site to replace the Squarespace site, built for free hosting on GitHub Pages.
Nothing is pushed, published or pointed at yet. Dawn or Nacho says go first (BIG CHANGE CHECK in PLAN.md).

## How it's built
- Every page comes from one script: `python3 _build/build.py`. Edit the words there, re-run, check, commit the `.html` files.
- Look: `assets/css/site.css`. Light by default (`#fbf7f4`, plum headings `#4f2445`), dark mode follows the phone/computer
  setting (greys `#2b2b2b`/`#353535`, cream `#eee6dc`, clay `#D49066`), prints black on white. Fonts: Archivo Black, Josefin Sans, IBM Plex Mono.
- `CNAME` = `www.debrantes.com`. `_config.yml` keeps this README out, and folders starting with `_` (`_build`, `_previews`) are not published by GitHub Pages (Jekyll skips them; do NOT add a `.nojekyll` file).
- Old URLs keep working: `/about`, `/brands`, `/video`, `/contact` etc. resolve to the `.html` files on GitHub Pages.

## The auto-feeds (home page, "What's new")
`assets/js/feeds.js`, newest on top, no server, no paid service:
1. YouTube channel RSS (TheHippieDiva `UCV4ryaE8XZvLEFTnFqlxbMA`) and the Substack RSS
   go through the free rss2json.com endpoint; if that fails, through the allorigins.win CORS proxy (XML parsed in the browser).
2. Homesteader Labs is read straight from its `llms.txt` + `sitemap.xml` (CORS open). House-tech posts are filtered out.
3. `assets/js/fallback.js` is a saved snapshot (11 Nov). It shows first, then the live list swaps in. Each box says "Live feed" or "Saved list".
   Refresh the snapshot now and then (any Claude session can re-run it).

## Pages
index · brands · consulting (3 lanes + Book a call) · video · branding · websites · portrait-photography · product-photography ·
adventure · family · 6ixman · about · contact · 404

## Walls kept
- Two Women One Prison is shown as WORK we did: a portfolio card on /video next to Boogeyman (TWOP header image + credit: brand design, episode production, channel management; one link out to twowomenoneprison.com), not as our brand, and has no feed (Dawn, 11 Nov). Dawn's bio says she co-hosts it.
- Didi & Baboo's Beat Box and FloofieButts: one plain card each, one link OUT (no pictures, characters only), in their own
  "Homestead & family" group, never beside the prison-story cards. Neither site links back.
- No grandkids, no children's photos: every old photo of a child (all of /family, kids on /portrait-photography, one on /adventure) was left out.
- Dropped for privacy: the old street address and phone (in every page header), Nacho's personal email on /about, people's names in old captions.
  Image files renamed to neutral names.
- Private projects stay off (PLAN.md "Never on this site"). Hestia left off to be safe; add back only with Nacho's OK.

## What's left (placeholders show as dashed boxes)
1. **Email**: the live /contact page has only a form, no hello@ address. Set `EMAIL` in `_build/build.py`, rebuild.
2. **Dawn's bio** on /about is the BIO_v4 short bio, still behind her review gate. Swap in the approved one.
3. **/family**: needs new photos with no children's faces, or the page goes.
4. **/6ixman**: the old page is password-locked; this one uses the public 6ixMan product shots. Nacho adds the rest.
5. Gimme My Face, on-the-one, Hestia, research band, prices: held (see PLAN.md v7 notes).
6. Switch day: create the repo, push, turn on Pages, then GoDaddy A records 185.199.108-111.153 + `www` CNAME, enforce HTTPS,
   verify, THEN cancel Squarespace. Email (MX) at GoDaddy is not touched.
