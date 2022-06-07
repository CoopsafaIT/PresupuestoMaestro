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

    def _set_fomart_value(format):
        if format == 'Porcentaje':
            return '0.00%'
        elif format == 'Moneda':
            return '#,##0.00'
        else:
            return '#,##0'

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
        if index == len(months_labels) - 1:
            ponderation_letter = alphabet[index + 1]
            percentage_letter = alphabet[index + 2]
            accumulated_execution_letter = alphabet[index + 3]
            ws[f'{alphabet[index + 1]}1'] = "Ponderación"
            ws[f'{alphabet[index + 2]}1'] = "Porcentaje"
            ws[f'{alphabet[index + 3]}1'] = "Ejecución Acumulada"

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
    ws['Q1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['S1'].alignment = Alignment(horizontal="center", vertical="center")

    for counter, item in enumerate(data, start=2):
        i_format = _set_fomart_value(item.get('Formato'))
        ws[f'A{counter}'].value = item.get('DescAgencia')
        ws[f'B{counter}'].value = item.get('Nivel2')

        ws[f'C{counter}'].value = float(item.get('MetaAnual'))
        ws[f'C{counter}'].number_format = i_format
        ws[f'D{counter}'].value = float(item.get('MetaAlMes'))
        ws[f'D{counter}'].number_format = i_format

        if 'Enero' in months_labels:
            ws[f'E{counter}'].value = float(item.get('EneroEjecucion'))
            ws[f'E{counter}'].number_format = i_format
        if 'Febrero' in months_labels:
            ws[f'F{counter}'].value = float(item.get('FebreroEjecucion'))
            ws[f'F{counter}'].number_format = i_format
        if 'Marzo' in months_labels:
            ws[f'G{counter}'].value = float(item.get('MarzoEjecucion'))
            ws[f'G{counter}'].number_format = i_format
        if 'Abril' in months_labels:
            ws[f'H{counter}'].value = float(item.get('AbrilEjecucion'))
            ws[f'H{counter}'].number_format = i_format
        if 'Mayo' in months_labels:
            ws[f'I{counter}'].value = float(item.get('MayoEjecucion'))
            ws[f'I{counter}'].number_format = i_format
        if 'Junio' in months_labels:
            ws[f'J{counter}'].value = float(item.get('JunioEjecucion'))
            ws[f'J{counter}'].number_format = i_format
        if 'Julio' in months_labels:
            ws[f'K{counter}'].value = float(item.get('JulioEjecucion'))
            ws[f'K{counter}'].number_format = i_format
        if 'Agosto' in months_labels:
            ws[f'L{counter}'].value = float(item.get('AgostoEjecucion'))
            ws[f'L{counter}'].number_format = i_format
        if 'Septiembre' in months_labels:
            ws[f'M{counter}'].value = float(item.get('SeptiembreEjecucion'))
            ws[f'M{counter}'].number_format = i_format
        if 'Octubre' in months_labels:
            ws[f'N{counter}'].value = float(item.get('OctubreEjecucion'))
            ws[f'N{counter}'].number_format = i_format
        if 'Noviembre' in months_labels:
            ws[f'O{counter}'].value = float(item.get('NoviembreEjecucion'))
            ws[f'O{counter}'].number_format = i_format
        if 'Diciembre' in months_labels:
            ws[f'P{counter}'].value = float(item.get('DiciembreEjecucion'))
            ws[f'P{counter}'].number_format = i_format
        ws[f'{ponderation_letter}{counter}'].value = float(item.get('Ponderacion'))
        ws[f'{ponderation_letter}{counter}'].number_format = _set_fomart_value('Cantidad')

        ws[f'{percentage_letter}{counter}'].value = float(item.get("Porcentaje"))
        ws[f'{percentage_letter}{counter}'].number_format = _set_fomart_value('Porcentaje')

        ws[f'{accumulated_execution_letter}{counter}'].value = float(item.get("EjecucionAcumulada")) # NOQA
        ws[f'{accumulated_execution_letter}{counter}'].number_format = i_format

    file_name = f'reporte_{dt.now()}'
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={file_name}.xlsx'
    wb.save(response)
    return response
