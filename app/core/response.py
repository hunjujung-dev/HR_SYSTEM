from fastapi.responses import JSONResponse


class Response:

    @staticmethod
    def ok(message="OK"):

        return JSONResponse({
            "success": True,
            "message": message,
            "data": None
        })

    @staticmethod
    def data(data, message="OK"):

        return JSONResponse({
            "success": True,
            "message": message,
            "data": data
        })

    @staticmethod
    def fail(message):

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": message,
                "data": None
            }
        )