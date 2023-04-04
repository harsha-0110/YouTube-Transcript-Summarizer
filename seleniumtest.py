import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestWebpage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000")

    def test_input_form(self):
        link_input = self.driver.find_element(By.ID, "link")
        link_input.send_keys("https://www.youtube.com/watch?v=k3apQQXbB-0&list=PLbRMhDVUMngcywxqfVOD9J9VVPn8m4NA2&index=2")

        submit_button = self.driver.find_element(By.ID, "submit")
        submit_button.click()

        s1_textarea = self.driver.find_element(By.ID, "s1")
        self.assertNotEqual("{{value}}", s1_textarea.get_attribute("value"))
        print("Test Passed!")
    def tearDown(self):
        try:
            self.driver.quit()
            print("Browser closed.")
        except:
            pass

if __name__ == "__main__":
    unittest.main()