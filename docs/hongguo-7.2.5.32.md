# 红果免费短剧 com.phoenix.read 广告域名分析

## 样本

| 项 | 值 |
|---|---|
| 文件名 | `红果免费小说（热门小说免费看）_7.2.5.32_apkcombo.com.apk` |
| 大小 | 136,528,995 字节（130 MB） |
| MD5 | `1279c35033facae30979547d8f10911a` |
| 包名 | `com.phoenix.read` |
| 开发者 | 北京笔墨留香科技有限公司（抖音集团） |
| 版本 | 7.2.5.32（小米应用商店最新为 7.3.9.32） |
| 来源 | apkcombo（Cloudflare 挡 curl，用真实浏览器下载） |
| 分析日期 | 2026-10-08 |

## 结论：红果的广告域名可以干净地拦掉

这是本次三个 App 里**唯一一个 DNS 层能真正解决问题**的。原因是红果用字节自研的广告接口，广告请求走**独立子域**，和内容 API 完全分开：

| 用途 | 域名 |
|---|---|
| **广告请求 API** | `ad.zijieapi.com`、`ads.zijieapi.com` |
| **广告服务集群** | `ads3-normal.zijieapi.com`、`ads5-normal.zijieapi.com`（含 `-lf`/`-hl`/`-lq` 区域变体，共 8 个） |
| 内容 API（**不能拦**） | `api.fqnovel.com`、`api5-normal*.fqnovel.com`、`reading.snssdk.com` |
| 封面图 CDN（**不能拦**） | `lf3-reading.fqnovelpic.com`、`p1-reading.byteimg.com`、`p3-novel.byteimg.com` |

## 证据

### 1. 广告 API 路径（`classes15.dex`）

```
https://ad.zijieapi.com
https://ad.zijieapi.com/api/ad/v1/
https://ad.zijieapi.com/api/ad/v1/dislike/
https://ad.zijieapi.com/api/ad/v1/dislike/filterwords/
https://ad.zijieapi.com/api/ad/v1/inspire_send/
https://ad.zijieapi.com/api/ad/v1/report/
```

`dislike`（不喜欢该广告）、`inspire_send`（激励广告完成回调）、`report`（曝光上报）——典型的广告 SDK 接口。

### 2. 广告调度配置（`classes6.dex`）

```json
{
  "service_name": "ad_default",
  "strategy_info": {
    "ad.zijieapi.com":  "ads5-normal.zijieapi.com",
    "ads.zijieapi.com": "ads5-normal.zijieapi.com"
  }
}
```
```json
{
  "service_name": "ad_serial_route",
  "strategy_info": {
    "candidates": [
      {"host": "ads5-normal.zijieapi.com", "threshold": 5000, "weight": 0},
      {"host": "ads3-normal.zijieapi.com", "threshold": 5000}
    ]
  }
}
```

也就是说 `ad.zijieapi.com` 只是入口，实际请求会被调度到 `ads3/5-normal*.zijieapi.com` 集群 —— **两边都要拦**，只拦入口会被调度绕过。

### 3. 没有集成公开版穿山甲 SDK

grep `pglstatp`、`pangolin-sdk-toutiao`、`gromore` 全部无域名命中，只有 Java 标识符（`dyEnablePangolin`、`dyUseCsj2Code`、`PANGOLIN_UNION`）。说明红果走的是字节内部广告接口，不是第三方穿山甲 SDK —— 所以不能照抄酷安那套规则。

## 为什么不要拦整个 `zijieapi.com`

同一个域下还有这些业务域名，拦了 App 会出问题：

`mon.zijieapi.com`、`verify.zijieapi.com`、`relation.zijieapi.com`、`polaris.zijieapi.com`、`gecko.zijieapi.com`（资源热更新）、`ma.zijieapi.com`、`vcs.zijieapi.com`、`thanos.zijieapi.com`、`minigame3/5-normal.zijieapi.com`、`feedback-c.zijieapi.com`、`mssdk.zijieapi.com`

所以规则必须精确到 `ad.` / `ads*.` 这几个子域。

## 副作用（需要实测）

红果有「看广告得金币 / 看广告解锁下一集」的机制。拦掉广告 API 之后：

- **期望效果**：集间插屏广告请求失败，直接跳过
- **可能问题**：金币任务、看广告解锁章节会点了没反应
- **未知**：App 是否会在请求失败后回退到别的域名（`ads*-normal-lf/hl/lq` 已经一并拦了，覆盖区域变体）

## 踩到的坑：`api.snssdk.com` / `i.snssdk.com` 是内容接口，不是广告

这两个域名原本在酷安那节里被当成穿山甲广告端点拦掉了（酷安确实用它们跑穿山甲）。但在红果里它们是**核心内容与金币接口**：

```
GET  api.snssdk.com/api/novel/book/reader/content/v1        ← 正文内容
GET  i.snssdk.com/luckycat/novel/v1/task/single             ← 金币任务
GET  i.snssdk.com/luckycat/novel/v1/user/gold_box_info      ← 金币宝箱
POST ib.snssdk.com/luckycat/novel/v1/task/done/post_invite_code
GET  is.snssdk.com/service/settings/v3/                     ← 设置
```

`i.snssdk.com` / `api.snssdk.com` 是字节的**公共 API 网关**，被多个 App 共用——在酷安是广告，在红果是内容。所以：

- 已把 `||api.snssdk.com^`、`||i.snssdk.com^` 从黑名单移除，并在「不建议拦截」里写明原因
- 白名单里加了精确放行（不要用 `@@||snssdk.com^` 这种父域，会把穿山甲的 `log.snssdk.com`、`applog.snssdk.com` 一起放掉）

这个冲突是 `check.py` 报出来的——**父域白名单覆盖子域黑名单**那类错误。加规则后一定要跑一遍自检。

## 附带发现

`assets/ad_charge_ring.json` 名字像是广告计费配置，实际是个 Lottie 动效（金币环动画），没有域名信息。

反查 anti-AD（94424 条）确认了以下同族域名也已被社区收录，本规则集已覆盖：
`ads3/5-normal.zijieapi.com`、`ads3/5-normal-lf/lq.zijieapi.com`、`mon.snssdk.com`、`mon.zijieapi.com`、`log.zijieapi.com`、`applog.zijieapi.com`、`applog.snssdk.com`、`monsetting.toutiao.com`、`log3/5-applog.fqnovel.com`、`rtlog3/5-applog.fqnovel.com`。
