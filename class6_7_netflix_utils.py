import logging

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

    logger.debug("Row count before dropping rows with missing values: %s, Row count after: %s", before, after)

    return rows_dropped
