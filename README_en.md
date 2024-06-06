# Query Minecraft Standard Translations

[![Pylint](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/pylint.yml/badge.svg)](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/pylint.yml) [![Update language files](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/update.yml/badge.svg)](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/update.yml) [![Generate font subset (I.Ming)](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/extract_font.yml/badge.svg)](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/extract_font.yml)

- **[English](README_en.md) | [中文](README.md)**

----

A simple web page for querying Minecraft standard translations of , using [Flask](https://github.com/pallets/flask) as the backend framework.

## Usage

### Main page

Enter the source string content that needs to be queried (i.e. the original English text) in the input box on the main page, click the "Query" button, select the string key name that needs to be queried in the list that appears, and click the "Query" button again.

By default, only the Chinese variants are displayed. You can switch whether to display Japanese, Korean, and Vietnamese translations by checking "Enable additional languages".

Demonstrations of the main page are available at the following URLs:

1. [mcst.teahouse.team](https://mcst.teahouse.team)
2. [skyeyefast.pythonanywhere.com](https://skyeyefast.pythonanywhere.com/) (Updates may be slower)
3. [mczhst.vercel.app](https://mczhst.vercel.app/) (May not be accessible from Chinese mainland)

The webpage style is referenced from [SkyEye-FAST/minecraft_translation_ppt](https://github.com/SkyEye-FAST/minecraft_translation_ppt), see section [#Colors](#colors).

![Sample](sample/sample_advancements_en.png)

### Translation table page

The automatically generated translation table can be found in the `/table` subpage of the website, including key name, original text and 7 supported languages.

Use the built-in page search function in browsers (shortcut key: `Ctrl + F` or `⌘ Command + F`) to quickly search for translations.

This page is useful for quick searches, but is not suitable for showing results to others. It is recommended to use a screenshot of the main page to show others the translation status.

Demonstrations of the translation table page are available at the following URLs:

1. [mcst.teahouse.team/table](https://mcst.teahouse.team/table)
2. [skyeyefast.pythonanywhere.com/table](https://skyeyefast.pythonanywhere.com/table) (Updates may be slower)
3. [mczhst.vercel.app/table](https://mczhst.vercel.app/table) (May not be accessible from Chinese mainland)

![Sample](sample/sample_table.png)

## Running

See [Flask documentation](https://flask.palletsprojects.com/en/3.0.x/)。

## Dependencies

Install dependencies using the following command:

``` shell
pip install -r requirements.txt
```

## Environment Variables

You need to set the `SECRET_KEY` environment variable either in `.env` or in your system. You can generate it using the following command:

``` shell
python -c 'import secrets; print(secrets.token_hex())'
```

## Instructions

### Minecraft Language Files

This repository automatically checks for updates to Minecraft: Java edition language files every day at 🕧00:30 (UTC+8, i.e., 🕟UTC 16:30). This process uses the script [`update.py`](update.py) and requires `requests`.

If you want to use language files from other versions of Minecraft: Java Edition in your own instance, use [SkyEye-FAST/minecraft_translation](https://github.com/SkyEye-FAST/minecraft_translation) to obtain them.

Obtained `en_us.json`, `zh_cn.json`, `zh_hk.json`, `zh_tw.json`, `lzh.json`, `ja_jp.json`, `ko_kr.json`, and `vi_vn.json` files should be placed in the language files folder (by default, it's the lang folder at the same level as the script, but you can adjust this in the configuration file).

[`supplements.json`](lang/supplements.json) contains currently (as of January 28, 2024) missing translations from the in-game language files that have been updated on Crowdin (currently empty). By default, this feature is disabled in the project configuration.

### Fonts

This project uses Source Han Serif and an automatically constructed subset of [I.Ming](https://github.com/ichitenfont/I.Ming).

This repository automatically checks whether the subset files of I.Ming need to be updated based on the content of classical Chinese every Thursday at 🕐01:00 (UTC+8, i.e., UTC Wednesday 🕔17:00).

This process uses the script [`extract_font.py`](extract_font.py) and requires [`fonttools`](https://github.com/fonttools/fonttools).

### Date and Timezone

The date and timezone displayed on the web page are determined based on the user's IP, using data obtained from the GeoIP2 GeoLite2 database.

Localization of date and timezone is handled by [`babel`](https://github.com/python-babel/babel) and [`flask-babel`](https://github.com/python-babel/flask-babel).

### Colors

The main page background color is `#f9f2e0`, and tables with different colored strings for different categories are used.

Below are the colors listed, first being the table border color; the table background color is the border color with 20% opacity, annotated with the equivalent color after overlaying the page background color in parentheses.

- Advancements: `#a02b93` (`#e7cad1`)

![Sample](sample/sample_advancements_en.png)

- Biomes: `#4ab5c4` (`#d6e6da`)

![Sample](sample/sample_biome_en.png)

- Blocks: `#5b9bd5` (`#d9e1de`)

![Sample](sample/sample_block_en.png)

- Effects: `#ffc000` (`#fae8b3`)

![Sample](sample/sample_effect_en.png)

- Enchantments: `#44546a` (`#d5d2c8`)

![Sample](sample/sample_enchantment_en.png)

- Entities: `#ed7d31` (`#f7dbbd`)

![Sample](sample/sample_entity_en.png)

- Items: `#70ad47` (`#dee4c1`)

![Sample](sample/sample_item_en.png)

## Feedback

Please feel free to raise issues for any problems encountered or feature suggestions.

Pull requests are welcome.

## Acknowledgments

The original files for the [favicon](static/favicon.ico) and [apple-touch-icon.png](static/apple-touch-icon.png) are from [Minecraft Wiki](https://minecraft.wiki/w/File:Favicon.ico) and are licensed under the CC BY-NC-SA 3.0 license.

The font for Classical Chinese is [I.Ming](https://github.com/ichitenfont/I.Ming), licensed under the [IPA Open Font License v1.0](https://github.com/ichitenfont/I.Ming/blob/master/LICENSE.md).

[`GeoLite2-City.mmdb`](GeoLite2-City.mmdb) is from [P3TERX/GeoLite.mmdb](https://github.com/P3TERX/GeoLite.mmdb). Copyright belongs to MaxMind, Inc.
