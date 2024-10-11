from urllib.parse import quote
from lxml import etree
from service import Service
from utils import get_name


class CourseTable:
    module_code = 'N121603'

    def __init__(self, service: Service):
        self.name = get_name(service)
        response = service.session.get(url=Service.domain + 'xskbcx.aspx',
                                       params={'xh': service.username, 'xm': quote(self.name.encode('gb2312')),
                                               'gnmkdm': CourseTable.module_code},
                                       headers={**Service.header,
                                                'Referer': Service.domain + f'xs_main.aspx?xh={service.username}'})
        html = etree.HTML(response.text)
        self.viewstate: str = html.xpath('//input[@name="__VIEWSTATE"]/@value')[0]
        self.current_year: str = html.xpath('//select[@name="xnd"]/option[@selected]/text()')[0]
        self.current_semester: str = html.xpath('//select[@name="xqd"]/option[@selected]/text()')[0]
        self.available_years: list = html.xpath('//select[@name="xnd"]/option/text()')
        self.available_semesters: list = html.xpath('//select[@name="xqd"]/option/text()')
        self.current_table = format_table(html=response.text)

    def get(self, service: Service, year: str = None, semester: str = None):
        if year is None:
            year = self.current_year
        if semester is None:
            semester = self.current_semester
        if (year not in self.available_years) or (semester not in self.available_semesters):
            return 0
        if (year == self.current_year) and (semester == self.current_semester):
            return self.current_table
        response = service.session.post(url=Service.domain + 'xskbcx.aspx',
                                        data={'__VIEWSTATE': self.viewstate, 'xnd': year, 'xqd': semester},
                                        params={'xh': service.username, 'xm': quote(self.name.encode('gb2312')),
                                                'gnmkdm': CourseTable.module_code},
                                        headers={**Service.header,
                                                 'Referer': Service.domain + f'xs_main.aspx?xh={service.username}'})
        return format_table(html=response.text)


def format_table(html: str) -> list:
    elements = etree.HTML(html)
    data = []
    for course_index in range(5):
        data.append([])
        for weekday_index in range(7):
            if course_index % 2 == 0:
                weekday_index += 1
            data[course_index].append(
                elements.xpath(
                    f'//table[@id="Table1"]/tr[{(2 * course_index) + 3}]/td[{weekday_index + 2}]/text()'))
    return data
