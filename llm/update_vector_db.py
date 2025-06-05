from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

# 配置参数
DB_PATH = "vector_db"
DB_TYPE = "faiss"  # 可选 faiss/hnswlib
NEW_DATA_PATH = "../knowledge/new_knowledge.md"
OLD_DATA_PATH = "../knowledge/old_knowledge.md"

def move_new_to_old():
    """将新知识库内容追加到旧知识库末尾，并清空新知识库文件"""
    try:
        # 检查文件是否存在，不存在则创建
        if not os.path.exists(OLD_DATA_PATH):
            open(OLD_DATA_PATH, 'w', encoding='utf-8').close()
            
        # 读取新知识内容
        with open(NEW_DATA_PATH, 'r', encoding='utf-8') as new_file:
            new_content = new_file.read()
        
        if not new_content.strip():
            print("新知识库文件为空，无需添加")
            return
            
        # 追加到旧知识库末尾
        with open(OLD_DATA_PATH, 'a', encoding='utf-8') as old_file:
            # 确保新内容前有换行
            old_file.write('\n\n' + new_content)
            
        # 清空新知识库文件
        with open(NEW_DATA_PATH, 'w', encoding='utf-8'):
            pass
            
        print(f"已将新知识添加到旧知识库中并清空新知识库文件")
    except Exception as e:
        print(f"移动知识库内容时出错: {e}")
        
def update_vector_db():
    print("处理新数据...")
    # 2. 处理新数据
    with open(NEW_DATA_PATH, "r", encoding="utf-8") as f:
        new_docs=f.read()
    
    # 2. 文本分块（按200字符切分）
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
        length_function=len,
        separators=["\n\n","\n#","\n##", "\n###","\n## # ","\n####", "\n", "\n- ", "。", "！", "？", "；", "，"],
        keep_separator=True
    )
    new_texts = text_splitter.create_documents([new_docs])
    print("新数据内容: \n")
    for i in new_texts:
        print(i)
        print("\n")
    print("条目数:", len(new_texts), "\n")
    print("完成")

    print('加载知识库检索模型...')
    # 1. 加载已有数据库
    embedding = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    print("完成")
    print('加载知识库...')
    if DB_TYPE == "faiss":
        if os.path.exists(DB_PATH):
            vector_db = FAISS.load_local(DB_PATH, embedding, allow_dangerous_deserialization=True)
            # 3. 增量添加
            print("添加新词条...")
            # FAISS需要合并索引
            new_db = FAISS.from_documents(new_texts, embedding)
            vector_db.merge_from(new_db)
        else:
            # 构建FAISS向量数据库
            print("知识库不存在，创建知识库，并保存词条...")
            vector_db = FAISS.from_documents(new_texts, embedding)
            # vector_db.save_local("vector_db")  # 保存到本地
            # vector_db = FAISS.from_texts([""], embedding)  # 创建空数据库
    # else:
    #     if os.path.exists(DB_PATH):
    #         vector_db = Hnswlib.load_local(DB_PATH, embedding)
    #     else:
    #         vector_db = Hnswlib.from_texts([""], embedding, space='cosine')
    print("完成")
    
    # else:
    #     # Hnswlib直接追加
    #     vector_db.add_documents(new_texts)

    # 4. 保存更新后的数据库
    vector_db.save_local(DB_PATH)
    print(f"成功添加{len(new_texts)}条新知识！")
    move_new_to_old()
    
if __name__ == "__main__":
    update_vector_db()