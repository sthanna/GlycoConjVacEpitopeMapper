import os
import requests
from typing import List, Dict
from pathlib import Path

class PaperRetriever:
    def __init__(self, out_dir: str):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def search_pubmed(self, query: str, max_results: int = 50) -> List[str]:
        """
        Search PubMed for a given query and return a list of PMIDs.
        
        Args:
            query (str): The search query.
            max_results (int): Maximum number of results to return.
            
        Returns:
            List[str]: List of PubMed IDs.
        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json"
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            id_list = data.get("esearchresult", {}).get("idlist", [])
            return id_list
        except Exception as e:
            print(f"Error searching PubMed: {e}")
            return []

    def fetch_abstracts(self, pmids: List[str]) -> List[Dict]:
        """
        Fetch abstracts for a list of PMIDs.
        
        Args:
            pmids (List[str]): List of PubMed IDs.
            
        Returns:
            List[Dict]: List of dictionaries containing title and abstract.
        """
        if not pmids:
            return []
            
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        ids_str = ",".join(pmids)
        params = {
            "db": "pubmed",
            "id": ids_str,
            "rettype": "abstract",
            "retmode": "text"
        }
        # Note: This is a simplified fetch that retrieves raw text. 
        # For structured data, 'xml' retmode and proper parsing is recommended.
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            # In a real implementation, parse the XML/Text to separate records.
            # Returning a dummy wrapper for now.
            return [{"id": ids_str, "content": response.text}]
        except Exception as e:
            print(f"Error fetching abstracts: {e}")
            return []

    def download_pdfs(self, records: List[Dict]):
        """
        Attempt to download PDFs for the records.
        This is highly dependent on access permissions and available open-access links.
        """
        print("PDF download logic to be implemented based on available APIs or scraping rules.")
        pass

    def run_full_pipeline(self, queries: List[str]):
        """
        Execute search and fetch for multiple queries.
        """
        for q in queries:
            print(f"Searching for: {q}")
            pmids = self.search_pubmed(q)
            print(f"Found {len(pmids)} results.")
            recs = self.fetch_abstracts(pmids)
            # self.download_pdfs(recs)
            # Save records to disk
            out_file = self.out_dir / f"{q.replace(' ', '_')}_abstracts.txt"
            with open(out_file, 'w', encoding='utf-8') as f:
                for r in recs:
                    f.write(str(r) + "\n\n")
