# IP地址筛选工具

## 简介

本项目提供了一套自动化流程，用于从APNIC数据库下载最新的IP分配信息，并筛选出特定国家（默认为中国）的IPv4和IPv6地址段。这些地址段将被保存到文本文件中，以便后续使用或分析。

## 功能特点

- **定时任务**：每天凌晨两点（UTC时间）自动运行。
- **手动触发**：支持通过GitHub Actions手动启动工作流。
- **地址筛选**：能够根据指定的国家代码筛选出该国的IP地址段。
- **文件输出**：生成包含IPv4和IPv6地址段的独立文本文件。
- **自动提交**：更新后的地址段文件会自动提交并推送到GitHub仓库。

## 使用方法

### 设置与配置

1. **克隆仓库**：首先，请使用`git clone`命令将此仓库克隆到本地计算机上。
   ```bash
   git clone https://github.com/yourusername/ip-address-filter.git
2. **安装依赖**：确保Python环境已正确设置，然后安装所需的Python包：
   ```bash
   python -m pip install --upgrade pip
   pip install requests
   ```
3. **编辑脚本**：如需更改目标国家或其他参数，可以在`filter_iplist_for_country.py`文件中进行相应修改。

### 运行脚本

- 你可以直接在GitHub Actions中触发工作流，也可以在本地环境中运行Python脚本：
  ```bash
  python filter_iplist_for_country.py
  ```

## 贡献指南

我们欢迎任何形式的贡献！如果您发现了错误或想要提出改进建议，请遵循以下步骤：

1. Fork 本仓库。
2. 创建一个新的分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 提交Pull Request。

请确保阅读并遵守[贡献者条约](CONTRIBUTING.md)，以维护一个开放和欢迎的社区。

## 注意事项

- 由于数据源可能发生变化，建议定期检查脚本以确保其正常工作。
- 请勿滥用获取的IP地址列表，遵守相关法律法规。

## 许可证

本项目采用MIT许可证，详情参见[许可证](LICENSE)文件。

---

## 开发者联系方式

如果有任何问题或需要进一步的帮助，请联系开发者 [JinkaiNiu] 或访问我们的 [GitHub Issues Page](https://github.com/yourusername/ip-address-filter/issues).

## 变更日志

查看项目的[变更日志](CHANGELOG.md)以了解每次版本更新的具体内容。
