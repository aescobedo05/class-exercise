import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    drop_missing_rows,
    remove_duplicates,
    show_overview,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    data_dir = Path(args.input)

    try:
        dataframe = pd.read_csv(data_dir)
    except FileNotFoundError:
        logger.error("Input file not found: %s", data_dir)
        sys.exit(1)

    logger.info("Loaded %s rows and %s columns", dataframe.shape[0], dataframe.shape[1])

    show_overview(dataframe)
    logger.info("Displayed DataFrame overview")

    removed = remove_duplicates(dataframe)
    removed_rows = len(removed)
    logger.info("Removed %s duplicate row(s)", removed_rows)
    
    dropped = drop_missing_rows(dataframe)
    dropped_rows = len(dropped)
    logger.info("Dropped %s row(s) with missing values", dropped_rows)


if __name__ == "__main__":
    main()
