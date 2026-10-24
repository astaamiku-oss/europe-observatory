from pathlib import Path
from html import escape as e
import json,re,zipfile,shutil
R=Path(__file__).parent
D=json.loads((R/'data.json').read_text()); S=json.loads((R/'synthesis.json').read_text())
OUT=R/'dist'; OUT.mkdir(exist_ok=True); (OUT/'reports').mkdir(exist_ok=True); (OUT/'read').mkdir(exist_ok=True)
for f in ['style.css','app.js']: shutil.copy(R/f,OUT/f)
def page(title,content,prefix='',description='十份B站字幕的欧洲衰落专题：逐篇报告、共识分歧与原因归类。'):
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(description)}"><meta name="theme-color" content="#173f37"><title>{e(title)} · 欧洲观察</title><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 50 50'%3E%3Crect width='50' height='50' fill='%23173f37'/%3E%3Ctext x='25' y='36' text-anchor='middle' fill='%23f4f1e9' font-size='35' font-family='serif'%3EE%3C/text%3E%3C/svg%3E"><link rel="stylesheet" href="{prefix}style.css"><script src="{prefix}app.js" defer></script></head><body><div class="progress" aria-hidden="true"></div><header class="topbar"><nav class="wrap nav" aria-label="主导航"><a class="brand" href="{prefix}index.html"><span>E</span>欧洲观察</a><div class="navlinks"><a href="{prefix}index.html#reports">报告目录</a><a href="{prefix}read/synthesis.html">综合对比 ↗</a><a class="optional" href="{prefix}index.html#method">阅读说明</a></div></nav></header>{content}<footer><div class="wrap foot"><span>EUROPE OBSERVATORY / 欧洲观察</span><span>基于10份视频字幕整理 · 仅呈现原视频论述 · 非实时经济数据库</span></div></footer></body></html>'''
def time_link(t,url):
 a=t.split(':');sec=int(a[0])*60+int(float(a[1]));return f'<a class="time" href="{url}?t={sec}" target="_blank" rel="noopener noreferrer" aria-label="在B站回看{t}">{t[:5]} ↗</a>'
def toc(items,download):
 return '<aside class="toc" aria-label="本页目录"><p>ON THIS PAGE / 本页目录</p>'+''.join(f'<a href="#{id}">{e(title)}</a>' for id,title in items)+f'<a class="download" download href="../reports/{download}">下载 Markdown ↓</a><a class="download" href="javascript:window.print()" onclick="window.print();return false">打印 / 保存 PDF ↗</a></aside>'
def render_md(d,num):
 lines=[f'# {d["title"]}',f'\n编号：{num:02d}｜UP：{d["up"]}｜分类：{d["category"]}',f'\n原视频：{d["url"]}',f'\n字幕范围：{d["start"]}—{d["end"]}，{d["lines"]}行。时间范围仅代表所给字幕，不等于全片时长。',f'\n来源文件：{d["source"]}', '\n> 本文仅据所给字幕总结；数字为视频口径，未进行外部事实核查。', '\n## 一句话结论', '\n'+d['conclusion'],'\n## 核心观点']
 for i,p in enumerate(d['points'],1):lines+=['\n'+str(i)+'. '+p]
 lines+=['\n## 论据与数据']
 for t,title,txt in d['evidence']:lines+=['\n### '+title+' ['+t+']','\n'+txt,f'\n[回看原视频]({d["url"]}?t={int(t.split(":")[0])*60+int(float(t.split(":")[1]))})']
 lines+=['\n## 结构脉络与关键时间点']
 for t,txt in d['outline']:lines+=['\n- ['+t+'] '+txt]
 lines+=['\n## 材料边界与阅读提醒']
 for n in d['notes']:lines+=['\n- '+n]
 return '\n'.join(lines)+'\n'
for i,d in enumerate(D,1):
 md=render_md(d,i); filename=d['id']+'.md';(R/'reports'/filename).write_text(md);(OUT/'reports'/filename).write_text(md)
 sections='<div class="conclusion"><div class="eyebrow">IN ONE SENTENCE / 一句话结论</div><p>'+e(d['conclusion'])+'</p></div>'
 sections+='<section id="views"><h2>01 / 核心观点</h2>'+''.join(f'<div class="point"><span>{n:02d}</span><p>{e(p)}</p></div>' for n,p in enumerate(d['points'],1))+'</section>'
 sections+='<section id="evidence"><h2>02 / 论据与数据</h2><p class="source-name">以下均为字幕中的说法。个人经历、设例、统计与预测的区别已在对应条目中说明。</p>'+''.join(f'<div class="evidence"><h3>{time_link(t,d["url"])}{e(title)}</h3><p>{e(txt)}</p></div>' for t,title,txt in d['evidence'])+'</section>'
 sections+='<section id="timeline"><h2>03 / 结构脉络与关键时间点</h2><ol class="timeline">'+''.join(f'<li>{time_link(t,d["url"])}<span>{e(txt)}</span></li>' for t,txt in d['outline'])+'</ol></section>'
 sections+='<section id="notes"><h2>04 / 材料边界与阅读提醒</h2><div class="notes"><ul>'+''.join('<li>'+e(n)+'</li>' for n in d['notes'])+'</ul></div><p class="source-name">字幕文件：'+e(d['source'])+'<br>正文与证据仅来自这一文件；标题及UP信息来自素材索引。</p></section>'
 prev=f'<a href="{D[i-2]["id"]}.html">← 上一篇</a>' if i>1 else '<a href="../index.html#reports">← 报告目录</a>'
 nex=f'<a href="{D[i]["id"]}.html">下一篇 →</a>' if i<len(D) else '<a href="synthesis.html">阅读综合篇 →</a>'
 sections+=f'<div class="pager">{prev}{nex}</div>'
 header=f'<div class="wrap report-header"><div class="crumb"><a href="../index.html">首页</a> / <a href="../index.html#reports">报告目录</a> / {i:02d}</div><div class="eyebrow">VIDEO STUDY {i:02d} / {e(d["category"])}</div><h1>{e(d["title"])}</h1><p class="report-deck">{e(d["deck"])}</p><div class="meta-row"><span>UP · {e(d["up"])}</span><span>字幕末时点 {d["end"][:5]} · {d["lines"]} 行</span><span>仅据字幕整理</span><a class="textlink" href="{d["url"]}" target="_blank" rel="noopener noreferrer">观看原视频 ↗</a></div></div>'
 body=header+'<main class="wrap report-layout">'+toc([('views','核心观点'),('evidence','论据与数据'),('timeline','结构与时间点'),('notes','材料边界')],filename)+'<article class="article">'+sections+'</article></main>'
 (OUT/'read'/(d['id']+'.html')).write_text(page(d['short'],body,'../',d['deck']))
# synthesis
md=['# '+S['title'],'\n'+S['deck'],'\n> 仅据10份成功字幕综合；重复版本不算独立证据，数字未作外部核验。','\n## 一句话结论','\n'+S['conclusion']]
article='<div class="conclusion"><div class="eyebrow">THE SYNTHESIS / 综合判断</div><p>'+e(S['conclusion'])+'</p></div>'
for sec in S['sections']:
 md+=['\n## '+sec['title']];article+=f'<section id="{sec["id"]}"><h2>{e(sec["title"])}</h2>'
 for p in sec.get('paragraphs',[]):md+=['\n'+p];article+='<p>'+e(p)+'</p>'
 for title,p in sec.get('items',[]):md+=['\n### '+title,'\n'+p];article+='<h3>'+e(title)+'</h3><p>'+e(p)+'</p>'
 if 'table'in sec:
  t=sec['table'];md+=['\n| '+' | '.join(t['heads'])+' |','|'+ '|'.join(['---']*len(t['heads']))+'|'];md+=['| '+' | '.join(row)+' |' for row in t['rows']]
  article+='<div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+e(x)+'</th>' for x in t['heads'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(x)+'</td>' for x in row)+'</tr>' for row in t['rows'])+'</tbody></table></div>'
 article+='</section>'
article+='<section id="sources"><h2>07 / 十份报告索引</h2><ol>'+''.join(f'<li><a class="textlink" href="{d["id"]}.html">{i:02d} · {e(d["short"])} / {e(d["up"])}</a></li>'for i,d in enumerate(D,1))+'</ol></section>'
md+=['\n## 报告编号对照']
for i,d in enumerate(D,1):md+=['\n- '+f'{i:02d}｜{d["title"]}｜{d["up"]}｜{d["url"]}']
(R/'reports'/'synthesis.md').write_text('\n'.join(md)+'\n');shutil.copy(R/'reports'/'synthesis.md',OUT/'reports'/'synthesis.md')
header=f'<div class="wrap report-header"><div class="crumb"><a href="../index.html">首页</a> / 综合对比</div><div class="eyebrow">THE BIG PICTURE / 专题综合篇</div><h1>{e(S["title"])}</h1><p class="report-deck">{e(S["deck"])}</p><div class="meta-row"><span>10份字幕 · 6类原因 · 4处分歧</span><span>编辑归纳，不是观点投票</span></div></div>'
body=header+'<main class="wrap report-layout">'+toc([(s['id'],s['title'].split(' / ')[1])for s in S['sections']]+[('sources','原始报告索引')],'synthesis.md')+'<article class="article">'+article+'<div class="pager"><a href="../index.html#reports">← 返回报告目录</a><a download href="../reports/all-reports.zip">下载全部报告 ↓</a></div></article></main>'
(OUT/'read'/'synthesis.html').write_text(page('综合对比',body,'../',S['deck']))
# home
atlas='''<div class="atlas" role="img" aria-label="欧洲专题示意：增长、分配、制度交织的三个圆环；非统计图表"><div class="atlas-top"><span>FIELD NOTES — EUROPE</span><span>VOL. 01</span></div><svg viewBox="0 0 500 380" fill="none" aria-hidden="true"><g stroke="#d7b983" stroke-width="1" opacity=".55"><ellipse cx="250" cy="190" rx="200" ry="85" transform="rotate(-30 250 190)"/><ellipse cx="250" cy="190" rx="200" ry="85" transform="rotate(30 250 190)"/><ellipse cx="250" cy="190" rx="100" ry="170"/><circle cx="250" cy="190" r="145" stroke-dasharray="2 8" opacity=".55"/></g><g fill="#e7d1a5"><circle cx="93" cy="267" r="4"/><circle cx="409" cy="270" r="4"/><circle cx="250" cy="20" r="4"/></g><g fill="#ece8d8" font-size="12" font-family="sans-serif"><text x="47" y="305">增长</text><text x="423" y="305">分配</text><text x="263" y="29">制度</text></g></svg><div class="atlas-label">Europe.<small>A CONTINENT IN QUESTION</small></div><div class="atlas-bottom"><span>增长 / 分配 / 制度</span><span>概念示意 · 非数据图</span></div></div>'''
hero='<main><div class="wrap"><section class="hero"><div><div class="eyebrow">EUROPE, RECONSIDERED / 字幕研究专题</div><h1>一个大陆，<br>如何<em>慢慢失速</em>？</h1><p class="intro">从工业与能源，到债务与代际分配。细读十份视频字幕，拆开“欧洲没落”的宏大叙事，辨认每一种解释的依据与边界。</p><div class="hero-actions"><a class="btn" href="read/synthesis.html">先读综合对比 <span>↗</span></a><a class="btn secondary" href="#reports">浏览十份报告 <span>↓</span></a></div></div>'+atlas+'</section>'
hero+='<div class="stats" role="group" aria-label="专题内容概览"><div><strong>10</strong><span>视频字幕<br>逐篇独立分析</span></div><div><strong>06</strong><span>原因类别<br>串联不同视角</span></div><div><strong>01</strong><span>综合对比<br>保留共识与分歧</span></div></div>'
hero+='<section class="feature"><div><div class="eyebrow">START HERE / 导读</div><h2>相似的担忧，<br>并不等于相同的答案。</h2></div><div><p>福利过重，还是挣钱能力不足？能源成本，还是制度与创新？欧洲在衰亡，还是正在失去“永远领先”的叙事？综合篇把各视频放回各自的论证和时代背景。</p><a class="textlink" href="read/synthesis.html">阅读：共识、分歧与六类原因 ↗</a></div></section>'
hero+='<section id="reports"><div class="section-head"><div><div class="eyebrow">THE READING ROOM / 十份报告</div><h2>逐篇，读懂论证。</h2></div><p id="count" aria-live="polite">显示 10 / 10 份报告</p></div><div class="tools"><div class="filters" role="group" aria-label="按主要视角筛选">'+''.join(f'<button type="button" data-filter="{c}" aria-pressed="{str(i==0).lower()}">{c}</button>'for i,c in enumerate(['全部','增长与制度','能源与产业','债务与货币','人口与分配','生活与文明']))+'</div><label><span class="eyebrow">查找 </span><input class="search" id="search" type="search" placeholder="标题、UP、观点关键词" aria-label="搜索报告"></label></div><div class="catalog">'
for i,d in enumerate(D,1):
 hay=' '.join([d['title'],d['short'],d['up'],d['deck'],*d['points']]).lower()
 flag=' · 重合版本／字幕中断' if i==2 else ' · 字幕中断' if i==4 else ''
 hero+=f'<a class="report-card" href="read/{d["id"]}.html" data-category="{d["category"]}" data-search="{e(hay,quote=True)}"><span class="num">{i:02d}</span><div><div class="card-meta"><span>{e(d["category"])}</span><span>字幕至 {d["end"][:5]}</span></div><h3>{e(d["short"])}</h3><p>{e(d["deck"])}</p><div class="card-footer">{e(d["up"])}{flag}</div></div><span class="arrow" aria-hidden="true">↗</span></a>'
hero+='</div><p class="empty" id="empty" hidden>没有匹配的报告。试试其他关键词或选择“全部”。</p></section>'
failed=[]
for line in (R/'source-index.md').read_text().splitlines():
 c=[x.strip()for x in line.split('|')[1:-1]]
 if len(c)==5 and '失败'in c[3]:failed.append(c)
hero+='<section class="method" id="method"><div><div class="eyebrow">A NOTE ON SOURCES</div><h2>先有字幕，<br>再有结论。</h2><a class="textlink" href="reports/all-reports.zip" download>下载全部11份报告 ↓</a></div><div><p>所有报告仅依据所给字幕。视频观点不等于已核实事实；数字保留原视频的年份与口径，预测、个人经验及修辞类比单独说明。时间按钮可跳转原视频对应位置。</p><p>两份付鹏字幕内容高度重合，综合篇不将其视为两个独立论据。两份材料明显在论证中途结束；“成功”是采集状态，并不保证覆盖全片。</p><details><summary>查看处理范围与未纳入的5条视频</summary><p>所选10份字幕均已完成分析，无新增处理失败。以下条目在源索引中已标为无字幕／采集失败，按要求排除：</p><ul>'+''.join(f'<li>{e(c[0])} · {e(c[1])}</li>'for c in failed)+'</ul></details></div></section></div></main>'
(OUT/'index.html').write_text(page('一个大陆，如何慢慢失速？',hero))
(OUT/'.nojekyll').write_text('')
with zipfile.ZipFile(OUT/'reports'/'all-reports.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((R/'reports').glob('*.md')):z.write(p,p.name)
(R/'README.md').write_text('''# 欧洲观察 · Europe Observatory

基于本地10份成功采集的B站字幕制作的中文专题阅读网站。包含10份单篇报告和1份综合对比。

- `reports/`：11份可独立阅读的Markdown报告。
- `data.json`：单篇报告结构化数据。
- `synthesis.json`：综合篇结构化数据。
- `dist/`：GitHub Pages静态站点，可直接托管。
- `build.py`：生成HTML、报告与ZIP，不依赖第三方包。

构建：`python3 build.py`（首次生成首页处理范围需原始index.md）。

本项目不发布原始字幕全文。所有数字为视频口径，未经外部事实核验。报告标注了重合版本、字幕缺失、时间与统计口径问题。
''')
print('Generated',len(list((OUT/'read').glob('*.html'))),'article pages;',len(list((R/'reports').glob('*.md'))),'Markdown reports')
