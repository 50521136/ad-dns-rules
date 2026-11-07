# XSOF Free v3.3 —— 域名提取与还原记录

> 来源文件：`readme.txt`（XSOF Free v3.3 模块的 README，KernelSU / Magisk 通用模块）
> 用途：禁用小米 HyperOS 的 XSOF 涉诈检测组件、拦截上报域名、清理本地行为库。
> 本文只做**域名提取与还原**，不评价该模块本身。

## 一、原始输入长什么样

README 第 25 行是唯一的域名清单：

```
| 拦截域名 | 19 个：`flash` / `api` / `virus-engine` / `detection-aigc` / `fraud-detection` / `data.sec` / `tracking` / `srv` / `dm.wo.com.cn` / `eps.caict.ac.cn` / `gateway-papa.cloud.weizhi.com` / `api.ad.xiaomi.com` / `om.tracking` / `framework.sec` / `pn-tracking-bak` / 海外 tracking 变体 |
```

程序化拆解（按 `/` 分隔，去掉首尾反引号与「19 个」前缀）得到 **16 项**，构成如下：

| 类别 | 数量 | 内容 |
|---|---|---|
| 完整域名 | 4 | `dm.wo.com.cn`、`eps.caict.ac.cn`、`gateway-papa.cloud.weizhi.com`、`api.ad.xiaomi.com` |
| 省略后缀的简称 | 11 | `flash`、`api`、`virus-engine`、`detection-aigc`、`fraud-detection`、`data.sec`、`tracking`、`srv`、`om.tracking`、`framework.sec`、`pn-tracking-bak` |
| 类别描述（非域名） | 1 | 「海外 tracking 变体」 |

**结论 1：README 声称 19 个，实际列了 16 项，只有 4 个是能直接写进规则的完整域名。**
差的 3 条疑为「海外 tracking 变体」展开后的条目，但 README 没写具体域名，不猜。

另外第 58 行的自检命令给出了第 5 个完整域名：

```bash
ping -c1 flash.sec.miui.com       # 期望解析到 127.0.0.1
```

这是还原简称的锚点：说明 `flash` 补全后是 `*.sec.miui.com`。

文档里 `raw.githubusercontent.com`（第 215 行）是 `updateJson` 模板地址，**不是拦截目标**。
其余长得像域名的都是误伤项：`127.0.0.1`（IP）、`com.miui.securitycenter` 等（Android 包名/组件类名）、
`net.dns1`（属性名）、`module.pop` / `verify.sh` / `fraud_detection_data.db`（文件名）、
`v2.9` / `v3.3` / `4.0.0.23.XOCCNXM`（版本号）。这些都没收进规则。

## 二、简称还原与证据链

按公开的同源小米 hosts / 逆向报告交叉验证。`flash.sec.miui.com` 由 README 自身给出，
其余均为外部规则佐证（**不是模块原文**，真机 `system/etc/hosts` 才是权威清单）。

| 简称 | 还原后 | 依据 |
|---|---|---|
| `flash` | `flash.sec.miui.com` | README L58 自证；LoopDns/Fuck-you-MIUI `Fhosts`、柴郡猫教程 |
| `api` | `api.sec.miui.com` | `Fhosts`（「流量更新、病毒白名单」）、Kittyskj/FreeFromMi `hosts_adguard` |
| `virus-engine` | `virus-engine.sec.miui.com` | `Fhosts`、柴郡猫教程、`hosts_adguard` |
| `detection-aigc` | `detection-aigc.engine.miui.com` | purainity/MIUIGuardProvider 逆向报告（AI Guard 音频/视频检测接口） |
| `fraud-detection` | `fraud-detection.engine.miui.com` | std-microblock《小米反诈监控传闻技术核验》、柴郡猫教程 |
| `data.sec` | `data.sec.miui.com` | `Fhosts`、柴郡猫教程、`hosts_adguard`、CyStack 子域枚举 |
| `tracking` | `tracking.miui.com` | `Fhosts`、hagezi `native.xiaomi.txt` |
| `srv` | `srv.sec.miui.com` | `Fhosts` 注释（「权限云控」） |
| `om.tracking` | `om.tracking.miui.com` | hagezi `native.xiaomi.txt`（Operations/monitoring tracking） |
| `framework.sec` | `framework.sec.miui.com` | CyStack `miui.com` 子域枚举 |
| `pn-tracking-bak` | — | 公开规则里查不到对应完整域名，**不还原、不猜** |
| 「海外 tracking 变体」 | — | 类别描述；疑似 `tracking.intl.miui.com` / `flash.sec.intl.miui.com` / `data.sec.intl.miui.com` 等 intl 系列，待真机 hosts 确认 |

**结论 2：去重后可用域名 14 条**（4 个原文完整域名 + L58 的 `flash.sec.miui.com` + 9 个简称还原；
`flash.sec.miui.com` 在原文完整域名组里没重复，还原组里那次已去掉）。

## 三、这批域名的实际用途（拦之前要知道）

公开逆向核验显示，README 把它们统称「实测上报域名」，但其中几条并非反诈上报，
拦了会有真实功能影响。所以本仓库把它们单独放 `oem-telemetry.txt`，不并入
`sources.json` 的合并流水线（那条对所有租户全局生效）。

| 域名 | 实际用途 / 副作用 |
|---|---|
| `eps.caict.ac.cn` | 中国信通院统一反诈接口；也是拨打 110/120 时上传号码、区号、定位的紧急报警辅助通道，有独立开关与隐私政策 |
| `gateway-papa.cloud.weizhi.com` | 同上，报警辅助通道，AES 加密上报 |
| `dm.wo.com.cn` | 中国联通终端管理遥测，仅存在于预置 `com.mobiletools.systemhelper` 的机型；走 `:18080` 且可能写死 IP，DNS 层拦不住 |
| `fraud-detection.engine.miui.com` | 固件里唯一调用点是 NFC 门禁卡模拟的**配置下发**（`/nfc/antifraud/config`），与通话反诈无关；拦了影响门禁 |
| `flash.sec.miui.com` | 安全中心通用接口：`/user/ra` 上传已装应用包名做隐私风险检测、`/gc/dir` 拉垃圾清理路径库 |
| `detection-aigc.engine.miui.com` | AI 通话防护（AI Guard）的机密计算检测通道，上传音视频片段做判定 |
| `srv.sec.miui.com` | 权限云控，公开 hosts 规则特意注释并注明「禁用后无法开启部分权限」 |
| `virus-engine.sec.miui.com` / `api.sec.miui.com` | 病毒扫描引擎、病毒白名单与流量更新；拦了安全扫描的云端查询会失效 |
| `data.sec.miui.com` / `framework.sec.miui.com` | 安全中心数据上报 / 框架云控 |
| `tracking.miui.com` / `om.tracking.miui.com` | OneTrack 系统追踪、运营监控追踪 |
| `api.ad.xiaomi.com` | 小米广告 SDK 接口 |

`README` 自己也写了「会失去什么」：AI 换脸 / 反诈预警提示、部分安全扫描的云端查询、
手机管家个别页面可能报错。

## 四、落地方式

规则已写入 `oem-telemetry.txt`，按品牌分节（小米是第一节，后续品牌照抄格式）。
14 条默认全部启用，带 ⚠ 的条目在文件内逐条注明副作用，只想拦纯遥测就把那几行注释掉。

- 独立订阅：`https://raw.githubusercontent.com/50521136/ad-dns-rules/main/oem-telemetry.txt`
- **不**加入 `sources.json`，不进 `dist/block-merged.txt`
- 自用设备或指定用户层导入，不当通用黑名单全局下发
- 已与 `blacklist.txt` / `whitelist.txt` 交叉检查：`api.ad.xiaomi.com` 在 blacklist 酷安节里是
  `!||api.ad.xiaomi.com^` 注释未启用状态，不构成重复启用；其余 13 条无重复
