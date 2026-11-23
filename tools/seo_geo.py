"""Content-based SEO and answer-ready landing pages; no inferred event dates/metrics."""
from pathlib import Path
from urllib.parse import urlsplit, quote, urljoin
import json, re, hashlib, sys
ROOT=Path(__file__).resolve().parents[1]

from bs4 import BeautifulSoup
SITES={
'zzhm':('郑州海名汇博会展策划有限公司','公司官网','提供公司介绍、展会项目、新闻资讯、招聘及联系信息。'),
'cdcyz':('成都餐饮供应链博览会','成都餐博会','面向餐饮供应链，展示食材、调味料、餐饮设备、食品加工包装及相关产品与服务。'),
'xacyz':('西安餐饮供应链博览会','西安餐博会','面向西北餐饮市场，展示餐饮食材、面食、烘焙茶饮、餐饮设备及供应链服务。'),
'shhgz':('四川火锅产业博览会','四川火锅展','聚焦火锅产业，提供火锅食材、调味料、设备用品及产业交流相关展会信息。'),
'zzhbz':('海名烘焙和潮流饮品展','成都/西安烘焙展','介绍成都、西安烘焙和潮流饮品系列展，涵盖烘焙原辅料、设备、包装及饮品相关产品。'),
'zzgbh':('郑州工业博览会','郑州工博会','提供工业展会的展示范围、同期活动、行业资讯、参展与参观服务信息。'),
'zzwjz':('郑州五金机电展','郑州五金展','展示五金工具、机电、泵与电机、焊接及劳动防护等工业品相关产品与服务。'),
'zzwlz':('郑州物流展','郑州物流展','立足郑州，聚焦仓储、运输、配送及物流行业供需对接，提供参展与参观信息。')}
CSS='''.seo-intro,.seo-faq{width:min(1000px,calc(100% - 32px));margin:32px auto;padding:24px;background:#f7f9fb;border:1px solid #e1e8ee;border-radius:10px;box-sizing:border-box;color:#303d49;font:15px/1.9 "Microsoft YaHei",Arial,sans-serif}.seo-intro h1{font-size:25px;line-height:1.5;margin:0 0 12px}.seo-faq h2{font-size:23px;margin:0 0 18px}.seo-faq article{margin:0;padding:16px 0;border-top:1px solid #e1e8ee}.seo-faq h3{font-size:17px;margin:0 0 8px}.seo-faq p,.seo-intro p{margin:0}.seo-faq a,.seo-intro a{color:#153e6a;text-decoration:underline}.seo-faq .seo-related{display:flex;flex-wrap:wrap;gap:12px;margin-top:18px}@media(max-width:640px){.seo-intro,.seo-faq{padding:18px;margin:22px auto}.seo-intro h1{font-size:21px}.seo-faq h2{font-size:21px}}'''

def faqs(slug):
 name,alias,desc=SITES[slug]
 if slug=='zzhm':return [
 ('郑州海名公司官网可以查询哪些信息？','本网站提供郑州海名、成都海名及企业文化介绍，以及海名展会、新闻中心、加入海名和联系我们等栏目。'),
 ('如何访问各展会的项目官网？','可通过顶部“海名展会”二级菜单或全部展会列表访问对应项目官网，查看餐饮、火锅、烘焙、工业、五金和物流等项目的信息。'),
 ('如何咨询参展或参观？','请进入对应项目官网，通过“预约参展”“我要参观”入口办理登记，或在项目站联系我们栏目咨询。不同展会使用各自的登记入口。'),
 ('如何联系郑州海名？','公司联系电话为0371-63696191、0371-63697930，邮箱为zzhmhz@126.com。各项目联系信息可在对应展会官网查询。'),
 ('如何查看招聘岗位？','请访问“加入海名”栏目，阅读现有岗位职责与任职要求，招聘咨询请通过公司联系我们栏目进行。')]
 return [(f'{name}主要展示什么？',desc),
 ('哪些观众适合了解本展会？',f'对{alias}展示范围涉及的产品采购、渠道合作和行业交流有需求的企业及专业人士，可先查看展示范围和同期活动，再结合自身业务安排参观。'),
 ('如何预约参展？','点击本页“预约参展”按钮进入该项目的外部登记平台。展位方案、参展费用及具体服务内容请通过联系我们栏目向项目组确认。'),
 ('如何办理参观登记？','点击本页“我要参观”按钮进入该项目的登记入口，按照登记平台要求填写信息。入场凭证及现场规则以该平台和项目组通知为准。'),
 ('在哪里查看展会资料和同期活动？','网站设有资料下载、同期活动、展会动态和联系我们栏目，可通过页面导航访问。历史文章所述活动与政策仅对应其发布时的安排。'),
 ('如何确认本届展期、地点及参观政策？','请通过联系我们栏目向项目组确认最新安排。本网站保留历届新闻和资料，不同年份的展期、规模或政策不可直接作为本届安排；报名平台和项目组通知是出行与登记前的核实渠道。')]

def apply(slugs=None):
 reports=[]
 for slug in slugs or ['zzgbh']:
  base=ROOT/'src'
  name,alias,description=SITES[slug];origin='https://'+slug+'.hm-d.cn'
  (base/'seo.css').write_text(CSS,encoding='utf-8');csshash=hashlib.sha256(CSS.encode()).hexdigest()[:12]
  pages=list(base.rglob('*.html'));urls=[];questions=faqs(slug)
  specifics={
   'cdcyz':('成都餐博会有哪些餐饮供应链品类？','网站展示范围包含火锅烧烤食材、调味料、水产、肉禽、牛羊肉、速冻米面、烘焙轻食、酒水茶饮及餐饮设备等。具体参展产品请查看展示范围与项目组资料。'),
   'xacyz':('西安餐博会是否涉及面食和烘焙茶饮？','是。现有展会介绍涉及面食产业、烘焙茶饮、餐饮设备及食品加工包装等领域；可通过展示范围和同期活动栏目进一步了解。'),
   'shhgz':('四川火锅展与餐饮供应链有什么关联？','网站介绍聚焦火锅产业，涉及火锅相关食材、调味料及设备用品，并保留与成都餐饮供应链展相关的历史同期活动信息。是否同期举办及本届安排需向项目组核实。'),
   'zzhbz':('这个烘焙展网站包含哪些城市的信息？','本网站同时保留成都与西安烘焙和潮流饮品系列展的介绍与资料。两个城市的展期和安排应分别核实，不应将其中一个城市的历史信息套用到另一个城市。'),
   'zzgbh':('如何了解郑州工博会的展示范围？','请通过展示范围、资料下载及展会动态栏目查看现有项目资料。具体参展领域、展位方案和本届安排请通过联系我们栏目向项目组确认。'),
   'zzwjz':('郑州五金展是否包含泵与电机、劳保产品？','网站展区规划包含泵与电机展区、劳动防护展区，以及五金工具、机电和焊接等展区。具体展品及本届展区设置请向项目组确认。'),
   'zzwlz':('郑州物流展聚焦哪些物流环节？','网站介绍以仓储、运输、配送为核心，提供物流供需对接与行业交流信息。采购需求与具体展示品类可通过展示范围及联系我们栏目进一步沟通。')}
  if slug in specifics:questions.insert(1,specifics[slug])
  for page in pages:
   route='/'+page.relative_to(base).as_posix();route=route[:-10] if route.endswith('index.html') else route
   s=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
   if not s.head or not s.body:continue
   for n in s.select('[data-seo-generated]'):n.decompose()
   home=route=='/'
   if home:
    intro=s.new_tag('section',attrs={'class':'seo-intro','data-seo-generated':'true','aria-label':'网站介绍'})
    h=s.new_tag('h1');h.string=name;intro.append(h)
    p=s.new_tag('p');p.string=description;intro.append(p)
    if slug=='zzhm':s.select_one('.hm-carousel').insert_after(intro)
    else:s.select_one('main').insert(0,intro)
    faq=s.new_tag('section',attrs={'class':'seo-faq','id':'faq','data-seo-generated':'true','aria-labelledby':'faq-title'})
    h=s.new_tag('h2',id='faq-title');h.string='常见问题与解答';faq.append(h)
    for i,(q,a) in enumerate(questions):
     item=s.new_tag('article',id=f'faq-{i+1}');h=s.new_tag('h3');h.string=q;p=s.new_tag('p');p.string=a;item.extend([h,p]);faq.append(item)
    nav=s.new_tag('nav',attrs={'class':'seo-related','aria-label':'问答相关入口'})
    for label,path in ([('全部展会','/zhtj/'),('联系我们','/lxwm/'),('加入海名','/jrhm/')] if slug=='zzhm' else [('展示范围','/zqgh/'),('同期活动','/tqhd/'),('资料下载','/zlxz/'),('联系我们','/lxwm/')]):
     a=s.new_tag('a',href=path);a.string=label;nav.append(a)
    faq.append(nav);s.select_one('footer').insert_before(faq)
   main=s.select_one('.show,.pic,main') or s.body
   clean=BeautifulSoup(str(main),'html.parser')
   for n in clean.select('script,style,nav,.banner,.hm-header,.media-rail,.seo-faq'):n.decompose()
   text=re.sub(r'\s+',' ',clean.get_text(' ',strip=True))
   heading=main.select_one('h1,h2')
   original=s.title.get_text(' ',strip=True) if s.title else name
   subject=heading.get_text(' ',strip=True) if heading else re.split(r'[|｜_]',original)[0]
   title=name+'官网｜'+alias if home else subject[:70]+'｜'+name
   desc=(description+' 提供展会介绍、展示范围、同期活动、参展参观入口和常见问题。' if home and slug!='zzhm' else description if home else text[:145])
   if not desc:desc=subject+'。'+description
   canonical_route=route
   if slug=='zzhm':
    if route in ['/gnzh/','/gjzh/']:canonical_route='/zhtj/'
    if route=='/zxns/':canonical_route='/jrhm/'
   canonical=origin+quote(canonical_route,safe='/')
   redirect=bool(s.select_one('meta[http-equiv="refresh"]'))
   for n in s.select('title,link[rel="canonical"],meta[name="description"],meta[name="keywords"],meta[name="robots"],meta[property^="og:"],meta[name^="twitter:"]'):n.decompose()
   t=s.new_tag('title');t.string=title;s.head.append(t)
   for attrs in [{'name':'description','content':desc},{'name':'robots','content':'noindex,follow' if redirect else 'index,follow,max-image-preview:large'},
                 {'property':'og:title','content':title},{'property':'og:description','content':desc},{'property':'og:url','content':canonical},{'property':'og:type','content':'website'},{'property':'og:locale','content':'zh_CN'},{'property':'og:site_name','content':name}]:s.head.append(s.new_tag('meta',attrs=attrs))
   s.head.append(s.new_tag('link',rel='canonical',href=canonical))
   image=s.select_one('.hm-slide img[src],.banner-slide img[src]') or main.select_one('img[src]')
   if image:
    image_url=urljoin(origin+route,image['src'])
    s.head.append(s.new_tag('meta',attrs={'property':'og:image','content':image_url}))
   s.head.append(s.new_tag('meta',attrs={'name':'twitter:card','content':'summary_large_image' if image else 'summary'}))
   for img in s.select('img[src]'):
    if not img.get('alt','').strip():
     card=img.find_parent(['dl','figure','article'])
     caption=card.get_text(' ',strip=True)[:80] if card else ''
     img['alt']=caption or subject+'相关图片'
   s.head.append(s.new_tag('link',attrs={'rel':'stylesheet','href':'/seo.css?v='+csshash,'data-seo-generated':'true'}))
   s.html['lang']='zh-CN'
   graph=[{'@type':'WebSite','@id':origin+'/#website','url':origin+'/','name':name,'alternateName':alias,'inLanguage':'zh-CN'},
          {'@type':'WebPage','@id':canonical+'#page','url':canonical,'name':title,'description':desc,'isPartOf':{'@id':origin+'/#website'},'inLanguage':'zh-CN'}]
   if slug=='zzhm' and home:graph.append({'@type':'Organization','@id':origin+'/#organization','name':name,'url':origin+'/','telephone':['0371-63696191','0371-63697930'],'email':'zzhmhz@126.com'})
   if home:graph.append({'@type':'FAQPage','@id':origin+'/#faq','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in questions]})
   else:graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'首页','item':origin+'/'},{'@type':'ListItem','position':2,'name':subject,'item':canonical}]})
   script=s.new_tag('script',attrs={'type':'application/ld+json','data-seo-generated':'true'});script.string=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/');s.head.append(script)
   page.write_text(str(s),encoding='utf-8')
   if not redirect and canonical_route==route and not any(part in route for part in ['/admin','/inc/','/Plug/']):urls.append(canonical)
  import xml.etree.ElementTree as ET
  root=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
  for url in sorted(set(urls)):ET.SubElement(ET.SubElement(root,'url'),'loc').text=url
  ET.ElementTree(root).write(base/'sitemap.xml',encoding='utf-8',xml_declaration=True)
  (base/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /admin_hm/\nDisallow: /inc/\nDisallow: /Plug/\n\nSitemap: '+origin+'/sitemap.xml\n',encoding='utf-8')
  (base/'llms.txt').write_text('# '+name+'\n\n> '+description+'\n\n## 官方入口\n- [首页]('+origin+'/)\n- [常见问题]('+origin+'/#faq)\n- [联系我们]('+origin+'/lxwm/)\n- [站点地图]('+origin+'/sitemap.xml)\n\n## 信息使用说明\n本站含历届资料。展期、规模、登记与参观政策请向项目组核实，不应从历史新闻推断本届安排。本文件为辅助索引，不代替网页正文。\n',encoding='utf-8')
  reports.append({'site':slug,'pages':len(pages),'sitemap_urls':len(set(urls)),'faq_count':len(questions)})
  print(reports[-1],flush=True)
 (ROOT/'docs/seo-geo-report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':apply()
