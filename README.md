# Minecraft中文标准译名查询

注：**此项目仍在开发中，网页样式亟需完善。**

可查询Minecraft中文标准译名的简易网页，后端框架使用Flask。

网页样式参考[SkyEye-FAST/minecraft_translation_ppt](SkyEye-FAST/minecraft_translation_ppt)。

## 需求

需要库[flask](https://github.com/pallets/flask/)（`flask`），请使用下面的命令安装：

``` shell
pip install flask -U
```

## 前期准备

### 语言文件

Java版语言文件请使用[SkyEye-FAST/minecraft_translation](SkyEye-FAST/minecraft_translation)获取。

请将获取到的`en_us.json`、`zh_cn.json`、`zh_hk.json`、`zh_tw.json`和`lzh.json`放置在语言文件文件夹下（默认为与脚本同级的`lang`文件夹，可以在配置文件中调整）。

[`supplements.json`](/lang/supplements.json)中存有目前（2024年1月13日）游戏内语言文件缺失，而Crowdin上已更新的内容。

## 运行

参见[Flask文档](https://flask.palletsprojects.com/en/3.0.x/)。

## 反馈

遇到的问题和功能建议等可以提出议题（Issue）。

欢迎创建拉取请求（Pull request）。
