import requests


class Service:
    domain = 'https://jw.gzu.edu.cn/'
    header = {'User-Agent': ''}

    def __init__(self):
        self.session = requests.session()
        self.session.get(url=Service.domain, headers={'User-Agent': ''})
        self.sessionID = self.session.cookies.get('ASP.NET_SessionId')
        self.sessionState = False
        self.username = None

    def check_state(self) -> bool:
        response = self.session.get(url=Service.domain + 'xs_main.aspx', params={'xh': self.username},
                                    headers=Service.header)
        title = response.text.split('<title>')[1].split('<')[0]
        state_code = {'欢迎使用正方教务管理系统！请登录': False, '正方教务管理系统': True}
        self.sessionState = state_code[title]
        return state_code[title]

