# ATOOLHUB

个人自制小工具的集成导航主页。以 ATH.html 为入口，自动扫描根目录下的子文件夹并生成工具卡片，点击卡片即可跳转到对应的小工具。

## 功能特性

- 自动发现工具：新建文件夹放入 HTML 后运行扫描脚本，工具自动出现在主页
- 入口智能识别：优先 index.html，其次与文件夹同名的 HTML
- 显示/隐藏控制：设置面板中可控制工具是否在集成页展示
- 排序功能：设置面板中调整卡片顺序
- 配置持久化：个人配置保存在浏览器 localStorage
- 兼容 file:// 直开：ATH.html 内嵌清单兜底，双击即可使用

## 使用

```bash
python3 -m http.server 8080
```

浏览器访问 http://localhost:8080/ATH.html

直接双击 ATH.html 也可以正常使用。

## 添加新工具

1. 在根目录新建文件夹，放入 HTML 文件（推荐命名为 index.html）
2. 运行扫描脚本：

```bash
python3 scan_tools.py
```

3. 刷新 ATH.html，新工具自动出现

## 项目结构

```
ATOOLHUB/
├── ATH.html          # 集成导航主页（入口）
├── tools.json        # 工具清单（扫描脚本自动生成）
├── scan_tools.py     # 自动发现脚本
├── assets/           # 本地资源（FontAwesome 图标字体等）
├── CyberShb/         # 示例工具：赛博圣杯
└── PiggyPeggy/       # 示例工具：存钱罐
```

## 说明

- tools.json 由扫描脚本自动生成，不要手动编辑
- 设置面板有密码保护，密码可在设置中修改

## License

PiggyPeggy 遵循其目录内的 NON-COMMERCIAL PUBLIC LICENSE，其余部分为个人项目，请勿商用。