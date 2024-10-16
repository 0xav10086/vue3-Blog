import express, { Request, Response } from 'express';
import multer, { StorageEngine } from 'multer';
import sqlite3 from 'sqlite3';
import path from 'path';
import fs from 'fs';

const app = express();
const db = new sqlite3.Database('diary.db');

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use('/uploads', express.static('uploads'));

// 设置 multer 存储配置
const storage: StorageEngine = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({ storage: storage });

// 初始化数据库
db.serialize(() => {
  db.run("CREATE TABLE IF NOT EXISTS diary (id INTEGER PRIMARY KEY, title TEXT, content TEXT, imagePath TEXT)");
});

// 上传文件和保存数据的路由
app.post('/upload', upload.single('image'), (req: Request, res: Response) => {
  const { title, content } = req.body;
  const imagePath = req.file ? req.file.path : null;

  db.run("INSERT INTO diary (title, content, imagePath) VALUES (?, ?, ?)", [title, content, imagePath], (err) => {
    if (err) {
      return res.status(500).send('Error uploading content.');
    }
    res.send('Content uploaded successfully!');
  });
});

// 获取所有日记条目的路由
app.get('/diaries', (req: Request, res: Response) => {
  db.all("SELECT * FROM diary", (err, rows) => {
    if (err) {
      return res.status(500).send('Error retrieving content.');
    }
    res.json(rows);
  });
});

// 删除日记条目的路由
app.delete('/diaries/:id', (req, res) => {
  const id = req.params.id;
  console.log(`Deleting diary with id: ${id}`); // 添加日志
  db.run("DELETE FROM diary WHERE id = ?", id, (err) => {
    if (err) {
      console.error('Error deleting diary:', err); // 添加日志
      return res.status(500).send('Error deleting diary.');
    }
    // 删除成功后重新获取所有日记条目
    db.all("SELECT * FROM diary", (err, rows) => {
      if (err) {
        return res.status(500).send('Error retrieving content.');
      }
      res.json(rows);
    });
  });
});

// 更新日记条目的路由
app.put('/diaries/:id', upload.single('image'), (req, res) => {
  const id = req.params.id;
  const { title, content } = req.body;
  const imagePath = req.file ? req.file.path : null;
  console.log(`Updating diary with id: ${id}`); // 添加日志

  db.run("UPDATE diary SET title = ?, content = ?, imagePath = ? WHERE id = ?", [title, content, imagePath, id], (err) => {
    if (err) {
      console.error('Error updating diary:', err); // 添加日志
      return res.status(500).send('Error updating diary.');
    }
    res.send('Diary updated successfully!');
  });
});

app.listen(3000, () => {
  console.log('Server started on port 3000');
});
