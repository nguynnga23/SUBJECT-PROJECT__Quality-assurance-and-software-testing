import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Tasks', result.data)

    def test_add_task(self):
        result = self.app.get('/addTask?task=TestTask')
        self.assertEqual(result.status_code, 302)

    def test_get_tasks(self):
        result = self.app.get('/getTasks')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Tasks', result.data)

    def test_edit_task(self):
        result = self.app.get('/editTask/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Edit Task', result.data)

    def test_update_task(self):
        result = self.app.post('/updateTask', data=dict(task_id=1, task='UpdatedTask'))
        self.assertEqual(result.status_code, 302)

    def test_move_to_done(self):
        result = self.app.post('/move-to-done/1/TestTask')
        self.assertEqual(result.status_code, 302)

    def test_delete_task(self):
        result = self.app.post('/deleteTask/1')
        self.assertEqual(result.status_code, 302)

    def test_delete_completed_task(self):
        result = self.app.post('/delete-completed/1')
        self.assertEqual(result.status_code, 302)

    def test_home_content(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Todo Tasks', result.data)
        self.assertIn(b'Tasks Completed', result.data)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(FlaskTestCase))


# PS C:\Users\Da Nguym\Desktop\SUBJECT-PROJECT__Quality-assurance-and-software-testing> python -m unittest tests.test_unit  
# .........
# ----------------------------------------------------------------------
# Ran 9 tests in 0.055s

# OK
# PS C:\Users\Da Nguym\Desktop\SUBJECT-PROJECT__Quality-assurance-and-software-testing> 