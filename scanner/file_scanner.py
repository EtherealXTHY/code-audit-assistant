import os
from .language_detector import LanguageDetector
from core.engine import RuleEngine

class FileScanner:
    # 文件扫描器，用于扫描文件和目录中的安全问题
    
    def __init__(self, rule_engine=None):
        self.rule_engine = rule_engine or RuleEngine()
        self.language_detector = LanguageDetector()
    
    def scan_file(self, file_path):
        # 扫描单个文件
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 检测语言
            language = self.language_detector.detect_by_content(content, file_path)
            
            if not self.language_detector.is_supported_language(language):
                return []
            
            # 检测安全问题
            issues = self.rule_engine.detect_issues(content, language)
            
            # 填充文件路径
            for issue in issues:
                issue['file'] = file_path
            
            return issues
        except Exception as e:
            print(f"Error scanning file {file_path}: {e}")
            return []
    
    def scan_directory(self, directory_path, exclude_patterns=None):
        # 扫描目录
        if exclude_patterns is None:
            exclude_patterns = ['.git', '__pycache__', 'node_modules', 'venv', 'env']
        
        all_issues = []
        
        for root, dirs, files in os.walk(directory_path):
            # 排除指定目录
            dirs[:] = [d for d in dirs if d not in exclude_patterns]
            
            for file in files:
                file_path = os.path.join(root, file)
                issues = self.scan_file(file_path)
                all_issues.extend(issues)
        
        return all_issues
    
    def scan(self, path, exclude_patterns=None):
        # 扫描文件或目录
        if os.path.isfile(path):
            return self.scan_file(path)
        elif os.path.isdir(path):
            return self.scan_directory(path, exclude_patterns)
        else:
            print(f"Error: {path} is not a valid file or directory")
            return []
    
    def get_summary(self, issues):
        # 获取扫描结果摘要
        summary = {
            'total_issues': len(issues),
            'by_severity': {},
            'by_language': {},
            'by_rule': {}
        }
        
        for issue in issues:
            # 按严重程度统计
            severity = issue['severity']
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
            
            # 按规则统计
            rule_name = issue['rule_name']
            summary['by_rule'][rule_name] = summary['by_rule'].get(rule_name, 0) + 1
            
            # 按文件统计（简化为语言统计）
            language = self.language_detector.detect_by_extension(issue['file'])
            summary['by_language'][language] = summary['by_language'].get(language, 0) + 1
        
        return summary
    
    def filter_issues(self, issues, min_severity=None):
        # 过滤问题
        if min_severity:
            return self.rule_engine.filter_issues_by_severity(issues, min_severity)
        return issues