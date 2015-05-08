import logging


class LoggerUtil():

    @staticmethod
    def get_logger(name=None, level=logging.DEBUG):
        work_logger = logging.getLogger(name)
        work_logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')
        ch.setFormatter(formatter)

        work_logger.addHandler(ch)

        return work_logger