# rag_integration.py

import json
import os
from openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from logging_utils import log_message, ConsoleColor


A1 = {
  "questions": [
    "What is the central theme of the book, and how is it developed throughout the narrative?",
    "Who are the key characters, and what are their motivations, conflicts, and arcs?",
    "What literary techniques (symbolism, metaphor, foreshadowing) are used, and how do they enhance the story?",
    "what crucial information or insights can be derived from this book?",
    "How does the book reflect its historical, cultural, or social context?",
    "What is the author's intent or message, and how is it conveyed through the text?",
    "What narrative structure is employed, and how does it affect the reader's experience?",
    "How do the setting and atmosphere contribute to the mood and themes of the book?",
    "What are the major conflicts and resolutions, and what do they reveal about the characters or themes?",
    "How does the book compare to other works in the same genre or by the same author?",
    "What are the notable quotes or passages, and why are they significant?",
    "How do literary devices like irony, allegory, and satire function within the text?",
    "What philosophical or moral questions are raised by the book, and how are they explored?",
    "How does the book's pacing and tone influence the reader's engagement?",
    "What critical interpretations or academic analyses exist for this book?",
  ]
}


def run_rag_system(
    api_key: str,
    persist_dir: str,
    data_dir: str,
) -> str:
    # 1) Create the OpenAI client directly with the passed API key
    client = OpenAI(api_key=api_key)

    # 2) Load or create the Llama Index
    try:
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        index = load_index_from_storage(storage_context)
        log_message("✅ Index loaded from disk.", color=ConsoleColor.GREEN)
    except FileNotFoundError:
        # If no index found, create it from data_dir
        if not os.path.isdir(data_dir) or not os.listdir(data_dir):
            raise ValueError(f"🚨 No documents found in '{data_dir}'. Please add files to index.")
        documents = SimpleDirectoryReader(data_dir).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=persist_dir)
        log_message("✅ Index created and persisted to disk.", color=ConsoleColor.GREEN)

    # Updated summary query with A* variables
    summary_query = ("Provide a concise summary of the key themes and content of this book. "
                     "Consider foundational assumptions, core elements, evident patterns, long-term implications, "
                     "and key stakeholders from the provided data: "
                     f"{json.dumps(A1)}")
    
    summary_response = index.as_query_engine().query(summary_query)
    book_summary = summary_response.response.strip()

    log_message("✅ RAG system completed. Returning final improved JSON.", color=ConsoleColor.GREEN)
    return book_summary
