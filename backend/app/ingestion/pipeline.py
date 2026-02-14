from typing import List
from app.ingestion.fetcher import RSSFetcher
from app.storage.models import AnalyzeRequest
from app.storage import repository

class IngestionPipeline:
    def __init__(self):
        self.fetcher = RSSFetcher()

    def run(self) -> List[AnalyzeRequest]:
        """
        Runs the ingestion pipeline: Fetch -> Clean (done in fetcher) -> Deduplicate
        Returns a list of NEW requests to be analyzed.
        """
        print("Starting ingestion pipeline...")
        
        # 1. Fetch
        raw_requests = self.fetcher.fetch_all()
        print(f"Fetched {len(raw_requests)} items.")
        
        # 2. Deduplicate
        new_requests = self._deduplicate(raw_requests)
        print(f"Found {len(new_requests)} new items after deduplication.")
        
        return new_requests

    def _deduplicate(self, requests: List[AnalyzeRequest]) -> List[AnalyzeRequest]:
        """
        Simple deduplication based on headline and source.
        Checks against existing events in the repository.
        """
        existing_events = repository.get_events()
        # Create a set of (headline, source) tuples for fast lookup
        existing_keys = {
            (e.get("headline"), e.get("source")) 
            for e in existing_events
        }
        
        unique_requests = []
        seen_in_batch = set()
        
        for req in requests:
            key = (req.headline, req.source)
            
            # Check if already processed in this batch
            if key in seen_in_batch:
                continue
                
            # Check if already in storage
            if key in existing_keys:
                continue
                
            unique_requests.append(req)
            seen_in_batch.add(key)
            
        return unique_requests
