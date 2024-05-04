# -*- encoding: utf-8 -*-
"""生成表格"""

from bs4 import BeautifulSoup
from base import P
from init import data

HTML = """
<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Translation Table</title>
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link rel="apple-touch-icon" href="{{ url_for('static', filename='apple-touch-icon.png') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='table.css') }}" type="text/css">
    <link rel="stylesheet" href="https://fonts.font.im/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
</head>

<body>
    <div class="header">
        Minecraft Standard Translation Table. Latest Update: {{ date_str }}<br>Made by SkyEye_FAST.&emsp;
        <a href="../"><span class="material-symbols-outlined b">home</span>Main Page</a>&emsp;
        <a class="github-link" href="https://github.com/SkyEye-FAST/minecraft_translation_flask">
            <img class="github-icon" src="{{ url_for('static', filename='images/github-icon.svg') }}" alt="GitHub">
            GitHub
        </a>
    </div>
    <table>
        <thead>
            <tr>
                <th>keys</th>
                <th>en_us</th>
                <th>zh_cn</th>
                <th>zh_hk</th>
                <th>zh_tw</th>
                <th>lzh</th>
                <th>ja_jp</th>
                <th>ko_kr</th>
                <th>vi_vn</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
</body>

</html>
"""

soup = BeautifulSoup(HTML, "html.parser")
tbody = soup.find("tbody")

for key in data["en_us"]:
    new_row = soup.new_tag("tr")
    key_cell = soup.new_tag("td")
    key_cell.string = key
    new_row.append(key_cell)
    for lang, lang_data in data.items():
        value = lang_data.get(key, "？")
        new_cell = soup.new_tag("td")
        new_cell.string = value
        new_row.append(new_cell)
    tbody.append(new_row)

with open(P / "templates" / "table.html", "w", encoding="utf-8") as f:
    f.write(str(soup))
