from sqlalchemy.orm import Query

from app.core.filter import Filter
from app.core.pagination import Pagination


class QueryBuilder:

    def __init__(self, query: Query):

        self.query = query

    ##################################################
    # contains
    ##################################################
    def contains(self, column, value):

        self.query = Filter.contains(
            self.query,
            column,
            value
        )

        return self

    ##################################################
    # equal
    ##################################################
    def equal(self, column, value):

        self.query = Filter.equal(
            self.query,
            column,
            value
        )

        return self

    ##################################################
    # between
    ##################################################
    def between(self, column, start, end):

        self.query = Filter.between(
            self.query,
            column,
            start,
            end
        )

        return self

    ##################################################
    # order
    ##################################################
    def order(self, column, order="ASC"):

        self.query = Filter.order(
            self.query,
            column,
            order
        )

        return self

    ##################################################
    # paging
    ##################################################
    def paging(self, page=1, size=20):

        return Pagination.make(
            self.query,
            page,
            size
        )

    ##################################################
    # all
    ##################################################
    def all(self):

        return self.query.all()