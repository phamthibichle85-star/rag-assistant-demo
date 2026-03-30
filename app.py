import streamlit as st
from rag_core import query

st.set_page_config(page_title="RAG 知识库演示", layout="centered")
st.title("📚 RAG 知识库检索演示")
st.markdown("根据公开笔记回答问题（基于 ChromaDB + 多语言 Embedding）")

@st.cache_resource
def init_rag():
    from rag_core import load_model_and_db
    load_model_and_db()
    return True

if 'rag_ready' not in st.session_state:
    with st.spinner("正在加载知识库，首次运行需要几分钟..."):
        init_rag()
        st.session_state.rag_ready = True

question = st.text_input("请输入你的问题:", placeholder="例如：泰勒的科学管理是什么？")

if question:
    with st.spinner("检索中..."):
        results = query(question, n_results=3)
    if results:
        st.subheader("📖 相关笔记片段")
        for i, (doc, dist, meta) in enumerate(results):
            st.markdown(f"**片段 {i+1}** (相似度: {dist:.4f})")
            st.info(doc)
            st.caption(f"来源：{meta['source']}")
    else:
        st.warning("没有找到相关笔记。")
        