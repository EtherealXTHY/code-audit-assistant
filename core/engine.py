import re
import yaml
import os

class RuleEngine:
    def __init__(self, config_path='config/rules.yaml'):
        self.config_path = config_path
        self.rules = self.load_rules()
    
    def load_rules(self):
        # 加载规则配置文件
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading rules: {e}")
            return {}
    
    def get_rules_by_language(self, language):
        # 根据语言获取对应的规则
        language_rule_map = {
            'python': 'python_rules',
            'javascript': 'javascript_rules',
            'java': 'java_rules',
            'c': 'c_rules',
            'cpp': 'c_rules'
        }
        
        rules = []
        
        # 添加通用规则
        if self.rules.get('enabled', {}).get('common_rules', True):
            common_rules = self.rules.get('common_rules', {})
            for rule_name, rule_config in common_rules.items():
                rules.append({
                    'name': rule_config['name'],
                    'severity': rule_config['severity'],
                    'description': rule_config['description'],
                    'patterns': rule_config['patterns'],
                    'type': 'common'
                })
        
        # 添加语言特定规则
        rule_key = language_rule_map.get(language)
        if rule_key and self.rules.get('enabled', {}).get(rule_key, True):
            lang_rules = self.rules.get(rule_key, {})
            for rule_name, rule_config in lang_rules.items():
                rules.append({
                    'name': rule_config['name'],
                    'severity': rule_config['severity'],
                    'description': rule_config['description'],
                    'patterns': rule_config['patterns'],
                    'type': language
                })
        
        return rules
    
    def detect_issues(self, file_content, language):
        # 检测代码中的安全问题
        issues = []
        rules = self.get_rules_by_language(language)
        
        lines = file_content.split('\n')
        for line_num, line in enumerate(lines, 1):
            for rule in rules:
                for pattern in rule['patterns']:
                    if re.search(pattern, line):
                        issues.append({
                            'file': '',  # 稍后填充
                            'line': line_num,
                            'code': line.strip(),
                            'rule_name': rule['name'],
                            'severity': rule['severity'],
                            'description': rule['description'],
                            'recommendation': self.get_recommendation(rule['name'])
                        })
        
        return issues
    
    def get_recommendation(self, rule_name):
        # 根据规则名称获取修复建议
        recommendations = {
            'SQL注入': '使用参数化查询或ORM框架',
            'XSS攻击': '对用户输入进行HTML转义',
            '命令注入': '避免直接拼接命令，使用参数化执行',
            '缓冲区溢出': '使用安全的字符串处理函数，如strncpy',
            '格式化字符串漏洞': '使用固定的格式化字符串，避免用户输入',
            '硬编码凭证': '使用环境变量或配置文件存储敏感信息',
            '调试信息泄露': '在生产环境中禁用调试信息输出',
            '不安全的随机数生成': '使用加密安全的随机数生成器',
            '敏感数据泄露': '对敏感数据进行加密存储'
        }
        return recommendations.get(rule_name, '请参考相关安全最佳实践')
    
    def update_rules(self, new_rules):
        # 更新规则配置
        self.rules.update(new_rules)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.rules, f, default_flow_style=False, allow_unicode=True)
    
    def get_severity_level(self, severity):
        # 获取严重程度的数值表示
        severity_map = self.rules.get('severity', {})
        return severity_map.get(severity, 0)
    
    def filter_issues_by_severity(self, issues, min_severity):
        # 根据严重程度过滤问题
        min_level = self.get_severity_level(min_severity)
        filtered_issues = []
        
        for issue in issues:
            issue_level = self.get_severity_level(issue['severity'])
            if issue_level >= min_level:
                filtered_issues.append(issue)
        
        return filtered_issues