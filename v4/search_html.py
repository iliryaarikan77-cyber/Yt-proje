import re, sys, time, urllib.parse, urllib.request, html
UA = "Yt-proje/1.0 (https://github.com/iliryaarikan77-cyber/Yt-proje; educational short)"
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read().decode("utf-8", "replace")
for q in sys.argv[1:]:
    u = "https://commons.wikimedia.org/w/index.php?" + urllib.parse.urlencode({"search": q, "title": "Special:Search", "ns6": 1, "fulltext": 1, "limit": 12})
    try:
        h = get(u)
    except Exception as e:
        print("ERR", q, e); continue
    files = []
    for m in re.finditer(r'href="/wiki/(File:[^"#?]+)"', h):
        f = urllib.parse.unquote(m.group(1))
        if f not in files: files.append(f)
    print("==", q); [print("  ", f) for f in files[:12]]
    time.sleep(2)
