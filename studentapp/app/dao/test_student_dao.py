from app.dao.student_dao import StudentDAO

def test_get_student_by_name():
    dao = StudentDAO()
    dao.add_student(id=1, name="John", age=17, class_="year 12")
    dao.add_student(id=2, name="Jane", age=18, class_="year 13")
    
    # Test case 1: Get student by name
    result = dao.get_student_by_name("John")
    assert len(result) == 1
    assert result[0].name == "John"
    
    # Test case 2: Get student by name (multiple students with the same name)
    result = dao.get_student_by_name("Jane")
    assert len(result) == 1
    assert result[0].name == "Jane"
    
    # Test case 3: Get student by name (no matching students)
    try:
        dao.get_student_by_name("Alice")
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Student not found"