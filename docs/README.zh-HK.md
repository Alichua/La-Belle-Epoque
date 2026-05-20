# La Belle Epoque

[English](README.en-US.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-HK.md) | [한국어](README.ko.md)

![圖像生成後](../examples/stage2-after-image-gen.png)

揀一個國家。揀一個日期。

La Belle Epoque 會將呢一刻變成一張復古頭版：先生成像素風報紙；如果目前 session 支援圖像編輯，仲可以再生成一張更光滑嘅商業插畫版。

一半係檔案，一半係 city-pop 海報，一半係懷舊旅程。

六個 Belle Epoque：

- 🇫🇷 法國，1870s-1914：經典 Belle Epoque，巴黎大道、Art Nouveau、歌舞廳、海報、電氣化同現代人群。
- 🇺🇸 美國，1980-2001：商場、有線電視、金融、早期電腦、霓虹樂觀，同漫長消費繁榮。
- 🇯🇵 日本，1955-1991：戰後增長到泡沫年代，東京夜色、City Pop、百貨公司、唱片、的士同脆弱嘅富足。
- 🇨🇳 中國，1978-2012：改革開放、地盤塵土、工廠、新高樓、家電、市場同高速現代化。
- 🇭🇰 香港，1970s-1997：海港霓虹、電影、金融、密度、的士、濕街，同回歸前嘅倒數。
- 🇰🇷 韓國，1988-1997：奧運後嘅首爾、公寓、電子產品、百貨公司、中產加速，同臨近嘅 IMF 衝擊。

## 佢會做咩

俾一個國家同日期：

```text
Use $pixel-belle-epoque for Hong Kong on December 25.
```

呢個 skill 會搜尋該國 Belle Epoque 範圍內對應日期嘅事件，生成像素主圖，嵌入本地報紙版式，加入廣告 sprites，再套上復古印刷濾鏡。若可用，仲會將最終報紙轉成商業插畫版。

支援國家：France, United States, Japan, China, Hong Kong, Korea.

## Gallery

Stage 1 係 skill 原生輸出：基於事件調研、sprites、真實報頭、廣告同復古報紙 renderer 合成嘅像素報紙。

Stage 2 係可選流程：如果目前 session 可以調用圖像生成/編輯，就會喺保留版式嘅前提下，將完成報紙轉成更乾淨嘅商業插畫風。

| Stage 1: Pixel Newspaper | Stage 2: After Image Generation |
| --- | --- |
| <img src="../examples/stage1-pixel-newspaper.png" width="420" alt="Stage 1 pixel newspaper"> | <img src="../examples/stage2-after-image-gen.png" width="420" alt="Stage 2 after image generation"> |

## 安裝

先安裝依賴 skill：

```text
Use $skill-installer to install pixel-art-creator.
```

安裝本 skill：

```text
Use $skill-installer to install git@github.com:Alichua/La-Belle-Epoque.git
```

安裝後重啟 Codex，令 `$pixel-belle-epoque` 生效。

渲染 scripts 需要 Python 3 同 Pillow：

```bash
python3 -m pip install pillow
```

最終商業插畫版依賴 `$imagegen`；如果使用 CLI/API fallback，可能需要 `OPENAI_API_KEY`。

## 使用

```text
Use $pixel-belle-epoque for Hong Kong on December 25.
Use $pixel-belle-epoque for Japan on October 23. Also create the final commercial illustration variant if image_gen is available.
```

輸出目錄：

```text
output/pixel-belle-epoque/<country>-<date>-<event-slug>/
```

主要文件：`newspaper.png`, `newspaper-commercial-illustration.png`, `final.png`, `research.md`, `sources.json`, `palette.json`.
