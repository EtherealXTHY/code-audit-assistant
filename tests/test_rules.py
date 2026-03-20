import pytest
import os
from core.engine import RuleEngine
from scanner.file_scanner import FileScanner
from scanner.language_detector import LanguageDetector

class TestRuleEngine:
    """测试规则引擎"""
    
    def setup_method(self):
        self.engine = RuleEngine()
    
    def test_load_rules(self):
        """测试加载规则"""
        assert isinstance(self.engine.rules, dict)
        assert 'severity' in self.engine.rules
        assert 'common_rules' in self.engine.rules
    
    def test_get_rules_by_language(self):
        """测试根据语言获取规则"""
        python_rules = self.engine.get_rules_by_language('python')
        assert len(python_rules) > 0
        
        js_rules = self.engine.get_rules_by_language('javascript')
        assert len(js_rules) > 0
    
    def test_detect_issues(self):
        """测试检测安全问题"""
        # 测试Python代码中的SQL注入
        python_code = "cursor.execute(\"SELECT * FROM users WHERE username = '\" + username + \"'\")"
        issues = self.engine.detect_issues(python_code, 'python')
        assert len(issues) > 0
        
        # 测试JavaScript代码中的XSS
        js_code = "document.write('<div>' + userInput + '</div>')"
        issues = self.engine.detect_issues(js_code, 'javascript')
        assert len(issues) > 0

class TestLanguageDetector:
    """测试语言检测器"""
    
    def test_detect_by_extension(self):
        """测试根据扩展名检测语言"""
        assert LanguageDetector.detect_by_extension('test.py') == 'python'
        assert LanguageDetector.detect_by_extension('test.js') == 'javascript'
        assert LanguageDetector.detect_by_extension('test.java') == 'java'
        assert LanguageDetector.detect_by_extension('test.c') == 'c'
    
    def test_detect_by_content(self):
        """测试根据内容检测语言"""
        # 测试Python代码
        python_code = "def test():\n    import os\n    print('test')"
        assert LanguageDetector.detect_by_content(python_code) == 'python'
        
        # 测试JavaScript代码
        js_code = "function test() {\n    var x = 1;\n    console.log('test');\n}"
        assert LanguageDetector.detect_by_content(js_code) == 'javascript'
    
    def test_is_supported_language(self):
        """测试语言是否被支持"""
        assert LanguageDetector.is_supported_language('python') is True
        assert LanguageDetector.is_supported_language('javascript') is True
        assert LanguageDetector.is_supported_language('java') is True
        assert LanguageDetector.is_supported_language('c') is True
        assert LanguageDetector.is_supported_language('cpp') is True
        assert LanguageDetector.is_supported_language('php') is False

class TestFileScanner:
    """测试文件扫描器"""
    
    def setup_method(self):
        self.scanner = FileScanner()
        # 创建测试文件
        self.test_file = 'test_temp.py'
        with open(self.test_file, 'w') as f:
            f.write("cursor.execute(\"SELECT * FROM users WHERE username = '\" + username + \"'\")\n")
            f.write("password = 'secret123'\n")
    
    def teardown_method(self):
        # 清理测试文件
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_scan_file(self):
        """测试扫描单个文件"""
        issues = self.scanner.scan_file(self.test_file)
        assert len(issues) > 0
    
    def test_get_summary(self):
        """测试获取扫描摘要"""
        issues = self.scanner.scan_file(self.test_file)
        summary = self.scanner.get_summary(issues)
        assert 'total_issues' in summary
        assert summary['total_issues'] > 0

if __name__ == '__main__':
    pytest.main(['-v', __file__])