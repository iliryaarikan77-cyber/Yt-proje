import re, sys, time, json, urllib.parse, urllib.request, html
UA = "Yt-proje/1.0 (https://github.com/iliryaarikan77-cyber/Yt-proje; educational short)"
def get(url):
    for i in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read().decode("utf-8","replace")
        except Exception as e: time.sleep(6*(i+1))
    return ""
out = {}
for f in sys.argv[1:]:
    h = get("https://commons.wikimedia.org/wiki/" + urllib.parse.quote(f))
    h = h.replace('&#95;','_')
    lic = re.findall(r'class="licensetpl_short"[^>]*>([^<]+)<', h)
    attr = re.findall(r'class="licensetpl_attr"[^>]*>(.*?)</span>', h, re.S)
    author = re.search(r'id="fileinfotpl_aut"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', h, re.S)
    src = re.search(r'id="fileinfotpl_src"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', h, re.S)
    full = re.search(r'href="(https://upload\.wikimedia\.org/wikipedia/commons/[0-9a-f]/[0-9a-f]{2}/[^"?]+)', h)
    clean = lambda s: re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',s))).strip()[:140] if s else ''
    rec = {"license": sorted(set(lic)), "author": clean(author.group(1)) if author else '', "attr": clean(attr[0]) if attr else '',
           "source": clean(src.group(1)) if src else '', "url": full.group(1) if full else ''}
    out[f] = rec
    print(f, "|", rec["license"], "|", rec["author"][:70], "|", rec["url"][-60:])
    time.sleep(2.5)
json.dump(out, open("img/candidates.json","w"), indent=1)
