# 代码审计助手 (Code Audit Assistant)

一个自动化检测常见安全编码问题的工具，帮助开发者在代码编写过程中及时发现和修复安全漏洞。

## 作者

EtherealXTHY-From Zhengzhou University

## 功能特性

- **多语言支持**：支持Python、JavaScript、Java、C/C++等多种编程语言
- **常见安全问题检测**：SQL注入、XSS攻击、命令注入、缓冲区溢出等
- **规则可配置**：支持自定义检测规则和阈值
- **详细报告**：生成清晰的HTML和JSON格式的审计报告
- **CI/CD集成**：可集成到持续集成/持续部署流程中

## 安装

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

## 使用方法

### 基本用法

```bash
# 扫描单个文件
python audit.py --file path/to/file.py

# 扫描目录
python audit.py --dir path/to/directory

# 生成HTML报告
python audit.py --dir path/to/directory --report html

# 生成JSON报告
python audit.py --dir path/to/directory --report json
```

### 配置选项

可以通过修改 `config/rules.yaml` 文件来配置检测规则：

- 启用/禁用特定规则
- 调整规则的严重程度
- 添加自定义规则

## 支持的安全检测类型

- **注入攻击**：SQL注入、NoSQL注入、命令注入
- **跨站脚本**：XSS攻击
- **认证问题**：弱密码、硬编码凭证
- **敏感数据泄露**：明文密码、API密钥泄露
- **访问控制**：权限绕过
- **安全配置错误**：默认配置、调试信息泄露
- **跨站请求伪造**：CSRF攻击
- **依赖项漏洞**：过时依赖

## 项目结构

```
code-audit-assistant/
├── audit.py          # 主入口文件
├── core/             # 核心模块
│   └── engine.py     # 规则引擎
├── scanner/          # 扫描模块
│   ├── file_scanner.py      # 文件扫描器
│   └── language_detector.py # 语言检测器
├── report/           # 报告模块
│   ├── html_report.py  # HTML报告生成
│   └── json_report.py  # JSON报告生成
├── config/           # 配置模块
│   └── rules.yaml    # 规则配置文件
├── tests/            # 测试模块
│   └── test_rules.py # 规则测试
├── docs/             # 文档
│   └── usage.md      # 使用指南
├── test_sample.py    # 测试样本
├── requirements.txt  # 依赖文件
└── README.md         # 项目说明
```

## 示例

### 扫描结果示例

```
代码审计助手 v1.0
作者: EtherealXTHY-From Zhengzhou University
==================================================
开始扫描: test_sample.py
扫描完成，发现 6 个安全问题
按严重程度分类:
  HIGH: 2
  MEDIUM: 3
  LOW: 1
HTML报告已生成: report.html
JSON报告已生成: report.json
```

## 贡献

欢迎提交问题和拉取请求！请确保遵循项目的代码风格和贡献指南。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 免责声明

本工具仅作为辅助开发工具，不能替代专业的安全审计。使用本工具进行代码审计时，请结合其他安全测试方法。