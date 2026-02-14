import sys
import os

# Add the current directory to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ingestion.pipeline import IngestionPipeline

if __name__ == "__main__":
    print("Testing Ingestion Pipeline...")
    pipeline = IngestionPipeline()
    try:
        new_items = pipeline.run()
        print(f"Successfully ingested {len(new_items)} items.")
        for item in new_items[:5]:  # Show first 5
            print(f"- {item.headline} ({item.source})")
    except Exception as e:
        print(f"Error running pipeline: {e}")