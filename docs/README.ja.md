# La Belle Epoque

[English](README.en-US.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-HK.md) | [한국어](README.ko.md)

![画像生成後](../examples/stage2-after-image-gen.png)

国を選ぶ。日付を選ぶ。

La Belle Epoque は、その一日をレトロな新聞の一面にします。まずはピクセル新聞として生成し、セッションで画像編集が使える場合は、さらに光沢のある商業イラスト風に変換できます。

アーカイブであり、シティポップのポスターであり、少しだけノスタルジアの旅でもあります。

6つの Belle Epoque：

- 🇫🇷 フランス、1870年代-1914年：古典的なベル・エポック。パリ、アール・ヌーヴォー、キャバレー、ポスター、電気、近代都市の群衆。
- 🇺🇸 アメリカ、1980-2001年：モール、ケーブルテレビ、金融、初期コンピューター、ネオン、長い消費ブーム。
- 🇯🇵 日本、1955-1991年：戦後成長からバブルへ。東京の夜景、シティポップ、百貨店、レコード、タクシー、壊れやすい豊かさ。
- 🇨🇳 中国、1978-2012年：改革開放、建設現場、工場、新しい高層ビル、家電、市場、急速な近代化。
- 🇭🇰 香港、1970年代-1997年：港のネオン、映画、金融、密度、タクシー、濡れた通り、返還前のカウントダウン。
- 🇰🇷 韓国、1988-1997年：オリンピック後のソウル、団地、電子機器、百貨店、中産階級の加速、そして近づくIMF危機。

## 何ができるか

国と日付を指定します：

```text
Use $pixel-belle-epoque for Japan on October 23.
```

この skill は、その国の Belle Epoque に含まれる日付イベントを調査し、ピクセルアートのメイン画像を作り、国ごとの新聞レイアウトに組み込み、広告スプライトと古い印刷風フィルターを加えます。必要に応じて、画像生成による商業イラスト版も作ります。

対応国：France, United States, Japan, China, Hong Kong, Korea.

## Gallery

Stage 1 は skill の標準出力です。調査したイベント、生成したスプライト、新聞題字、広告、レトロ印刷レンダラーから作られたピクセル新聞です。

Stage 2 はオプションです。画像生成/編集が使える場合、完成した新聞を同じレイアウトのまま、より滑らかな商業イラスト風に変換します。

| Stage 1: Pixel Newspaper | Stage 2: After Image Generation |
| --- | --- |
| <img src="../examples/stage1-pixel-newspaper.png" width="420" alt="Stage 1 pixel newspaper"> | <img src="../examples/stage2-after-image-gen.png" width="420" alt="Stage 2 after image generation"> |

## Install

まず依存 skill を入れます：

```text
Use $skill-installer to install pixel-art-creator.
```

この skill をインストールします：

```text
Use $skill-installer to install git@github.com:Alichua/La-Belle-Epoque.git
```

インストール後、Codex を再起動してください。

レンダリングスクリプトには Python 3 と Pillow が必要です：

```bash
python3 -m pip install pillow
```

最後の画像生成版には `$imagegen` が必要になる場合があり、CLI 経由では `OPENAI_API_KEY` が必要です。

## 使い方

```text
Use $pixel-belle-epoque for Japan on October 23.
Use $pixel-belle-epoque for Japan on October 23. Also create the final commercial illustration variant if image_gen is available.
```

出力先：

```text
output/pixel-belle-epoque/<country>-<date>-<event-slug>/
```

主なファイル：`newspaper.png`, `newspaper-commercial-illustration.png`, `final.png`, `research.md`, `sources.json`, `palette.json`.
