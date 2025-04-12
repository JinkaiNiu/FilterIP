# FilterIP

## 项目简介

`FilterIP` 是一个用于从 APNIC 数据中提取特定国家（如中国）IP 地址的工具。该项目通过 Python 脚本实现 IP 地址的过滤，并通过 GitHub Actions 自动化运行和更新结果。

## 功能

- 从 APNIC 数据源下载最新的 IP 地址分配文件。
- 根据指定的国家代码（默认 `CN`）过滤 IPv4 和 IPv6 地址。
- 自动化运行脚本并将结果推送到代码仓库。

## 文件结构

- `filter_iplist_for_country.py`：主脚本文件，包含下载、过滤和日志记录功能。
- `.github/workflows/filter_ip_addresses_for_country.yml`：GitHub Actions 工作流文件，用于定时或手动触发脚本运行。
- `all_cn.txt`：过滤后的中国 IPv4 地址列表。
- `all_cn_ipv6.txt`：过滤后的中国 IPv6 地址列表。

## 使用方法

### 本地运行

1. 克隆仓库：
   ```bash
   git clone <仓库地址>
   cd FilterIP
   ```

2. 安装依赖：
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. 运行脚本：
   ```bash
   python filter_iplist_for_country.py
   ```

### 自动化运行

GitHub Actions 工作流会每天 UTC 时间 18:00（中国时间凌晨 2:00）自动运行脚本，并将结果推送到仓库。

## 日志

脚本运行时会生成详细的日志文件，命名格式为 `script_YYYYMMDD_HHMMSS.log`，用于记录下载和过滤过程中的信息。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进本项目。

## 许可证

本项目采用 MIT 许可证，详情请参阅 [LICENSE](LICENSE) 文件。
