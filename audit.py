import argparse
import os
from scanner.file_scanner import FileScanner
from report.html_report import HTMLReport
from report.json_report import JSONReport

class AuditTool:
    # 代码审计工具主类
    
    def __init__(self):
        self.scanner = FileScanner()
    
    def parse_args(self):
        # 解析命令行参数
        parser = argparse.ArgumentParser(description='代码审计助手 - 自动化检测常见安全编码问题')
        
        # 必选参数：文件或目录路径
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--file', type=str, help='要扫描的单个文件')
        group.add_argument('--dir', type=str, help='要扫描的目录')
        
        # 可选参数
        parser.add_argument('--report', type=str, choices=['html', 'json', 'both'], default='html',
                          help='报告格式 (默认: html)')
        parser.add_argument('--output', type=str, default='report',
                          help='报告输出文件名 (不含扩展名)')
        parser.add_argument('--severity', type=str, choices=['LOW', 'MEDIUM', 'HIGH'],
                          help='最低严重程度')
        parser.add_argument('--exclude', type=str, nargs='+',
                          default=['.git', '__pycache__', 'node_modules', 'venv', 'env'],
                          help='要排除的目录')
        
        return parser.parse_args()
    
    def run(self):
        # 运行审计工具
        args = self.parse_args()
        
        # 确定扫描路径
        if args.file:
            path = args.file
        else:
            path = args.dir
        
        # 检查路径是否存在
        if not os.path.exists(path):
            print(f"错误: 路径 '{path}' 不存在")
            return
        
        # 开始扫描
        print(f"开始扫描: {path}")
        issues = self.scanner.scan(path, args.exclude)
        
        # 过滤问题
        if args.severity:
            issues = self.scanner.filter_issues(issues, args.severity)
        
        # 获取摘要
        summary = self.scanner.get_summary(issues)
        
        # 打印摘要
        print(f"扫描完成，发现 {summary['total_issues']} 个安全问题")
        if summary['by_severity']:
            print("按严重程度分类:")
            for severity, count in summary['by_severity'].items():
                print(f"  {severity}: {count}")
        
        # 生成报告
        if args.report in ['html', 'both']:
            html_path = f"{args.output}.html"
            HTMLReport.generate(issues, summary, html_path)
            print(f"HTML报告已生成: {html_path}")
        
        if args.report in ['json', 'both']:
            json_path = f"{args.output}.json"
            JSONReport.generate(issues, summary, json_path)
            print(f"JSON报告已生成: {json_path}")

if __name__ == '__main__':
    print("代码审计助手 v1.0")
    print("作者: EtherealXTHY-From Zhengzhou University")
    print("=" * 50)
    tool = AuditTool()
    tool.run()