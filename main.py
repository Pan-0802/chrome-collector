from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai

app = FastAPI()

# 允许跨域请求（因为插件在浏览器运行）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PageData(BaseModel):
    title: str
    content: str
    url: str

# 配置你的 OpenAI Key
openai.api_key = "你的API_KEY"

@app.post("/process")
async def process_content(data: PageData):
    # 构建 Prompt
    prompt = f"""
    请分析以下网页内容，并给出分类和简短摘要。
    标题: {data.title}
    内容: {data.content[:500]} 
    
    返回格式必须是 JSON: 
    {{"category": "类别", "summary": "一句话摘要"}}
    类别仅限：[技术, 职场, 生活, 美食, 穿搭, 其他]
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # 或 gpt-4o-mini
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    
    # 模拟返回（如果没有Key，可以用下面这行测试）
    # return {"category": "技术", "summary": "这是一个关于Chrome插件开发的教程。"}
    
    import json
    result = json.loads(response.choices[0].message.content)
    
    # 这里可以添加代码将 result 存入你的数据库（如 Supabase）
    print(f"已整理：{data.title} -> {result['category']}")
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)