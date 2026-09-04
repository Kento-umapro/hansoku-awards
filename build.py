import json, html, datetime
items=json.load(open('data/awards.json',encoding='utf-8'))
items.sort(key=lambda i:(-i['kai'], ['グランプリ','ゴールド','シルバー','ブロンズ','学生賞','協賛企業賞','審査員個人賞'].index(i['category']) if i['category'] in ['グランプリ','ゴールド','シルバー','ブロンズ','学生賞','協賛企業賞','審査員個人賞'] else 9))
data=json.dumps(items,ensure_ascii=False,separators=(',',':'))
today=datetime.date.today().isoformat()
kais=sorted({i['kai'] for i in items},reverse=True)
cats=['グランプリ','ゴールド','シルバー','学生賞','協賛企業賞','審査員個人賞']
clients=sorted({i['client'] for i in items if i['client']})

TPL = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>販促コンペ 受賞企画書アーカイブ</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700;800&display=swap">
<style>
:root{--ink:#1A1712;--cream:#F7F3E6;--paper:#FFFDF7;--amber:#F2A32C;--amber-l:#FCEBC8;--sauce:#D8412A;--navy:#1C3054;--line:#E2D8BE;--gray:#7A6F5A}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"M PLUS Rounded 1c","Hiragino Sans",sans-serif;background:var(--cream);color:var(--ink);font-size:14px;line-height:1.7}
.wrap{max-width:1240px;margin:0 auto;padding:0 20px 80px}
header{background:var(--ink);color:var(--cream);border-radius:0 0 14px 14px;padding:26px 28px;margin-bottom:20px}
h1{font-size:26px;font-weight:800;letter-spacing:.01em}
h1 span{color:var(--amber)}
.sub{color:#C9BFA6;font-size:13px;margin-top:8px}
.sub a{color:var(--amber)}
.stats{display:flex;gap:22px;flex-wrap:wrap;margin-top:14px;font-size:12.5px;color:#C9BFA6}
.stats b{font-size:19px;color:var(--cream);font-weight:800;margin-right:4px}
.bar{position:sticky;top:0;z-index:9;background:var(--cream);padding:12px 0;border-bottom:1px solid var(--line);display:flex;gap:10px;flex-wrap:wrap;align-items:center}
select,input{font-family:inherit;font-size:13.5px;padding:9px 12px;border:1.5px solid var(--ink);border-radius:8px;background:var(--paper);color:var(--ink)}
input{flex:1;min-width:200px}
button.clear{font-family:inherit;font-size:13px;padding:9px 14px;border:1.5px solid var(--ink);border-radius:8px;background:var(--ink);color:var(--cream);cursor:pointer;font-weight:700}
.count{font-size:13px;color:var(--gray);margin:14px 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(268px,1fr));gap:16px}
.card{background:var(--paper);border:1.5px solid var(--ink);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;transition:transform .12s}
.card:hover{transform:translateY(-3px)}
.thumb{aspect-ratio:16/9;background:var(--amber-l);display:flex;align-items:center;justify-content:center;border-bottom:1.5px solid var(--ink);overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.thumb .ph{font-size:12px;color:var(--gray);padding:14px;text-align:center;font-weight:700}
.body{padding:14px 15px 15px;display:flex;flex-direction:column;gap:7px;flex:1}
.tags{display:flex;gap:6px;flex-wrap:wrap}
.tag{font-size:10.5px;font-weight:700;padding:3px 8px;border-radius:5px;letter-spacing:.02em}
.t-kai{background:var(--ink);color:var(--cream)}
.t-cat{background:var(--sauce);color:#fff}
.t-cat.gp{background:var(--amber);color:var(--ink)}
.t-cat.sp{background:var(--navy)}
h2{font-size:16px;font-weight:800;line-height:1.4}
.client{font-size:12.5px;font-weight:700;color:var(--navy)}
.brief{font-size:12px;color:var(--gray);line-height:1.6}
.win{font-size:11.5px;color:var(--gray);border-top:1px dashed var(--line);padding-top:7px;margin-top:auto}
.go{display:block;text-align:center;margin-top:9px;padding:9px;background:var(--amber);color:var(--ink);border-radius:7px;font-weight:800;font-size:13px;text-decoration:none;border:1.5px solid var(--ink)}
.go.slide{background:var(--paper)}
.none{padding:50px 0;text-align:center;color:var(--gray)}
footer{margin-top:36px;padding-top:16px;border-top:1px solid var(--line);font-size:11.5px;color:var(--gray);line-height:1.8}
@media(max-width:600px){h1{font-size:21px}.wrap{padding:0 14px 60px}header{padding:20px}}
</style></head><body>
<div class="wrap">
<header>
  <h1>販促コンペ <span>受賞企画書</span> アーカイブ</h1>
  <div class="sub">宣伝会議「販促コンペ」の歴代受賞作品。企画書づくりの参考用に、社内から探せるようにまとめたものです。<br>
  出典：<a href="https://awardg.sendenkaigi.com/hansoku/history" target="_blank" rel="noopener">awardg.sendenkaigi.com</a>　各作品のリンク先は公式サイトのPDF／スライドです。</div>
  <div class="stats"><span><b>__N__</b>作品</span><span><b>__K__</b>回分</span><span><b>__C__</b>社の課題</span><span>更新 __D__</span></div>
</header>

<div class="bar">
  <select id="fk"><option value="">回次（すべて）</option>__OPTK__</select>
  <select id="fc"><option value="">賞（すべて）</option>__OPTC__</select>
  <select id="fb"><option value="">課題企業（すべて）</option>__OPTB__</select>
  <input id="q" placeholder="キーワードで検索（タイトル・課題・受賞者）">
  <button class="clear" id="cl">クリア</button>
</div>
<div class="count" id="cnt"></div>
<div class="grid" id="g"></div>
<footer>
本ページは社内の参考用に、公開されている受賞作品の一覧と公式リンクをまとめたものです。企画書の内容そのものは各リンク先（宣伝会議／SlideShare）でご覧ください。<br>
第1回〜第13回は公式サイト上でグランプリのみが公開されており、それ以外の受賞作品は応募者ログインが必要です。
</footer>
</div>
<script>
const D=__DATA__;
const g=document.getElementById('g'),cnt=document.getElementById('cnt');
const fk=document.getElementById('fk'),fc=document.getElementById('fc'),fb=document.getElementById('fb'),q=document.getElementById('q');
const esc=s=>(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function cls(c){return c==='グランプリ'?'gp':(c==='協賛企業賞'||c==='審査員個人賞')?'sp':''}
function render(){
  const k=fk.value,c=fc.value,b=fb.value,s=q.value.trim().toLowerCase();
  const r=D.filter(i=>(!k||i.kai==k)&&(!c||i.category===c)&&(!b||i.client===b)&&
    (!s||[i.title,i.client,i.brief,i.winners,i.award].join(' ').toLowerCase().includes(s)));
  cnt.textContent=r.length+' 件';
  g.innerHTML=r.length?r.map(i=>{
    const url=i.pdf||i.slide, isPdf=!!i.pdf;
    const th=i.thumb?`<img src="${esc(i.thumb)}" loading="lazy" alt="">`:`<div class="ph">${esc(i.title)}</div>`;
    return `<article class="card">
      <div class="thumb">${th}</div>
      <div class="body">
        <div class="tags"><span class="tag t-kai">第${i.kai}回 / ${i.year}</span><span class="tag t-cat ${cls(i.category)}">${esc(i.category)}</span></div>
        <h2>${esc(i.title)}</h2>
        <div class="client">${esc(i.client)}</div>
        <div class="brief">${esc(i.brief)}</div>
        <div class="win">${esc(i.winners)}${i.judge?'<br>審査員：'+esc(i.judge):''}</div>
        <a class="go ${isPdf?'':'slide'}" href="${esc(url)}" target="_blank" rel="noopener">${isPdf?'企画書PDFを開く':'スライドを開く'}</a>
      </div></article>`}).join(''):'<div class="none">条件に合う作品がありません</div>';
}
[fk,fc,fb].forEach(e=>e.onchange=render); q.oninput=render;
document.getElementById('cl').onclick=()=>{fk.value='';fc.value='';fb.value='';q.value='';render()};
render();
</script></body></html>"""

out=(TPL.replace('__DATA__',data)
        .replace('__N__',str(len(items)))
        .replace('__K__',str(len(kais)))
        .replace('__C__',str(len(clients)))
        .replace('__D__',today)
        .replace('__OPTK__',''.join(f'<option value="{k}">第{k}回（{2008+k}）</option>' for k in kais))
        .replace('__OPTC__',''.join(f'<option>{c}</option>' for c in cats))
        .replace('__OPTB__',''.join(f'<option>{html.escape(c)}</option>' for c in clients)))
open('index.html','w',encoding='utf-8').write(out)
print('index.html', round(len(out)/1024),'KB /', len(items),'件')
