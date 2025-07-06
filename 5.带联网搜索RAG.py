from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatTongyi
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import json
import requests
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

keyword = config['keyword']
output_dir = config['output_dir']
model_name = config['model_name']
model_kwargs = config['model_kwargs']
encode_kwargs = config['encode_kwargs']
model = config['model']
api_key = config['api_key']

dir_path = f"{output_dir}{keyword}/"
vector_dir = f"{output_dir}VectorStore/{keyword}"
embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

# 对数据进行加载
db = Chroma(persist_directory=vector_dir, embedding_function=embeddings)

retriever = db.as_retriever()
tongyi_chat = ChatTongyi(model=model, api_key=api_key)


def baidu_search_tool(query: str) -> str:
    messages = [{"content": query, "role": "user"}]
    data = {
        "messages": messages,
        "search_source": "baidu_search_v2",
        "search_recency_filter": "year"  # 可以自定义各种检索条件
    }

    response = requests.post(config['baidu_url'], headers=config['baidu_headers'], json=data)

    if response.status_code == 200:
        # 返回给大模型的格式化的搜索结果文本
        # 可以自己对博查的搜索结果进行自定义处理
        return str(response.json())
    else:
        raise Exception(f"API请求失败，状态码: {response.status_code}, 错误信息: {response.text}")


template = "你是一个从参考文本中提取关键信息回答问题的助手，如果问题涉及了参考文本中没有提及的信息并且联网搜索也没有合适的结果，回答‘不知道’。" \
           "参考文本：{context}, 问题：{input}。请给出回答。"
prompt = PromptTemplate(input_variables=["context", "input"], template=template)
tools = [Tool(name="BaiduSearch",
              func=baidu_search_tool,
              description="使用Baidu Search API进行联网搜索，返回搜索结果的字符串")]
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chain = {"context": retriever, "input": RunnablePassthrough()} | prompt | tongyi_chat | StrOutputParser()
agent = initialize_agent(tools, tongyi_chat,
                         agent="conversational-react-description",
                         verbose=True,
                         memory=memory)

while True:
    print("---------输入问题来进行询问，输入“退出”则退出对话---------")
    question = input("你的问题：")
    if question == "退出":
        break
    answer = agent.invoke({"input": question})
    print(f"Agent输出：{answer['output']}")
    print("------------------------------------\n")
