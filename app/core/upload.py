import os

import uuid


class Upload:

    @staticmethod
    def save(file, folder):

        ext = os.path.splitext(file.filename)[1]

        filename = str(uuid.uuid4()) + ext

        path = os.path.join(

            folder,

            filename

        )

        with open(path, "wb") as f:

            f.write(file.file.read())

        return filename