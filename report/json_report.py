import json
from datetime import datetime

class JSONReport:
    # JSON报告生成器
    
    @staticmethod
    def generate(issues, summary, output_path='report.json'):
        # 生成JSON报告
        # 构建报告数据
        report = {
            'generated_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': summary,
            'issues': issues,
            'author': 'EtherealXTHY-From Zhengzhou University'
        }
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return output_path