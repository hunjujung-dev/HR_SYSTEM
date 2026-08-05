from sqlalchemy import asc
from sqlalchemy import desc


class Filter:

    @staticmethod
    def contains(query,column,value):

        if value:

            query=query.filter(

                column.contains(value)

            )

        return query

    @staticmethod
    def equal(query,column,value):

        if value is not None:

            query=query.filter(

                column==value

            )

        return query

    @staticmethod
    def between(query,column,start,end):

        if start:

            query=query.filter(

                column>=start

            )

        if end:

            query=query.filter(

                column<=end

            )

        return query

    @staticmethod
    def order(query,column,order):

        if order=="DESC":

            return query.order_by(

                desc(column)

            )

        return query.order_by(

            asc(column)

        )