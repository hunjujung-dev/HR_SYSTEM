from math import ceil


class Pagination:

    @staticmethod
    def make(query, page=1, size=20):

        total = query.count()

        items = query.offset(

            (page-1)*size

        ).limit(size).all()

        return {

            "page": page,

            "size": size,

            "total": total,

            "pages": ceil(total/size),

            "items": items

        }