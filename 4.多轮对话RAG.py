from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatTongyi
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
import warnings
import json
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

template = "你是一个从参考文本中提取关键信息回答问题的助手，如果问题涉及了参考文本中没有提及的信息并且联网搜索也没有合适的结果，回答‘不知道’。" \
           "参考文本：{context}。历史记录：{chat_history} 问题：{input}。请给出回答。"
prompt = PromptTemplate(input_variables=["context", "input", "chat_history"], template=template)

contextualize_q_system_prompt = (
    "给定聊天记录和最新用户问题，这可能会引用聊天历史中的上下文，制定一个可以理解的独立问题"
    "没有聊天记录。不要回答问题，如果需要，只需重新规划，否则按原样退回。"
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

history_aware_retriever = create_history_aware_retriever(tongyi_chat, retriever, contextualize_q_prompt)
combine_docs_chain = create_stuff_documents_chain(tongyi_chat, prompt)
qa_chain = create_retrieval_chain(history_aware_retriever, combine_docs_chain)

chat_history = []
while True:
    print("---------输入问题来进行询问，输入“退出”则退出对话---------")
    question = input("你的问题：")
    if question == "退出":
        break
    response = qa_chain.invoke({"input": question, "chat_history": chat_history})
    chat_history.extend([HumanMessage(content=question), AIMessage(content=response["answer"])])

    print(f"Agent输出：{response['answer']}")
    print("------------------------------------\n")
