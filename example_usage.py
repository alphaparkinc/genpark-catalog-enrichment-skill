"""
example_usage.py -- Demonstrates the CatalogEnrichmentClient SDK.
"""
from client import CatalogEnrichmentClient

def main():
    client = CatalogEnrichmentClient()

    raw_catalog = [
        {"id": "P001", "name": "Vitamin C Serum 30ml", "price": 34.99, "description": "Great serum.", "category": "beauty", "tags": ["skincare"], "images": ["img1.jpg"]},
        {"id": "P002", "name": "Wireless Earbuds Pro", "price": "$89.00", "description": "", "category": "", "tags": [], "images": []},
        {"id": "P003", "name": "Yoga Mat Premium", "price": 68.00, "description": "", "category": "", "tags": [], "images": ["yoga.jpg"]},
        {"id": "P004", "name": "Coffee French Press", "description": "Makes great coffee", "category": "home", "tags": ["kitchen"], "images": []},
        {"id": "P005", "name": "Running Shoes V2", "price": 95.00},
    ]

    print("[Catalog Enrichment]")
    result = client.enrich(raw_catalog, required_fields=["name","description","price","category","tags","images"])

    health = result["catalog_health"]
    print(f"Catalog Health: Grade {health['health_grade']} | Avg Completeness: {health['avg_completeness_score']}%")
    print(f"Fully Complete: {health['fully_complete']} | Needs Attention: {health['needs_attention']} | Critical: {health['critical_incomplete']}")

    print(f"\nEnriched Products:")
    for p in result["enriched_products"]:
        print(f"  [{p['_completeness_score']}%] {p['name']} | Cat: {p['category']} | Tags: {str(p.get('tags',[])[: 3])}")
        if p["_changes_made"]:
            print(f"    Changes: {', '.join(p['_changes_made'])}")
        if p["_missing_fields"]:
            print(f"    Still Missing: {p['_missing_fields']}")

    if result["issues"]:
        print(f"\nIssues ({len(result['issues'])} products need attention):")
        for issue in result["issues"][:3]:
            print(f"  {issue['name']} [{issue['completeness']}%]: missing {issue['missing']}")

if __name__ == "__main__":
    main()
