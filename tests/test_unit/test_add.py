import unittest
import csv
from app import app


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.test_data = self.load_test_data(
            r'D:\Nga\Nam4\Ki1_Nam4\dam-bao-chat-luong-va-kiem-thu-phan-mem\TEAMWORK\management-components-of-software-quality\todo-app\tests\test_unit\data\test_unit.csv')

    def tearDown(self):
        pass

    def load_test_data(self, file_name):
        data = []
        with open(file_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data

    def test_add_task(self):
        for task in self.test_data:
            result = self.app.get(f"/addTask?task={task['task']}")
            self.assertEqual(result.status_code, 302)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(FlaskTestCase))
