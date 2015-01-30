from selenium import webdriver

browser = webdriver.Firefox()

# Edith has heard about a cool CMS. She goes to check out its homepage.
browser.get('http://localhost:8000')

# She notices the page title and header mention login page.
assert 'Login' in browser.title

# She types "1" into "ユーザーID" box.

# She types "a" into "パスワード" box.

# She clicks "Connection" button.

# She notices the page title and header mention account list page.

# Satisfied, she goes back to sleep.
browser.quit()
