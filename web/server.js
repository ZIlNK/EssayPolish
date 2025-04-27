import express from 'express';
import multer from 'multer';
import cors from 'cors';

const app = express();
const port = 3000;

// 使用 cors 中间件
app.use(cors());

// 配置 multer 用于处理文件上传
const storage = multer.memoryStorage();
const upload = multer({ storage });

app.get('/appraise', (req, res) => {
    const responseText = '评价文本';
    res.send(responseText);
});

app.get('/rewrite', (req, res) => {
    const responseText = '润色文本';
    res.send(responseText);
});
// 处理包含文件上传的 POST 请求
app.post('/post', upload.fields([{ name: 'images', maxCount: 10 }]), (req, res) => {
    let textData = '';
    if (req.body.text) {
        textData = req.body.text;
    }
    if (req.files && req.files.images) {
        // 这里简单处理，实际可按需对上传图片做存储等操作
        console.log('接收到上传的图片数量:', req.files.images.length);
    }
    // 模拟返回文本数据，这里直接返回接收到的文本或者自定义内容
    const responseText =
        '这是来自后端的虚拟响应文本\n这是来自后端的虚拟响应文本';
    res.send(responseText);
});

app.listen(port, () => {
    console.log(`服务器运行在 http://localhost:${port}`);
});