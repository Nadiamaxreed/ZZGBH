# 郑州工业博览会

正式网站：https://zzgbh.hm-d.cn/

本仓库保存此站独立的静态网站源文件。`src/` 中的 HTML、CSS、JavaScript 和本地图片可直接由 Nginx 或其他静态服务器提供服务，不需要 Node.js、PHP 或数据库。参展、参观登记继续跳转项目原有外部平台。

## 本地预览与维护

```sh
python -m http.server 8080 --directory src
```

浏览器访问 http://localhost:8080 。修改 `src/` 内相应 HTML/CSS/JS 后即可预览。SEO 与首页问答生成器：

```sh
python -m pip install -r requirements.txt
python tools/seo_geo.py
```

生成器配置保存在 `tools/seo_geo.py`，再次运行会替换由它生成的问答与检索标签。新增或删除页面后应重新生成站点地图。图像原文件与已优化的响应式图片均保留，以维护既有页面引用；主视觉切换前等待图片解码完成。项目网站二维码保留原图。

## SEO / GEO 优化

- 首页新增可直接阅读、可定位的常见问题；HTML 问答与 FAQPage JSON-LD 内容一致。
- 全站标题、内容摘要、HTTPS canonical、语言声明、Open Graph 社交分享信息及空缺图片描述。
- WebSite / WebPage 结构化数据；内页 BreadcrumbList；公司站首页另含已核实的 Organization 联系方式。
- `robots.txt` 指向 `sitemap.xml`；站点地图排除跳转页和已确认的重复栏目入口。
- `llms.txt` 提供官方首页、问答、联系和站点地图入口，仅作为辅助索引，不是搜索或 AI 平台保证支持的排名标准。
- 内容保持静态可抓取，问答答案直接写入 HTML，不依赖客户端请求或折叠后才能读取。

## 内容准确性与边界

现存页面含历届资料和部分未统一的展期、届次、规模数据。新增问答不承诺未经确认的日期、费用、规模、优惠或主办方身份；本届安排应向项目组核实。没有为未确认届次生成 Event 日期/票价，也没有伪造评分、访问量或问答排名保证。Google 已在2026年停止 FAQ 富媒体展示，FAQ 标记仅用于表达可见问答语义。详见 `docs/SEO-GEO.md`。

## 发布与仓库

正式部署时将 `src/` 的内容放入域名对应静态根目录，保留路径与大小写。建议先发布到新版本目录，验证后切换软链接，保留旧版本回退；HTML 使用重新验证缓存，带哈希的优化图片使用长期缓存。仓库不保存 SSH 私钥、服务器账号凭据或报名后台数据。

- GitHub：https://github.com/Nadiamaxreed/ZZGBH
- Gitee：https://gitee.com/nadia20109/zzgbh
- 内容更新及本轮优化日期：2026-11-23。

既有图片和历史转载文章随站保留，素材使用权及授权范围由网站运营方维护。
