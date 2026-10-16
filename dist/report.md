# 合并报告


## 各源贡献

| 类型 | 源 | 原始行 | 有效 | 其中 hosts | 其中裸域名 | 去重后 | 通配符跳过 | 丢弃 |
|---|---|---|---|---|---|---|---|---|
| block | 217heidai | 236122 | 236111 | 0 | 0 | 236084 | 0 | 1 |
| block | menghui | 293636 | 292958 | 68 | 0 | 292989 | 399 | 206 |
| block | 扶风 | 33608 | 20789 | 10900 | 0 | 24161 | 841 | 527 |
| block | 海哥 | 13135 | 12919 | 0 | 0 | 12918 | 165 | 36 |
| block | 暗雅日记 | 415 | 385 | 0 | 0 | 385 | 25 | 1 |
| block | 自建 | 292 | 82 | 0 | 0 | 82 | 0 | 0 |
| allow | menghui | 458 | 441 | 0 | 0 | 441 | 10 | 2 |
| allow | kuner | 80 | 37 | 0 | 0 | 37 | 11 | 1 |
| allow | trli | 1431 | 0 | 0 | 1409 | 1404 | 10 | 0 |
| allow | 自建 | 182 | 93 | 0 | 0 | 93 | 0 | 0 |

## 结果

- 黑名单输出：**355951** 条
- 白名单输出：**1893** 条（已统一 `@@||domain^` 语法）
- 自建黑名单域名：**82** 个
- 因自建黑名单优先而剔除的放行条目：**10** 条
- 同域既拦又放（保留放行侧）：**1047** 条

## 解析备注

- `block/217heidai` 有 1 条无法解析被丢弃，样例：`||fb_servpub-a.akamaihd.net^`
- ⚠️ **block/234** 下载失败：`下载失败 https://www.23-4.cn/rules/merged-block.txt: <urlopen error [Errno 104] Connection reset by peer>`
- `block/menghui` 有 399 条含通配符/正则的规则被跳过，样例：`/193.200.64.24:/`, `analytics-*.aasaam.com`, `||*-datareceiver.aki-game.net^`, `||*-default-cn.rum.aliyuncs.com^`
- `block/menghui` 有 206 条无法解析被丢弃，样例：`255.255.255.255 broadcasthost`, `charlestownwyllie.oaklawnnonantum.co`, `dlsdk.appsflyer.com^`, `dlsdk.appsflyersdk.com^`
- `block/扶风` 有 841 条含通配符/正则的规则被跳过，样例：`||at*.doubanio.com^`, `||163487*.qmgmw.com^`, `||bjkedv*.xyz^`, `||gtlpa*.com^`
- `block/扶风` 有 527 条无法解析被丢弃，样例：`.xyz/$domain=pan.huang1111.cn`, `||172.247.208.87/js/head.js`, `||qishula.com/css/ding.js`, `||aiqu2727.com/da/`
- `block/海哥` 有 165 条含通配符/正则的规则被跳过，样例：`||*-99wanyou-com-idvkrgg.qiniudns.co`, `||*-default.ixigua.com^`, `||*-hl.toutiaoapi.com^`, `||*-jor0b302fdhgwnccw8g.com^`
- `block/海哥` 有 36 条无法解析被丢弃，样例：`||/7gq78s4ltrea/^`, `||0019a^`, `||216.239.35.0/24^`, `||295cdn^`
- `block/暗雅日记` 有 25 条含通配符/正则的规则被跳过，样例：`||ad*.idcyz.hb1.kwaidc.com^`, `||ads*-normal-hl.zijieapi.com^`, `||ads*-normal-lf.zijieapi.com^`, `||ads*-normal-lq.zijieapi.com^`
- `block/暗雅日记` 有 1 条无法解析被丢弃，样例：`||api.zhihu.com/ad-style-service`
- ⚠️ **allow/234** 下载失败：`下载失败 https://www.23-4.cn/rules/merged-allow.txt: <urlopen error [Errno 104] Connection reset by peer>`
- `allow/menghui` 有 10 条含通配符/正则的规则被跳过，样例：`@@||api-v*.trbo.com^`, `@@||bcicl.*.evergage.com^`, `@@||brm-core-*.brsrvr.com^`, `@@||cdn.us*.exponea.com^`
- `allow/menghui` 有 2 条无法解析被丢弃，样例：`@@-ds.metric.gstatic.com^`, `@@||白名单仅用于测试.com^`
- `allow/kuner` 有 11 条含通配符/正则的规则被跳过，样例：`@@||*m*.360buyimg.com^`, `@@||storage*360buyimg.com^`, `@@||p*reading*sign.fqnovelpic.com^`, `@@||api*normal*fqnovel.com^`
- `allow/kuner` 有 1 条无法解析被丢弃，样例：`@@auni.telecome.cn^`
- `allow/trli` 有 10 条含通配符/正则的规则被跳过，样例：`*-ssl.apple.com`, `*.sspai.net.cn`, `*.img.mobile.sina.cn`, `*.wikipedia.org`

## 被剔除的放行条目（因为覆盖了你的自建黑名单）

| 被剔除的放行 | 它覆盖的自建黑名单域名 |
|---|---|
| `aegis.qq.com` | aegis.qq.com |
| `alibaba.com` | fourier.alibaba.com |
| `app-measurement.com` | app-measurement.com |
| `baidu.com` | union.baidu.com |
| `bytedance.com` | scc.bytedance.com |
| `e.kuaishou.com` | e.kuaishou.com |
| `mon.zijieapi.com` | mon.zijieapi.com |
| `qq.com` | aegis.qq.com, appchannel.html5.qq.com, btrace.qq.com, e.qq.com, gdt.qq.com, masdk.3g.qq.com, pingjs.qq.com, pmir.3g.qq.com, tdid.m.qq.com, trace.qq.com, union.eff.qq.com |
| `snssdk.com` | applog.snssdk.com, log.snssdk.com, rtapplog.snssdk.com, rtlog.snssdk.com |
| `taobao.com` | fourier.taobao.com, h-adashx.ut.taobao.com |

## 剩余整域放行（段数 <= 2，建议人工复核）

共 174 条：

- `000714.xyz`
- `123pan.com`
- `126.net`
- `163.com`
- `360.cn`
- `360safe.com`
- `a-msedge.net`
- `afdian.net`
- `afi-b.com`
- `akamai.net`
- `akamaiedge.net`
- `aliapp.org`
- `alibabadns.com`
- `alicdn.com`
- `alidns.com`
- `alipay.com`
- `aliyun.com`
- `aliyuncs.com`
- `apkmirror.com`
- `apple-dns.net`
- `awin1.com`
- `b23.tv`
- `baidupcs.com`
- `bcy.net`
- `bing.com`
- `blueskyxn.com`
- `bootcdn.net`
- `bytednsdoc.com`
- `bytegecko.com`
- `byteimg.com`
- `camscanner.com`
- `cdn-go.cn`
- `chatglm.cn`
- `cmpassport.com`
- `cnzz.com`
- `coolapk.com`
- `coolapkmarket.com`
- `ctobsnssdk.com`
- `cubox.pro`
- `cupfox.app`
- `cutcaptcha.com`
- `cz88.net`
- `dns.google`
- `dns.pub`
- `dnscheck.tools`
- `doh.pub`
- `dot.pub`
- `douban.com`
- `dpurl.cn`
- `drvsky.com`
- `duckduckgo.com`
- `dynamic-dns.net`
- `dynv6.com`
- `elemecdn.com`
- `envato.market`
- `example.org`
- `facebook.com`
- `flydigi.com`
- `fqnovel.com`
- `fqnovelpic.com`
- `fqnovelstatic.com`
- `gepush.com`
- `getquicker.net`
- `getui.com`
- `getui.net`
- `ghproxy.com`
- `giscus.app`
- `gitcode.net`
- `github.com`
- `gov.cn`
- `greasyfork.org`
- `gtimg.cn`
- `haiwaikan.com`
- `hcfy.ai`
- `heytapdownload.com`
- `hicloud.com`
- `hidive.com`
- `hitokoto.cn`
- `href.li`
- `iana.org`
- `ibytedapm.com`
- `icloud.com`
- `idqqimg.com`
- `igexin.com`
- `intel.com`
- `ip.sb`
- `ip111.cn`
- `ip138.com`
- `ipify.org`
- `ipinfo.io`
- `ipip.net`
- `japaneseasmr.com`
- `jcloud-cdn.com`
- `jd.com`
- `jihulab.com`
- `jomodns.com`
- `leechers-paradise.org`
- `limestart.cn`
- `linka.page`
- `logentries.com`
- `maimemo.com`
- `maimemostatus.com`
- `mega.nz`
- `meiqia.com`
- `meituan.net`
- `metaso.cn`
- `mi.com`
- `microsoft.com`
- `microsoftapp.net`
- `miui.com`
- `miwifi.com`
- `mt2.cn`
- `musescore.org`
- `myqcloud.com`
- `myquark.cn`
- `mzstatic.com`
- `netease.com`
- `novelquickapp.com`
- `oray.com`
- `outlook.com`
- `pgpartner.com`
- `pixso.cn`
- `pstatp.com`
- `qcloud.com`
- `qishui.com`
- `qpic.cn`
- `remembering.ca`
- `rethinkdns.com`
- `servicewechat.com`
- `shifen.com`
- `shuzilm.cn`
- `sinaimg.cn`
- `singapore.com`
- `skype.com`
- `smartplg.com`
- `so.com`
- `sogou.com`
- `spartaindependent.com`
- `src.top`
- `stackoverflow.com`
- `steamcommunity.com`
- `suo.im`
- `syncthing.net`
- `t.cn`
- `tanx.com`
- `tb.cn`
- `tdnsdp1.cn`
- `tdnsvod1.cn`
- `telegra.ph`
- `tencent-cloud.com`
- `tencent-cloud.net`
- `tencent.com`
- `tenpay.com`
- `termux.net`
- `tlaol.com`
- `uc.cn`
- `ufileos.com`
- `used.ca`
- `visa.cn`
- `warhammer40000.com`
- `weatheroffer.com`
- `weibo.cn`
- `weibo.com`
- `wht.im`
- `wikipedia.org`
- `wpengapp.com`
- `wpsdns.com`
- `wpsmail.net`
- `wsglb0.com`
- `xhslink.com`
- `ydns.io`
- `youtube.com`
- `ys168.com`
- `ysepan.com`

## 同域冲突

共 1047 条：这些域名在合并黑名单里要拦、在合并白名单里要放，AGH 里例外优先，所以**实际不会拦**。

想把其中某几个恢复拦截：把它们加进 `blacklist.txt`，下次跑流水线会自动剔除白名单侧对应条目。
完整清单见 `dist/conflicts.txt`。

- `000714.xyz`
- `316.coolapk1s.com`
- `360.cn`
- `3g.ali213.net`
- `5471782.fls.doubleclick.net`
- `79423.analytics.edgekey.net`
- `a.adwolf.ru`
- `a.sellpoint.net`
- `a0.app.xiaomi.com`
- `aapl-edge0.qtlcdn.com`
- `aax-fe.amazon.co.jp`
- `abtest-ch.snssdk.com`
- `abtest3-misc-lf.zijieapi.com`
- `ac.ebis.ne.jp`
- `access.open.uc.cn`
- `account.xiaomi.com`
- `accounts.google.com`
- `acs-m.daraz.com.bd`
- `acs-m.daraz.pk`
- `acs.m.taobao.com`
- `acs.youku.com`
- `acs4baichuan.m.taobao.com`
- `acstatic-dun.126.net`
- `act-webstatic.hoyoverse.com`
- `act.hoyoverse.com`
- `act.vip.iqiyi.com`
- `action.metaffiliation.com`
- `activity.hdslb.com`
- `ad-log-upload.mihoyo.com`
- `ad.10010.com`
- `ad.abchina.com`
- `ad.kazakinfo.com`
- `ad.ourgame.com`
- `ad.tencentmusic.com`
- `adash-emas.cn-hangzhou.aliyuncs.com`
- `adcdn.pingan.com`
- `adcdn.tencentmusic.com`
- `adclick.tencentmusic.com`
- `adexpo.tencentmusic.com`
- `admin.dable.io`
- `admin.mailchimp.com`
- `ads.tdbank.com`
- `adsmind.gdtimg.com`
- `adstats.tencentmusic.com`
- `advert.kf5.com`
- `advertise.baicizhan.com`
- `adx-bj-req.anythinktech.com`
- `adx-bj.anythinktech.com`
- `adx.anythinktech.com`
- `ae.bdstatic.com`
- `ae01.alicdn.com`
- `afi-b.com`
- `aks.jdpay.com`
- `ali-gamezone.static.yximgs.com`
- `ali-ky.static.yximgs.com`
- `ali-stats.jpush.cn`
- `ali.static.yximgs.com`
- `ali2.a.kwimgs.com`
- `ali2.a.yximgs.com`
- `alt1-mtalk.google.com`
- `alt2-mtalk.google.com`
- `alt3-mtalk.google.com`
- `alt4-mtalk.google.com`
- `alt5-mtalk.google.com`
- `alt6-mtalk.google.com`
- `alt7-mtalk.google.com`
- `alt8-mtalk.google.com`
- `amdc.alipay.com`
- `amdc.m.taobao.com`
- `amp-api-edge.apps.apple.com`
- `ams.lenovomm.com`
- `analytics-api-01.smzdm.com`
- `analytics.95516.com`
- `analytics.95516.com.wscdns.com`
- `analytics.amplitude.com`
- `analytics.githubassets.com`
- `analytics.map.qq.com`
- `analytics.meituan.net`
- `analytics.umetrip.com`
- `android-artworks.25pp.com`
- `android.bugly.qq.com`
- `ant.pingan.com.cn`
- `anwb.webpower.eu`
- `ap01.records.in.treasuredata.com`
- `ap6.ssl.msdk.qq.com`
- `apd-vodp2plogin.teg.tencent-cloud.net`
- `api-access.pangolin-sdk-toutiao-b.com`
- `api-access.pangolin-sdk-toutiao.com`
- `api-access.pangolin-sdk-toutiao1.com`
- `api-cn.cdo.heytapmobi.com`
- `api-cn.store.heytapmobi.com`
- `api-cn.theme.heytapmobi.com`
- `api-ks.wtzw.com`
- `api-push.meizu.com`
- `api-sc.wtzw.com`
- `api-shoulei-ssl.xunlei.com`
- `api-unionid.meituan.com`
- `api.account.xiaomi.com`
- `api.ad.xiaomi.com`
- `api.ads.tvb.com`
- `api.cloud.huawei.com`
- `api.comm.miui.com`
- `api.coolapk.com`
- `api.developer.xiaomi.com`
- `api.device.xiaomi.net`
- `api.docodoco.jp`
- `api.e.kuaishou.com`
- `api.g.micloud.xiaomi.net`
- `api.github.com`
- `api.io.mi.com`
- `api.iplay.163.com`
- `api.jr.mi.com`
- `api.karte.io`
- `api.kingdata.ksyun.com`
- `api.kuaishouzt.com`
- `api.live.bilibili.com`
- `api.map.baidu.com`
- `api.micloud.xiaomi.net`
- `api.miwifi.com`
- `api.neixin.cn`
- `api.open.oppomobile.com`
- `api.revenuecat.com`
- `api.sec.miui.com`
- `api.smoot.apple.com`
- `api.tw06.xlmc.sec.miui.com`
- `api.union.vip.com`
- `api.vip.miui.com`
- `api.xunyou.mobi`
- `api.zhuti.xiaomi.com`
- `api2.e.kuaishou.com`
- `api5-normal-lf.fqnovel.com`
- `apihb6.ksapisrv.com`
- `apijs.gifshow.com`
- `apijsv6.gifshow.com`
- `apijsv6.ksapisrv.com`
- `apikey.map.qq.com`
- `apisnd.heytapmobi.com`
- `apissl.gifshow.com`
- `apissl.ksapisrv.com`
- `apiv4-iyes.youku.com`
- `app-advertise.zhihuishu.com`
- `app-monitor.ele.me`
- `app.adjust.com`
- `app.appsflyer.com`
- `app.bilibili.com`
- `app.home.360.cn`
- `app.market.xiaomi.com`
- `app.toutiao.com`
- `appcloud2.in.zhihu.com`
- `appconf.heytapdownload.com`
- …（还有 897 条，见 conflicts.txt）
