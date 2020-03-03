import requests
import smtplib
import json
from bs4 import BeautifulSoup
from email.mime.text import MIMEText


def search(query):
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"

    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"

    headers = {"user-agent": USER_AGENT}
    page = requests.get(URL, headers=headers)

    results = []
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        for item in soup.find_all('div', class_='r'):
            anchors = item.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = item.find('h3').text
                news = {
                    "title": title,
                    "link": link
                }
                results.append(news)

    return results


def send_msg(results):
    news = ''
    for i, each in enumerate(results, start=1):
        news += f"{i}. {each['title']} -> {each['link']}\n\n"

    # get login info from .json file
    with open('C:\\Users\\WATNEY\\Desktop\\news-crawler\\config.json') as f:
        user = json.load(f)

    # create message object
    message = MIMEText(news)
    message['to'] = 'achuaphan@gmail.com'
    message['from'] = f'Info <{user["email"]}>'
    message['subject'] = 'COVID-19 News Update'

    print('Sending...')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(user['email'], user['password'])
        # smtp.send_message(msg, EMAIL_ADDR, EMAIL_ADDR)
        smtp.send_message(message)
    print('Sent message successfully!')


query = "coronavirus seattle"
print(send_msg(search(query)))
