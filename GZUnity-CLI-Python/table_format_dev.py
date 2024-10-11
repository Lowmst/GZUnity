from lxml import etree


def form_table(html: str):
    elements = etree.HTML(html)
    table = []
    for course_index in range(5):
        table.append([])
        for weekday_index in range(7):
            if course_index % 2 == 0:
                weekday_index += 1
            table[course_index].append(
                elements.xpath(f'//table[@id="Table1"]/tr[{(2 * course_index) + 3}]/td[{weekday_index + 2}]/text()'))
    return table


with open('response.html', mode='r') as response:
    table = form_table(response.read())
    for row in table:
        for element in row:
            print(element, end=" ")
        print('\n')
