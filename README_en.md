# Query Minecraft Chinese Standard Translations

[![Pylint](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/pylint.yml/badge.svg)](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/pylint.yml) [![Update language files](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/update.yml/badge.svg)](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/update.yml) [![Generate font subset (I.Ming)](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/extract_font.yml/badge.svg)](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/extract_font.yml)

- **[English](/README_en.md) | [中文](/README.md)**

----

A simple web page for querying Chinese standard translations of Minecraft, using [Flask](https://github.com/pallets/flask) as the backend framework.

Demonstrations of the web page are available at the following URLs:

1. [mcst.teahouse.team](https://mcst.teahouse.team)
2. [skyeyefast.pythonanywhere.com](https://skyeyefast.pythonanywhere.com/) (Updates may be slower)
3. [mczhst.vercel.app](https://mczhst.vercel.app/) (May not be accessible from Chinese mainland)

The style used on the web page is referenced from [SkyEye-FAST/minecraft_translation_ppt](https://github.com/SkyEye-FAST/minecraft_translation_ppt):

![Sample](/sample/1.png)

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

## Minecraft Language Files

This repository automatically checks for updates to Minecraft: Java edition language files every day at 🕧00:30 (UTC+8, i.e., 🕟UTC 16:30). This process uses the script [`update.py`](/update.py) and requires `requests`.

If you want to use language files from other versions of Minecraft: Java Edition in your own instance, use [SkyEye-FAST/minecraft_translation](https://github.com/SkyEye-FAST/minecraft_translation) to obtain them.

Obtained `en_us.json`, `zh_cn.json`, `zh_hk.json`, `zh_tw.json`, and `lzh.json` files should be placed in the language files folder (by default, it's the lang folder at the same level as the script, but you can adjust this in the configuration file).

[`supplements.json`](/lang/supplements.json) contains currently (as of January 28, 2024) missing translations from the in-game language files that have been updated on Crowdin (currently empty). By default, this feature is disabled in the project configuration.

## Fonts

This project uses Source Han Serif and an automatically constructed subset of [I.Ming](https://github.com/ichitenfont/I.Ming).

This repository automatically checks whether the subset files of I.Ming need to be updated based on the content of classical Chinese every Thursday at 🕐01:00 (UTC+8, i.e., UTC Wednesday 🕔17:00).

This process uses the script [`extract_font.py`](/extract_font.py) and requires [`fonttools`](https://github.com/fonttools/fonttools).

## Date and Timezone

The date and timezone displayed on the web page are determined based on the user's IP, using data obtained from the GeoIP2 GeoLite2 database.

Localization of date and timezone is handled by [`babel`](https://github.com/python-babel/babel) and [`flask-babel`](https://github.com/python-babel/flask-babel).

## Feedback

Please feel free to raise issues for any problems encountered or feature suggestions.

Pull requests are welcome.

## Acknowledgments

The original files for the [favicon](/static/favicon.ico) and [apple-touch-icon.png](/static/apple-touch-icon.png) are from [Minecraft Wiki](https://minecraft.wiki/w/File:Favicon.ico) and are licensed under the CC BY-NC-SA 3.0 license.

The font for Classical Chinese is [I.Ming](https://github.com/ichitenfont/I.Ming), licensed under the [IPA Open Font License v1.0](https://github.com/ichitenfont/I.Ming/blob/master/LICENSE.md).

[`GeoLite2-City.mmdb`](/GeoLite2-City.mmdb) is from [P3TERX/GeoLite.mmdb](https://github.com/P3TERX/GeoLite.mmdb). Copyright belongs to MaxMind, Inc.
