# # import requests
# # from bs4 import BeautifulSoup

# # # URL of the web page
# # url = 'https://www.screener.in/company/SBILIFE/'

# # # Send an HTTP GET request to the URL
# # response = requests.get(url)

# # # Get the HTML content from the response
# # html_content = response.text

# # # Create a BeautifulSoup object with the HTML content
# # soup = BeautifulSoup(html_content, 'html.parser')

# # # Find the section with id "cash-flow"
# # cash_flow_section = soup.find('section', id='cash-flow')

# # # Find the cash flow table within the section
# # table = cash_flow_section.find('table')

# # # Extract the table data
# # table_data = []

# # header_data=[]

# # for header in table.find_all('th'):
# #     header_data.append(header.text.strip())

# # for row in table.find_all('tr'):
# #     row_data = []
# #     for cell in row.find_all('td'):
# #         row_data.append(cell.text.strip())
# #     if row_data:
# #         table_data.append(row_data)

# # # Print the table data
# # print(header_data)
# # for row in table_data:
# #     print(row)

# # import requests
# # import matplotlib.pyplot as plt
# # from bs4 import BeautifulSoup

# # # URL of the web page
# # url = 'https://www.screener.in/company/SBILIFE/'

# # # Send an HTTP GET request to the URL
# # response = requests.get(url)

# # # Get the HTML content from the response
# # html_content = response.text

# # # Create a BeautifulSoup object with the HTML content
# # soup = BeautifulSoup(html_content, 'html.parser')

# # # Find the section with id "cash-flow"
# # cash_flow_section = soup.find('section', id='cash-flow')

# # # Find the cash flow table within the section
# # table = cash_flow_section.find('table')

# # header_data=[]
# # for header in table.find_all('th'):
# #     header_data.append(header.text.strip())

# # # Extract the table data
# # table_data = []
# # for row in table.find_all('tr'):
# #     row_data = []
# #     for cell in row.find_all('td'):
# #         row_data.append(cell.text.strip())
# #     if row_data:
# #         table_data.append(row_data)

# # # Extract the years from the first column
# # years = header_data[1:]
# # print(years)

# # # Extract the cash flow values for plotting
# # cash_flow_values = []
# # for row in table_data[1:]:
# #     cash_flow_values.append(row[1:])

# # # Create the plot
# # plt.figure(figsize=(10, 6))
# # for i, row in enumerate(cash_flow_values):
# #     plt.plot(years, row, label=f'Row {i+1}')
# # plt.xlabel('Years')
# # plt.ylabel('Cash Flow')
# # plt.title('Cash Flow over the Years')
# # plt.legend()
# # plt.show()


# import requests
# from bs4 import BeautifulSoup

# # URL of the page to scrape
# url = "https://finance.yahoo.com/quote/IBM/key-statistics?p=IBM"

# # Send a GET request to the URL
# response = requests.get(url)

# # Create a BeautifulSoup object with the response text and specify the parser
# soup = BeautifulSoup(response.text, "html.parser")

# # Find the table with the balance sheet data
# balance_sheet_table = soup.find("table", {"data-reactid": "36"})

# # Extract the table headers
# headers = [header.text for header in balance_sheet_table.find_all("th")]

# # Extract the table rows
# rows = []
# for row in balance_sheet_table.find_all("tr"):
#     rows.append([cell.text for cell in row.find_all("td")])

# # Print the headers and rows
# print(headers)
# for row in rows:
#     print(row)

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

# # Specify the URL of the page containing the div
# url = 'https://www.macrotrends.net/stocks/charts/IBM/ibm/financial-ratios'

# # Configure Selenium webdriver
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run Chrome in headless mode
# driver = webdriver.Chrome(options=options)

# # Navigate to the URL
# driver.get(url)

# # Find the div with the specified class
# div = driver.find_element(By.CSS_SELECTOR, 'div.jqx-clear.jqx-border-reset.jqx-overflow-hidden.jqx-max-size.jqx-position-relative')

# # Scroll the div horizontally to the end
# scroll_script = "arguments[0].scrollLeft = arguments[0].scrollWidth"
# driver.execute_script(scroll_script, div)

# # Extract the content of the div
# div_content = div.text

# # Print the extracted content
# print(div_content)

# # Quit the driver and close the browser
# driver.quit()

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz

# filename = list(uploaded.keys())[0]
url = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

headlines=[]
times=[]

articles = soup.find_all('article')
i=0

for article in articles:
    headline = article.find('h4').text
    print(headline)