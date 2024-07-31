from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

NOTES_DATA_PATH = '../../public/data/note'

@app.route('/api/NotesFiles', methods=['GET'])
def list_notes():
    folders = []
    for root, dirs, files in os.walk(NOTES_DATA_PATH):
        folder = {
            'name': os.path.basename(root),
            'files': sorted(files)
        }
        folders.append(folder)
    return jsonify(folders)

@app.route('/api/FanList', methods=['GET'])
def list_fans():
    date_str = request.args.get('date')
    print(f"Received date: {date_str}")  # 调试信息
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        year = date.year
        month = date.month
        weekday = date.weekday()
    else:
        now = datetime.now()
        year = now.year
        month = now.month
        weekday = now.weekday()

    if month in [1, 2, 3]:
        quarter = '01'
    elif month in [4, 5, 6]:
        quarter = '04'
    elif month in [7, 8, 9]:
        quarter = '07'
    else:
        quarter = '10'

    url = f'https://acgsecrets.hk/bangumi/{year}{quarter}/'
    print(f"Fetching URL: {url}")  # 调试信息

    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    anime_names = soup.find_all(class_='anime_name')
    fanDays = soup.find_all(class_='day')
    fanTimes = soup.find_all(class_='time')

    anime_schedule = defaultdict(list)

    for anime, day, time in zip(anime_names, fanDays, fanTimes):
        anime_name = anime.get_text(strip=True)
        day_name = day.get_text(strip=True)
        time_name = time.get_text(strip=True)
        anime_schedule[day_name].append((anime_name, time_name))  # 添加到list中

    day_map = {
        0: '一',  # 周一
        1: '二',  # 周二
        2: '三',  # 周三
        3: '四',  # 周四
        4: '五',  # 周五
        5: '六',  # 周六
        6: '日'   # 周日
    }

    output = []
    day_key = day_map[weekday]
    if day_key in anime_schedule:
        output.append(f"周{day_key}")
        for anime, time in anime_schedule[day_key]:
            output.append(f"{anime} - {time}")

    result = "\n".join(output)
    print(f"Returning result: {result}")  # 调试信息
    return result

if __name__ == '__main__':
    app.run(debug=True)
