"""
作者声明：
        本软件仅适用于南京理工大学紫金学院的校园网认证。
        本脚本仅用于学习和研究，不用于任何商业用途。
        作者不承担因使用本脚本而导致的任何损失或责任。
        请勿联系作者索要破解校园网的思路，也请勿使用本脚本进行任何形式的攻击或滥用。
"""
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver import ActionChains
import time
import traceback
from selenium import webdriver
import requests
from urllib.parse import urlparse


class WiFiAutoConnect:
    def __init__(self, username, password, operator, check_interval=60):
        self.username = username
        self.password = password
        self.operator = operator
        self.driver = None
        self.check_interval = check_interval  # 检查间隔，单位为秒
        # 运营商映射关系
        self.operator_map = {
            "校园网": ("校园网", "校园网", "0"),
            "中国移动": ("移动", "中国移动", "1"),
            "中国电信": ("电信", "中国电信", "2"),
            "中国联通": ("联通", "中国联通", "3")
        }
    
    def is_connected(self):
        """
        检查当前网络是否已认证
        返回True表示已认证，False表示未认证
        """
        try:
            # 直接访问认证服务器地址
            auth_url = "http://172.21.2.10:8080/"
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 正在检查网络认证状态，访问: {auth_url}")
            # 允许重定向以查看最终URL
            session = requests.Session()
            # 设置超时时间，避免长时间等待
            response = session.get(auth_url, timeout=5, allow_redirects=True)
            # 获取最终重定向后的URL
            final_url = response.url
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 最终URL: {final_url}")
            # 检查最终URL是否包含认证成功的标识
            if "success.jsp" in final_url:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 网络已认证，认证成功")
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 下次检测将在 {self.check_interval} 秒后进行")
                return True
            # 检查最终URL是否包含未认证的标识
            elif "logout.jsp" in final_url:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 未认证，需要登录")
                return False
            # 其他情况也视为未认证
            else:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 未识别的URL模式: {final_url}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 网络连接检查失败: {e}")
            # 网络连接错误时，也需要尝试认证
            return False
    
    def setup_driver(self):
        # 设置Edge浏览器选项
        edge_options = Options()
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--window-size=1920,1080")
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--log-level=3")
        edge_options.add_argument("--disable-extensions")
        edge_options.add_argument("--no-sandbox")
        
        # 初始化Edge驱动
        self.driver = webdriver.Edge(options=edge_options)
    
    def login(self):
        try:
            # 打开认证页面
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 正在打开认证页面...")
            self.driver.get("http://172.21.2.10:8080/")
            
            # 等待页面加载
            time.sleep(2)
            
            # 1. 填写账号
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 填写账号...")
            self.driver.execute_script(f"""
                var username_tip = document.getElementById('username_tip');
                if(username_tip) username_tip.click();
                var username_input = document.getElementById('username');
                if(username_input) {{ 
                    username_input.value = '{self.username}';
                    username_input.dispatchEvent(new Event('input'));
                    username_input.dispatchEvent(new Event('change'));
                }}
            """)
            
            # 2. 填写密码
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 填写密码...")
            self.driver.execute_script(f"""
                var pwd_tip = document.getElementById('pwd_tip');
                if(pwd_tip) pwd_tip.click();
                var pwd_input = document.getElementById('pwd');
                if(pwd_input) {{ 
                    pwd_input.value = '{self.password}';
                    pwd_input.dispatchEvent(new Event('input'));
                    pwd_input.dispatchEvent(new Event('change'));
                }}
            """)
            
            # 3. 选择运营商
            if self.operator in self.operator_map:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 选择运营商：{self.operator}")
                service_name, service_show_name, service_code = self.operator_map[self.operator]
                
                # 调用页面自带的selectService函数选择运营商
                self.driver.execute_script(f"""
                    if(typeof selectService === 'function') {{ 
                        selectService('{service_name}','{service_show_name}','{service_code}');
                    }}
                """)
            # 等待页面加载
            time.sleep(2)

            # 4. 点击登录按钮
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 点击登录按钮...")
            self.driver.execute_script("""
                var loginLink = document.getElementById('loginLink');
                if(loginLink) {
                    loginLink.click();
                }
            """)
            
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 登录操作已完成")
            
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 登录过程中发生错误：{e}")
            traceback.print_exc()
    
    def close(self):
        # 关闭浏览器
        if self.driver:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 关闭浏览器...")
            self.driver.quit()
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 浏览器已关闭")

    def start_monitoring(self):
        """
        开始无限循环监控网络认证状态
        """
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始监控网络认证状态...")
        
        try:
            while True:
                # 检查认证状态
                if not self.is_connected():
                    # 需要认证，设置浏览器驱动
                    self.setup_driver()
                    # 执行登录操作
                    self.login()
                    # 等待一段时间后关闭浏览器
                    time.sleep(3)
                    self.close()
                
                # 等待指定的检查间隔
                time.sleep(self.check_interval)
                    
        except KeyboardInterrupt:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 检测到Ctrl+C，退出监控...")
        finally:
            # 确保浏览器关闭
            self.close()
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 监控已停止")

if __name__ == "__main__":
    # 替换为你自己的账号和密码
    username = "#"
    password = '#'
    operator = "#" # 中国联通，中国电信，中国移动，校园网。
    check_interval = 5 # 检查间隔，单位为秒
    
    # 修复条件判断逻辑，任何一个字段为空就提示输入
    if username == "" or password == "" or operator == "":
        print("请输入账号、密码和运营商")
        exit(1)
    
    try:
        # 初始化WiFi自动连接工具
        wifi = WiFiAutoConnect(username, password, operator, check_interval)
        
        # 开始无限循环监控
        wifi.start_monitoring()
        
    except Exception as e:
        print(f"程序运行出错: {e}")
        traceback.print_exc()