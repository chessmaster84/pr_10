from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from grades.utils.StudentDataProcessor import StudentDataProcessor

processor = StudentDataProcessor()
students = processor.list_students()

def html_home():
    return """
    <br><hr><br>
    <a href='/students/'>Список студентів</a><br>
    <a href='/tests/'>Список самостійних</a>
    <br><br><br>
    """

def index(request):
    html_content = "<h1>Головна сторінка</h1>" + html_home()
    return HttpResponse(html_content)

def html_list_studends():
    html_content = '<table border="1">'
    html_content += '<tr><th>ПІБ</th><th>Профіль</th></tr>'

    for student in students:
        print(students)
        profile_url = f"/students/{student['student_code']}/"
        html_content += f"<tr><td>{student['name']}</td><td><a href='{profile_url}'>Профіль</a></td></tr>"

    html_content += '</table>'
    return html_content

def students_list(request):
    return HttpResponse(html_list_studends())

def student_details(request, student_code):
    grades = processor.get_student_data(student_code)
    # Знаходимо студента за кодом
    student = next((s for s in students if s['student_code'] == student_code), None)
    if not student:
        return HttpResponse("Студент не знайдений", status=404)

    html_content = f"<h1>{student['name']}</h1>"
    html_content += f"<p>Код студента: {student_code}</p>"

    html_content += "<table border='1'>"
    html_content += "<tr><th>Завдання</th><th>Оцінка</th></tr>"

    total_score = 0.0  # Змінна для підрахунку загальної суми балів
    for grade in grades:
        html_content += f"<tr><td>Завдання {grade['task_id']}</td><td>{grade['grade']}</td></tr>"
        total_score += float(grade['grade'])  # Додаємо бал до загальної суми

    average_score = total_score / len(grades) if grades else 0  # Обраховуємо середній бал
    html_content += f"<tr><td><strong>Загальний бал</strong></td><td>{total_score:.2f}</td></tr>"
    html_content += f"<tr><td><strong>Середній бал</strong></td><td>{average_score:.2f}</td></tr>"
    html_content += "</table>"

    html_content += ""+ html_home() + "<a href='/'>Головна сторінка</a>"

    return HttpResponse(html_content)

def tests_list(request):
    num_tasks = processor.count_tasks()

    html_content = '<h1>Список Самостійних Робіт</h1>'
    html_content += '<ul>'
    for i in range(1, num_tasks + 1):
        html_content += f'<li><a href="/tests/{i}/">Самостійна Робота №{i}</a></li>'
    html_content += '</ul>'

    return HttpResponse(html_content + html_home())


def test_details(request, task_id):

    # Отримання даних для конкретної самостійної роботи
    task_data = processor.get_task_data(int(task_id))

    # Створення HTML таблиці
    html_content = f"<h1>Деталі Самостійної Роботи №{task_id}</h1>"
    html_content += "<table border='1'><tr><th>Ім'я</th><th>Код Студента</th><th>Оцінка</th></tr>"

    for item in task_data:
        html_content += f"<tr><td>{item['name']}</td><td>{item['student_code']}</td><td>{item['grade']}</td></tr>"

    html_content += "</table>"

    return HttpResponse(html_content)
