import logging
import re

import pandas as pd

logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""
    logger.debug("Dataframe shape: %s", df.shape)

    print("Shape:", df.shape)
    print(df.head(5))
    print("Columns:", df.columns)
    print("Data types:", df.dtypes)



def remove_duplicates(df):
    """Remove exact duplicate rows."""
    before = len(df)

    df_dropped = df.drop_duplicates()

    after = len(df_dropped)

    logger.debug("Row count before removing duplicates: %s, Row count after: %s", before, after)

    return df_dropped


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    before = len(df)

    rows_dropped = df.dropna()

    after = len(rows_dropped)

    logger.debug("Row count before dropping rows with missing values: %s, " \
    "Row count after: %s", before, after)

    return rows_dropped


def clean_text(value):
    """Normalize one text value."""
    value = value.strip()
    value = value.lower()
    value = re.sub(r"\s+", " ", value)


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    if column not in df.columns:
        logger.error("%s doesnt exist", column)
        raise ValueError(f"Column {column} doesn't exist")

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - threshold * iqr
    upper = q3 + threshold * iqr

    df_score_cleaned = df[(df[column] >= lower) & (df[column] <= upper)]

    rows_removed = len(df) - len(df_score_cleaned)
    logger.debug("lower bound: %s, upper bound: %s, %s rows removed", lower, upper, rows_removed)

    return df_score_cleaned
