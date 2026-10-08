# 酷安 CoolApk 16.6.4 广告域名分析

## 样本

| 项 | 值 |
|---|---|
| 文件名 | `CoolApk-16.6.4-2609291-coolapk-arm64-sign.apk` |
| 大小 | 116,965,943 字节（111 MB） |
| MD5 | `a7f362019530968866f9b3c2e4ccd22b` |
| 架构 | arm64-v8a only |
| 下载源 | `https://dl.coolapk.com/down?pn=com.coolapk.market&id=NDU5OQ&h=46bb9d98&from=from-web`（跟随 302 得到 `dl-t2.coolapkmarket.com` 直链） |
| 分析日期 | 2026-10-08 |

## 方法

1. `unzip` 解包 → 对 `classes.dex`、`lib/arm64-v8a/*.so`、`assets/**` 做域名正则收割（共 1033 个候选）。
2. 单独解开嵌套 jar `assets/gdt_plugin/gdtadv2.jar` 再扫一遍。
3. 批量 DNS 解析验证，109/114 存活。
4. 与 anti-AD（94424 条，版本 20261005）做父域交叉比对。
5. grep 反查 DoH/DoT 与硬编码 DNS。

## 集成的广告 / 追踪 SDK

| SDK | 证据 | 域名来源 |
|---|---|---|
| **穿山甲 / Pangle / GroMore**（主广告源） | `assets/SDK_Setting_5014732.json`：`site_id 5014732`、`app_id 302029`、`partner pangle_302029`；`assets/csj_site_config.json`（加密，`cypher:2`）；类名 `com.bytedance.sdk.openadsdk.*`、`com.bytedance.pangle.*` | `classes.dex` + `assets/lottie_json/*` |
| **优量汇 / GDT** | `assets/gdt_plugin/gdtadv2.jar`；适配器 `com.bytedance.msdk.adapter.gdt`、`com.anythink.network.gdt` | **只在嵌套 jar 内** |
| **快手广告 Ksad** | `assets/ksad_idc.json` 明文列出全部 IDC 域名；`lib/arm64-v8a/libPglbizssdk_ml.so` | `assets/ksad_idc.json` |
| **TopOn / AnyThink 聚合** | `assets/anythink/pl/`、类名 `com.anythink.*` | `classes.dex` |
| **友盟统计** | `libumeng-spy.so`、`libumonitor.so`、`com.umeng.commonsdk.*` | `classes.dex` |
| **点击追踪 / 策略下发** | 上下文里能看到完整 URL，如 `https://adx-strategy-api-cn.statisticslinks.com/sdk/pl_strategy`、`https://tk.statisticslinks.com/v2/open/a_tk` | `classes.dex` |
| 网易易盾（风控） | `libnesec.so`、`ac-v6.dun.163yun.com`、`cstaticdun.126.net` | — |
| 数美（风控） | `assets/cn.shuzilm.config.json`、`libsgcore.so`、`id6.me` | — |
| Adjust（归因） | `libEncryptorP.so` 附近字符串、`adjust` 相关常量 | — |
| Bugly（崩溃） | `libucrash.so`、`libuCrash-core.so` | — |
| vivo 广告 | `assets/supplierconfig.json`：`appid 100215079` | — |

酷安自己的广告封装类：`com.coolapk.market.view.ad.toutiao.*`（穿山甲）、`com.coolapk.market.view.ad.tencent.*`（优量汇）。

## 关键结论

### 1. 优量汇域名藏在嵌套 jar 里

直接扫 APK 本体，`gdt.qq.com` / `ugdtimg.com` / `e.qq.com` **一个都扫不到**——它们在 `assets/gdt_plugin/gdtadv2.jar`（2 MB，内含 `classes.dex`）里。不解嵌套 jar 就会漏掉整个优量汇。

### 2. 没有 DoH/DoT，DNS 层拦截有效

全 APK grep 结果：

| 模式 | 命中 |
|---|---|
| `8.8.8.8` / `1.1.1.1` / `223.5.5.5` / `114.114.114.114` | 0 |
| `dns-query` / `application/dns-message` | 0 |
| `dns.google` / `cloudflare-dns` | 0 |
| `resolvers-*.httpdns.aliyuncs.com` | 各 1（阿里云 HTTPDNS，仅用于自家业务解析） |

即：广告 SDK 的域名解析走系统 DNS，拦得住。

### 3. 酷安自营广告拦不住

`api.coolapk.com` / `api2.coolapk.com` 同时承载登录、帖子、图片和自营广告，**没有独立的广告域名**（没有 `ad.coolapk.com` / `adx.coolapk.com` 之类）。DNS 层无法只拦广告。这部分只能靠 App 内设置/会员，或 AdGuard for Android 的 HTTPS 过滤 + 内容规则。

### 4. 拦广告 SDK 的副作用

激励视频、看广告得酷币这类功能会直接黑屏或报错。

## 不宜拦截的域名

| 域名 | 用途 | 拦了会怎样 |
|---|---|---|
| `shuzilm.cn`、`id6.me` | 数美设备指纹 | 触发风控、验证码异常 |
| `dun.163.com`、`cstaticdun.126.net` | 网易易盾 | 登录验证失败 |
| `cmpassport.com`、`e.189.cn` | 移动/电信一键登录 | 登录失败 |
| `tpns.tencent.com`、`mpush-api.aliyun.com` | 移动推送 | 推送收不到 |
| `log.wechatpay.cn` | 微信支付 | 支付异常风险 |
| `i.gtimg.cn`、`qzonestyle.gtimg.cn` | QQ 登录/分享静态资源 | 第三方登录挂 |
| `api.coolapk.com` | 酷安自身 API | App 直接不可用 |

这些已写入 `whitelist.txt` 做兜底放行。
