"""
作者声明：
        本软件仅适用于南京理工大学紫金学院的校园网认证。
        本脚本仅用于学习和研究，不用于任何商业用途。
        作者不承担因使用本脚本而导致的任何损失或责任。
        请勿联系作者索要破解校园网的思路，也请勿使用本脚本进行任何形式的攻击或滥用。
"""
import requests
import time
USERNAME = '#'#你的身份证号
PASSWORD = '#'#你的密码
CAPTIVE_SERVER = r'http://connect.rom.miui.com/generate_204'#小米接入商的认证服务器
CHECK_INTERVAL = 300  # 检测间隔时间，单位：秒（这里设为5分钟）
SERVICE = r'%25E8%2581%2594%25E9%2580%259A'#你的互联网接入商，从下方注释挑选
'''
中国联通：%25E8%2581%2594%25E9%2580%259A
中国移动：%25E7%25A7%25BB%25E5%258A%25A8
中国电信：%25E7%2594%25B5%25E4%25BF%25A1
'''


def get_captive_server_response():
    return requests.get(CAPTIVE_SERVER)

def login(response):
    response_text = response.text
    login_page_url = response_text.split('\'')[1]
    login_url = login_page_url.split('?')[0].replace('index.jsp', 'InterFace.do?method=login')
    query_string = login_page_url.split('?')[1]
    query_string = query_string.replace('&', '%2526')
    query_string = query_string.replace('=', '%253D')
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0'
    }
    login_post_data = 'userId={}&password={}&service={}&queryString={}&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false'.format(
        USERNAME, PASSWORD, SERVICE, query_string)
    login_result = requests.post(
        url=login_url,
        data=login_post_data,
        headers=headers
    )


def check_connection():
    """检查网络连接状态"""
    try:
        response = get_captive_server_response()
        if response.status_code == 204:
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] 网络连接正常，无需认证')
            return True
        else:
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] 需要进行认证...')
            login(response)
            response = get_captive_server_response()
            if response.status_code == 204:
                print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] 认证成功')
                return True
            else:
                print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] 认证失败，状态码: {response.status_code}')
                return False
    except Exception as e:
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] 检查连接时发生错误: {e}')
        return False


if __name__ == '__main__':
    print(f'锐捷认证守护程序已启动，将每{CHECK_INTERVAL}秒检查一次网络连接...')
    
    # 初始检查
    check_connection()
    # 无限循环定时检测
    while True:
        time.sleep(CHECK_INTERVAL)
        check_connection()
