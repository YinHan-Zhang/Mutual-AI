# Mutual-AI

Mutual-AI致力于在人工智能新时代提供中文交互式AI入门科普，填补中文互联网空缺。

## 环境准备

- Python版本3.9
- Fastapi版本>=0.95.1
- Pillow版本>=9.4.0
- Torchvision版本>=0.15.0
- Torch版本>=2.0.0
- Torchaudio版本>=0.0.0
- Python-Multipart
- Uvicorn

## 运行

将代码克隆至本地。

```bash
git clone https://github.com/YinHan-Zhang/Mutual-AI
```

进入文件夹，使用Uvicorn开启服务端。

```bash
uvicorn main:app
```

访问`http://127.0.0.1:8000/`。

