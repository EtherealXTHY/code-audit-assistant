import os

class LanguageDetector:
    # 语言检测器，用于识别代码文件的编程语言
    
    # 文件扩展名到语言的映射
    EXTENSION_MAP = {
        # Python
        '.py': 'python',
        '.pyw': 'python',
        # JavaScript
        '.js': 'javascript',
        '.jsx': 'javascript',
        # Java
        '.java': 'java',
        # C/C++
        '.c': 'c',
        '.h': 'c',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.hpp': 'cpp',
        '.hxx': 'cpp',
        # PHP
        '.php': 'php',
        # Ruby
        '.rb': 'ruby',
        # Go
        '.go': 'go',
        # Rust
        '.rs': 'rust',
        # Swift
        '.swift': 'swift',
        # Kotlin
        '.kt': 'kotlin',
        # TypeScript
        '.ts': 'typescript',
        '.tsx': 'typescript'
    }
    
    @staticmethod
    def detect_by_extension(filename):
        # 根据文件扩展名检测语言
        ext = os.path.splitext(filename)[1].lower()
        return LanguageDetector.EXTENSION_MAP.get(ext, 'unknown')
    
    @staticmethod
    def detect_by_content(file_content, filename=None):
        # 根据文件内容检测语言
        # 首先尝试根据扩展名检测
        if filename:
            lang = LanguageDetector.detect_by_extension(filename)
            if lang != 'unknown':
                return lang
        
        # 根据内容特征检测
        content = file_content.lower()
        
        # Python 特征
        if 'def ' in content and 'import ' in content:
            return 'python'
        
        # JavaScript 特征
        if 'function ' in content and ('var ' in content or 'let ' in content or 'const ' in content):
            return 'javascript'
        
        # Java 特征
        if 'public class ' in content or 'import java.' in content:
            return 'java'
        
        # C/C++ 特征
        if '#include <' in content or 'int main(' in content:
            return 'c'
        
        return 'unknown'
    
    @staticmethod
    def is_supported_language(language):
        # 检查语言是否被支持
        supported_languages = ['python', 'javascript', 'java', 'c', 'cpp']
        return language in supported_languages