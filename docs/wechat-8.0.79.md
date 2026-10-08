# 微信 WeChat 8.0.79 广告域名分析

## 样本

| 项 | 值 |
|---|---|
| 文件名 | `weixin8079android3200_0x28004f30_arm64.apk` |
| 大小 | 285,283,432 字节（272 MB） |
| MD5 | `fc2ed347e4af93dc585df86ce537006d` |
| 架构 | arm64-v8a |
| 下载源 | 微信官网 https://weixin.qq.com/ 首页里的 `dldir1v6.qq.com/weixin/android/...` 直链 |
| 分析日期 | 2026-10-08 |

## 方法

APK 太大，**没有解包到磁盘**——直接用 `zipfile` 在内存里逐条目流式扫描（16011 个 zip 条目，扫了 13178 个非媒体条目），提取 4357 个域名。再与 anti-AD 交叉比对。

## 结论：微信文章里的广告，DNS 层基本拦不住

这是结构性原因，不是没找到：

| 环节 | 走的域名 | 能否 DNS 拦截 |
|---|---|---|
| 广告请求与下发 | `mp.weixin.qq.com/cgi-bin/mmbiz-bin/recommend/timelinecard`、`advertisement_report` | ✗ 与文章本体同域 |
| 广告点击落地页 | `mp.weixin.qq.com?...&weixinadinfo=...&gdt_vid=...` | ✗ 同上 |
| 广告素材图/视频 | `mmbiz.qpic.cn`、`wxsnsdythumb.wxs.qq.com`、`wxsnsdy.wxs.qq.com` | ✗ 与正文图片、朋友圈缩略图同域 |
| 曝光/点击上报 | `ad.wx.com:12638/cgi-bin/exposure`、`/cgi-bin/click` | ✓ 可以拦 |
| 广点通上报 | `pingjs.qq.com` | ✓ 可以拦 |

**广告位本身是服务端注入到公众号文章 HTML 里的**，客户端只负责渲染。所以 DNS 拦截的效果最多是「广告图加载不出来、曝光不计数」，广告位占的空白还在。

想要真正干净，需要的是 **AdGuard for Android 的 HTTPS 过滤 + 内容规则**（按 HTML 元素/选择器过滤），而不是 DNS 域名规则——网上流传的"微信广告规则"基本都是内容规则，原因就在这里。

## 可以安全拦截的（已加入 blacklist.txt）

| 域名 | 证据 | 说明 |
|---|---|---|
| `ad.wx.com` | `assets/mbad_pic.txt` / `mbad_video.txt` 里的 `apurl`(曝光) 和 `rl`(点击)；`MagicAdBrandService.wspkg` 用 `apurl.includes("ad.wx.com")` 判定是否为微信自营广告引擎 | 公网 NXDOMAIN（疑似仅内网/灰度可用），拦了无害 |
| `pingjs.qq.com` | `classes7.dex` | 广点通曝光/点击上报 |
| `btrace.qq.com` | `libDownloadProxy.so` | 行为追踪，已解析到 `0.0.0.1`（等于已是黑洞） |

微信内嵌的广点通落地页与素材——`h5.gdt.qq.com`、`xj.gdt.qq.com`、`wxadliteapp.gdt.qq.com`、`pa.ugdtimg.com`、`review.ugdtimg.com`、`bricks.e.qq.com`、`h.trace.qq.com`——**已被酷安分节的 `gdt.qq.com` / `ugdtimg.com` / `e.qq.com` / `trace.qq.com` 覆盖**，无需重复添加。

另外在微信 APK 里发现一批通用第三方广告/统计域名（`googlesyndication.com`、`doubleclick.net`、`googleadservices.com`、`google-analytics.com`、`app-measurement.com`、`masdk.3g.qq.com`、`appchannel.html5.qq.com`、`pmir.3g.qq.com`、`aegis.qq.com`），已单独成节加入。

## 不能拦的（通用规则集会误伤）

| 域名 | 实际用途 | 拦了会怎样 |
|---|---|---|
| `mp.weixin.qq.com` | 公众号文章本体 | 文章打不开 |
| `mmbiz.qpic.cn` | 正文图片 + 广告图片共用 | 正文图片全挂 |
| `wxs.qq.com`（含 `wxa.wxs.qq.com`、`wxsnsdythumb.wxs.qq.com`） | 朋友圈缩略图 / 小程序静态资源 | 朋友圈缩略图、小程序资源挂 |
| `dns.weixin.qq.com`、`dns.weixin.qq.com.cn` | 微信私有 DNS 解析 | 网络异常 |
| `aedns.weixin.qq.com` | 微信加速 DNS（`libilink_network.so`） | 解析变慢 |
| `as.weixin.qq.com` | `r/s/domain_mainland.json` 域名映射表里的正常业务域 | 部分业务异常 |
| `apd-pcdnwxstat/login/nat.teg.tencent-cloud.net` | `libwechatmm.so` 里的 PCDN / 登录长连接 / NAT 穿透（`NatProtocolHandler`、`LoginLink`、`TcpTransMgr`） | 掉线、连不上 |
| `ad.weixin.qq.com`、`ads.privacy.qq.com` | **个性化广告关闭入口**（`/pdf.html?post_id=`、`/ads/wxoptout.html`） | 关不掉个性化广告 |

> 注意：`wxs.qq.com`、`aedns.weixin.qq.com`、`as.weixin.qq.com`、`apd-pcdnwx*.teg.tencent-cloud.net`、`dns.weixin.qq.com.cn` 这几条 **anti-AD 是拦的**。如果你订阅了 anti-AD，务必把 `whitelist.txt` 也一起导入，否则微信会出各种毛病。

## 顺带发现

- `assets/mbad_pic.txt`、`assets/mbad_video.txt` 是**明文广告样本数据**（含 `ad_posid`、`aid`、`traceid`、曝光/点击上报链接），分析微信广告结构时可以直接读这两个文件，不用抓包。
- `assets/mbpkgs/MagicAd*.wspkg` 是微信的广告服务包（`MagicAdBrandService`、`MagicAdMiniProgram`、`MagicNewAdPlayableBasic` 等），是未加密的 JS bundle，广告逻辑都在里面。
