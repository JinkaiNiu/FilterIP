# 自动化过滤 IP 地址并更新到 GitHub 仓库

## 目标

本项目旨在使用 GitHub Actions 自动化过滤特定国家（如中国）的 IP 地址，并将结果定期更新到 GitHub 仓库中。这有助于简化 IP 地址管理流程，提高效率，并减少手动操作的错误率。

## 主要功能

1. **定时任务**：每天凌晨两点（中国时间）自动运行。
2. **IP 地址过滤**：使用 Python 脚本从 APNIC 数据库中提取并过滤中国的 IPv4 和 IPv6 地址。
3. **自动提交**：将过滤后的 IP 地址列表提交到 GitHub 仓库。

## 目录

- [安装与配置](#安装与配置)
- [GitHub Actions 工作流](#github-actions-工作流)
- [Python 脚本](#python-脚本)
- [贡献](#贡献)
- [许可证](#许可证)

## 安装与配置

### 克隆仓库

首先，克隆本仓库到本地：

```bash
git clone https://github.com/yourusername/filter-ip-addresses.git
cd filter-ip-addresses
```

### 配置 GitHub Secrets

为了使 GitHub Actions 能够推送到仓库，你需要在仓库设置中添加一个 `GITHUB_TOKEN` secret。GitHub Actions 会自动提供此令牌，但你需要确保它具有写权限。

1. 进入你的 GitHub 仓库页面。
2. 点击 `Settings`。
3. 在左侧菜单中选择 `Secrets and variables` -> `Actions`。
4. 点击 `New repository secret`。
5. 输入名称 `GITHUB_TOKEN`，值留空，因为 GitHub 会自动填充此令牌。

## GitHub Actions 工作流

### 文件路径

`.github/workflows/filter-ip-addresses.yml`

### 内容

```yaml
name: Filter IP Addresses for Country

on:
  schedule:
    - cron: '0 18 * * *' # 每天下午六点 UTC 运行，对应中国时间每天凌晨两点
  workflow_dispatch: # 手动触发

jobs:
  run-script:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        echo "Upgrading pip..."
        python -m pip install --upgrade pip
        echo "Installing requests library..."
        pip install requests

    - name: Run script
      run: |
        echo "Running the filtering script..."
        python filter_iplist_for_country.py

    - name: Check if changes are present
      id: check_changes
      run: |
        echo "Checking for changes in the repository..."
        git status
        if [[ $(git diff-index --quiet HEAD || echo "modified") == "modified" ]]; then
          echo "changed=true" >> $GITHUB_ENV
        fi
      shell: bash

    - name: Commit and push changes
      if: env.changed == 'true'
      run: |
        echo "Adding new files to staging area..."
        git add all_cn.txt all_cn_ipv6.txt delegated-apnic-latest
        echo "Configuring Git user information..."
        git config user.name "JinkaiNiu"
        git config user.email "niujinkai@vip.qq.com"
        echo "Committing changes..."
        git commit -m "Update IP lists"
        echo "Pushing changes to repository..."
        git push origin ${{ github.ref }}
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Log completion
      run: echo "Workflow completed successfully."
```

### 解释

1. **定时任务**：使用 `cron: '0 18 * * *'` 设置每天下午六点 UTC 运行，对应中国时间每天凌晨两点。
2. **检查变更**：在 `Check if changes are present` 步骤中，使用 `git status` 检查仓库状态，并通过环境变量 `changed` 记录是否有变更。
3. **提交更改**：只有在检测到有变更时才执行添加、提交和推送操作。

## Python 脚本

### 文件路径

`filter_iplist_for_country.py`

### 内容

```python
# filter_iplist_for_country.py
import requests

def fetch_ip_list():
    url = "https://example.com/delegated-apnic-latest"  # 替换为实际的 URL
    response = requests.get(url)
    return response.text.splitlines()

def filter_ips(ip_list):
    cn_ips = []
    for line in ip_list:
        parts = line.split('|')
        if len(parts) > 2 and parts[1] == 'CN':
            cn_ips.append(parts[3])
    return cn_ips

def save_to_file(ips, filename):
    with open(filename, 'w') as f:
        for ip in ips:
            f.write(f"{ip}\n")

if __name__ == "__main__":
    ip_list = fetch_ip_list()
    cn_ips = filter_ips(ip_list)
    save_to_file(cn_ips, 'all_cn.txt')
    save_to_file([ip for ip in cn_ips if ':' in ip], 'all_cn_ipv6.txt')
```

### 解释

1. **获取 IP 列表**：从指定的 URL 获取 APNIC 的 IP 分配数据。
2. **过滤 IP 地址**：筛选出属于中国的 IP 地址。
3. **保存文件**：将过滤后的 IPv4 和 IPv6 地址分别保存到 `all_cn.txt` 和 `all_cn_ipv6.txt` 文件中。

## 贡献

欢迎任何形式的贡献，包括但不限于 bug 报告、功能建议和代码改进。请按照以下步骤进行贡献：

1. Fork 本仓库。
2. 创建一个新的分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 打开一个 Pull Request。

## 许可证

本项目采用 MIT 许可证。详细内容请参阅 [LICENSE](LICENSE) 文件。

---

希望这个 `README.md` 文档能够帮助用户更好地理解和使用你的项目。如果有任何进一步的修改或补充，请告诉我！
