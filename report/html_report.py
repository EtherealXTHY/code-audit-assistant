import os
from jinja2 import Template

class HTMLReport:
    # HTML报告生成器
    
    @staticmethod
    def generate(issues, summary, output_path='report.html'):
        # 生成HTML报告
        # HTML模板
        template = Template('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>代码审计报告</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
        }
        
        .container {
            max-width: 1200px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }
        
        h2 {
            color: #34495e;
            margin: 20px 0 10px;
        }
        
        .summary {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px 0;
        }
        
        .summary-card {
            flex: 1;
            min-width: 200px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        
        .summary-card h3 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .summary-card ul {
            list-style: none;
        }
        
        .summary-card li {
            margin: 5px 0;
        }
        
        .issue {
            margin: 15px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #e74c3c;
            background-color: #f9f2f4;
        }
        
        .issue.high {
            border-left-color: #e74c3c;
            background-color: #f9f2f4;
        }
        
        .issue.medium {
            border-left-color: #f39c12;
            background-color: #fef9e7;
        }
        
        .issue.low {
            border-left-color: #3498db;
            background-color: #ebf5fb;
        }
        
        .issue-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        
        .issue-file {
            font-weight: bold;
            color: #2c3e50;
        }
        
        .issue-severity {
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }
        
        .severity-high {
            background-color: #e74c3c;
            color: white;
        }
        
        .severity-medium {
            background-color: #f39c12;
            color: white;
        }
        
        .severity-low {
            background-color: #3498db;
            color: white;
        }
        
        .issue-code {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            margin: 10px 0;
        }
        
        .issue-description {
            margin: 10px 0;
        }
        
        .issue-recommendation {
            margin: 10px 0;
            padding: 10px;
            background-color: #e8f5e8;
            border-radius: 4px;
        }
        
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #777;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>代码审计报告</h1>
        
        <div class="summary">
            <div class="summary-card">
                <h3>总体统计</h3>
                <ul>
                    <li>总问题数: {{ summary.total_issues }}</li>
                </ul>
            </div>
            
            <div class="summary-card">
                <h3>按严重程度</h3>
                <ul>
                    {% for severity, count in summary.by_severity.items() %}
                    <li>{{ severity }}: {{ count }}</li>
                    {% endfor %}
                </ul>
            </div>
            
            <div class="summary-card">
                <h3>按语言</h3>
                <ul>
                    {% for language, count in summary.by_language.items() %}
                    <li>{{ language }}: {{ count }}</li>
                    {% endfor %}
                </ul>
            </div>
            
            <div class="summary-card">
                <h3>按规则</h3>
                <ul>
                    {% for rule, count in summary.by_rule.items() %}
                    <li>{{ rule }}: {{ count }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        
        <h2>详细问题</h2>
        
        {% if issues %}
            {% for issue in issues %}
            <div class="issue {{ issue.severity.lower() }}">
                <div class="issue-info">
                    <span class="issue-file">{{ issue.file }}:{{ issue.line }}</span>
                    <span class="issue-severity severity-{{ issue.severity.lower() }}">{{ issue.severity }}</span>
                </div>
                <h3>{{ issue.rule_name }}</h3>
                <div class="issue-description">{{ issue.description }}</div>
                <div class="issue-code">{{ issue.code }}</div>
                <div class="issue-recommendation">
                    <strong>修复建议:</strong> {{ issue.recommendation }}
                </div>
            </div>
            {% endfor %}
        {% else %}
            <p>未发现安全问题</p>
        {% endif %}
        
        <div class="footer">
            <p>报告生成时间: {{ generated_time }}</p>
            <p>代码审计助手 © 2025</p>
            <p>作者: EtherealXTHY-From Zhengzhou University</p>
        </div>
    </div>
</body>
</html>
        ''')
        
        # 生成时间
        from datetime import datetime
        generated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 渲染模板
        html_content = template.render(
            issues=issues,
            summary=summary,
            generated_time=generated_time
        )
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path