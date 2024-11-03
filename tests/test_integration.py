import pytest
from flask import Flask
from app import app  #import the app from app.py
import sqlite3
import os

@pytest.fixture  # fixture duoc su dung de tao ra mot doi tuong hoac mot gia tri cho kiem thu
def client():
    app.config['TESTING'] = True  # Bật chế độ kiểm thử
    with app.test_client() as client: # Tạo một ứng dụng khách hàng để kiểm thử
        yield client # Trả về ứng dụng khách hàng cho kiểm thử

@pytest.fixture  # Fixture sẽ được sử dụng để thiết lập một môi trường cho các bài kiểm tra
def init_db():
    # Khởi tạo cơ sở dữ liệu tạm thời cho kiểm thử
    conn = sqlite3.connect('todo.db')  # Sử dụng một cơ sở dữ liệu tạm
    cursor = conn.cursor()  # Cho phép bạn thực hiện các câu lệnh SQL trên cơ sở dữ liệu mà bạn đã kết nối.
    # Xóa bảng nếu nó đã tồn tại
    cursor.execute('DROP TABLE IF EXISTS tasks')
    cursor.execute('DROP TABLE IF EXISTS done')
    # Tạo lại bảng
    cursor.execute('CREATE TABLE tasks (tid INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)')
    cursor.execute('CREATE TABLE done (did INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, task_id INTEGER)')
    conn.commit()
    yield conn  # Trả về kết nối cơ sở dữ liệu cho kiểm thử
    conn.close()  # Đóng kết nối sau khi kiểm thử hoàn tất

#---------------------------------Kiểm thử unit bằng pytest---------------------------------#
def test_add_task(client, init_db):
    response = client.get('/addTask?task=Test%20Task') 
    assert response.status_code == 302  # Kiểm tra xem có chuyển hướng sau khi thêm nhiệm vụ
    # Kiểm tra nếu nhiệm vụ đã được thêm
    cursor = init_db.cursor()  #kết nối cơ sở dữ liệu init_db để thực hiện các truy vấn SQL.
    cursor.execute("SELECT * FROM tasks WHERE task='Test Task'") # tìm nhiệm vụ vừa thêm vào cơ sở dữ liệu.
    task = cursor.fetchone() #Nếu tìm thấy nhiệm vụ, biến task sẽ chứa thông tin về nhiệm vụ đó; nếu không, nó sẽ là None.
    assert task is not None  #Kiểm tra xem nhiệm vụ đã được thêm vào cơ sở dữ liệu chưa

def test_edit_task(client, init_db):
    cursor = init_db.cursor()
    cursor.execute("INSERT INTO tasks(task) VALUES('TASK_TEST_EDIT')")
    init_db.commit()
    task_id = cursor.lastrowid
    # Gọi đến hàm edit_task
    response = client.get(f'/editTask/{task_id}')
    # Kiểm tra mã trạng thái phản hồi
    assert response.status_code == 200 
    # Kiểm tra nội dung của phản hồi
    assert b'TASK_TEST_EDIT' in response.data  # Kiểm tra xem nội dung 'TASK_TEST_EDIT có trong phản hồi không

def test_update_task(client, init_db):
    cursor = init_db.cursor()
    cursor.execute("INSERT INTO tasks(task) VALUES('Old_Task_Unit_Test')")
    init_db.commit()
    task_id = cursor.lastrowid # Lấy id của nhiệm vụ vừa thêm vào cơ sở dữ liệu
    response = client.post('/updateTask', data={'task_id': task_id, 'task': 'Updated_Task_Unit_Test'})
    assert response.status_code == 302  # Kiểm tra xem có chuyển hướng sau khi cập nhật nhiệm vụ
    cursor.execute("SELECT * FROM tasks WHERE tid=?", (task_id,))
    updated_task = cursor.fetchone()
    assert updated_task[1] == 'Updated_Task_Unit_Test'  # Kiểm tra nếu nhiệm vụ đã được cập nhật

def test_move_to_done(client, init_db):
    cursor = init_db.cursor()
    cursor.execute("INSERT INTO tasks(task) VALUES('Task to Move')")
    init_db.commit()
    task_id = cursor.lastrowid
    response = client.post(f'/move-to-done/{task_id}/Task to Move')
    assert response.status_code == 302  # Kiểm tra xem có chuyển hướng sau khi chuyển nhiệm vụ
    cursor.execute("SELECT * FROM done WHERE task_id=?", (task_id,))
    done_task = cursor.fetchone()
    assert done_task is not None  # Kiểm tra nếu nhiệm vụ đã được chuyển đến danh sách hoàn thành

def test_delete_task(client, init_db):
    cursor = init_db.cursor()
    cursor.execute("INSERT INTO tasks(task) VALUES('TASK_TEST_DELETE')")
    init_db.commit()
    task_id = cursor.lastrowid
    response = client.post(f'/deleteTask/{task_id}')
    assert response.status_code == 302  # Kiểm tra xem có chuyển hướng sau khi xóa nhiệm vụ
    cursor.execute("SELECT * FROM tasks WHERE tid=?", (task_id,))
    deleted_task = cursor.fetchone()
    assert deleted_task is None  # Kiểm tra nếu nhiệm vụ đã bị xóa

def test_delete_completed_task(client, init_db):
    cursor = init_db.cursor()
    cursor.execute("INSERT INTO done(task, task_id) VALUES('COMPLETED_TASK_TEST', 1)")
    init_db.commit()
    completed_task_id = cursor.lastrowid
    #Gọi hàm để test
    response = client.post(f'/delete-completed/{completed_task_id}')
    assert response.status_code == 302  # Kiểm tra xem có chuyển hướng không
    
    # Bước 4: Kiểm tra rằng nhiệm vụ đã bị xóa khỏi bảng done
    cursor.execute("SELECT * FROM done WHERE did=?", (completed_task_id,))
    completed_task = cursor.fetchone() 
    assert completed_task is None  # Kiểm tra xem nhiệm vụ có tồn tại không, nó phải là None
#---------------------------------Kiểm thử unit bằng pytest-------------------------------------#


#---------------------------------Kiểm thử tích hợp bằng pytest---------------------------------#
def test_edit_and_update_task(client, init_db):
    # Bước 1: Thêm một nhiệm vụ vào cơ sở dữ liệu để có nhiệm vụ để chỉnh sửa
    cursor = init_db.cursor()
    cursor.execute("INSERT INTO tasks(task) VALUES('Old Task')")
    init_db.commit()
    task_id = cursor.lastrowid  # Lấy ID của nhiệm vụ vừa thêm

    # Bước 2: Gửi yêu cầu GET đến đường dẫn /editTask với ID của nhiệm vụ (giống gọi hàm edit_task)
    response = client.get(f'/editTask/{task_id}')
    assert response.status_code == 200  # Kiểm tra xem yêu cầu có thành công không
    assert b'Old Task' in response.data  # Kiểm tra xem nội dung trang có chứa nhiệm vụ cũ không

    # Bước 3: Gửi yêu cầu POST để cập nhật nhiệm vụ
    response = client.post('/updateTask', data={'task_id': task_id, 'task': 'Updated Task'})
    assert response.status_code == 302  # Kiểm tra xem có chuyển hướng sau khi cập nhật nhiệm vụ

    # Bước 4: Kiểm tra xem nhiệm vụ đã được cập nhật trong cơ sở dữ liệu chưa
    cursor.execute("SELECT * FROM tasks WHERE tid = ?", (task_id,))
    updated_task = cursor.fetchone() # Lấy kết quả
    assert updated_task[1] == 'Updated Task'  # Kiểm tra xem nhiệm vụ đã được cập nhật

def test_move_and_delete_completed_task(client, init_db):
    cursor = init_db.cursor()
    # Bước 1: Thêm một nhiệm vụ mới
    cursor.execute("INSERT INTO tasks(task) VALUES('Task to Move')")
    init_db.commit()
    task_id = cursor.lastrowid
    # Bước 2: Chuyển nhiệm vụ sang bảng done (gọi hàm move_to_done)
    response = client.post(f'/move-to-done/{task_id}/Task to Move')
    assert response.status_code == 302
    # Bước 3: Kiểm tra
    cursor.execute("SELECT * FROM done WHERE task_id=?", (task_id,))
    done_task = cursor.fetchone()
    assert done_task is not None  # Nhiệm vụ phải tồn tại trong bảng done
    # Bước 4: Xóa nhiệm vụ vừa hoàn thành (gọi hàm deleteCompletedTask)
    completed_task_id = done_task[0]  # Lấy ID của nhiệm vụ hoàn thành
    response = client.post(f'/delete-completed/{completed_task_id}')
    assert response.status_code == 302
    # Bước 5: Kiểm tra rằng nhiệm vụ đã bị xóa khỏi bảng done
    cursor.execute("SELECT * FROM done WHERE did=?", (completed_task_id,))
    completed_task = cursor.fetchone()
    assert completed_task is None  # Nhiệm vụ hoàn thành phải không còn tồn tại


def test_add_and_get_task(client, init_db):
    # Bước 1: Thêm một nhiệm vụ mới (gọi hàm add_task)
    response = client.get('/addTask?task=Test Task')
    assert response.status_code == 302
    cursor = init_db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE task='Test Task'")
    task = cursor.fetchone()
    assert task is not None
    # Bước 2: Kiểm tra xem nhiệm vụ vừa thêm có xuất hiện trong danh sách nhiệm vụ không
    response = client.get('/getTasks')
    assert b'Test Task' in response.data


def test_add_and_delete_task(client, init_db):
    response = client.get('/addTask?task=Test%20Task')
    assert response.status_code == 302 
    cursor = init_db.cursor() 
    cursor.execute("SELECT * FROM tasks WHERE task='Test Task'") 
    task = cursor.fetchone() 
    assert task is not None
    task_id = task[0] 
    response = client.post(f'/deleteTask/{task_id}')
    assert response.status_code == 302
    cursor.execute("SELECT * FROM tasks WHERE tid=?", (task_id,))
    deleted_task = cursor.fetchone()
    assert deleted_task is None 

def test_add_and_move_task_to_done(client, init_db):
    response = client.get('/addTask?task=Test%20Task')
    assert response.status_code == 302 
    cursor = init_db.cursor() 
    cursor.execute("SELECT * FROM tasks WHERE task='Test Task'") 
    task = cursor.fetchone()
    assert task is not None 
    task_id = task[0] 
    response = client.post(f'/move-to-done/{task_id}/Test Task')
    assert response.status_code == 302 
    cursor.execute("SELECT * FROM done WHERE task_id=?", (task_id,))
    done_task = cursor.fetchone()
    assert done_task is not None 

def test_add_edit_and_update_task(client, init_db):
    response = client.get('/addTask?task=Old%20Task')
    assert response.status_code == 302 

    cursor = init_db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE task='Old Task'") 
    task = cursor.fetchone() 
    assert task is not None 

    task_id = task[0] 
    response = client.get(f'/editTask/{task_id}')
    assert response.status_code == 200 
    assert b'Old Task' in response.data 

    response = client.post('/updateTask', data={'task_id': task_id, 'task': 'Updated Task'})
    assert response.status_code == 302 

    cursor.execute("SELECT * FROM tasks WHERE tid = ?", (task_id,))
    updated_task = cursor.fetchone()
    assert updated_task[1] == 'Updated Task' 

def test_add_edit_update_and_delete_task(client, init_db):
    response = client.get('/addTask?task=Old%20Task')
    assert response.status_code == 302 

    cursor = init_db.cursor() 
    cursor.execute("SELECT * FROM tasks WHERE task='Old Task'")
    task = cursor.fetchone()
    assert task is not None 

    task_id = task[0]
  
    response = client.get(f'/editTask/{task_id}')
    assert response.status_code == 200
    assert b'Old Task' in response.data 

    response = client.post('/updateTask', data={'task_id': task_id, 'task': 'Updated Task'})
    assert response.status_code == 302

    cursor.execute("SELECT * FROM tasks WHERE tid = ?", (task_id,))
    updated_task = cursor.fetchone() 
    assert updated_task[1] == 'Updated Task'

    response = client.post(f'/deleteTask/{task_id}')
    assert response.status_code == 302 

    cursor.execute("SELECT * FROM tasks WHERE tid=?", (task_id,))
    deleted_task = cursor.fetchone()
    assert deleted_task is None 
#---------------------------------Kiểm thử tích hợp bằng pytest---------------------------------#