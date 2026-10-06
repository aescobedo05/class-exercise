import logging

logger = logging.getLogger(__name__)

def require_columns(df, required_columns):
    """Check that all required columns exist."""
    missing = set(required_columns) - set(df.columns)

    if missing:
        logger.error("Missing a required column")
        raise ValueError("Missing a required column")

    logger.info("Validation completed")

    return df
