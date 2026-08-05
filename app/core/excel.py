
from openpyxl import Workbook


class Excel:

    @staticmethod
    def export(columns, rows):

        wb = Workbook()

        ws = wb.active

        ws.append(columns)

        for row in rows:

            ws.append(row)

        return wb

    @staticmethod
    def template(columns):

        wb = Workbook()

        ws = wb.active

        ws.append(columns)

        return wb