#!/usr/bin/env python3
"""测试用例文件，包含各种安全问题"""

import os
import random
import subprocess

# 1. SQL注入漏洞
username = input("请输入用户名: ")
cursor.execute("SELECT * FROM users WHERE username = '" + username + "'")

# 2. 硬编码凭证
API_KEY = "secret_key_123456"
password = "admin123"

# 3. 命令注入漏洞
user_input = input("请输入命令: ")
os.system("echo " + user_input)

# 4. 不安全的随机数生成
random_number = random.randint(1, 100)

# 5. 调试信息泄露
print("调试信息: " + str(user_input))

# 6. 敏感数据泄露
def get_user_info():
    return {
        "username": "admin",
        "password": "plaintext_password",
        "email": "admin@example.com"
    }

# 7. XSS漏洞（Flask示例）
@app.route('/user')
def user_profile():
    username = request.args.get('name')
    return flask.render_template_string('<h1>Hello, ' + username + '</h1>')

# 8. 缓冲区溢出（模拟C代码）
# char buffer[10];
# gets(buffer); // 危险函数

# 9. 格式化字符串漏洞（模拟C代码）
# char user_input[100];
# scanf("%s", user_input);
# printf(user_input); // 危险

# 10. 跨站请求伪造（CSRF）漏洞
# @app.route('/transfer', methods=['POST'])
# def transfer_money():
#     amount = request.form.get('amount')
#     recipient = request.form.get('recipient')
#     # 没有CSRF保护
#     transfer(amount, recipient)
#     return "转账成功"