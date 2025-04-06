import logging


class BorealisFormatter(logging.Formatter):
    """
    Styilised logging formatter for Borealis to assist end-users.
    """

    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"

    MESSAGE_FORMAT: str = (
        "\033[1m(BOREALIS) [%(asctime)s] %(levelname)s\033[0m: %(message)s\033[0m"
    )

    # Actual formats used by the logger.
    FORMATS = {
        logging.DEBUG: GREY + MESSAGE_FORMAT,
        logging.INFO: GREY + MESSAGE_FORMAT,
        logging.WARNING: YELLOW + MESSAGE_FORMAT,
        logging.ERROR: RED + MESSAGE_FORMAT,
        logging.CRITICAL: RED + MESSAGE_FORMAT,
    }

    def format(self, record):
        logging_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(logging_fmt)

        return formatter.format(record)
