import os
import sys
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
from chromadb.errors import NotFoundError
import chardet

os.chdir(os.path.dirname(os.path.abspath(__file__)))

OBSIDIAN_FOLDER = "./demo_notes"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 80
DB_PATH = "./chroma_db"
COLLECTION_NAME = "demo_notes"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        raw_data = f.read(10000)
        result = chardet.detect(raw_data)
        return result["encoding"] or "utf-8"

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    paragraphs = text.split('\n\n')
    chunks = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(para) <= chunk_size:
            chunks.append(para)
        else:
            start = 0
            para_len = len(para)
            while start < para_len:
                end = min(start + chunk_size, para_len)
                chunks.append(para[start:end])
                if end == para_len:
                    break
                start = end - overlap
    return chunks

_embed_model = None
_collection = None

def load_model_and_db():
    global _embed_model, _collection
    if _embed_model is None:
        print("加载 Embedding 模型中...")
        _embed_model = SentenceTransformer(EMBEDDING_MODEL)

    if _collection is None:
        print("初始化 ChromaDB 客户端...")
        client = chromadb.PersistentClient(path=DB_PATH, settings=Settings(anonymized_telemetry=False))

        try:
            _collection = client.get_collection(COLLECTION_NAME)
            print(f"已存在集合 {COLLECTION_NAME}，直接加载")
        except NotFoundError:
            print(f"创建新集合 {COLLECTION_NAME}，开始读取演示笔记...")
            if not os.path.exists(OBSIDIAN_FOLDER):
                raise FileNotFoundError(f"未找到演示笔记文件夹：{OBSIDIAN_FOLDER}")

            all_chunks = []
            all_metadatas = []
            all_ids = []

            idx = 0
            for root, dirs, files in os.walk(OBSIDIAN_FOLDER):
                for file in files:
                    if file.endswith(".md"):
                        filepath = os.path.join(root, file)
                        try:
                            enc = detect_encoding(filepath)
                            with open(filepath, "r", encoding=enc) as f:
                                content = f.read()
                            chunks = chunk_text(content)
                            for chunk in chunks:
                                all_chunks.append(chunk)
                                all_metadatas.append({"source": filepath})
                                all_ids.append(f"chunk_{idx}")
                                idx += 1
                        except Exception as e:
                            print(f"跳过 {filepath}: {e}")

            print(f"共读取 {idx} 个文本块")

            _collection = client.create_collection(COLLECTION_NAME)

            print("生成向量并存储...")
            batch_size = 100
            for i in range(0, len(all_chunks), batch_size):
                batch_ids = all_ids[i:i+batch_size]
                batch_chunks = all_chunks[i:i+batch_size]
                batch_metadatas = all_metadatas[i:i+batch_size]
                batch_embeddings = _embed_model.encode(batch_chunks).tolist()
                _collection.add(
                    ids=batch_ids,
                    documents=batch_chunks,
                    metadatas=batch_metadatas,
                    embeddings=batch_embeddings
                )
            print("嵌入完成！")

    return _embed_model, _collection

def query(question, n_results=2):
    model, collection = load_model_and_db()
    q_emb = model.encode([question]).tolist()
    results = collection.query(
        query_embeddings=q_emb,
        n_results=n_results,
        include=["documents", "distances", "metadatas"]
    )
    docs = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]
    return list(zip(docs, distances, metadatas))
