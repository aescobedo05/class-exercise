import argparse
import logging
import sys

from class5_file_utils import inspect_file, inspect_extension

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Inspect a text file"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to a .txt file"
    )
    args = parser.parse_args()

    try:
        info = inspect_file(args.input)
    except FileNotFoundError as error:
        logger.error("File doesn't exist: %s", error)
        sys.exit(1)

    try:
        ext = inspect_extension(info)
    except ValueError as error:
        logger.error("Unsupported format: %s", error)
        sys.exit(1)

    logger.info("File: %s, extension: %s", info['name'], info['extension'])

if __name__ == "__main__":
    main()
