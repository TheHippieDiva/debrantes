/* Auto-feeds for debrantes.com: no server, no paid service.
 * Each feed tries, in order:
 *   1. rss2json.com free endpoint (RSS -> JSON with CORS)
 *   2. allorigins.win raw proxy (CORS) + parse the XML in the browser
 *   3. the static list in fallback.js (snapshot), so a box is never empty.
 * Homesteader Labs serves llms.txt + sitemap.xml with CORS open, so it is read directly.
 * Mark-up: <div class="feed" data-feed="thd|substack|hsl" data-n="3"></div><p class="status" data-for="thd"></p>
 */
(function () {
  var FEEDS = {
    thd: { kind: 'yt', url: 'https://www.youtube.com/feeds/videos.xml?channel_id=UCV4ryaE8XZvLEFTnFqlxbMA' },
    substack: { kind: 'rss', url: 'https://thehippiediva.substack.com/feed' },
    hsl: { kind: 'hsl' }
  };
  var TIMEOUT = 8000;

  function esc(s) { return String(s || '').replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function strip(s) { var d = document.createElement('div'); d.innerHTML = String(s || '').replace(/<img[^>]*>/gi, ''); return (d.textContent || '').replace(/\s+/g, ' ').trim(); }
  function clip(s, n) { return s.length > n ? s.slice(0, n).replace(/\s+\S*$/, '') + '…' : s; }
  function day(d) { var t = new Date(String(d).replace(' ', 'T')); return isNaN(t) ? '' : t.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }); }
  function get(url) {
    var c = window.AbortController ? new AbortController() : null;
    var t = setTimeout(function () { if (c) c.abort(); }, TIMEOUT);
    return fetch(url, c ? { signal: c.signal } : {}).then(function (r) { clearTimeout(t); if (!r.ok) throw new Error(r.status); return r; });
  }
  function ytId(link) { var m = String(link).match(/(?:v=|shorts\/|youtu\.be\/)([\w-]{11})/); return m ? m[1] : ''; }
  function ytItem(title, link, date, desc) {
    var id = ytId(link), short = /#shorts/i.test(title);
    return { title: title.replace(/\s*#shorts/ig, ''), link: short ? 'https://www.youtube.com/shorts/' + id : link, date: date, img: id ? 'https://i.ytimg.com/vi/' + id + '/hqdefault.jpg' : '', short: short, dek: clip(strip(desc), 140) };
  }

  // 1. rss2json
  function viaRss2Json(f) {
    return get('https://api.rss2json.com/v1/api.json?rss_url=' + encodeURIComponent(f.url)).then(function (r) { return r.json(); }).then(function (j) {
      if (j.status !== 'ok' || !j.items || !j.items.length) throw new Error('rss2json');
      return j.items.map(function (i) {
        if (f.kind === 'yt') return ytItem(i.title, i.link, i.pubDate, i.description);
        return { title: i.title, link: i.link, date: i.pubDate, img: (i.enclosure && i.enclosure.link) || i.thumbnail || '', dek: clip(strip(i.description), 160) };
      });
    });
  }
  // 2. allorigins + DOMParser
  function viaProxy(f) {
    return get('https://api.allorigins.win/raw?url=' + encodeURIComponent(f.url)).then(function (r) { return r.text(); }).then(function (x) {
      var doc = new DOMParser().parseFromString(x, 'text/xml');
      var tx = function (el, sel) { var n = el.getElementsByTagName(sel)[0]; return n ? n.textContent : ''; };
      var out;
      if (f.kind === 'yt') {
        out = [].map.call(doc.getElementsByTagName('entry'), function (e) {
          var l = e.getElementsByTagName('link')[0];
          return ytItem(tx(e, 'title'), l ? l.getAttribute('href') : '', tx(e, 'published'), tx(e, 'media:description'));
        });
      } else {
        out = [].map.call(doc.getElementsByTagName('item'), function (e) {
          var enc = e.getElementsByTagName('enclosure')[0];
          return { title: tx(e, 'title'), link: tx(e, 'link'), date: tx(e, 'pubDate'), img: enc ? enc.getAttribute('url') : '', dek: clip(strip(tx(e, 'description')), 160) };
        });
      }
      if (!out.length) throw new Error('proxy empty');
      return out;
    });
  }
  // Homesteader Labs: llms.txt (titles + blurbs) + sitemap.xml (dates), both CORS-open
  function viaHsl() {
    return Promise.all([get('https://homesteaderlabs.com/llms.txt').then(function (r) { return r.text(); }), get('https://homesteaderlabs.com/sitemap.xml').then(function (r) { return r.text(); })]).then(function (a) {
      var info = {}, m, re = /- \[([^\]]+)\]\((https:\/\/homesteaderlabs\.com\/archive\/[^)]+)\): ([^\n]+)/g;
      while ((m = re.exec(a[0]))) info[m[2]] = { title: m[1], dek: clip(m[3], 160) };
      var posts = [], re2 = /<loc>(https:\/\/homesteaderlabs\.com\/archive\/[^<]+\/)<\/loc>\s*<lastmod>([^<]+)<\/lastmod>/g;
      while ((m = re2.exec(a[1]))) {
        // house-tech build logs stay off this site
        if (info[m[1]] && !/hestia|house-brain|harness/.test(m[1])) posts.push({ title: info[m[1]].title, dek: info[m[1]].dek, link: m[1], date: m[2] });
      }
      if (!posts.length) throw new Error('hsl empty');
      return posts;
    });
  }

  function card(it, kind) {
    var pic = it.img ? '<img class="pic" loading="lazy" alt="" src="' + esc(it.img) + '">' : '';
    var meta = (it.short ? 'Short · ' : '') + day(it.date);
    var go = kind === 'yt' ? 'Watch' : 'Read';
    return '<a class="card" target="_blank" rel="noopener" href="' + esc(it.link) + '">' + pic +
      '<div class="bd"><div class="meta">' + esc(meta) + '</div><h3>' + esc(it.title) + '</h3>' +
      (it.dek ? '<p>' + esc(it.dek) + '</p>' : '') + '<span class="go">' + go + ' →</span></div></a>';
  }

  function render(box, items, kind, state) {
    var n = +box.getAttribute('data-n') || 3;
    items = items.slice().sort(function (a, b) { return new Date(String(b.date).replace(' ', 'T')) - new Date(String(a.date).replace(' ', 'T')); }).slice(0, n); // newest on top
    box.innerHTML = items.map(function (i) { return card(i, kind); }).join('');
    box.setAttribute('data-state', state);
    var st = document.querySelector('.status[data-for="' + box.getAttribute('data-feed') + '"]');
    if (st) { st.textContent = state === 'live' ? 'Live feed · newest first' : 'Saved list · live feed unavailable right now'; st.className = 'status' + (state === 'live' ? ' live' : ''); }
  }

  [].forEach.call(document.querySelectorAll('[data-feed]'), function (box) {
    var key = box.getAttribute('data-feed'), f = FEEDS[key];
    if (!f) return;
    var fb = (window.FALLBACK || {})[key] || [];
    // show the saved list at once, then swap in the live one when it lands
    if (fb.length) render(box, fb, f.kind, 'saved');
    var p = f.kind === 'hsl' ? viaHsl() : viaRss2Json(f).catch(function () { return viaProxy(f); });
    p.then(function (items) { render(box, items, f.kind, 'live'); })
      .catch(function (e) { if (window.console) console.warn('feed ' + key + ' fell back:', e && e.message); });
  });
})();
