# La Belle Epoque

[English](README.en-US.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-HK.md) | [한국어](README.ko.md)

![图像生成后](../examples/stage2-after-image-gen.png)

选一个国家。选一个日期。

La Belle Epoque 会把这个时刻变成一张复古头版：先生成像素风报纸；如果当前 session 支持图像编辑，还可以继续生成一张更光滑的商业插画版。

一部分是档案，一部分是 city-pop 海报，一部分是怀旧旅行。

六个 Belle Epoque：

- 🇫🇷 法国，1870s-1914：经典 Belle Epoque，巴黎大道、Art Nouveau、歌舞厅、海报、电气化和现代人群。
- 🇺🇸 美国，1980-2001：商场、有线电视、金融、早期电脑、霓虹乐观，以及漫长的消费繁荣。
- 🇯🇵 日本，1955-1991：战后增长到泡沫时代，东京夜色、City Pop、百货店、唱片、出租车和脆弱的富足。
- 🇨🇳 中国，1978-2012：改革开放、工地尘土、工厂、新高楼、家电、市场和高速现代化。
- 🇭🇰 香港，1970s-1997：海港霓虹、电影、金融、密度、的士、湿街，以及回归前的倒计时。
- 🇰🇷 韩国，1988-1997：奥运后的首尔、公寓、电子产品、百货店、中产加速，以及临近的 IMF 冲击。

## 它会做什么

给它一个国家和日期：

```text
Use $pixel-belle-epoque for Japan on October 23.
```

这个 skill 会搜索该国家 Belle Epoque 范围内对应日期的事件，生成像素主图，嵌入本国报纸版式，加入广告 sprites，套上复古印刷滤镜。若可用，还会把最终报纸再转成商业插画版。

支持国家：France, United States, Japan, China, Hong Kong, Korea.

## Gallery

Stage 1 是 skill 的原生输出：基于事件调研、sprites、真实报头、广告和复古报纸渲染器合成出的像素报纸。

Stage 2 是可选流程：如果当前 session 能调用图像生成/编辑，会把完成的报纸在保留版式的前提下转成更干净的商业插画风格。

| Stage 1: Pixel Newspaper | Stage 2: After Image Generation |
| --- | --- |
| <img src="../examples/stage1-pixel-newspaper.png" width="420" alt="Stage 1 pixel newspaper"> | <img src="../examples/stage2-after-image-gen.png" width="420" alt="Stage 2 after image generation"> |

## 安装

先安装依赖 skill：

```text
Use $skill-installer to install pixel-art-creator.
```

安装本 skill：

```text
Use $skill-installer to install git@github.com:Alichua/La-Belle-Epoque.git
```

安装后重启 Codex，让 `$pixel-belle-epoque` 生效。

渲染脚本需要 Python 3 和 Pillow：

```bash
python3 -m pip install pillow
```

最终商业插画版依赖 `$imagegen`；如果走 CLI/API fallback，可能需要 `OPENAI_API_KEY`。

## 使用

```text
Use $pixel-belle-epoque for China on October 1.
Use $pixel-belle-epoque for Japan on October 23. Also create the final commercial illustration variant if image_gen is available.
```

输出目录：

```text
output/pixel-belle-epoque/<country>-<date>-<event-slug>/
```

主要文件：`newspaper.png`, `newspaper-commercial-illustration.png`, `final.png`, `research.md`, `sources.json`, `palette.json`.
