# -*- encoding: utf-8 -*-
"""Minecraft语言文件更新器"""

import hashlib
import sys
from zipfile import ZipFile
from pathlib import Path
import requests as r


def get_json(url: str):
    """获取JSON"""
    try:
        resp = r.get(url, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except r.exceptions.RequestException as ex:
        print(f"请求发生错误: {ex}")
        sys.exit()


# 语言文件列表
lang_list = [
    "zh_cn.json",
    "zh_tw.json",
    "zh_hk.json",
    "lzh.json",
]

# 文件夹
P = Path(__file__).resolve().parent
LANG_DIR = P / "lang"
LANG_DIR.mkdir(exist_ok=True)

# 获取version_manifest_v2.json
version_manifest_path = P / "version_manifest_v2.json"
try:
    print("正在获取版本清单“version_manifest_v2.json”……\n")
    version_manifest = r.get(
        "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json",
        timeout=60,
    )
    version_manifest.raise_for_status()
    version_manifest_json = version_manifest.json()
except r.exceptions.RequestException as e:
    print("无法获取版本清单，请检查网络连接。")
    sys.exit()
V = version_manifest_json["latest"]["snapshot"]

# 获取client.json
client_manifest_url = next(
    (i["url"] for i in version_manifest_json["versions"] if i["id"] == V), None
)

print(f"正在获取客户端索引文件“{client_manifest_url.rsplit('/', 1)[-1]}”……")
client_manifest = get_json(client_manifest_url)

# 获取资产索引文件
asset_index_url = client_manifest["assetIndex"]["url"]
print(f"正在获取资产索引文件“{asset_index_url.rsplit('/', 1)[-1]}”……\n")
asset_index = get_json(asset_index_url)["objects"]

# 获取客户端JAR
client_url = client_manifest["downloads"]["client"]["url"]
client_path = P / "client.jar"
print("正在下载客户端Java归档（client.jar）……")
try:
    response = r.get(client_url, timeout=120)
    response.raise_for_status()
    with open(client_path, "wb") as f:
        f.write(response.content)
except r.exceptions.RequestException as e:
    print(f"请求发生错误: {e}")
    client_path.unlink()
    sys.exit()

# 解压English (US)语言文件
with ZipFile(client_path) as client:
    with client.open("assets/minecraft/lang/en_us.json") as content:
        with open(LANG_DIR / "en_us.json", "wb") as f:
            print("正在从client.jar解压语言文件“en_us.json”……")
            f.write(content.read())

# 删除客户端JAR
print("正在删除client.jar……\n")
client_path.unlink()

# 获取语言文件
for e in lang_list:
    if "minecraft/lang/" + e in asset_index:
        file_hash = asset_index["minecraft/lang/" + e]["hash"]
        print(f"正在下载语言文件“{e}”（{file_hash}）……")
        asset_url = (
            "https://resources.download.minecraft.net/"
            + file_hash[:2]
            + "/"
            + file_hash
        )
        lang_file_path = LANG_DIR / e
        try:
            response = r.get(asset_url, timeout=60)
            response.raise_for_status()
            with open(lang_file_path, "wb") as f:
                f.write(response.content)
            with open(lang_file_path, "rb") as f:
                if hashlib.file_digest(f, "sha1").hexdigest() == file_hash:
                    print("文件SHA1校验一致。\n")
        except r.exceptions.RequestException as e:
            print(f"请求发生错误: {e}")

print("\n已完成。")
