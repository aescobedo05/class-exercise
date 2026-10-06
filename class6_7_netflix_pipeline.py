import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    clean_text,
    drop_missing_rows,
    remove_duplicates,
    remove_iqr_outliers,
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

    df_original = dataframe.copy()

    logger.info("Loaded %s rows and %s columns", dataframe.shape[0], dataframe.shape[1])

    show_overview(dataframe)
    logger.info("Displayed DataFrame overview")

    removed = remove_duplicates(dataframe)
    removed_rows = len(dataframe) - len(removed)
    logger.info("Removed %s duplicate row(s)", removed_rows)

    dropped = drop_missing_rows(removed)
    dropped_rows = len(removed) - len(dropped)
    logger.info("Dropped %s row(s) with missing values", dropped_rows)

    try:
        outliers = remove_iqr_outliers(dropped, 'runtime_minutes', 1.5)
    except ValueError:
        sys.exit(1)

    outliers_total = len(dropped) - len(outliers)

    logger.info("Remove %s runtime_minutes outerlier(s)", outliers_total)

    clean_text('title')
    logger.info("Cleaned text column: title")

    clean_text('type')
    logger.info("Cleaned text column: type")

    clean_text('country')
    logger.info("Cleaned text column: country")

    df_final = outliers

    report = {
        "row_before": len(df_original),
        "rows_after": len(df_final),
        "rows_removed": len(df_original) - len(df_final),
        "columns": len(df_final.columns),
    }

    logger.info("Cleaning complete: {'rows_before': %s,'rows_after': %s, 'rows_removed': %s, " \
    "'columns': %s}", 
                report["row_before"], report["rows_after"],
                report["rows_removed"], report["columns"])

if __name__ == "__main__":
    main()
