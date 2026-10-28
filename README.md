# ATOOLHUB

个人自制小工具集成导航主页。以 ATH.html 为入口，自动扫描根目录下的子文件夹生成工具卡片，点击卡片跳转到对应小工具。

## 使用

用浏览器打开 ATH.html 即可。推荐通过本地服务器访问：

```bash
python3 -m http.server 8080
```

然后访问 http://localhost:8080/ATH.html

直接双击 ATH.html 也可以（file:// 模式有内嵌清单兜底）。

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
- 排序、隐藏等个人配置保存在浏览器 localStorage，换浏览器或清缓存会重置
- 设置面板需 4 位密码，默认 0000