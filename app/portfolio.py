


# import pandas as pd
# import chromadb
# import uuid

# class Portfolio:
#     def __init__(self, file_path="app/resource/my_portfolio.csv"):
#         self.file_path = file_path
#         self.data = pd.read_csv(file_path)
#         self.chroma_client = chromadb.PersistentClient('vectorstore')
#         self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

#     def load_portfolio(self):
#         if not self.collection.count():
#             for _, row in self.data.iterrows():
#                 self.collection.add(
#                     documents=[str(row["Techstack"])],
#                     metadatas={"links": str(row["Links"])},
#                     ids=[str(uuid.uuid4())]
#                 )

#     def query_links(self, skills, extra_queries=None, n_results=4):
#         queries = list(set([s for s in skills if isinstance(s, str) and s.strip()]))[:10]
#         if extra_queries:
#             queries += [q for q in extra_queries if isinstance(q, str) and q.strip()]
#         if not queries:
#             return []
#         result = self.collection.query(query_texts=queries, n_results=n_results)
#         metas = result.get("metadatas", [])
#         links = []
#         for m in metas:
#             for item in m:
#                 link_str = item.get("links")
#                 if link_str and link_str not in links:
#                     links.append(link_str)
#         return links[:4]


import pandas as pd
import chromadb
import uuid
from langchain_community.document_loaders import WebBaseLoader

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[str(row["Techstack"])],
                    metadatas={"links": str(row["Links"])},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills, extra_queries=None, n_results=4):
        queries = list(set([s for s in skills if isinstance(s, str) and s.strip()]))[:10]
        if extra_queries:
            queries += [q for q in extra_queries if isinstance(q, str) and q.strip()]
        if not queries:
            return []
        result = self.collection.query(query_texts=queries, n_results=n_results)
        metas = result.get("metadatas", [])
        links = []
        for m in metas:
            for item in m:
                link_str = item.get("links")
                if link_str and link_str not in links:
                    links.append(link_str)
        return links[:4]

    def load_job_posting(self, job_url):
        """Loads job description text from a given URL."""
        loader = WebBaseLoader(job_url)
        docs = loader.load()
        return docs[0].page_content if docs else ""
