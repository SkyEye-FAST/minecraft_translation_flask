# Minecraft中文标准译名查询

注：**此项目仍在开发中，网页样式仍需完善，尤其是移动端适配的问题。**

可查询Minecraft中文标准译名的简易网页，后端框架使用Flask。

目前网页的演示可在[skyeyefast.pythonanywhere.com](https://skyeyefast.pythonanywhere.com/)和[mczhst.vercel.app](https://mczhst.vercel.app/)查看。

网页样式参考[SkyEye-FAST/minecraft_translation_ppt](https://github.com/SkyEye-FAST/minecraft_translation_ppt)。

## 需求

需要库[flask](https://github.com/pallets/flask/)（`flask`），请使用下面的命令安装：

``` shell
pip install flask -U
```

## 前期准备

### 语言文件

本仓库会在每天00:00（UTC+8，即UTC 16:00）自动检查语言文件更新。使用脚本为[`update.py`](/update.py)，需要安装库`requests`。

如果希望使用其他版本的Java版语言文件，请使用[SkyEye-FAST/minecraft_translation](https://github.com/SkyEye-FAST/minecraft_translation)获取。

请将获取到的`en_us.json`、`zh_cn.json`、`zh_hk.json`、`zh_tw.json`和`lzh.json`放置在语言文件文件夹下（默认为与脚本同级的`lang`文件夹，可以在配置文件中调整）。

[`supplements.json`](/lang/supplements.json)中存有目前（2024年1月18日）游戏内语言文件缺失，而Crowdin上已更新的内容（目前为空）。

### 字体

本项目使用思源宋体和[一点明体](https://github.com/ichitenfont/I.Ming)的自动构建子集。

本仓库会在每周日00:00（UTC+8，即UTC 16:00）自动检查一点明体的子集是否需要根据文言更新。

使用脚本为[`extract_font.py`](/extract_font.py)，需要安装库`fonttools`。

## 运行

参见[Flask文档](https://flask.palletsprojects.com/en/3.0.x/)。

## 反馈

遇到的问题和功能建议等可以提出议题（Issue）。

欢迎创建拉取请求（Pull request）。

## 感谢

[Favicon](/static/favicon.ico)和[apple-touch-icon.png](/static/apple-touch-icon.png)的原始文件来自[Minecraft Wiki](https://minecraft.wiki/w/File:Favicon.ico)，以CC BY-NC-SA 3.0协议授权。

文言使用[一点明体](https://github.com/ichitenfont/I.Ming)，按照[IPA Open Font License v1.0](https://github.com/ichitenfont/I.Ming/blob/master/LICENSE.md)授权。
