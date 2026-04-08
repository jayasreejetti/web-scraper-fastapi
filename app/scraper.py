import requests
import json
import os
import logging
import time
import sys

# Fix import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BASE_URL = "https://api.github.com/users"

# Load token if available
from dotenv import load_dotenv
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}


def fetch_with_retry(url, params, retries=3):
    """Fetch URL with retry on failure"""
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=10)

            # Rate limit hit
            if response.status_code == 403:
                logger.warning("Rate limit hit. Waiting 60 seconds...")
                time.sleep(60)
                continue

            # Success
            if response.status_code == 200:
                return response

            logger.error(f"Status {response.status_code} on attempt {attempt+1}")

        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error. Retrying in 5 seconds... (attempt {attempt+1})")
            time.sleep(5)

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout. Retrying in 5 seconds... (attempt {attempt+1})")
            time.sleep(5)

    logger.error("All retries failed for this page.")
    return None


def fetch_users():
    all_users = []

    for page in range(1, 101):
        params = {
            "per_page": 10,
            "page": page
        }

        logger.info(f"Fetching page {page}...")

        response = fetch_with_retry(BASE_URL, params)

        if response is None:
            logger.error(f"Skipping page {page}")
            continue

        data = response.json()

        if not data:
            logger.info(f"Empty page at {page}, stopping.")
            break

        for user in data:
            all_users.append({
                "id": user.get("id"),
                "login": user.get("login"),
                "url": user.get("html_url")
            })

        # Small delay to avoid rate limit
        time.sleep(1)

    logger.info(f"Total users fetched: {len(all_users)}")
    return all_users


def save_to_json(data):
    os.makedirs("data", exist_ok=True)
    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=4)
    logger.info("Saved to data/users.json")


def save_to_db(users):
    db = SessionLocal()
    added = 0

    for user in users:
        existing = db.query(User).filter(User.id == user["id"]).first()
        if not existing:
            new_user = User(
                id=user["id"],
                login=user["login"],
                url=user["url"]
            )
            db.add(new_user)
            added += 1

    db.commit()
    db.close()
    logger.info(f"Inserted {added} new users into DB")


if __name__ == "__main__":
    users = fetch_users()
    save_to_json(users)
    save_to_db(users)
    print(" Scraping done! Data saved to JSON and DB.")