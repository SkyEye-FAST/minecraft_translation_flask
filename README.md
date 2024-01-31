# Minecraft中文标准译名查询

[![Pylint](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/pylint.yml/badge.svg)](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/pylint.yml) [![Update language files](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/update.yml/badge.svg)](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/update.yml) [![Generate font subset (I.Ming)](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/extract_font.yml/badge.svg)](https://github.com/SkyEye-FAST/minecraft_translation_flask/actions/workflows/extract_font.yml)

注：**⚠️此项目仍在开发中，网页样式仍需完善，欢迎提交Issue和Pull Request。**

可查询Minecraft中文标准译名的简易网页，后端框架使用[Flask](https://github.com/pallets/flask)。

目前网页的演示可在以下网址查看：

1. [mcst.teahouse.team](https://mcst.teahouse.team)
2. [skyeyefast.pythonanywhere.com](https://skyeyefast.pythonanywhere.com/) （更新可能较慢）
3. [mczhst.vercel.app](https://mczhst.vercel.app/)（国内网络可能无法访问）

网页样式参考[SkyEye-FAST/minecraft_translation_ppt](https://github.com/SkyEye-FAST/minecraft_translation_ppt)。

## 运行

参见[Flask文档](https://flask.palletsprojects.com/en/3.0.x/)。

### 依赖项

请使用下面的命令安装依赖项：

``` shell
pip install -r requirements.txt
```

### 环境变量

需要在`.env`或者系统中设置`SECRET_KEY`环境变量，可以使用以下命令生成：

``` shell
python -c 'import secrets; print(secrets.token_hex())'
```

## 说明

### Minecraft语言文件

本仓库会在每天🕧00:30（UTC+8，即🕟UTC 16:30）自动检查Minecraft Java版语言文件更新。使用脚本为[`update.py`](/update.py)，需要安装库`requests`。

如果希望在自己搭建的实例中使用其他版本的Java版语言文件，请使用[SkyEye-FAST/minecraft_translation](https://github.com/SkyEye-FAST/minecraft_translation)获取。

请将获取到的`en_us.json`、`zh_cn.json`、`zh_hk.json`、`zh_tw.json`和`lzh.json`放置在语言文件文件夹下（默认为与脚本同级的`lang`文件夹，可以在配置文件中调整）。

[`supplements.json`](/lang/supplements.json)中存有目前（2024年1月28日）游戏内语言文件缺失，而Crowdin上已更新的内容（目前为空）。目前项目默认配置为关闭读取此项。

### 字体

本项目使用思源宋体和[一点明体](https://github.com/ichitenfont/I.Ming)的自动构建子集。

本仓库会在每周四🕐01:00（UTC+8，即UTC每周三🕔17:00）自动检查一点明体的子集文件是否需要根据文言的内容而更新。

使用脚本为[`extract_font.py`](/extract_font.py)，需要库[`fonttools`](https://github.com/fonttools/fonttools)。

### 日期与时区

网页上显示的日期和时区根据用户的IP决定，相关数据从GeoIP2 GeoLite2数据库获取。

日期和时区的本地化由[`babel`](https://github.com/python-babel/babel)和[`flask-babel`](https://github.com/python-babel/flask-babel)完成。

## 反馈

遇到的问题和功能建议等可以提出议题（Issue）。

欢迎创建拉取请求（Pull request）。

## 感谢

[Favicon](/static/favicon.ico)和[apple-touch-icon.png](/static/apple-touch-icon.png)的原始文件来自[Minecraft Wiki](https://minecraft.wiki/w/File:Favicon.ico)，以CC BY-NC-SA 3.0协议授权。

文言使用[一点明体](https://github.com/ichitenfont/I.Ming)，以[IPA Open Font License v1.0](https://github.com/ichitenfont/I.Ming/blob/master/LICENSE.md)授权。

[`GeoLite2-City.mmdb`](/GeoLite2-City.mmdb)来自[P3TERX/GeoLite.mmdb](https://github.com/P3TERX/GeoLite.mmdb)。版权归MaxMind, Inc.所有。
