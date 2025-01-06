import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(messages)s",
    handlers=[
        logging.StreamHandler()
    ]
)