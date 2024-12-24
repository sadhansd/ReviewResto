from streamlit.testing.v1 import AppTest

def test_title():
    at = AppTest.from_file('src/main.py').run()
    assert at.title[0].value == 'ReviewResto'