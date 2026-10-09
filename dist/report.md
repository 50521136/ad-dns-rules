# 合并报告


## 各源贡献

| 类型 | 源 | 原始行 | 有效 | 其中 hosts | 其中裸域名 | 去重后 | 通配符跳过 | 丢弃 |
|---|---|---|---|---|---|---|---|---|
| block | 217heidai | 225923 | 225912 | 0 | 0 | 225885 | 0 | 1 |
| block | 234 | 476214 | 474828 | 0 | 0 | 474828 | 1241 | 140 |
| block | menghui | 285883 | 285189 | 81 | 0 | 285221 | 400 | 208 |
| block | 扶风 | 34039 | 20663 | 11412 | 0 | 24039 | 818 | 597 |
| block | 海哥 | 13044 | 12828 | 0 | 0 | 12827 | 165 | 36 |
| block | 暗雅日记 | 415 | 385 | 0 | 0 | 385 | 25 | 1 |
| block | 自建 | 292 | 82 | 0 | 0 | 82 | 0 | 0 |
| allow | 234 | 6569 | 6375 | 0 | 0 | 6375 | 190 | 0 |
| allow | menghui | 457 | 440 | 0 | 0 | 440 | 10 | 2 |
| allow | kuner | 80 | 37 | 0 | 0 | 37 | 11 | 1 |
| allow | trli | 1431 | 0 | 0 | 1409 | 1404 | 10 | 0 |
| allow | 自建 | 182 | 93 | 0 | 0 | 93 | 0 | 0 |

## 结果

- 黑名单输出：**552883** 条
- 白名单输出：**6647** 条（已统一 `@@||domain^` 语法）
- 自建黑名单域名：**82** 个
- 因自建黑名单优先而剔除的放行条目：**19** 条
- 同域既拦又放（保留放行侧）：**3865** 条

## 解析备注

- `block/217heidai` 有 1 条无法解析被丢弃，样例：`||fb_servpub-a.akamaihd.net^`
- `block/234` 有 1241 条含通配符/正则的规则被跳过，样例：`||?adspot_.^`, `||?local_ga_js=.^`, `/(https?:\/\/)213\.32\.115\..{100,}/`, `/(https?:\/\/)217\.182\.11\..{100,}/`
- `block/234` 有 140 条无法解析被丢弃，样例：`||09_19.supfree.net^`, `||ad-cdn_core.cctv.com^`, `||ad_core.cctv.com^`, `||ad_m.cctv.com^`
- `block/menghui` 有 400 条含通配符/正则的规则被跳过，样例：`/193.200.64.24:/`, `analytics-*.aasaam.com`, `||*-datareceiver.aki-game.net^`, `||*-default-cn.rum.aliyuncs.com^`
- `block/menghui` 有 208 条无法解析被丢弃，样例：`255.255.255.255 broadcasthost`, `charlestownwyllie.oaklawnnonantum.co`, `dlsdk.appsflyer.com^`, `dlsdk.appsflyersdk.com^`
- `block/扶风` 有 818 条含通配符/正则的规则被跳过，样例：`||at*.doubanio.com^`, `||163487*.qmgmw.com^`, `||bjkedv*.xyz^`, `||gtlpa*.com^`
- `block/扶风` 有 597 条无法解析被丢弃，样例：`.xyz/$domain=pan.huang1111.cn`, `||172.247.208.87/js/head.js`, `||qishula.com/css/ding.js`, `||aiqu2727.com/da/`
- `block/海哥` 有 165 条含通配符/正则的规则被跳过，样例：`||*-99wanyou-com-idvkrgg.qiniudns.co`, `||*-default.ixigua.com^`, `||*-hl.toutiaoapi.com^`, `||*-jor0b302fdhgwnccw8g.com^`
- `block/海哥` 有 36 条无法解析被丢弃，样例：`||/7gq78s4ltrea/^`, `||0019a^`, `||216.239.35.0/24^`, `||295cdn^`
- `block/暗雅日记` 有 25 条含通配符/正则的规则被跳过，样例：`||ad*.idcyz.hb1.kwaidc.com^`, `||ads*-normal-hl.zijieapi.com^`, `||ads*-normal-lf.zijieapi.com^`, `||ads*-normal-lq.zijieapi.com^`
- `block/暗雅日记` 有 1 条无法解析被丢弃，样例：`||api.zhihu.com/ad-style-service`
- `allow/234` 有 190 条含通配符/正则的规则被跳过，样例：`||*.*.szbdyd.com^`, `||*.4399.com^`, `||*.5054399.com^`, `||*.7k7k.com^`
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
| `anythinktech.com` | anythinktech.com |
| `app-measurement.com` | app-measurement.com |
| `baidu.com` | union.baidu.com |
| `btrace.qq.com` | btrace.qq.com |
| `bytedance.com` | scc.bytedance.com |
| `e.kuaishou.com` | e.kuaishou.com |
| `gdtimg.com` | gdtimg.com |
| `google-analytics.com` | google-analytics.com |
| `googlesyndication.com` | googlesyndication.com |
| `h-adashx.ut.taobao.com` | h-adashx.ut.taobao.com |
| `log.snssdk.com` | log.snssdk.com |
| `mon.zijieapi.com` | mon.zijieapi.com |
| `pingjs.qq.com` | pingjs.qq.com |
| `qq.com` | aegis.qq.com, appchannel.html5.qq.com, btrace.qq.com, e.qq.com, gdt.qq.com, masdk.3g.qq.com, pingjs.qq.com, pmir.3g.qq.com, tdid.m.qq.com, trace.qq.com, union.eff.qq.com |
| `snssdk.com` | applog.snssdk.com, log.snssdk.com, rtapplog.snssdk.com, rtlog.snssdk.com |
| `taobao.com` | fourier.taobao.com, h-adashx.ut.taobao.com |
| `tdid.m.qq.com` | tdid.m.qq.com |

## 剩余整域放行（段数 <= 2，建议人工复核）

共 1181 条：

- `0.com`
- `000714.xyz`
- `123pan.com`
- `126.net`
- `163.com`
- `17u.cn`
- `18comic.org`
- `18comic.vip`
- `1drv.com`
- `1drv.ms`
- `1kinobig.ru`
- `1sapp.com`
- `22.do`
- `321mh.com`
- `360.cn`
- `360buyimg.com`
- `360kuai.com`
- `360safe.com`
- `3975.com`
- `40017.cn`
- `4ix.com`
- `4shared.com`
- `56.com`
- `7x24s.com`
- `7zap.com`
- `8pecxstudios.com`
- `91haoka.cn`
- `a-msedge.net`
- `abuelos.com`
- `ac24horas.com`
- `acg02.cc`
- `acgnet.cn`
- `acompli.net`
- `actuabd.com`
- `ad-gone.com`
- `ad.jp`
- `ad.nl`
- `adaway.org`
- `adnmb3.com`
- `ads.finance`
- `adtidy.org`
- `aeotec.com`
- `afdian.com`
- `afdian.net`
- `afi-b.com`
- `afraid.org`
- `agrd.io`
- `aihuishou.com`
- `aikq.de`
- `airydress.com`
- `aizhan.com`
- `ak.sv`
- `akadns.net`
- `akamai.net`
- `akamaiedge.net`
- `akamaihd.net`
- `akamaitechnologies.com`
- `akamaized.net`
- `al-aqsanews.com`
- `aliapp.org`
- `alibabadns.com`
- `alicdn.com`
- `alidns.com`
- `aliexpress.com`
- `alipay.com`
- `alistgo.com`
- `aliyun.com`
- `aliyuncs.com`
- `allrecipes.com`
- `altervista.org`
- `amazon.com`
- `amazonaws.com`
- `amazonforum.com`
- `angelfire.com`
- `animerep.com`
- `aniview.com`
- `annas-archive.org`
- `apartments.com`
- `apkmirror.com`
- `app.link`
- `appboy-images.com`
- `appcenter.ms`
- `apple-cloudkit.com`
- `apple-dns.net`
- `apple-livephotoskit.com`
- `apple-mapkit.com`
- `apple.com`
- `appleiphonecell.com`
- `apzones.com`
- `archive.fo`
- `archive.org`
- `arenascan.com`
- `arkoselabs.com`
- `aspnetcdn.com`
- `atomz.com`
- `audible.de`
- `auditude.com`
- `auslogics.com`
- `autoscout24.com`
- `avgle.com`
- `awin1.com`
- `azureedge.net`
- `b23.tv`
- `b3log.org`
- `b3logfile.com`
- `backblazeb2.com`
- `bad.news`
- `baidupcs.com`
- `baixing.com`
- `bamgrid.com`
- `banggood.com`
- `bankofamerica.com`
- `bccard.com`
- `bcelive.com`
- `bcy.net`
- `bdsmtest.org`
- `bdsmtv.cc`
- `bestbuy.com`
- `bestgore.fun`
- `bestvpnrating.com`
- `bet365.com`
- `bethesda.net`
- `bidobido.xyz`
- `binarypiano.com`
- `bing.com`
- `bing.net`
- `bit.do`
- `bit.ly`
- `bitbucket.org`
- `bitly.com`
- `bitsumactivationserver.com`
- `biz.ua`
- `blackcircles.ca`
- `blizzard.com`
- `bluehost.com`
- `blueskyxn.com`
- `bmap6.cn`
- `bnc.lt`
- `bongacams.com`
- `bonuscloud.io`
- `bootcdn.cn`
- `bootcdn.net`
- `boxcryptor.com`
- `brightcove.com`
- `brightcove.net`
- `britannica.com`
- `browser-intake-datadoghq.eu`
- `budgetbankers.com`
- `bufferapp.com`
- `bulbagarden.net`
- `burnermail.io`
- `bytednsdoc.com`
- `bytegecko.com`
- `byteimg.com`
- `cafe24.com`
- `cainiao.com`
- `camscanner.com`
- `capebretonpost.com`
- `capitalone.com`
- `captcha-display.com`
- `cbox.ws`
- `cbsi.com`
- `ccmbg.com`
- `cd4o.com`
- `cdn-apple.com`
- `cdn-go.cn`
- `cdn-noc.net`
- `cdnfinder.xyz`
- `cdninstagram.com`
- `cdnjs.com`
- `cec.ro`
- `cedexis.net`
- `charterbankwa.com`
- `chase.com`
- `chatglm.cn`
- `cheatography.com`
- `chelpus.com`
- `chickenkiller.com`
- `chipotle.com`
- `cibntv.net`
- `cinsscore.com`
- `clck.ru`
- `cli.im`
- `click-trk.com`
- `clickdimensions.com`
- `clickfunnels.com`
- `clickhouse.com`
- `clips4sale.com`
- `cloudflare-dns.com`
- `cloudflare.com`
- `cloudflareinsights.com`
- `cloudflareworkers.com`
- `cloudfront.net`
- `cloudns.cl`
- `cmpassport.com`
- `cnzz.com`
- `connatix.com`
- `controleng.com`
- `convertertogenerator.com`
- `conviva.com`
- …（还有 981 条）

## 同域冲突

共 3865 条：这些域名在合并黑名单里要拦、在合并白名单里要放，AGH 里例外优先，所以**实际不会拦**。

想把其中某几个恢复拦截：把它们加进 `blacklist.txt`，下次跑流水线会自动剔除白名单侧对应条目。
完整清单见 `dist/conflicts.txt`。

- `000714.xyz`
- `17u.cn`
- `18comic.org`
- `18comic.vip`
- `1kinobig.ru`
- `1sapp.com`
- `1tian.kuaishou.com`
- `2.android.pool.ntp.org`
- `22.do`
- `316.coolapk1s.com`
- `360.cn`
- `360buyimg.com`
- `360kuai.com`
- `3975.com`
- `39d0825d09f05.cdn.sohucs.com`
- `3d-platform-pro.obs.cn-south-1.myhuaweicloud.com`
- `3g.163.com`
- `3g.ali213.net`
- `3gimg.qq.com`
- `40017.cn`
- `48609.activity-42.m.duiba.com.cn`
- `5471782.fls.doubleclick.net`
- `79423.analytics.edgekey.net`
- `7x24s.com`
- `91haoka.cn`
- `96956.com.cn`
- `a.9game.cn`
- `a.adwolf.ru`
- `a.game.163.com`
- `a.klaviyo.com`
- `a.sellpoint.net`
- `a.video.qq.com`
- `a0.app.xiaomi.com`
- `a1.mzstatic.com`
- `a1.qpic.cn`
- `a2.mzstatic.com`
- `a3.mzstatic.com`
- `a4.mzstatic.com`
- `a5.mzstatic.com`
- `a6.mzstatic.com`
- `a7.mzstatic.com`
- `a8.mzstatic.com`
- `a8onlineshop.trendmicro.co.jp`
- `aa.tweakers.nl`
- `aaid.umeng.com`
- `aan.amazon.com`
- `aapl-edge0.qtlcdn.com`
- `aax-fe.amazon.co.jp`
- `ab.tweakers.nl`
- `about.gitlab.cn`
- `about.gitlab.com`
- `abre-videos.cdn1122.com`
- `abs-0.twimg.com`
- `abs.twimg.com`
- `abtest-ch.snssdk.com`
- `abtest3-misc-lf.zijieapi.com`
- `abtestvm.bytedance.com`
- `ac.dun.163yun.com`
- `ac.ebis.ne.jp`
- `access.open.uc.cn`
- `access1.tpns.tencent.com`
- `account.agiso.com`
- `account.dianping.com`
- `account.oneplus.com`
- `account.oppo.com`
- `account.qzhua.net`
- `account.realme.com`
- `account.vivo.com`
- `account.wps.cn`
- `account.xfinfr.com`
- `account.xiaomi.com`
- `account.xunfei.cn`
- `account.youku.com`
- `accountapi.dianping.com`
- `accounts.google.com`
- `accscdn.m.taobao.com`
- `accscdn4public.m.taobao.com`
- `acg02.cc`
- `acs-m.daraz.com.bd`
- `acs-m.daraz.pk`
- `acs.m.goofish.com`
- `acs.m.taobao.com`
- `acs.youku.com`
- `acs4baichuan.m.taobao.com`
- `acs4public.m.taobao.com`
- `acstatic-dun.126.net`
- `act-webstatic.hoyoverse.com`
- `act.hoyoverse.com`
- `act.vip.iqiyi.com`
- `act.zhuanzhuan.com`
- `action.metaffiliation.com`
- `active.jd.com`
- `activity.browser.intl.miui.com`
- `activity.hdslb.com`
- `activity.huaweicloud.com`
- `activity.tuiapple.com`
- `activity.youku.com`
- `acts.qidian.com`
- `ad-experience.bytedance.com`
- `ad-log-upload.mihoyo.com`
- `ad.10010.com`
- `ad.abchina.com`
- `ad.e.kuaishou.com`
- `ad.kazakinfo.com`
- `ad.mcloud.139.com`
- `ad.ourgame.com`
- `ad.tencentmusic.com`
- `adash-emas.cn-hangzhou.aliyuncs.com`
- `adashx.ut.dingtalk.com`
- `adcdn.pingan.com`
- `adcdn.tencentmusic.com`
- `adclick.tencentmusic.com`
- `adexpo.tencentmusic.com`
- `adidasapp.api.adidas.com.cn`
- `adm.10jqka.com.cn`
- `admin-oss-xlvip.a.88cdn.com`
- `admin.dable.io`
- `admin.mailchimp.com`
- `adnmb3.com`
- `ads.95516.com`
- `ads.cdn.tvb.com`
- `ads.google.com`
- `ads.microsoft.com`
- `ads.pinterest.com`
- `ads.privacy.qq.com`
- `ads.snapchat.com`
- `ads.spotify.com`
- `ads.tdbank.com`
- `ads.twitter.com`
- `ads.vk.com`
- `ads.vk.ru`
- `ads.x.com`
- `adserviceretry.kugou.com`
- `adsmind.gdtimg.com`
- `adstats.tencentmusic.com`
- `adv.ccb.com`
- `adv.sec.miui.com`
- `advert.kf5.com`
- `advertise.baicizhan.com`
- `adx-bj-req.anythinktech.com`
- `adx-bj.anythinktech.com`
- `adx.anythinktech.com`
- `ae.bdstatic.com`
- `ae01.alicdn.com`
- `aedns.weixin.qq.com`
- `aeventlog.beacon.qq.com`
- `afdian.com`
- `afi-b.com`
- `ai-cdn.duba.net`
- `ai.yimg.jp`
- …（还有 3715 条，见 conflicts.txt）
