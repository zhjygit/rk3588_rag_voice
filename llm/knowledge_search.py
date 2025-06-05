from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

logging.basicConfig(level=logging.ERROR)
transformers_logging.set_verbosity_error()

print('加载知识库检索模型...')
embedding_model = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
print('完成')
print('加载知识库...')
vector_db = FAISS.load_local("deepseek_vector_db", embedding_model, allow_dangerous_deserialization=True)
print('完成')
app = Flask(__name__)

# 搜索内容 search_content
docs = vector_db.similarity_search(search_content, k=3)
context = "\n".join([doc.page_content for doc in docs])
print("搜索结果：",context)