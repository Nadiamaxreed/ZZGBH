# 八站 SEO / GEO 优化说明

本轮日期：2026-11-23。范围：郑州海名公司官网与成都餐饮、西安餐饮、四川火锅、烘焙、郑州工博会、五金、物流七个项目官网。

## 已实施

1. 八个首页新增常见问题。公司站覆盖业务入口、展会跳转、参展参观、联系及招聘；项目站覆盖展示范围、该项目特有品类、登记入口、资料与活动以及如何核实最新安排。答案直接写入静态 HTML，不依赖脚本渲染，支持标题和段落锚点引用。
2. 首页增加简短实体介绍和明确的 H1，用正式项目名称、别名和可核实的业务范围识别站点，避免仅依靠轮播图中的文字。
3. 全站更新 title、基于正文的 description、HTTPS canonical、中文语言声明、robots meta、Open Graph 与社交卡片；为原本缺少说明的图片补充与所在内容相关的 alt。
4. JSON-LD 包含 WebSite、WebPage；内页包含 BreadcrumbList；首页 FAQPage 与可见问答逐条一致。公司站另标记已核实的公司名、电话和邮箱。未把所有项目的主办方简单归为同一公司。
5. robots.txt 允许公开页面抓取并提供 sitemap.xml；站点地图采用对应域名绝对地址，排除已确认跳转页及公司站重复分类、重复招聘入口。保留旧入口访问，通过 canonical 指向统一页面，不删除历史文章。
6. llms.txt 提供官方首页、问答、联系和站点地图的辅助索引，并明确历史资料与本届安排的区别。它不是强制行业标准，不保证被任何模型采用。
7. 保留图片压缩、响应式图像、按需加载、HTTP/2 和已有缓存优化；新增样式采用哈希参数，避免发布后使用旧缓存。

## 信息边界

现存内容中有部分展期、届次、规模口径冲突，详见《原站业务数据待确认》。本轮没有凭空改写历史新闻、没有从海报推断已确认的新届次日期，也没有生成未经核实的 Event 日期、票价、评分或规模。问题答案明确提示通过项目组核实最新安排。

GEO 的重点是使页面内容清楚、可信、可检索及可引用，而不是添加特殊隐藏关键词。没有隐藏给 AI 的另一份答案，没有伪造权威来源或堆砌城市与行业关键词。

## 效果边界与后续运营

这些修改改善技术可抓取性和内容理解基础，不代表搜索引擎一定收录、排名提升或 AI 一定引用。Google 已在 2026 年停止 FAQ 富媒体展示；本轮 FAQPage 仅表达可见问答语义，不将其视为富媒体入口。

尚未代用户开通或验证 Google Search Console、Bing Webmaster Tools、百度搜索资源平台，也未提交依赖账号验证的站点地图；本轮生成的 robots.txt 与 sitemap.xml 可供自动发现。后续应在运营方账号完成站长平台验证及提交，并持续更新展期、地点和联系方式，观察真实索引与查询数据。

## 依据

- Google Search Central：AI features and your website：https://developers.google.com/search/docs/appearance/ai-features
- Google：FAQ structured data：https://developers.google.com/search/updates
- OpenAI crawler overview：https://developers.openai.com/api/docs/bots

## 维护与验证

统一工作区生成器为 scripts/seo_geo.py。独立仓库包含 src/ 静态源文件、tools/seo_geo.py 可重跑的本站生成器、README、requirements.txt 和内容口径说明。公司和项目站的现有完整生成链在最后执行 SEO 生成器。

验证覆盖规范地址、页面元数据、JSON-LD 可解析性、可见问答与结构化答案一致、站点地图文件存在性，以及八站电脑和手机端问答布局。线上发布采用新版本目录与文件哈希校验，保留旧版本回退。
