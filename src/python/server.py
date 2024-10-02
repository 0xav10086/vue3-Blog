from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime, timedelta
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.send_file_max_age_default = timedelta(seconds=1)

# 设置运行的图片格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 设置上传文件夹
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '../../public/data/log')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 动态获取工作目录
NOTES_DATA_PATH = os.path.join(BASE_DIR, '../../public/data/note')
print('NOTES_DATA_PATH:', NOTES_DATA_PATH)  # 打印路径以确认

@app.route('/api/NotesFiles', methods=['GET'])
def list_notes():
    folders = []
    print('NOTES_DATA_PATH:', os.path.abspath(NOTES_DATA_PATH))  # 打印路径
    for root, dirs, files in os.walk(NOTES_DATA_PATH):
        print('Walking through:', root)  # 打印当前遍历的目录
        folder = {
            'name': os.path.basename(root),
            'files': sorted(files)
        }
        print('Folder:', folder)  # 打印当前文件夹信息
        folders.append(folder)
    print("All Folders:", folders)  # 打印所有文件夹信息
    print('Current Working Directory:', os.getcwd())
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

# 初始数据库
def init_db():
    with sqlite3.connect('diary.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS diary (
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            content TEXT,
                            imagePath TEXT)''')
        conn.commit()

init_db()

# upload log files
@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        title = request.form['title']
        content = request.form['content']
        file = request.files.get('image')
        imagePath = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            imagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            app.logger.info(f"Saving file to: {imagePath}")
            file.save(imagePath)

        # 存储文件名
        filename_only = os.path.basename(imagePath)

        with sqlite3.connect('diary.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO diary (title, content, imagePath) VALUES (?, ?, ?)",
                           (title, content, filename_only))
            conn.commit()

        return jsonify({'message': 'Content uploaded successfully!', 'filename': filename_only}), 200
    except Exception as e:
        app.logger.error(f"Error uploading content: {e}")
        return jsonify({'error': 'Error uploading content.'}), 500

# 获取所有日记条目的路由
@app.route('/api/diaries', methods=['GET'])
def get_diaries():
    with sqlite3.connect('diary.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM diary')
        rows = cursor.fetchall()
        diaries = [{'id': row[0], 'title': row[1], 'content': row[2], 'imagePath': row[3]} for row in rows]
    return jsonify(diaries)

# 删除日记条目的路由
@app.route('/api/diaries/<int:id>', methods=['DELETE'])
def delete_diary(id):
    with sqlite3.connect('diary.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM diary WHERE id = ?", (id,))
        conn.commit()

    return 'Diary deleted successfully!'

# 更新日记条目的路由
@app.route('/api/diaries/<int:id>', methods=['PUT'])
def update_diary(id):
    title = request.form['title']
    content = request.form['content']
    file = request.files.get('image')
    imagePath = None

    if file:
        filename = secure_filename(file.filename)
        imagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(imagePath)

    # 存储文件名
    filename_only = os.path.basename(imagePath)

    with sqlite3.connect('diary.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE diary SET title = ?, content = ?, imagePath = ? WHERE id = ?",
                       (title, content, filename_only, id))
        conn.commit()

    return 'Diary updated successfully!'

# 静态文件路由
@app.route('/api/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
