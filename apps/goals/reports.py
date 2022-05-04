from string import ascii_uppercase
from datetime import datetime as dt
from django.http import HttpResponse
from openpyxl import Workbook, load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.styles.alignment import Alignment


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


def generate_subsidiary_goal_execute_excel_file(data, qs):
    wb = Workbook()
    ws = wb.active
    ws['A1'] = 'Identificador'
    ws['B1'] = 'Meta'
    ws['C1'] = 'Filial'
    ws['D1'] = 'Ene'
    ws['E1'] = 'Feb'
    ws['F1'] = 'Mar'
    ws['G1'] = 'Abr'
    ws['H1'] = 'May'
    ws['I1'] = 'Jun'
    ws['J1'] = 'Jul'
    ws['K1'] = 'Ago'
    ws['L1'] = 'Sep'
    ws['M1'] = 'Oct'
    ws['N1'] = 'Nov'
    ws['O1'] = 'Dic'

    x = 2
    for item in data:
        ws[f'A{x}'].value = item.pk
        ws[f'B{x}'].value = item.id_goal.description
        ws[f'C{x}'].value = f'{item.id_cost_center.zone} | {item.id_cost_center}'
        ws[f'D{x}'].value = item.amount_exec_january
        ws[f'E{x}'].value = item.amount_exec_february
        ws[f'F{x}'].value = item.amount_exec_march
        ws[f'G{x}'].value = item.amount_exec_april
        ws[f'H{x}'].value = item.amount_exec_may
        ws[f'I{x}'].value = item.amount_exec_june
        ws[f'J{x}'].value = item.amount_exec_july
        ws[f'K{x}'].value = item.amount_exec_august
        ws[f'L{x}'].value = item.amount_exec_september
        ws[f'M{x}'].value = item.amount_exec_october
        ws[f'N{x}'].value = item.amount_exec_november
        ws[f'O{x}'].value = item.amount_exec_december
        x = x + 1

    file_name = f'formato_ejecucion_metas_filial_{dt.now()}'
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


def generate_report_by_subsidiary(data, months_labels):

    def _set_fomart_value(value, format):
        value = value or 0
        if format == 'Porcentaje':
            new_value = value * 100
            return '{:.2f}%'.format(new_value)
        value = float('{:.2f}'.format(value))
        return '{:,}'.format(value)
    alphabet = list(ascii_uppercase)
    alphabet.remove('A')
    alphabet.remove('B')
    alphabet.remove('C')
    alphabet.remove('D')

    wb = Workbook()
    ws = wb.active
    ws['A1'] = 'Filial'
    ws['B1'] = 'Descripción'
    ws['C1'] = 'Meta Anual'
    ws['D1'] = 'Meta Al Mes'
    for index, value in enumerate(months_labels, start=0):
        ws[f'{alphabet[index]}1'] = value

    ws['A1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['B1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['C1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['D1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['E1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['F1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['G1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['H1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['I1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['J1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['K1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['L1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['M1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['N1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['O1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['P1'].alignment = Alignment(horizontal="center", vertical="center")

    for counter, item in enumerate(data, start=2):
        ws[f'A{counter}'].value = item.get('DescAgencia')
        ws[f'B{counter}'].value = item.get('Nivel2')
        ws[f'C{counter}'].value = _set_fomart_value(item.get('MetaAnual'), item.get('Formato')) # NOQA
        ws[f'D{counter}'].value = _set_fomart_value(item.get('MetaAlMes'), item.get('Formato')) # NOQA
        if 'Enero' in months_labels:
            ws[f'E{counter}'].value = _set_fomart_value(item.get('EneroEjecucion'), item.get('Formato')) # NOQA
        if 'Febrero' in months_labels:
            ws[f'F{counter}'].value = _set_fomart_value(item.get('FebreroEjecucion'), item.get('Formato')) # NOQA
        if 'Marzo' in months_labels:
            ws[f'G{counter}'].value = _set_fomart_value(item.get('MarzoEjecucion'), item.get('Formato')) # NOQA
        if 'Abril' in months_labels:
            ws[f'H{counter}'].value = _set_fomart_value(item.get('AbrilEjecucion'), item.get('Formato')) # NOQA
        if 'Mayo' in months_labels:
            ws[f'I{counter}'].value = _set_fomart_value(item.get('MayoEjecucion'), item.get('Formato')) # NOQA
        if 'Junio' in months_labels:
            ws[f'J{counter}'].value = _set_fomart_value(item.get('JunioEjecucion'), item.get('Formato')) # NOQA
        if 'Julio' in months_labels:
            ws[f'K{counter}'].value = _set_fomart_value(item.get('JulioEjecucion'), item.get('Formato')) # NOQA
        if 'Agosto' in months_labels:
            ws[f'L{counter}'].value = _set_fomart_value(item.get('AgostoEjecucion'), item.get('Formato')) # NOQA
        if 'Septiembre' in months_labels:
            ws[f'M{counter}'].value = _set_fomart_value(item.get('SeptiembreEjecucion'), item.get('Formato')) # NOQA
        if 'Octubre' in months_labels:
            ws[f'N{counter}'].value = _set_fomart_value(item.get('OctubreEjecucion'), item.get('Formato')) # NOQA
        if 'Noviembre' in months_labels:
            ws[f'O{counter}'].value = _set_fomart_value(item.get('NoviembreEjecucion'), item.get('Formato')) # NOQA
        if 'Diciembre' in months_labels:
            ws[f'P{counter}'].value = _set_fomart_value(item.get('DiciembreEjecucion'), item.get('Formato')) # NOQA

    file_name = f'reporte_{dt.now()}'
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={file_name}.xlsx'
    wb.save(response)
    return response
