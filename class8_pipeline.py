import logging
from pathlib import Path
import sys
from class8_data_loader import load_netflix
from class8_data_validator import require_columns

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():
    input_path = Path("data/messy_netflix_titles.csv")

    try:
        require_columns(load_netflix(input_path), ["title", "type", "release_year"])       
    except ValueError:
        sys.exit(1)

    logger.info("Dataframe succesful")

if __name__ == "__main__":
    main()
