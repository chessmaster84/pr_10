import csv
import requests

class StudentDataProcessor:
    def __init__(self):
        self.file_url = 'https://informer.com.ua/dut/python/pr_10/pd24.csv'
        self.processed_data = []
        self.fetch_data()
        self.process_data()

    def fetch_data(self):
        response = requests.get(self.file_url)
        response.encoding = 'utf-8'
        lines = response.text.splitlines()
        reader = csv.reader(lines)
        self.raw_data = list(reader)

    def process_data(self):

        headers = self.raw_data[0]
        task_indices = [i for i, h in enumerate(headers) if "Завдання:" in h]

        for row in self.raw_data[1:]:
            for idx in task_indices:

                student_code = self.transliterate(row[1].lower())
                task_id = idx - task_indices[0] + 1  # Starting id from 1
                grade = row[idx]
                if grade == '-':
                    grade = '0.00'  # Default grade if missing

                self.processed_data.append({
                    'name': f"{row[0]} {row[1]}",
                    'student_code': student_code,
                    'task_id': task_id,
                    'grade': grade
                })

    def list_students(self):
        """ Returns a list of unique student full names with their codes. """
        unique_students = {}
        for item in self.processed_data:
            key = (item['name'], item['student_code'])
            if key not in unique_students:
                unique_students[key] = {'name': item['name'], 'student_code': item['student_code']}
        return list(unique_students.values())

    def count_tasks(self):
        """ Returns the number of unique tasks (assignments). """
        return len(set(item['task_id'] for item in self.processed_data))

    def get_student_data(self, code):
        """ Returns all task data for a student given their student code. """
        return [item for item in self.processed_data if item['student_code'] == code]

    def get_task_data(self, number):
        """ Returns all task data for a student given their student code. """
        return [item for item in self.processed_data if item['task_id'] == int(number)]

    def transliterate(self, word):
        TRANSLIT_DICT = {
            'А': 'A', 'а': 'a',
            'Б': 'B', 'б': 'b',
            'В': 'V', 'в': 'v',
            'Г': 'H', 'г': 'h',
            'Ґ': 'G', 'ґ': 'g',
            'Д': 'D', 'д': 'd',
            'Е': 'E', 'е': 'e',
            'Є': 'Ye', 'є': 'ie',
            'Ж': 'Zh', 'ж': 'zh',
            'З': 'Z', 'з': 'z',
            'И': 'Y', 'и': 'y',
            'І': 'I', 'і': 'i',
            'Ї': 'Yi', 'ї': 'i',
            'Й': 'Y', 'й': 'i',
            'К': 'K', 'к': 'k',
            'Л': 'L', 'л': 'l',
            'М': 'M', 'м': 'm',
            'Н': 'N', 'н': 'n',
            'О': 'O', 'о': 'o',
            'П': 'P', 'п': 'p',
            'Р': 'R', 'р': 'r',
            'С': 'S', 'с': 's',
            'Т': 'T', 'т': 't',
            'У': 'U', 'у': 'u',
            'Ф': 'F', 'ф': 'f',
            'Х': 'Kh', 'х': 'kh',
            'Ц': 'Ts', 'ц': 'ts',
            'Ч': 'Ch', 'ч': 'ch',
            'Ш': 'Sh', 'ш': 'sh',
            'Щ': 'Shch', 'щ': 'shch',
            'Ю': 'Yu', 'ю': 'iu',
            'Я': 'Ya', 'я': 'ia',
            'ь': '', '’': '',
            '’': "'", 'ґ': 'g'
        }
        return ''.join(TRANSLIT_DICT.get(char, char) for char in word)

if __name__ == '__main__':
    # Припустимо, що URL файлу заданий наступним чином:
    processor = StudentDataProcessor()

    print(processor.get_task_data(2))
    print(processor.list_students())
    print(processor.count_tasks())
    #print(processor.get_student_data('barcenko'))