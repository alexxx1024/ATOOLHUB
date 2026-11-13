# ATOOLHUB

个人自制小工具的集成导航主页。以 index.html 为入口，自动扫描根目录下的子文件夹并生成工具卡片，点击卡片即可跳转到对应的小工具。

## 功能特性

- 自动发现工具：新建文件夹放入 HTML 后运行扫描脚本，工具自动出现在主页
- 入口智能识别：优先 index.html，其次与文件夹同名的 HTML
- 标签/emoji/介绍统一配置：在 meta.json 中维护，扫描时自动合并进清单
- 兼容 file:// 直开：index.html 内嵌清单兜底，双击即可使用

## 使用

```bash
python3 scan_tools.py
```

运行后自动更新 tools.json 与 index.html 内嵌清单。

## 维护工具信息

编辑根目录 `meta.json`，按工具文件夹名（id）配置：

```json
{
  "CyberShb": {
    "category": "趣味",
    "emoji": "🏆",
    "desc": "赛博求签，许愿祈愿"
  }
}
```

支持字段：`category`（标签）、`emoji`（图标）、`desc`（介绍）、`name`（名称，可选，默认取页面 title）。修改后重新运行扫描脚本。

## 项目结构

```
ATOOLHUB/
├── index.html         # 集成导航主页（入口）
├── tools.json         # 工具清单（扫描脚本自动生成）
├── meta.json          # 工具元数据（标签/emoji/介绍，手动维护）
├── scan_tools.py      # 自动发现脚本
├── assets/            # 本地资源（FontAwesome 图标字体等）
├── CyberShb/          # 示例工具：赛博圣杯
├── PiggyPeggy/        # 示例工具：存钱罐
└── xiaopin/           # 示例工具：DOCX 转 EPUB 在线转换工具
```

## 说明

- tools.json 由扫描脚本自动生成，不要手动编辑
- 工具信息（标签/emoji/介绍）以 meta.json 为准

## License

PiggyPeggy 遵循其目录内的 NON-COMMERCIAL PUBLIC LICENSE，其余部分为个人项目，请勿商用。