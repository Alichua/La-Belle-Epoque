# La Belle Epoque

[English](README.en-US.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-HK.md) | [한국어](README.ko.md)

![Après génération d'image](../examples/stage2-after-image-gen.png)

Choisissez un pays. Choisissez une date.

La Belle Epoque transforme ce moment en une une rétro : d'abord en journal pixel art, puis, si votre session le permet, en illustration commerciale plus lisse.

À moitié archive, à moitié affiche city-pop, à moitié voyage nostalgique.

Six Belle Epoques, au sens large :

- 🇫🇷 France, années 1870-1914 : la Belle Époque classique, Paris, Art nouveau, cabarets, affiches, électricité et foules modernes.
- 🇺🇸 États-Unis, 1980-2001 : centres commerciaux, câble, finance, premiers ordinateurs, néon et long boom de consommation.
- 🇯🇵 Japon, 1955-1991 : croissance d'après-guerre, bulle, Tokyo nocturne, City Pop, grands magasins, disques et abondance fragile.
- 🇨🇳 Chine, 1978-2012 : réforme, ouverture, chantiers, usines, tours neuves, marchés et vitesse de la modernisation.
- 🇭🇰 Hong Kong, années 1970-1997 : port, néons, cinéma, finance, densité, taxis, rues mouillées et compte à rebours avant la rétrocession.
- 🇰🇷 Corée, 1988-1997 : Séoul après les Jeux olympiques, appartements, électronique, grands magasins, accélération de la classe moyenne et choc du FMI tout proche.

## Ce que fait le skill

Donnez un pays et une date :

```text
Use $pixel-belle-epoque for Japan on October 23.
```

Le skill cherche un événement daté dans la Belle Epoque du pays, génère une image principale en pixel art, compose une une de journal locale, ajoute des publicités et applique une finition de vieux papier. Une variante finale avec génération d'image peut aussi être créée.

Pays pris en charge : France, United States, Japan, China, Hong Kong, Korea.

## Galerie

Stage 1 est la sortie native : un journal pixel art construit à partir de la recherche, des sprites, des manchettes, des publicités et du moteur de rendu rétro.

Stage 2 est optionnel : si l'édition d'image est disponible, le journal fini est restylisé en illustration commerciale en gardant la même mise en page.

| Stage 1 : journal pixel | Stage 2 : après génération d'image |
| --- | --- |
| <img src="../examples/stage1-pixel-newspaper.png" width="420" alt="Stage 1 journal pixel"> | <img src="../examples/stage2-after-image-gen.png" width="420" alt="Stage 2 après génération d'image"> |

## Installation

Installez d'abord le skill requis :

```text
Use $skill-installer to install pixel-art-creator.
```

Installez ensuite ce skill :

```text
Use $skill-installer to install git@github.com:Alichua/La-Belle-Epoque.git
```

Redémarrez Codex après l'installation.

Python 3 et Pillow sont nécessaires pour les scripts de rendu :

```bash
python3 -m pip install pillow
```

La variante finale avec image generation dépend du skill `$imagegen` et peut nécessiter `OPENAI_API_KEY`.

## Utilisation

```text
Use $pixel-belle-epoque for France on July 1.
Use $pixel-belle-epoque for Japan on October 23. Also create the final commercial illustration variant if image_gen is available.
```

Les sorties sont écrites dans :

```text
output/pixel-belle-epoque/<country>-<date>-<event-slug>/
```

Fichiers principaux : `newspaper.png`, `newspaper-commercial-illustration.png`, `final.png`, `research.md`, `sources.json`, `palette.json`.
