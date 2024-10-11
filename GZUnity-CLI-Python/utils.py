from urllib.parse import quote

from service import Service


def get_check_code(service: Service):
    image = service.session.get(url=Service.domain + 'CheckCode.aspx', headers=Service.header).content
    with open(file='CheckCode.gif', mode='wb') as gif:
        gif.write(image)


def login(username:str, password: str, check_code: str, service: Service) -> int:
    service.username = username
    identity = quote('学生'.encode('gb2312'))
    payload = {
        '__VIEWSTATE': 'dDwtMTM0OTIyMDA2Nzs7PtbBxqaOIxH5Z3YbOnI0ATitlwnR',
        'txtUserName': f'{service.username}',
        'TextBox2': f'{password}',
        'txtSecretCode': f'{check_code}',
        'RadioButtonList1': f'{identity}',
        'Button1': '',
        'lbLanguage': '',
        'hidPdrs': '',
        'hidsc': '',
    }
    response = service.session.post(url=Service.domain + 'default2.aspx', data=payload, headers=service.header)
    state_code = {'验证码不正确！！': 1, '验证码不能为空，如看不清请刷新！！': 2, '用户名或密码不正确！！': 3}
    try:
        state = response.text.split("alert('")[1].split("'")[0]
        return state_code[state]
    except IndexError:
        service.sessionState = 1
        return 0


def get_name(service: Service) -> str:
    response = service.session.get(url=Service.domain + 'xs_main.aspx', params={'xh': service.username},
                                   headers=Service.header)
    return response.text.split('<span id="xhxm">')[1].split('同学')[0]

def get_score(service: Service) -> list:
    pass