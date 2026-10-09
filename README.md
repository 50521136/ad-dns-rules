# ad-dns-rules

自用广告域名拦截规则，来源于 **APK 静态逆向**——不是抄公共规则集，而是从 App 实际会连的域名里提取出来的。

## 订阅地址

### 自建规则（手工维护，APK 逆向产出）

**黑名单（拦截）**

```
https://raw.githubusercontent.com/50521136/ad-dns-rules/main/blacklist.txt
```

**白名单（例外）**

```
https://raw.githubusercontent.com/50521136/ad-dns-rules/main/whitelist.txt
```

### 合并产物（GitHub Actions 自动生成）

由 [`.github/workflows/merge.yml`](.github/workflows/merge.yml) 每周自动拉取
[`sources.json`](sources.json) 里配置的上游订阅源，**归一化语法 → 合并 → 去重 → 按策略裁剪**：

```
https://raw.githubusercontent.com/50521136/ad-dns-rules/main/dist/block-merged.txt   # 约 55 万条
https://raw.githubusercontent.com/50521136/ad-dns-rules/main/dist/allow-merged.txt   # 约 6600 条
```

用这两条可以**替换掉原来 9 个第三方订阅**（规则量从 126 万降到 55 万，去重 56%）。

**导入方式：两条都按「添加黑名单」加入**——`allow-merged.txt` 已统一成 `@@||domain^`
语法，所以它就是一个普通的例外列表，不需要占用 AGH 的「白名单」槽位。

> **为什么要放在普通槽位而不是白名单槽位？**
> AGH 的「白名单过滤器（whitelist_filters）」是独立引擎，命中就 return，**连 `$important`
> 都压不过**（见 `internal/filtering/filtering.go` 的 `matchHost`）。放在普通槽位后，
> `@@` 例外照常生效，但需要时可以用 `||domain^$important` 覆盖它——日志里点「拦截」按钮
> 生成的正是这条规则。

### 合并策略（`sources.json` 的 `policy`）

| 策略 | 作用 |
|---|---|
| `self_block_wins` | `blacklist.txt` 里每个域名，都会把 allow 列表里**覆盖它自身及其所有父域**的条目剔除。保证自建规则一定生效 |
| `strip_allow_max_labels` | 设为 `2` 会剔除所有两段整域放行（更激进）；默认 `null` |
| `drop_undecidable_rules` | 丢弃通配符/正则/无法解析的规则（AGH 的 DNS 层对它们行为不可控） |

每次跑完会产出 [`dist/report.md`](dist/report.md)（各源贡献、剔除明细、整域放行清单）
和 [`dist/conflicts.txt`](dist/conflicts.txt)（同域既拦又放的完整清单）。

**想把某个被放行的域名恢复拦截**：把它加进 `blacklist.txt`，下次跑流水线会自动剔除白名单侧
对应条目——不用去改别人的订阅。


> 国内网络访问 raw.githubusercontent.com 可能不通，可换 jsDelivr 镜像。
> **注意用 `fastly.jsdelivr.net` 或 `gcore.jsdelivr.net`，不要用 `cdn.jsdelivr.net`** ——
> 后者（Cloudflare 节点）对 `@main` 分支引用有最长 12 小时的缓存，推送后经常还在发旧版。
>
> ```
> https://fastly.jsdelivr.net/gh/50521136/ad-dns-rules@main/blacklist.txt
> https://fastly.jsdelivr.net/gh/50521136/ad-dns-rules@main/whitelist.txt
> ```
>
> 仓库已配好 GitHub Action，每次推送会自动调 jsDelivr 的 purge 接口；但 Cloudflare 节点仍可能滞后。
> 要绝对拿到当前版本，用 commit SHA 或 raw 地址：
> `https://raw.githubusercontent.com/50521136/ad-dns-rules/main/blacklist.txt`

### AdGuard Home 导入

`过滤器 → DNS 黑名单 → 添加黑名单`，填黑名单地址；
再 `添加黑名单` 一次，填白名单地址（AGH 里白名单也是作为一种过滤列表加入，`@@` 规则会自动生效）。

## 规则语法

AdGuard / AdGuard Home / 任意 adblock 语法的过滤器都能用：

| 写法 | 含义 |
|---|---|
| `||example.com^` | 拦截 example.com 及其所有子域 |
| `@@||example.com^` | 放行（例外），优先级最高 |
| `! 文字` | 注释，不生效 |

**未启用的规则统一用 `!` 注释保留**，想开启就把行首的 `!` 删掉，不用去别处翻。

## 现有内容

| App | 版本 | 拦截规则 | 分析记录 |
|---|---|---|---|
| 酷安 CoolApk | 16.6.4 (2609291) | 47 条 | [docs/coolapk-16.6.4.md](docs/coolapk-16.6.4.md) |
| 今日水印相机 | 3.0.465.8 | 9 条 | [docs/xcamera-3.0.465.8.md](docs/xcamera-3.0.465.8.md) |
| 红果免费短剧 | 7.2.5.32 | 10 条 | [docs/hongguo-7.2.5.32.md](docs/hongguo-7.2.5.32.md) |
| 微信 WeChat | 8.0.79 | 3 条 + 9 条通用第三方 | [docs/wechat-8.0.79.md](docs/wechat-8.0.79.md) |

四个 App 的拦截难度完全不同：

- **今日水印相机**：✅ 自营广告走 `ad.xhey.top`，业务走 `net-cloud.xhey.top`，完全分离，拦了不影响拍照水印。
- **红果免费短剧**：✅ 广告走独立子域（`ad.zijieapi.com` / `ads*-normal*.zijieapi.com`），和内容 API（`api.fqnovel.com`）完全分开，DNS 层能真正拦干净。
- **酷安**：⚠️ 第三方广告 SDK（穿山甲/优量汇/快手）能拦；自营广告走 `api.coolapk.com`，与业务同域拦不掉。
- **微信**：❌ 广告请求、下发、落地页、素材全部和正文同域（`mp.weixin.qq.com` / `mmbiz.qpic.cn`），DNS 层只能拦上报，拦不掉广告位本身。这一节的主要价值反而是 `whitelist.txt` 里那批放行规则——防止 anti-AD 之类的通用规则集把微信的网络/DNS/CDN 一起拦掉。

## 添加新的 App

1. 在 `blacklist.txt` 末尾照抄现有分节格式，新增一节：

   ```
   ! ==========================================================================
   ! [App 名 版本号] SDK 名 / 广告平台
   ! 来源: 域名是从哪个文件提取出来的（dex / assets/xxx.json / 某个嵌套 jar）
   ! ==========================================================================
   ||domain.com^
   ```

2. 若该 App 的正常功能依赖某些被拦的域名，往 `whitelist.txt` 加对应的 `@@||domain^`。
3. 跑一遍自检：`python3 check.py`（推送后 GitHub Actions 也会自动跑）。

## 方法论

提取流程和踩过的坑都写在 [docs/methodology.md](docs/methodology.md)。要点：

1. 解包后扫 `classes*.dex`、`lib/*.so`、`assets/`，**嵌套 jar 必须单独解开**（优量汇全套域名只存在于 `gdt_plugin/gdtadv2.jar` 里，直接扫 APK 一个都扫不到）。
2. 候选域名批量做 **DNS 存活验证**，剔除 Java 包名噪声。
3. 与 anti-AD 等公共规则集做父域交叉比对，确认哪些是公认广告域。
4. 反查 DoH/DoT：有 DoH 就说明 DNS 层拦不住，得改拦 DoH 端点本身。

## 已知边界

- **App 自营广告拦不住**：走的是和业务接口同一个域名（如酷安的 `api.coolapk.com`），DNS 层无法区分。只能靠 App 内设置/会员，或 AdGuard for Android 的 HTTPS 过滤 + 内容规则。
- **拦广告 SDK 有副作用**：激励视频、看广告得积分这类功能会直接报错或黑屏。
- 规则只做**域名层**拦截，不做 HTTPS 内容过滤。

## License

自用，随手维护。规则本身无版权。
