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
import java.io.Serializable;
import java.util.List;
import com.google.gson.annotations.SerializedName;

/**
 * xxx
 *
 * @author xxx 
 */
public class CustomPojo implements Serializable {
    private static final long serialVersionUID = 2401113242771510981L;

    @SerializedName("name")
    public String mName;
    @SerializedName("age")
    public int mAge;
    @SerializedName("sex")
    public int mSex;
    @SerializedName("scores")
    public List<CustomScores> mScores;

    public static class CustomScores implements Serializable {
        private static final long serialVersionUID = 5835901118477215543L;
        @SerializedName("type")
        public String mType;
        @SerializedName("score")
        public String mScore;
    }

}
```
