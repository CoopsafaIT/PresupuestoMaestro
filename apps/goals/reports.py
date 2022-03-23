from datetime import datetime as dt
from django.http import HttpResponse
from openpyxl import Workbook, load_workbook
from openpyxl.utils.exceptions import InvalidFileException


def generate_subsidiary_goal_excel_file(data, qs):
    wb = Workbook()
    ws = wb.active
    ws['A1'] = 'Identificador'
    ws['B1'] = 'Meta'
    ws['C1'] = 'Filial'
    ws['D1'] = 'Total meta anual'
    ws['E1'] = 'Ene'
    ws['F1'] = 'Feb'
    ws['G1'] = 'Mar'
    ws['H1'] = 'Abr'
    ws['I1'] = 'May'
    ws['J1'] = 'Jun'
    ws['K1'] = 'Jul'
    ws['L1'] = 'Ago'
    ws['M1'] = 'Sep'
    ws['N1'] = 'Oct'
    ws['O1'] = 'Nov'
    ws['P1'] = 'Dic'
    ws['Q1'] = 'Ponderación'

    x = 2
    for item in data:
        ws[f'A{x}'].value = item.pk
        ws[f'B{x}'].value = item.id_goal.description
        ws[f'C{x}'].value = f'{item.id_cost_center.zone} | {item.id_cost_center}'
        ws[f'D{x}'].value = item.annual_amount_subsidiary
        ws[f'E{x}'].value = item.amount_january
        ws[f'F{x}'].value = item.amount_february
        ws[f'G{x}'].value = item.amount_march
        ws[f'H{x}'].value = item.amount_april
        ws[f'I{x}'].value = item.amount_may
        ws[f'J{x}'].value = item.amount_june
        ws[f'K{x}'].value = item.amount_july
        ws[f'L{x}'].value = item.amount_august
        ws[f'M{x}'].value = item.amount_september
        ws[f'N{x}'].value = item.amount_october
        ws[f'O{x}'].value = item.amount_november
        ws[f'P{x}'].value = item.amount_december
        ws[f'Q{x}'].value = item.ponderation
        x = x + 1

    file_name = f'formato_metas_filial_{dt.now()}'
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={file_name}.xlsx'
    wb.save(response)
    return response


def load_excel_file(file):
    try:
        book = load_workbook(file, data_only=True)
        sheet_list = book.sheetnames
        first_sheet = book.get_sheet_by_name(sheet_list[0])
        number_rows = first_sheet.max_row
        return {
            'status': 'ok',
            'sheet': first_sheet,
            'number_rows': number_rows
        }
    except InvalidFileException as e:
        raise InvalidFileException(
            f'Error loading excel file: {e.__str__()}'
        )
