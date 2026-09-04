import re, json, urllib.request, time, html, os

BASE="https://awardg.sendenkaigi.com"
PAGES=[(17,f"{BASE}/hansoku/history")]+[(n,f"{BASE}/hansoku/history/{n}th") for n in range(16,0,-1)]
strip=lambda s: html.unescape(re.sub(r'<[^>]+>','',s or '')).replace('　',' ').strip()
sq=lambda s: re.sub(r'\s+',' ',s or '').strip()

def get(u):
    req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
    return urllib.request.urlopen(req,timeout=45).read().decode('utf-8','replace')

all_items=[]
for kai,url in PAGES:
    try: doc=get(url)
    except Exception as e:
        print('NG',kai,e); continue
    # 見出しと作品ブロックを文書順に取得
    marks=[]
    for m in re.finditer(r'<h[1-4][^>]*>(.*?)</h[1-4]>', doc, re.S):
        t=sq(strip(m.group(1)))
        if t and 'history-title' not in m.group(0): marks.append((m.start(),'h',t))
    blocks=[m.start() for m in re.finditer(r'<div class="history-base', doc)]
    chunks=[]
    for i,p in enumerate(blocks):
        end=blocks[i+1] if i+1<len(blocks) else len(doc)
        chunks.append((p,doc[p:end]))
    def near_head(pos):
        cand=[t for (s,k,t) in marks if s<pos]
        return cand[-1] if cand else ''
    n=0
    for pos,c in chunks:
        award=sq(strip((re.search(r'history-award-text">(.*?)</p>',c,re.S) or [None,''])[1] if re.search(r'history-award-text">(.*?)</p>',c,re.S) else ''))
        pdf=(re.search(r'<a href="([^"]+\.pdf)"',c) or [None,''])[1]
        thumb=(re.search(r'<img src="(https?://[^"]+\.(?:png|jpg|jpeg))"',c) or [None,''])[1]
        slide=(re.search(r'<iframe[^>]+src="([^"]+)"[^>]*class="history-slide"',c) or re.search(r'<iframe[^>]+class="history-slide"[^>]*src="([^"]+)"',c) or [None,''])[1]
        title=sq(strip((re.search(r'history-title">(.*?)</h4>',c,re.S) or [None,''])[1]))
        winners=''; client=''; brief=''
        for dl in re.finditer(r'<dl class="history-definition-item">(.*?)</dl>', c, re.S):
            body=dl.group(1)
            dt=sq(strip((re.search(r'<dt>(.*?)</dt>',body,re.S) or [None,''])[1]))
            dd=(re.search(r'<dd>(.*?)</dd>',body,re.S) or [None,''])[1]
            if '受賞者' in dt: winners=sq(strip(dd))
            elif '課題' in dt:
                ps=[sq(strip(x)) for x in re.findall(r'<p[^>]*>(.*?)</p>',dd,re.S) if sq(strip(x))]
                if ps: client=ps[0]; brief=' / '.join(ps[1:])
                else: client=sq(strip(dd))
        if not (title or pdf): continue
        sec=near_head(pos)
        MAJ=('グランプリ','ゴールド','シルバー','ブロンズ','学生賞','協賛企業賞','審査員個人賞')
        cat = sec if sec in MAJ else (award if award in MAJ else ('審査員個人賞' if award.endswith('氏') else ('協賛企業賞' if sec.startswith('第') is False else award)))
        if award in MAJ: cat=award
        elif sec in MAJ: cat=sec
        judge = award if award.endswith('氏') else ''
        all_items.append(dict(kai=kai, year=2008+kai, category=cat, award=award, judge=judge, section=sec,
                              title=title, client=client, brief=brief, winners=winners,
                              pdf=pdf, slide=slide, thumb=thumb, page=url))
        n+=1
    print(f'第{kai}回 {n}件  {url}')
    time.sleep(0.8)

json.dump(all_items, open('data/awards.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('TOTAL', len(all_items))
from collections import Counter
print('賞の種類:', Counter(i['award'] for i in all_items).most_common())
