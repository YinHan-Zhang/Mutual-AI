# Mutual AI API命名规范

## 路径文件

路径名称必须与业务相关，且全为小写字母，多个单词间用下划线分割。

API文档名称必须与路径名称相同，每个路径占用一个py文件，同一个文件只专注于一个路径。

例如：定义了路径`host/liner`，则API文档中必须同步创建`liner.md`文档。

正确示范：

`liner.py`

```python
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from model import Liner

router = APIRouter()
liner_model = Liner.Liner_Model()

@router.get("/liner")
async def liner(data: int):
    return JSONResponse({
        "code": 200,
        "data": {
            "result": liner_model.run(data)
        }
    })
```

错误示范：

`liner.py`

```python
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from model import Liner

router = APIRouter()
liner_model = Liner.Liner_Model()

@router.get("/liner")
async def liner(data: int):
    return JSONResponse({
        "code": 200,
        "data": {
            "result": liner_model.run(data)
        }
    })

@router.get("/face_recognition")
async def face_identify():
    return JSONResponse({
        "code": 200
    })
```

### 路径参数

路径参数必须定义类型。

### 与模型的联动

[模型](##模型)必须在当前文件中引用，不可在其他文件中重复创建。

## 模型与参数文件

模型的命名必须与路径参数相同，且首字母大写。

参数文件使用pickle封装，并且与路径文件同名，后缀为pickle。

[学习pickle模块](https://zhuanlan.zhihu.com/p/419362785)。

例如：

| 路径文件名          | 模型文件名          | 参数文件名              |
| ------------------- | ------------------- | ----------------------- |
| liner.py            | Liner.py            | liner.pickle            |
| face_recognition.py | Face_Recognition.py | face_recognition.pickle |

### 模型类定义

模型类与模型文件名称相同，后加入_Model。

例如：

| 模型文件名          | 模型类名               |
| ------------------- | ---------------------- |
| Liner.py            | Liner_Model            |
| Face_Recognition.py | Face_Recognition_Model |

模型使用方法必须为run()。

例如：

`Liner.py`

```python
class Liner_Model:
    def __init__(self):
        pass

    def run(self, args: int):
        return args * 2 + 1
```

如果有参数文件，则在`__init__`魔术方法中传入。