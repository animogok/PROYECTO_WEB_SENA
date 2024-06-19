from django.test import Client, TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from .models import User_registrations
'''

#This part will be in charge of doing unit testing of the views.py classes

class RegisterTest_1(TestCase):
        
    # SUB TEST NUMBER 1
    #This test it is to ensure the HTTP_200_ok status code reffering to the correct load of the form
    def testGetForm(self):
        client = Client()
        response = client.get("/sign-in/")
        self.assertEqual(response.status_code, 200)
        
    # SUB TEST NUMBER 2
    #This test it is to ensure the HTTP_302 status code reffering to the correct commit data from the request in the post form
    def testPostRegisterForm(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post("/sign-in/", {"firsName" : "Sebastian1", "lastName": "Avendano1", "email": "sebastian1@gmail.com", "idNumber": "1111111", "password":"12345678"})
        self.assertEqual(response.status_code, 302)
    
    #SUB TEST NUMBER 3
    #This test it's for ensuring the csrf token in the cookies of the client
    def testCSRFToken(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get("/sign-in/")
        self.assertEqual(response.status_code, 200)
        

#This part will be in charge of doing unit testing reffering to the login

class LoginTest_1(TestCase):
    
    # Make the instance of the User_registrations model class for doing the correct use of the login class in the views.py archive
    @classmethod
    def setUpTestData(cls):
        cls.user = User_registrations.objects.create(firsName="Sebastian1", lastName= "Avendano1", email= "sebastian1@gmail.com", idNumber = "1111111", password = "12345678")
        cls.user.set_password("12345678")
    
    
    # SUB TEST NUMBER 1
    #This test it is for ensuring the correct load of the static files on the page
    def testGetForm(self):
        client = Client()
        response = client.get("/login-app/")
        self.assertEqual(response.status_code, 200)
    
    
    # SUB TEST NUMBER 2
    #This test it is for ensuring the functionality of the login, this will work cheking the password
    def testPostLoginForm_1(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post("/login-app/", {"email": "sebastian1@gmail.com", "password": "12345678"})
        self.assertEqual(self.user.check_password("12345678"), True)
        
    #SUB TEST NUMBER 3
    #This test it's for working with the status code 401
    def testPostLoginForm_3(self):
        client = Client()
        raw_password = "123456789"
        response = client.post("/login-app/", {"email": "sebastian1@gmail.com", "password": raw_password})
        self.assertEqual(response.status_code, 200)
    
    
    #SUB TEST NUMBER 4
    #This test it's for ensuring the csrf token in the cookies of the client
    def testCSRFToken(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get("/login-app/")
        self.assertEqual(response.status_code, 200)
           
#This part will be in charge of doing unit testing reffering to the login required decorator referring to enforcing the user to Register or Login into the app 
#for getting access to the whole application


class Account_SettingsTest(TestCase):
    # Make the instance of the User_registrations model class for doing the correct use of the login class in the views.py archive
    @classmethod
    def setUpTestData(cls):
        cls.user = User_registrations.objects.create(firsName="Sebastian1", lastName= "Avendano1", email= "sebastian1@gmail.com", idNumber = "1111111", password = "12345678")
        cls.user.set_password("12345678")
    
    # TEST NUMBER 1
    #This test will be ensuring to us the correct implementation of the "@login_required" decorator, meaning the temporal redirect to "login-app" which it's the status code 302
    def testGet_1(self):
        client = Client()
        response = client.get("/account-settings/")
        self.assertEqual(response.status_code, 302)
    
    
    # TEST NUMBER 2
    #This test will be ensuring to us the access to the page "account login" when the user it's authenticated via login
    #If the session key exists, then it will be loaded with the html
    def testGet_2(self):
        client = Client()
        client.force_login(self.user)
        response = client.session.exists(client.session.session_key)
        self.assertEqual(response, True)

'''
#AUTOMATIC TESTS WITH SELENIUM
class LoginTest_2(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        return super().tearDownClass()
        
    def test_login(self):
        self.selenium.get(f"{self.live_server_url}/login-app/")
        username_input = self.selenium.find_element(By.NAME,"email")
        password_input = self.selenium.find_element(By.NAME,"password")
        
        password_input.send_keys("123456789")
        username_input.send_keys("sebastian1@gmail.com")
        self.selenium.find_element(By.CLASS_NAME,"submit").click()
        
        self.assertIn("/", self.selenium.current_url)
        
class RegisterTest_2(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        return super().tearDownClass()
    
    def test_register(self):
        self.selenium.get(f"{self.live_server_url}/sign-in/")
        
        firstName_input = self.selenium.find_element(By.NAME,"firsName")
        lastName_input = self.selenium.find_element(By.NAME, "lastName")
        email_input = self.selenium.find_element(By.NAME, "email")
        idNumber_input = self.selenium.find_element(By.NAME, "idNumber")
        password_input = self.selenium.find_element(By.NAME, "password")
        
        firstName_input.send_keys("Sebastian1")
        lastName_input.send_keys("Avendano1")
        email_input.send_keys("sebastian1@gmail.com")
        idNumber_input.send_keys("1111111")
        password_input.send_keys("12345678")
        self.selenium.find_element(By.CLASS_NAME,"submit").click()
        
        self.assertIn("/login-app", self.selenium.current_url)
        
        from .models import User_registrations
        self.assertTrue(User_registrations.objects.filter(email = "sebastian1@gmail.com").exists())   

class AuthenticateUser_decorator(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        return super().tearDownClass()
    
    def test_listbookinf(self):
        self.selenium.get(f"{self.live_server_url}/list-booking/")
        self.assertIn(f"{self.live_server_url}/login-app/?next=/list-booking/", self.selenium.current_url)
        
    def test_menu(self):
        self.selenium.get(f"{self.live_server_url}/menu-restaurant/")
        self.assertIn(f"{self.live_server_url}/login-app/?next=/menu-restaurant/", self.selenium.current_url)
        
    def test_account(self):
        self.selenium.get(f"{self.live_server_url}/account-settings/")
        self.assertIn(f"{self.live_server_url}/login-app/?next=/account-settings/", self.selenium.current_url)

class ObjectExistenceTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        return super().tearDownClass()
    
    def test_generalHome(self):
        self.selenium.get(f"{self.live_server_url}")
        self.assertTrue(self.selenium.find_element(By.NAME, "home").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "menu").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "booking").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "login").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "signUp").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "signUp").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "homeImage").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "QualityInfoImage").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "RecomendationImage").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "footer").is_displayed)
        
    def test_generalLogin(self):
        self.selenium.get(f"{self.live_server_url}/login-app/")
        self.assertTrue(self.selenium.find_element(By.NAME, "email").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "password").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "form").is_displayed)
        
    def test_generalRegister(self):
        self.selenium.get(f"{self.live_server_url}/sign-in/")
        self.assertTrue(self.selenium.find_element(By.NAME,"firsName").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "lastName").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "email").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "idNumber").is_displayed)
        self.assertTrue(self.selenium.find_element(By.NAME, "password").is_displayed)
