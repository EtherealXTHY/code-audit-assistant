# 代码审计助手使用指南

## 1. 项目简介

代码审计助手是一个自动化检测常见安全编码问题的工具，帮助开发者在代码编写过程中及时发现和修复安全漏洞。

### 主要功能

- **多语言支持**：支持Python、JavaScript、Java、C/C++等多种编程语言
- **常见安全问题检测**：SQL注入、XSS攻击、命令注入、缓冲区溢出等
- **规则可配置**：支持自定义检测规则和阈值
- **详细报告**：生成清晰的HTML和JSON格式的审计报告
- **CI/CD集成**：可集成到持续集成/持续部署流程中

## 2. 安装指南

### 环境要求

- Python 3.7+

### 安装步骤

1. 克隆项目
   ```bash
   git clone https://github.com/yourusername/code-audit-assistant.git
   cd code-audit-assistant
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

## 3. 使用方法

### 3.1 命令行参数

```bash
# 扫描单个文件
python audit.py --file path/to/file.py

# 扫描目录
python audit.py --dir path/to/directory

# 生成HTML报告
python audit.py --dir path/to/directory --report html

# 生成JSON报告
python audit.py --dir path/to/directory --report json

# 生成两种格式的报告
python audit.py --dir path/to/directory --report both

# 指定报告输出文件名
python audit.py --dir path/to/directory --output my_report

# 按严重程度过滤
python audit.py --dir path/to/directory --severity MEDIUM

# 排除指定目录
python audit.py --dir path/to/directory --exclude node_modules venv
```

### 3.2 示例用法

#### 示例1：扫描单个Python文件

```bash
python audit.py --file example.py
```

输出：
```
开始扫描: example.py
扫描完成，发现 3 个安全问题
按严重程度分类:
  HIGH: 1
  MEDIUM: 1
  LOW: 1
HTML报告已生成: report.html
```

#### 示例2：扫描整个项目目录

```bash
python audit.py --dir my_project --report both --output project_audit
```

这将扫描 `my_project` 目录中的所有文件，并生成 `project_audit.html` 和 `project_audit.json` 两个报告文件。

## 4. 配置规则

### 4.1 规则配置文件

规则配置文件位于 `config/rules.yaml`，您可以根据需要修改或添加规则。

### 4.2 规则结构

```yaml
# 规则严重程度定义
severity:
  HIGH: 3
  MEDIUM: 2
  LOW: 1
  INFO: 0

# 规则定义
rule_name:
  name: 规则名称
  severity: 严重程度
  description: 规则描述
  patterns:
    - 正则表达式1
    - 正则表达式2

# 规则启用状态
enabled:
  rule_set: true/false
```

### 4.3 添加自定义规则

要添加自定义规则，只需在相应的规则集中添加新的规则定义。例如，要添加一个新的Python规则：

```yaml
python_rules:
  # 现有规则...
  my_custom_rule:
    name: 自定义规则
    severity: MEDIUM
    description: 检测自定义安全问题
    patterns:
      - 正则表达式
```

## 5. 报告格式

### 5.1 HTML报告

HTML报告提供了一个美观、易于阅读的界面，包含：
- 扫描摘要（总问题数、按严重程度分类等）
- 详细的问题列表，包括：
  - 文件路径和行号
  - 严重程度
  - 问题描述
  - 代码片段
  - 修复建议

### 5.2 JSON报告

JSON报告提供了机器可解析的格式，包含：
- 生成时间
- 扫描摘要
- 详细的问题列表

## 6. 集成到CI/CD

### 6.1 GitHub Actions

在 `.github/workflows/audit.yml` 中添加：

```yaml
name: Code Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run code audit
        run: python audit.py --dir . --report json
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: audit-report
          path: report.json
```

### 6.2 GitLab CI/CD

在 `.gitlab-ci.yml` 中添加：

```yaml
code_audit:
  stage: test
  script:
    - pip install -r requirements.txt
    - python audit.py --dir . --report json
  artifacts:
    paths:
      - report.json
```

## 7. 支持的安全检测类型

| 安全问题类型 | 严重程度 | 支持的语言 |
|-------------|----------|------------|
| SQL注入 | HIGH | Python, JavaScript, Java |
| XSS攻击 | HIGH/MEDIUM | Python, JavaScript, Java |
| 命令注入 | HIGH | Python, JavaScript, C/C++ |
| 缓冲区溢出 | HIGH | C/C++ |
| 格式化字符串漏洞 | HIGH | C/C++ |
| 硬编码凭证 | MEDIUM | 所有语言 |
| 不安全的随机数生成 | MEDIUM | Python |
| 调试信息泄露 | LOW | 所有语言 |

## 8. 常见问题

### 8.1 规则误报

如果遇到误报，可以通过修改 `config/rules.yaml` 文件来调整规则的模式或禁用特定规则。

### 8.2 性能问题

对于大型项目，扫描可能会比较耗时。可以通过以下方式优化：
- 排除不需要扫描的目录（如 `node_modules`、`venv` 等）
- 按严重程度过滤，只关注高危问题
- 分批次扫描不同模块

### 8.3 支持更多语言

要添加对新语言的支持，需要：
1. 在 `scanner/language_detector.py` 中添加语言检测逻辑
2. 在 `config/rules.yaml` 中添加相应的规则集
3. 在 `core/engine.py` 中的 `language_rule_map` 中添加语言映射

## 9. 贡献指南

欢迎提交问题和拉取请求！请确保遵循以下准则：

1. 确保代码通过所有测试
2. 遵循项目的代码风格
3. 提供清晰的提交信息
4. 对于新功能，添加相应的测试用例

## 10. 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 11. 免责声明

本工具仅作为辅助开发工具，不能替代专业的安全审计。使用本工具进行代码审计时，请结合其他安全测试方法。