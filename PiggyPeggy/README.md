# Piggy Peggy 🐷

[English](#english) | [中文](#chinese)

---

<a name="chinese"></a>
## 中文说明

**Piggy Peggy** 是一个简约且有趣的网页极简存钱罐应用。

### 🌟 功能特点
* **存钱交互**：点击硬币即可向小猪存钱，伴有动画效果。
* **翻转查看**：点击小猪可翻转至底面查看当前余额。
* **摇晃取钱**：按住小猪左右拖拽摇晃即可把钱取出。
* **数据管理**：支持查看存取记录、导出 CSV 明细及一键清空重置。
* **本地日志自动同步**：首次使用时自动弹出“数据管理”窗口，设置本地路径（支持 macOS / Windows）并授权文件夹后，每次开启页面自动扫描该路径下的 `piggypeggy_data` 日志文件加载数据，每次存钱 / 取钱后自动覆盖写入日志文件。
* **单文件运行**：内置所有矢量图形（SVG）与逻辑，无任何外部文件依赖。

### ⚠️ 免责声明（数据安全）
本应用为纯前端本地应用，所有数据**仅保存在您授权的本地文件夹日志文件中**，不使用浏览器缓存。
* **开发者不对任何因清除浏览器缓存、更换设备、系统故障或不可抗力导致的数据丢失、损坏或记录不准确承担任何责任。**
* 为保障您的数据安全，请务必保管好本地日志文件，避免误删。可定期使用“管理”功能中的 **导出 CSV** 备份您的存钱记录。
* 本地文件自动同步基于浏览器 File System Access API，需使用 Chrome / Edge 等支持浏览器，并通过 `http://localhost` 或 HTTPS 方式打开页面。

---

<a name="english"></a>
## English

**Piggy Peggy** is a minimalist, and fun interactive piggy bank web application.

### 🌟 Features
* **Interactive Savings**: Click coins to deposit money into the piggy bank with fun animations.
* **Flip to Check Balance**: Click the piggy bank to flip it over and inspect your current balance.
* **Shake to Withdraw**: Click and drag/shake the pig left and right to withdraw funds.
* **Data Management**: View transaction logs, export CSV files, and reset data.
* **Auto Local Log Sync**: On first use, the "Data Management" window opens automatically. After setting a local path (macOS / Windows) and authorizing the folder, every page open auto-scans the folder for the `piggypeggy_data` log file and loads data; after each deposit / withdrawal it automatically overwrites the log file.
* **Single-File Zero-Dependency**: Fully self-contained with embedded SVGs and styles.

### ⚠️ Disclaimer (Data Loss)
This application is a pure front-end tool, and all data is stored **only in the local log file in the folder you authorize**; no browser cache is used.
* **The developer assumes NO responsibility or liability for any data loss, corruption, or inaccuracies caused by clearing browser cache, switching devices, system errors, or any other reasons.**
* To prevent data loss, please keep your local log files safe and avoid accidental deletion. You may regularly use the **Export CSV** feature in the "Management" panel to back up your records.
* Local file auto-sync uses the browser File System Access API, which requires Chrome / Edge and opening the page via `http://localhost` or HTTPS.