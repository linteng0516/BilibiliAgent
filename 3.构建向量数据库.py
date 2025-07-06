from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os
import json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 处理多个文件
keyword = config['keyword']
output_dir = config['output_dir']
model_name = config['model_name']
model_kwargs = config['model_kwargs']
encode_kwargs = config['encode_kwargs']

dir_path = f"{output_dir}{keyword}/"
vector_dir = f"{output_dir}VectorStore/{keyword}"

embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

documents = []
for file in os.listdir(dir_path):
    if file.endswith('.txt'):
        file_path = os.path.join(dir_path, file)
        loader = TextLoader(file_path, encoding='utf-8')
        documents.extend(loader.load())
print(f'documents:{len(documents)}')

# # 用CharacterTextSplitter会报错：Created a chunk of size xxx, which is longer than the specified xxx
# # 因为不会根据换行符、句号来分割，使用RecursiveCharacterTextSplitter可以解决问题
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "."],
    chunk_size=500,
    chunk_overlap=50,
)

chunks = text_splitter.split_documents(documents=documents)

print("split_docs size:", len(chunks))

if not os.path.exists(vector_dir):
    os.makedirs(vector_dir)
db = Chroma.from_documents(chunks, embeddings, persist_directory=vector_dir)
# 持久化
db.persist()
print("数据库构建完成")
