# 今日水印相机 com.xhey.xcamera 广告域名分析

## 样本

| 项 | 值 |
|---|---|
| 文件名 | `今日水印相机-30046508-20260930.apk` |
| 大小 | 219,287,074 字节（209 MB） |
| MD5 | `f61df39da82f97ebb84c5094d846125f` |
| 包名 | `com.xhey.xcamera` |
| 版本 | 3.0.465.8（versionCode 30046508） |
| 开发者 | 北京小嘿科技有限责任公司 |
| 来源 | 官方落地页 `https://longmen.xhey.top/app/install_analysis?channelCode=cebianlan`（OpenInstall 下发） |
| 分析日期 | 2026-10-08 |

## 结论：自家广告接口和业务域名分离，可以拦

`classes11.dex` 里明文字符串：

```
https://ad.xhey.top/next/
https://ad-acc.xhey.top/next/
https://aa.birdgesdk.com/v1/d_api
https://h5.xhey.top/feedback-ad?app-transparent-navbar=1&complainAdPlatform=
```

广告位下发走 `ad.xhey.top/next/`，而业务全部在另外的域名上：

| 用途 | 域名 |
|---|---|
| **广告接口（可拦）** | `ad.xhey.top`、`ad-acc.xhey.top` |
| 业务 API（**不能拦**） | `net-cloud.xhey.top`（212 次）、`net-cloud-tx.xhey.top`、`longmen.xhey.top` |
| 业务 H5（**不能拦**） | `h5.xhey.top`（137 次）、`static.xhey.top`、`www.xhey.top` |
| 资源 CDN（**不能拦**） | `xcamerares.xhey.top`（阿里云 OSS：xcamera.oss-cn-beijing.aliyuncs.com） |

所以 `||ad.xhey.top^` + `||ad-acc.xhey.top^` 这两条就能掐掉它自营的广告位，拍照、水印、上传、团队同步都不受影响。

## 集成的广告 SDK

| SDK | 证据 |
|---|---|
| **穿山甲 / GroMore**（字节） | `libpanglearmor.so`、`libpangleflipped.so`、`libtt_ugen_layout.so`、`libttmplayer_lite.so`；`sf3-fe-tos.pglstatp-toutiao.com`（65 次）、`api-access.pangolin-sdk-toutiao*.com`、`www.csjplatform.com` |
| **快手广告 Ksad** | `assets/ksad_idc.json`（明文列出全部 IDC 域名）、`p1/p2/p5-lm.adkwai.com` |
| **TopOn / AnyThink 聚合** | `cn-api.anythinktech.com`、`adx.anythinktech.com` 等 10 个子域 |
| **百度广告联盟** | `cpro.baidustatic.com`、`union.baidu.com`、`com.baidu.mobads.sdk.internal.ai` |
| **1RTB 广告交易平台** | `sdk.1rtb.net`、`dsp.1rtb.com`、`sdk-report.1rtb.com` |
| 巨量引擎统计 | `analytics.oceanengine.com`、`lf-event-manager.oceanengine.com` |
| 广告策略/追踪 | `statisticslinks.com`（与酷安同族） |
| 反作弊 | `aa.birdgesdk.com`、`libsgcore.so`（数美） |
| Bugly 崩溃 | `libBugly_Native.so`、`libbuglybacktrace.so` |
| 神策分析 | `sareport.xhey.top`、`*.saas.sensorsdata.cn` |
| 腾讯灯塔/监控 | `beacon.qq.com`、`rmonitor.qq.com`、`mta.qq.com`、`mdt.qq.com` |
| 个推推送 | `getui.com`、`gepush.com`、`igexin.com` |

`assets/supplierconfig.json` 里配了 vivo / 小米 / 华为 / OPPO 的 appid，但 APK 里**没有对应的厂商广告域名**——这些 appid 用于厂商推送和统计，不是广告联盟。

## 本轮新增的规则

穿山甲、快手、TopOn、statisticslinks、birdgesdk、Google 广告这些域名**已经被前面酷安那节覆盖**，没有重复添加。真正新增的是：

```
||ad.xhey.top^
||ad-acc.xhey.top^
||cpro.baidustatic.com^
||union.baidu.com^
||1rtb.net^
||1rtb.com^
||analytics.oceanengine.com^
||lf-event-manager.oceanengine.com^
||universe.ad.live^
```

## 不能拦的（通用规则集会误伤）

| 域名 | 用途 | 拦了会怎样 |
|---|---|---|
| `net-cloud.xhey.top`、`net-cloud-tx.xhey.top` | 业务 API（上传、同步、团队） | 照片传不上去 |
| `longmen.xhey.top` | 版本/活动/渠道接口 | 更新检查、活动页异常 |
| `h5.xhey.top` | 水印模板、活动 H5、广告投诉页 | 模板加载不出来 |
| `xcamerares.xhey.top` | 资源 CDN | 素材加载失败 |
| `member-ship.xhey.top` | 会员 | 会员功能失效 |
| `api.map.baidu.com`、`loc.map.baidu.com` 等 | 百度定位 | **水印写不出经纬度/地点** |
| `openspeech.bytedance.com` | 语音识别 | 语音输入水印失效 |
| `getui.com`、`gepush.com`、`igexin.com` | 个推推送 | 收不到推送 |

特别注意：**不要写 `@@||xhey.top^` 或 `||xhey.top^` 这种整域规则**——前者会把 `ad.xhey.top` 广告接口一起放行，后者会把整个 App 打死。规则必须精确到子域。

## 官方下载链接能不能用

能。`https://longmen.xhey.top/app/install_analysis?channelCode=cebianlan` 是一个 OpenInstall 落地页（appKey `nq24yu`），页面本身不直接暴露 APK 地址，点「立即下载」时由 OpenInstall 运行时下发。

`curl` 抓不到（按钮是 JS 事件），但用真实浏览器打开、设置好下载目录、点击按钮即可拿到直链并下载。下载到的就是官方最新版 3.0.465.8（与小米应用商店一致），比 apkcombo 上的 3.0.265.10 新。

顺带一提，这个落地页还暴露了两个信息：`sareport.xhey.top/sa?project=ACamera`（神策分析）和 `res.openinstall.com`（渠道归因 SDK）——都是分析上报，不是广告。
