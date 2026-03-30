# 🧠 企业级私有数据检索与生成管线 · 演示版
<img width="2710" height="1544" alt="e0acbb0345728d265b7a093317610bc9" src="https://github.com/user-attachments/assets/9d47f5f9-ea01-4d7b-93ab-db543c8ee800" />
<img width="2707" height="1566" alt="5aa2f6a08ffc58703c3ea5da1e20b32f" src="https://github.com/user-attachments/assets/f0408fcf-54bb-4bb7-84dc-e5c76d1b90db" />
<img width="2860" height="1566" alt="e00e7edeb96a61c244b75d22be8b15b5" src="https://github.com/user-attachments/assets/31c91738-6fb3-49e2-b2d6-d81e944428cb" />
<img width="2880" height="1800" alt="d393356d76db91a049a86feef5441f2c" src="https://github.com/user-attachments/assets/553791b9-0ad2-4b7e-9645-4b4c1813cbac" />

> **当前版本**：已完成本地语义检索与 Streamlit 界面演示。  
> **下一步**：接入大模型生成回答，并部署公网在线体验。

## 🎯 在线体验
**暂未部署公网** – 您可在本地运行以下代码，亲自验证检索效果。



## 💡 核心价值
- **数据隐私绝对隔离**：所有向量化与检索均在本地完成（ChromaDB），敏感数据永不离开您的设备。
- **语义分块策略**：优先按段落切分，保证检索片段完整；长段自动硬切，兼顾精度与上下文。
- **即开即用的演示笔记**：内置管理学、Python、经济学公开语料，方便快速测试。

## 🛠 技术底座（当前实现）
| 模块 | 技术选型 |
|------|----------|
| 前端界面 | Streamlit |
| 向量数据库 | ChromaDB（本地持久化） |
| 文本嵌入 | `paraphrase-multilingual-MiniLM-L12-v2`（多语言支持） |
| 分块策略 | 段落优先 + 长段硬切（`CHUNK_SIZE=800`） |
| 隐私保障 | 无任何数据上传，向量库本地存储 |

## 🚀 快速开始（本地运行）

1. **克隆仓库**
   ```bash
   git clone https://github.com/你的用户名/rag-assistant-demo.git
   cd rag-assistant-demo
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动应用**
   ```bash
   streamlit run app.py
   ```

4. 浏览器自动打开 `http://localhost:8501`，输入问题即可检索演示笔记。

*首次运行会自动下载约 420MB 的 Embedding 模型，并索引 `demo_notes` 中的笔记，请耐心等待。*

## 📁 项目结构
```
rag-assistant-demo/
├── demo_notes/          # 公开演示笔记（管理学、Python、经济学）
├── app.py               # Streamlit 界面
├── rag_core.py          # 核心检索逻辑（分块、向量化、查询）
├── requirements.txt     # 依赖列表
├── .gitignore           # 忽略向量库等本地文件
└── README.md            # 项目说明
```

## 🔒 隐私与安全
- 向量数据仅存储在项目下的 `chroma_db` 文件夹，**永不传输至任何云端**。
- 演示笔记全部为公开知识，无任何个人隐私。
- 若需处理真实敏感文档，请替换 `demo_notes` 中的内容并在本地运行。

## 📈 开发路线图
- [x] 本地 Markdown 笔记检索（当前）
- [ ] 接入 DeepSeek API，实现检索增强生成（RAG 闭环）
- [ ] 支持动态文件上传（用户即时上传自己的文档）
- [ ] 部署至 Streamlit Cloud，提供公网演示链接

## 👨‍💻 关于开发者
- **定位**：投资学背景 + AI 应用开发能力的准产品人。
- **能力**：熟练运用 Python、LLM API、向量数据库，擅长将业务问题转化为自动化工具。
- **认证**：阿里云达摩院高级人工智能训练师、科大讯飞/Datawhale联合认证微调/智能体工程师。
- 📩 联系方式：zhy52111@qq.com

## 📄 许可证
MIT
```

---

