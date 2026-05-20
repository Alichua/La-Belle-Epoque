# La Belle Epoque

[English](README.en-US.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-HK.md) | [한국어](README.ko.md)

![이미지 생성 후](../examples/stage2-after-image-gen.png)

나라를 고르고, 날짜를 고르세요.

La Belle Epoque는 그 순간을 복고풍 신문 1면으로 만듭니다. 먼저 픽셀 신문을 만들고, 세션에서 이미지 편집을 사용할 수 있으면 더 매끈한 상업 일러스트 버전도 생성합니다.

아카이브이자, 시티팝 포스터이자, 작은 노스탤지어 여행입니다.

여섯 개의 Belle Epoque:

- 🇫🇷 프랑스, 1870년대-1914년: 고전적인 벨 에포크. 파리의 대로, 아르누보, 카바레, 포스터, 전기와 근대의 군중.
- 🇺🇸 미국, 1980-2001년: 쇼핑몰, 케이블 TV, 금융, 초기 컴퓨터, 네온의 낙관, 긴 소비 붐.
- 🇯🇵 일본, 1955-1991년: 전후 성장에서 버블 시대로. 도쿄의 밤, 시티팝, 백화점, 레코드, 택시, 깨지기 쉬운 풍요.
- 🇨🇳 중국, 1978-2012년: 개혁개방, 공사장의 먼지, 공장, 새 고층빌딩, 가전, 시장, 빠른 현대화.
- 🇭🇰 홍콩, 1970년대-1997년: 항구의 네온, 영화, 금융, 높은 밀도, 택시, 젖은 거리, 반환 전의 카운트다운.
- 🇰🇷 한국, 1988-1997년: 올림픽 이후의 서울, 아파트, 전자제품, 백화점, 중산층의 가속, 가까워지는 IMF 충격.

## 무엇을 하나요

나라와 날짜를 입력합니다:

```text
Use $pixel-belle-epoque for Korea on September 17.
```

이 skill은 해당 나라의 Belle Epoque 안에서 날짜와 관련된 사건을 조사하고, 픽셀 아트 메인 이미지를 만들고, 나라별 신문 레이아웃에 배치합니다. 광고 스프라이트와 복고 인쇄 필터를 더하며, 가능하면 최종 신문을 상업 일러스트 스타일로도 변환합니다.

지원 국가: France, United States, Japan, China, Hong Kong, Korea.

## Gallery

Stage 1은 skill의 기본 결과물입니다. 조사한 사건, 생성된 sprites, 실제 신문 제호, 광고, 복고 인쇄 렌더러로 만든 픽셀 신문입니다.

Stage 2는 선택 사항입니다. 이미지 생성/편집을 사용할 수 있으면, 완성된 신문을 같은 레이아웃을 유지한 채 더 깔끔한 상업 일러스트 버전으로 바꿉니다.

| Stage 1: Pixel Newspaper | Stage 2: After Image Generation |
| --- | --- |
| <img src="../examples/stage1-pixel-newspaper.png" width="420" alt="Stage 1 pixel newspaper"> | <img src="../examples/stage2-after-image-gen.png" width="420" alt="Stage 2 after image generation"> |

## 설치

먼저 필요한 skill을 설치합니다:

```text
Use $skill-installer to install pixel-art-creator.
```

이 skill을 설치합니다:

```text
Use $skill-installer to install git@github.com:Alichua/La-Belle-Epoque.git
```

설치 후 Codex를 재시작해야 `$pixel-belle-epoque`가 로드됩니다.

렌더링 스크립트에는 Python 3와 Pillow가 필요합니다:

```bash
python3 -m pip install pillow
```

마지막 상업 일러스트 버전은 `$imagegen`에 의존할 수 있으며, CLI/API fallback을 사용할 경우 `OPENAI_API_KEY`가 필요할 수 있습니다.

## 사용

```text
Use $pixel-belle-epoque for Korea on September 17.
Use $pixel-belle-epoque for Japan on October 23. Also create the final commercial illustration variant if image_gen is available.
```

출력 폴더:

```text
output/pixel-belle-epoque/<country>-<date>-<event-slug>/
```

주요 파일: `newspaper.png`, `newspaper-commercial-illustration.png`, `final.png`, `research.md`, `sources.json`, `palette.json`.
