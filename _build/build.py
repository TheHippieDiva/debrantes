#!/usr/bin/env python3
"""Builds every page of the debrantes.com static site from one template.
Run:  python3 _build/build.py   (from the github-site folder or anywhere)
Edit the content here, re-run, then commit the .html files. Folders starting with _ are not published by GitHub Pages.
"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape

NAV = [('index.html', 'Home'), ('brands.html', 'Brands'), ('consulting.html', 'Work with us'), ('video.html', 'Video'),
       ('portrait-photography.html', 'Photography'), ('about.html', 'About'), ('contact.html', 'Contact')]

# Placeholder until Dawn/Nacho name the hello@ address (the live /contact page shows only a form, no address).
EMAIL = 'REPLACE-hello@-address'

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=IBM+Plex+Mono:wght@400;500&family=Josefin+Sans:wght@300;400;600&display=swap" rel="stylesheet">')

FOOT = '''<footer><div class="wrap"><div class="cols">
<div><h4>Our sites</h4><ul>
<li><a href="https://homesteaderlabs.com" rel="noopener">Homesteader Labs</a></li>
<li><a href="https://www.thehippiediva.com" rel="noopener">TheHippieDiva</a></li>
<li><a href="https://www.thehippiediva.com/cookbook" rel="noopener">The cookbook</a></li>
</ul></div>
<div><h4>Follow Nacho</h4><ul>
<li><a href="https://x.com/thefullnacho" rel="noopener">X · @thefullnacho</a></li>
<li><a href="https://www.instagram.com/debrantes_studios/" rel="noopener">Instagram · de Brantes Studios</a></li>
<li><a href="https://www.facebook.com/debrantes" rel="noopener">Facebook · de Brantes</a></li>
<li><a href="https://www.pinterest.com/debrantes_studios/" rel="noopener">Pinterest</a></li>
</ul></div>
<div><h4>Follow Dawn</h4><ul>
<li><a href="https://www.youtube.com/@TheHippieDiva" rel="noopener">YouTube · @TheHippieDiva</a></li>
<li><a href="https://thehippiediva.substack.com" rel="noopener">Substack</a></li>
<li><a href="https://www.instagram.com/thehippiediva" rel="noopener">Instagram</a> · <a href="https://www.tiktok.com/@thehippiediva" rel="noopener">TikTok</a></li>
<li><a href="https://x.com/JustHippie" rel="noopener">X · @JustHippie</a></li>
</ul></div>
</div>
<p class="sig">de Brantes · Nacho &amp; Dawn · <a href="contact.html">Book a call</a></p>
</div></footer>'''


def page(fn, title, desc, body, feeds=False, scripts=''):
    nav = ''.join(f'<li><a href="{h}"{" aria-current=page" if h == fn else ""}>{E(t)}</a></li>' for h, t in NAV)
    js = '<script src="assets/js/fallback.js"></script><script src="assets/js/feeds.js" defer></script>' if feeds else ''
    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#fbf7f4" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#2b2b2b" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
{FONTS}
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<header class="top"><div class="wrap">
<a class="logo" href="index.html">de Brantes<small>Nacho &amp; Dawn</small></a>
<nav aria-label="Main"><details><summary>Menu</summary><ul>{nav}</ul></details></nav>
</div></header>
<main>
{body}
</main>
{FOOT}
{js}{scripts}
<script>
// open the menu on wide screens; play videos on tap (no YouTube load until asked)
var dt=document.querySelector('nav details'),mq=matchMedia('(min-width:900px)');function nv(){{dt.open=mq.matches;}}nv();mq.addEventListener('change',nv);
document.querySelectorAll('a.vid').forEach(function(a){{a.addEventListener('click',function(e){{e.preventDefault();a.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+a.dataset.id+'?autoplay=1" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen title="'+(a.getAttribute('aria-label')||'Video')+'"></iframe>';}});}});
</script>
</body>
</html>
'''
    open(os.path.join(ROOT, fn), 'w').write(out)


def gallery(paths, cls='', alt=''):
    return f'<div class="gallery {cls}">' + ''.join(f'<img loading="lazy" src="{p}" alt="{E(alt)}">' for p in paths) + '</div>'


def imgs(folder, names):
    return [f'assets/img/{folder}/{n}' for n in names]


def rng(prefix, a, b, ext='jpg'):
    return [f'{prefix}-{i:02d}.{ext}' for i in range(a, b + 1)]


def vid(yid, label, meta, line='', more=None):
    return (f'<div class="card"><a class="vid" href="https://youtu.be/{yid}" data-id="{yid}" aria-label="Play {E(label)}" '
            f'style="background-image:url(https://i.ytimg.com/vi/{yid}/hqdefault.jpg)"></a>'
            f'<div class="bd"><div class="meta">{E(meta)}</div><h3>{E(label)}</h3>{f"<p>{E(line)}</p>" if line else ""}'
            f'<a class="go" href="https://youtu.be/{yid}" rel="noopener">Watch on YouTube →</a>'
            + (f'<a class="go" style="margin-top:8px" href="{more[0]}" rel="noopener">{E(more[1])} →</a>' if more else '') + '</div></div>')


def brand(name, who, line, url, label, img=''):
    pic = f'<img class="pic" style="object-position:top" loading="lazy" src="{img}" alt="">' if img else ''
    return (f'<a class="card brand" href="{url}" rel="noopener">{pic}<div class="bd"><div class="who">{E(who)}</div>'
            f'<h3>{E(name)}</h3><p>{line}</p><span class="go">{E(label)} →</span></div></a>')


# ---------- brand cards (shared by home + brands) ----------
# Groups keep the walls: homestead/family brands sit apart from the prison-story brands.
# Didi & Baboo + FloofieButts: one link OUT only, no pictures, characters only, never next to the prison cards.
G_HOME = ''.join([
    brand('Homesteader Labs', 'Nacho', 'The logbook of a half acre: what was built, what it cost and what it measured, with printable parts and free planting, weather and resilience tools.', 'https://homesteaderlabs.com', 'homesteaderlabs.com'),
    brand('FloofieButts', 'Our Lhasa Apsos', 'Our floofy crew: Lhasa Apso puppies and the happy dogs who raise them.', 'https://floofiebutts.com', 'floofiebutts.com'),
    brand("Didi &amp; Baboo's Beat Box".replace('&amp;', '&'), 'For little ears', 'Songs, beats and craft-time adventures with Didi and Baboo.', 'https://didiandbaboo.com', 'didiandbaboo.com'),
])
G_DAWN = ''.join([
    brand('TheHippieDiva', 'Dawn', 'Dawn\'s home base: music videos, writing on Substack, the kitchen and building in public with AI as her crew.', 'https://www.thehippiediva.com', 'thehippiediva.com'),
    brand('Walking Out', 'Dawn · the album', 'A Suno album about every kind of prison, and walking out. <em>One Mirror at a Time</em> and <em>Hey Ya, Sister</em> are the first songs.', 'https://suno.com/@TheHippieDiva', 'Listen on Suno'),
    brand('Commissary Bitch in the Kitch', 'Dawn · the cookbook', 'A cookbook for women in federal prison: full meals from commissary, a hot jug of water and a clothes iron.', 'https://www.thehippiediva.com/cookbook', 'Get the book', 'assets/img/cookbook-cover.jpg'),
])
G_STUDIO = ''.join([
    brand('de Brantes Studios', 'Nacho', 'Branding, websites, portrait and product photography, adventure shoots and music videos for artists.', 'branding.html', 'See the studio'),
    brand('6ixMan', 'Studio client', 'Beard oil, balm and grooming: product photography and brand work for 6ixMan.', '6ixman.html', 'See the 6ixMan work'),
])


def brand_groups(intro=True):
    return (f'<div class="group"><h3>Homestead &amp; family</h3><div class="grid three">{G_HOME}</div></div>'
            f'<div class="group"><h3>Dawn\'s voice</h3><div class="grid three">{G_DAWN}</div></div>'
            f'<div class="group"><h3>The studio</h3><div class="grid">{G_STUDIO}</div></div>')


LANES = '''<div class="grid three">
<div class="lane"><div class="who">Build it · by Nacho</div><h3>AI systems for your business</h3>
<p>Practical intelligence. Nacho knows when plain code solves the problem and when you actually need a model. He builds small models that do more, not dressed-up scripts.</p>
<ul><li>Memory, documents, receipts and inventory, kept by AI</li><li>An AI-kept wiki for your team, with a checker that keeps it clean (<a href="https://github.com/thefullnacho/ligaments" rel="noopener">ligaments</a>)</li><li>Tools like the Homesteader Labs planting calendar and weather station</li></ul>
<a class="btn" href="contact.html">Book a call</a></div>
<div class="lane"><div class="who">Make it · by Dawn</div><h3>AI music videos</h3>
<p>Your song, your face, your story. Dawn writes, directs and finishes music videos with AI: made for you, or taught to you so you can make your own.</p>
<ul><li>A storyboard you approve first</li><li>Wide for YouTube + tall for Shorts, Reels and TikTok</li><li>Or the class: lessons at your pace, templates, live calls</li></ul>
<a class="btn" href="contact.html">Book a call</a></div>
<div class="lane"><div class="who">Hear it · Dawn (and Nacho)</div><h3>Speaking &amp; podcast guesting</h3>
<p>Keynotes, workshops, panels and podcast guest spots.</p>
<ul><li>One woman, an AI crew</li><li>Walking out of every kind of prison</li><li>Make an AI music video, live</li></ul>
<a class="btn" href="contact.html">Book a call</a></div>
</div>'''


def feed(key, title, more_url, more_label, n=3):
    return (f'<div class="feedhead"><h3>{E(title)}</h3><a href="{more_url}" rel="noopener">{E(more_label)} →</a></div>'
            f'<div class="feed" data-feed="{key}" data-n="{n}"><p class="ph">Loading…</p></div><p class="status" data-for="{key}"></p>')


# ---------- HOME ----------
page('index.html', 'de Brantes · Nacho & Dawn', 'Dawn and Alex (Nacho) de Brantes: every brand we build, in one place. AI systems, music videos, a homestead lab and a cookbook.', f'''
<section class="hero"><div class="wrap grid2" style="display:grid">
<div><div class="eyebrow">Nacho &amp; Dawn de Brantes</div>
<h1>We build with AI: systems, stories and music videos.</h1>
<p class="lede">de Brantes is Nacho's family name, and we build under it together: a half-acre homestead lab, music videos, podcast production, a cookbook and the everyday stuff in between.</p>
<div class="btns"><a class="btn" href="consulting.html">Work with us</a><a class="btn ghost" href="#brands">See our brands</a></div></div>
<img src="assets/img/adventure/adventure-08.jpg" alt="Sunset over the water in Arkansas, shot by Nacho">
</div></section>

<section id="brands"><div class="wrap">
<div class="eyebrow">Every brand, one place</div><h2>Our brands</h2>
{brand_groups()}
</div></section>

<section id="new"><div class="wrap">
<div class="eyebrow">Fresh off the line · updates itself</div><h2>What's new</h2>
<p class="sub">The newest from each of our channels, newest first. These fill in on their own as we post.</p>
{feed('hsl', 'From Homesteader Labs', 'https://homesteaderlabs.com/archive/', 'All guides')}
{feed('thd', 'New on TheHippieDiva', 'https://www.youtube.com/@TheHippieDiva/videos', 'All videos')}
{feed('substack', 'Dawn on Substack', 'https://thehippiediva.substack.com', 'All posts')}
</div></section>

<section id="work"><div class="wrap">
<div class="eyebrow">Consulting</div><h2>Work with us</h2>
<p class="sub">Have Nacho build it, have Dawn make it, or bring us in to talk.</p>
{LANES}
</div></section>
''', feeds=True)

# ---------- BRANDS ----------
CLIENTS = [
    ('letters-from-jett.png', 'Letters From Jett', 'Marketing', 'Website design, branding, logo creation and marketing', 'https://lettersfromjett.com'),
    ('rock-city-outfitters.png', 'Rock City Outfitters', 'Photography', 'Products and Instagram lifestyle', 'https://rockcityoutfitters.com'),
    ('6ixman.png', '6ixMan', 'Photography', 'Instagram', 'https://us.6ixman.com'),
    ('gr1m.jpg', 'GR1M', 'Marketing', 'Photography, videos, web development, ads and social media', 'https://gr1mmus1c.com'),
    ('our-only-hope.png', 'Our Only Hope', 'Photography', 'Album cover', 'https://open.spotify.com/track/28r140GNiaAvJwngdVpK2U'),
]
clients = ''.join(f'<a class="card" href="{u}" rel="noopener"><img class="pic" style="object-fit:contain;background:#fff;padding:18px" loading="lazy" src="assets/img/brands/{f}" alt="{E(n)} logo"><div class="bd"><div class="meta">{E(k)}</div><h3>{E(n)}</h3><p>{E(d)}</p></div></a>' for f, n, k, d, u in CLIENTS)
page('brands.html', 'Our brands · de Brantes', 'Every brand Dawn and Nacho de Brantes run, plus the brands de Brantes Studios has worked with.', f'''
<section><div class="wrap"><div class="eyebrow">Ours</div><h1>Our brands</h1>
<p class="lede">Everything we build, in one place. Each card goes to its own home.</p>
{brand_groups()}
</div></section>
<section><div class="wrap"><div class="eyebrow">de Brantes Studios</div><h2>Brands we've worked with</h2>
<div class="grid three">{clients}</div>
</div></section>''')

# ---------- CONSULTING ----------
page('consulting.html', 'Work with us · de Brantes', 'AI systems for businesses, AI music videos, and speaking and podcast guesting with Dawn and Nacho de Brantes.', f'''
<section><div class="wrap"><div class="eyebrow">Consulting</div><h1>Work with us</h1>
<p class="lede">Three ways in: Nacho builds the system, Dawn makes the video, or we come talk to your people.</p>
{LANES}
<div class="btns"><a class="btn" href="contact.html">Book a call</a></div>
</div></section>
<section><div class="wrap"><div class="eyebrow">See the work</div><h2>Made by us</h2>
<div class="grid three">{vid('zE_3iIWAUMI', 'AI N00b', 'Dawn · music video · 30 Oct 2026', "Dawn's newest. Written, directed and finished by her, with AI as the crew.")}{vid('3EgUaX-Siw4', 'One Mirror at a Time', 'Dawn · music video · 21 Oct 2026')}{vid('pQ1DeOfOwsg', 'Boogeyman · GR1M x KelsOh', 'Directed by Dawn · shot by Nacho')}</div>
<div class="btns"><a class="btn ghost" href="https://homesteaderlabs.com/tools/planting-calendar/" rel="noopener">Nacho's planting calendar</a><a class="btn ghost" href="https://homesteaderlabs.com/tools/weather/" rel="noopener">Nacho's weather station</a></div>
</div></section>''')

# ---------- VIDEO ----------
page('video.html', 'Video · de Brantes', 'Music videos by Dawn and Nacho de Brantes: AI music videos and the de Brantes Studios reel.', f'''
<section><div class="wrap"><div class="eyebrow">Music videos</div><h1>Video</h1>
<p class="lede">Dawn's AI music videos and Nacho's studio reel for artists.</p>
<div class="group"><h3>Dawn's songs, made with AI</h3><div class="grid three">
{vid('zE_3iIWAUMI', 'AI N00b', 'Premiered 30 Oct 2026', "58. Zero code. Her first hackathon. Her own song.")}
{vid('3EgUaX-Siw4', 'One Mirror at a Time', 'Official music video · 21 Oct 2026', 'A song about the curses we inherit, and breaking them with love, not blame.')}
{vid('os7tRsXkc7U', 'Hey Ya, Sister', 'Official music video · 7 Oct 2026', 'About walking out: out of the labels, out of the pills, out of the prison gates.')}
</div></div>
<div class="group"><h3>Studio reel · work for artists and shows</h3><div class="grid">
{vid('pQ1DeOfOwsg', 'Boogeyman · GR1M x KelsOh', 'Directed by Dawn · shot by Nacho')}
<div class="card"><a href="https://twowomenoneprison.com" rel="noopener" aria-label="Visit twowomenoneprison.com"><img class="pic" loading="lazy" src="assets/img/two-women-one-prison-header.jpg" alt="Two Women One Prison"></a><div class="bd"><div class="meta">Podcast</div><h3>Two Women One Prison</h3><p>Brand design, episode production and channel management</p><a class="go" href="https://twowomenoneprison.com" rel="noopener">twowomenoneprison.com →</a></div></div>
{vid('gRDKBWXkCsQ', 'Corrupted · GR1M & Clizz', 'Shot, edited and directed by Nacho')}
{vid('ydhebm0mabA', 'Hometown Haters · GR1M', 'Shot, edited and directed by Nacho')}
</div></div>
<div class="btns"><a class="btn" href="https://www.youtube.com/@TheHippieDiva" rel="noopener">More on TheHippieDiva</a><a class="btn ghost" href="https://suno.com/@TheHippieDiva" rel="noopener">Hear the album on Suno</a></div>
</div></section>''')

# ---------- STUDIO PAGES (carried over from the old site) ----------
STUDIO_NAV = ('<ul class="chips">' + ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in [
    ('branding.html', 'Branding'), ('websites.html', 'Websites'), ('video.html', 'Video'), ('portrait-photography.html', 'Portraits'),
    ('product-photography.html', 'Product'), ('adventure.html', 'Adventure'), ('family.html', 'Family'), ('6ixman.html', '6ixMan')]) + '</ul>')


def studio(fn, title, h1, lede, body, desc):
    page(fn, f'{title} · de Brantes Studios', desc, f'<section><div class="wrap"><div class="eyebrow">de Brantes Studios</div><h1>{h1}</h1><p class="lede">{lede}</p>{STUDIO_NAV}</div></section><section><div class="wrap">{body}</div></section>')


studio('branding.html', 'Branding', 'Branding', 'Logos, crests, banners and the look of a brand, start to finish.',
       gallery(imgs('branding', ['busy-gypsy-banner.jpg', 'hmpstr-logo.png', 'letters-from-jett-banner.jpg', 'letters-from-jett-crest.png', 'shawnee-detail.jpg']), 'logos', 'Brand work by de Brantes Studios'),
       'Branding by de Brantes Studios: logos, crests and banners.')

studio('websites.html', 'Websites', 'Websites', 'eCommerce stores built, stocked and marketed.', f'''
<div class="group"><h3>CableToolsUSA · Shopify</h3><p>Developed the Shopify store for <a href="https://cabletoolsusa.com" rel="noopener">CableToolsUSA</a>. Managed all product upload, page creation, email marketing suite integration, policies, about us, and design aesthetics.</p>
{gallery(imgs('websites', rng('websites', 1, 5, 'png')), 'shots', 'CableToolsUSA store screen')}</div>
<div class="group"><h3>PeaceLoveandLilies · Etsy</h3><p>Developed the pattern store for <a href="https://peaceloveandlilies.com" rel="noopener">PeaceLoveandLilies</a> on the Etsy platform. Managed product photography, content optimization, listing optimization, policies, and off-site marketing.</p>
{gallery(imgs('websites', rng('websites', 6, 9, 'png')), 'shots', 'PeaceLoveandLilies store screen')}</div>''',
       'Websites by de Brantes Studios: Shopify and Etsy stores.')

studio('portrait-photography.html', 'Portrait Photography', 'Portrait photography', 'Fall shoots, maternity, artists and portraits, by Nacho.', f'''
<div class="group"><h3>Fall photo shoots</h3>{gallery(imgs('portrait', rng('portrait', 1, 3)), '', 'Fall portrait')}</div>
<div class="group"><h3>Maternity photo shoots</h3>{gallery(imgs('portrait', rng('portrait', 4, 8)), '', 'Maternity portrait')}</div>
<div class="group"><h3>GR1M</h3>{gallery(imgs('portrait', rng('portrait', 9, 15)), '', 'Artist portrait of GR1M')}</div>
<div class="group"><h3>Portraits</h3>{gallery(imgs('portrait', rng('portrait', 16, 22)), '', 'Portrait')}</div>''',
       'Portrait photography by Nacho de Brantes: fall, maternity and artist portraits.')

P = {'plants': (1, 5, 'Peace Love and Lilies'), '6ixman': (6, 14, '6ixMan'), 'rock-city': (15, 25, 'Rock City'), 'album-art': (26, 29, 'Album art'), 'eliquid': (30, 43, 'AR eLiquid Co')}
prod = ''.join(f'<div class="group"><h3>{E(lbl)}</h3>{gallery(imgs("product", rng(k, a, b) + (["6ixman-44.jpg"] if k == "6ixman" else [])), "", lbl + " product photo")}</div>' for k, (a, b, lbl) in P.items())
studio('product-photography.html', 'Product Photography', 'Product photography', 'Products shot for the grid: plants, grooming, outdoor gear, album art and more.', prod,
       'Product photography by de Brantes Studios.')

studio('adventure.html', 'Adventure', 'Adventure', 'Out in the hills, rivers and racetracks.', f'''
<div class="group"><h3>Adventuring Arkansas</h3>{gallery(imgs('adventure', [f'adventure-{i:02d}.jpg' for i in list(range(1, 12)) + [13, 14]]), '', 'Arkansas landscape')}</div>
<div class="group"><h3>4 State Drift Show</h3>{gallery(imgs('adventure', rng('adventure', 15, 17)), '', 'Drift car at the 4 State Drift Show')}</div>''',
       'Adventure photography by Nacho de Brantes: Arkansas outdoors and the 4 State Drift Show.')

studio('family.html', 'Family', 'Family sessions', 'Family photo sessions by Nacho.',
       '<p class="ph">Placeholder: the old /family gallery was all photos of a child, so it was not carried over. Nacho picks new family-session photos with no children\'s faces, or this page goes.</p>'
       '<div class="btns"><a class="btn" href="contact.html">Book a session</a></div>',
       'Family photo sessions by de Brantes Studios.')

studio('6ixman.html', '6ixMan', '6ixMan', 'Beard oil, balms and grooming: product photography and Instagram for 6ixMan.', f'''
{gallery(imgs('product', rng('6ixman', 6, 14) + ['6ixman-44.jpg']) + ['assets/img/home/6ixman-beard-brush.jpg'], '', '6ixMan product photo')}
<div class="btns"><a class="btn" href="https://us.6ixman.com" rel="noopener">Visit 6ixMan</a></div>
<p class="ph">The old /6ixman page is password-locked, so its own content could not be read. These are the 6ixMan shots from the public product page. Nacho: add anything else here.</p>''',
       '6ixMan product photography by de Brantes Studios.')

# ---------- ABOUT ----------
page('about.html', 'About · de Brantes', 'About Dawn and Alex (Nacho) de Brantes.', '''
<section><div class="wrap"><div class="eyebrow">About</div><h1>Nacho &amp; Dawn</h1>
<p class="lede">de Brantes is Nacho's family name, and we build under it together.</p></div></section>
<section class="hero"><div class="wrap grid2" style="display:grid">
<div><div class="eyebrow">Alex "Nacho" de Brantes</div><h2>Maker, photographer, builder</h2>
<p>Alex de Brantes is an entrepreneur with a passion for photography and videography from Arkansas. Social media gave microphones to many, but it put a camera in my hands.</p>
<p>My interest in photography was born out of necessity. I've had multiple ecommerce businesses over the years; on a shoestring budget you learn to wear a lot of hats. The most important one being product photography.</p>
<p>Instagram's rise in popularity, and the boom of the influencer, meant my brands needed to deliver top-notch product photography for the grid or be left behind. The pressure to deliver quality content spurred my love for photo and video.</p>
<p>Today he leads <a href="https://homesteaderlabs.com" rel="noopener">Homesteader Labs</a>, the logbook of a half acre: every build named, measured and shipped as a post, a clip and a printable part.</p></div>
<img src="assets/img/about/alex.jpg" alt="Nacho at the water's edge at sunset">
</div></section>
<section><div class="wrap"><div class="eyebrow">Dawn de Brantes · TheHippieDiva</div><h2>Marketer, music-video maker, podcast host</h2>
<p class="lede">Dawn de Brantes is TheHippieDiva: a serial entrepreneur and marketer with 25+ years in startups, decentralized sales and software. After four and a half years in federal prison, she came home and rebuilt in public.</p>
<p>She writes and directs AI music videos (<em>One Mirror at a Time</em>, <em>AI N00b</em>), co-hosts the podcast <em>Two Women One Prison</em> with Sabrena Morgan, and wrote <em>Commissary B*tch in the Kitch</em>, a cookbook for women in federal prison. She teaches people how to make AI work for their lives and set their creativity free.</p>
<p><strong>Co-host of Two Women One Prison.</strong></p>
<p class="ph">Draft: Dawn's short bio from BIO_v4.md, which is still behind her review gate (Desk card review-bio-v2). Swap in her approved version before launch.</p>
<div class="btns"><a class="btn" href="consulting.html">Work with us</a><a class="btn ghost" href="https://www.thehippiediva.com" rel="noopener">thehippiediva.com</a></div>
</div></section>''')

# ---------- CONTACT ----------
page('contact.html', 'Contact · de Brantes', 'Book a call or a session with Dawn and Nacho de Brantes.', f'''
<section><div class="wrap"><div class="eyebrow">Contact</div><h1>Book a call</h1>
<p class="lede">Interested in a build, a music video, a talk or a photo session? We'd love to hear from you. Email us and we'll get back to you within a day or two.</p>
<div class="btns"><a class="btn" href="mailto:{EMAIL}?subject=Booking%20a%20call">Email us</a></div>
<p class="ph" style="margin-top:18px">Placeholder: the live /contact page has only a Squarespace form and no hello@ address. Put the real address in EMAIL in _build/build.py and rebuild.</p>
<div class="group"><h3>Tell us</h3><ul class="sub"><li>What you want: a build, a music video, a talk or a photo session</li><li>Your timeline</li><li>A link to your business, song or show</li></ul></div>
<div class="group"><h3>Or find us here</h3><ul class="chips">
<li><a href="https://x.com/thefullnacho" rel="noopener">Nacho on X</a></li><li><a href="https://www.instagram.com/debrantes_studios/" rel="noopener">de Brantes Studios on Instagram</a></li>
<li><a href="https://www.facebook.com/debrantes" rel="noopener">de Brantes on Facebook</a></li><li><a href="https://x.com/JustHippie" rel="noopener">Dawn on X</a></li>
<li><a href="https://www.instagram.com/thehippiediva" rel="noopener">Dawn on Instagram</a></li></ul></div>
</div></section>''')

# 404 for GitHub Pages
page('404.html', 'Not found · de Brantes', 'Page not found.', '<section><div class="wrap"><h1>Not here.</h1><p class="lede">That page moved when we rebuilt the site.</p><div class="btns"><a class="btn" href="index.html">Home</a><a class="btn ghost" href="brands.html">Our brands</a></div></div></section>')

print('built', sorted(f for f in os.listdir(ROOT) if f.endswith('.html')))
