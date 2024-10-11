import me
from utils import *
from service import Service
from coursetable import CourseTable

app = Service()

get_check_code(app)
CheckCode = input('验证码：')
print(login(username=me.ID, password=me.password, check_code=CheckCode, service=app))

table = CourseTable(app)
print(table.current_year)
print(table.current_semester)
print(table.available_years)
print(table.available_semesters)
print(table.get(service=app))
print(table.get(service=app, year='2024-2024', semester='1'))
