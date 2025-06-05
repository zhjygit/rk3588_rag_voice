Based on the rknpu computing power of RK3588, the deployment of RKRLM is completed, combined with the RAG knowledge base and LLM large model, API interfaces are provided in the LAN, and then voice interaction is carried out through ASR and TTS.

基于 RK3588 的 rknpu 算力，完成 RKLLM 的部署，结合 RAG 知识库和 LLM 大模型，在局域网中提供 API 接口，然后通过 ASR 和 TTS 进行语音交互。

当前的项目文件结构说明：

    update_vector_db.py 建立数据库

    knowledge_search.py 检索数据

    flask_server.py

    通过prompt强化模型输出(参考 rk官方 flask_server 示例)


to do list

    1.asr+tts+zeroMQ
  
    2.improve the rag
  
  
