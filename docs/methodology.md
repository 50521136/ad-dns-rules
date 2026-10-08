# 方法论：从 APK 提取广告域名

## 工具链

```bash
mkdir -p ~/apk-tools && cd ~/apk-tools
apt-get install -y openjdk-17-jre-headless
curl -sL -o jadx.zip https://github.com/skylot/jadx/releases/download/v1.5.1/jadx-1.5.1.zip && unzip -oq jadx.zip -d jadx
curl -sL -o apktool.jar https://github.com/iBotPeaches/Apktool/releases/download/v2.11.1/apktool_2.11.1.jar
```

纯域名提取**不需要**跑 jadx 全量反编译（100 MB+ 的 APK 会吃掉几 GB 磁盘、十几分钟）。dex 的字符串常量池是明文，直接对二进制做正则扫描就够，秒级完成。jadx/apktool 只在需要看代码逻辑或解 `AndroidManifest.xml` 时才用。

## 流程

### 1. 拿 APK

国内 App 走官方 CDN 最稳。应用宝（`sj.qq.com/appdetail/<pkg>`）和豌豆荚的详情页是 JS 渲染，抓不到直链；APKPure 直链（`d.apkpure.com/b/APK/<pkg>`）现在返 403。

常见做法是打开官网首页，在 HTML 里找 `dl.<domain>/down?pn=<包名>` 形式的跳转，跟随 302 拿到真实 apk 地址。

### 2. 解包并扫描

```bash
unzip -oq app.apk -d apk_raw
```

按信息量排序的扫描目标：

| 目标 | 说明 |
|---|---|
| `classes*.dex` | 明文域名常量，主要来源 |
| `lib/arm64-v8a/*.so` | 加固/加密 SDK 的域名常留在这里 |
| `assets/*.json` | **最高价值**：广告 SDK 的 IDC 配置是明文的，如 `ksad_idc.json`（快手广告全部域名）、`SDK_Setting_*.json`（穿山甲 site_id/app_id）、`supplierconfig.json` |
| `assets/**/*.jar` | **嵌套 jar 必须单独解**，正则扫不到 deflate 内容 |
| `res/raw`、`res/*.xml` | 补充 |

正则用宽口径，同时记录匹配点后 70 字符的**上下文片段**——这是判断域名用途的关键：

```
https://adx-strategy-api-cn.statisticslinks.com/sdk/pl_strategy   → 一眼看出是广告策略下发
https://da.dun.163.com/sn.gif?d=                                  → 网易易盾上报，风控不是广告
```

### 3. 三道准确性关卡

**① DNS 存活验证。** 批量解析候选域名，存活的才可能是真端点。Java 包名（`com.foo.bar`）会大量混进来，解析失败直接剔除。32 线程并发跑几百个域名几秒完事。

注意有些域名会解析到 `127.0.0.1`（如 `cnlogs.umeng.com`）或内网 IP（`10.8.15.x`），这是 SDK 的本地兜底配置，不代表端点无效。

**② 公共规则集交叉比对。** 拉 anti-AD 做父域匹配，确认哪些已是公认广告域、哪些是新挖到的。既是验证也是交付亮点。

- anti-AD easylist：`https://anti-ad.net/easylist.txt`（约 9.4 万条，中文场景最全）
- AdGuard 中文过滤器：`https://raw.githubusercontent.com/AdguardTeam/AdGuardFilters/master/ChineseFilter/sections/adservers.txt`

**③ 反查 DoH/DoT。** grep `dns-query`、`application/dns-message`、`8.8.8.8`、`1.1.1.1`、`dns.google`、`cloudflare-dns`、`dot.`。**有 DoH 就说明 DNS 层拦不住**，必须改拦 DoH 端点本身或上 SNI 层。

## 踩过的坑

- **IPv6 出网不通时 curl 会挂死**（DNS 返回 AAAA 但 TLS 无响应）→ 所有 curl 一律加 `-4`。
- **加固 App 的 `classes.dex` 头部可能被改坏**：见过 102 MB 的 dex 头部写着 `string_ids_size=980`、`class_defs_size=30`，但字符串区仍是明文，正则照样能提取。别被这个假象劝退。
- **别用 `sed 's/^[^:]*://'` 处理 `grep -a` 的二进制匹配输出**，会把匹配内容本身截断。
- **TLD 白名单两难**：`app|dev|io|co|me|cc|tv|live|link|top|shop|site|online|pro|fun|store|tech|work|info` 既是真 TLD 又是 Java 包名段。别靠 TLD 白名单追求准确，靠 DNS 存活验证兜底。

## 交付格式

不要给一坨平铺规则。分三档：

- **A 档**：核心广告 SDK，建议启用。
- **B 档**：可选，注释掉并注明副作用（抖音唤起、图片 CDN、统计 SDK）。
- **C 档**：**明确不建议拦**，注释掉并写原因（风控 / 一键登录 / 推送 / 支付 / 第三方登录资源）。用户最容易被通用规则集坑的就是这一块。

外加 `@@||` 白名单兜底，防大规则集误杀 App 正常功能。

交付前自检：语法、去重、拦截与白名单冲突、以及**规则集对提取域名列表的命中覆盖率**（覆盖率太低说明漏了 SDK）。
