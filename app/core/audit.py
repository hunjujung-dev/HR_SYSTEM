from datetime import datetime

import logging

logger = logging.getLogger("HR_SYSTEM")


class Audit:

    @staticmethod
    def write(user, action, table, key):

        logger.info(

            "[%s] %s %s (%s)",

            datetime.now(),

            user,

            action,

            f"{table}:{key}"

        )
