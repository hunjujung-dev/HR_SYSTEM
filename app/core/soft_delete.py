class SoftDelete:

    @staticmethod
    def delete(obj):

        if hasattr(obj, "use_yn"):

            obj.use_yn = "N"

            return True

        return False