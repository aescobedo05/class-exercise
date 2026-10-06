import logging

logger = logging.getLogger(__name__)

def require_columns(df, required_columns):
    """Check that all required columns exist."""
    if list(set(df.columns)) != list(set(required_columns)):
        logger.error("Missing a required column")
        raise ValueError("Missing a required column")
    logger.info("All required columns exist")

    return df