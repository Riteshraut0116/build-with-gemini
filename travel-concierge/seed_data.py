"""Seed Firestore database with initial destination catalog data."""

import logging
from google.cloud import firestore

# IMPORTANT: Hardcode project ID explicitly as required by Agent Platform standards
FIRESTORE_PROJECT_ID = "qwiklabs-gcp-03-6c1be26b1412"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INITIAL_DESTINATIONS = [
    {
        "id": "tokyo",
        "name": "Tokyo",
        "country": "Japan",
        "category": "Culture & Modernity",
        "budget_tier": "Moderate",
        "description": "A vibrant metropolis blending futuristic skyscrapers with historical temples.",
        "popular_spots": ["Shibuya Crossing", "Senso-ji Temple", "Tokyo Tower", "Akihabara"],
        "best_season": "Spring & Autumn",
    },
    {
        "id": "paris",
        "name": "Paris",
        "country": "France",
        "category": "Art & Cuisine",
        "budget_tier": "High",
        "description": "The City of Light, world-renowned for art, gastronomy, fashion, and culture.",
        "popular_spots": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Montmartre"],
        "best_season": "Spring & Summer",
    },
    {
        "id": "kyoto",
        "name": "Kyoto",
        "country": "Japan",
        "category": "History & Nature",
        "budget_tier": "Moderate",
        "description": "Japan's cultural heart filled with classical Buddhist temples, gardens, and imperial palaces.",
        "popular_spots": ["Fushimi Inari Shrine", "Arashiyama Bamboo Grove", "Kinkaku-ji", "Gion District"],
        "best_season": "Spring (Cherry Blossoms)",
    },
    {
        "id": "banff",
        "name": "Banff National Park",
        "country": "Canada",
        "category": "Outdoor & Adventure",
        "budget_tier": "Moderate",
        "description": "Stunning Canadian Rockies destination known for turquoise glacial lakes and mountain peaks.",
        "popular_spots": ["Lake Louise", "Moraine Lake", "Banff Townsite", "Johnston Canyon"],
        "best_season": "Summer & Winter",
    },
]


def seed_database():
    """Populates initial destination documents into the Firestore database."""
    logger.info("Initializing Firestore client for project: %s", FIRESTORE_PROJECT_ID)
    db = firestore.Client(project=FIRESTORE_PROJECT_ID)
    collection_ref = db.collection("destinations")

    for dest in INITIAL_DESTINATIONS:
        doc_id = dest["id"]
        doc_ref = collection_ref.document(doc_id)
        doc_ref.set(dest)
        logger.info("Seeded destination: %s (%s)", dest["name"], doc_id)

    logger.info("Successfully seeded %d destinations.", len(INITIAL_DESTINATIONS))


if __name__ == "__main__":
    seed_database()
