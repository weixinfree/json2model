# jon2model
将json转换为java model

# install
`pip3 install json2model`

# usage
1. 把一段合法json粘贴到剪切板
2. 执行命令 `json2model`，生成的代码会自动复制到剪切板
3. paste 代码


# demo

#### json
```json
{

    "name": "小明",
    "age": 10,
    "sex": 1,
    "scores": [ // 这是comment
        {
            "type": "数学",
            "score": "84"
        },
        {
            "type": "语文",
            "score": "76"
        }
    ]
}
```

#### 对应生成的代码

```java
...
```
