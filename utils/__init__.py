from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# create service and install chrome driver
service: Service = Service(ChromeDriverManager().install())

# create Chrome webdriver
browser: webdriver = webdriver.Chrome(service=service)
