"""
Excel Worksheet remover

Arguments:
Arg1 : Excel File Name
Arg2: No of worksheets that needs to be deleted
"""
import openpyxl
import sys


def worksheet_remove(excel_file, no_of_sheet):
    workbook = openpyxl.load_workbook(excel_file)
    sheets = workbook.get_sheet_names()

    if len(sheets) < no_of_sheet:
        print("Excel file has less than {} worksheets".format(no_of_sheet))
        return False
    else:
        for sh in sheets[:no_of_sheet]:
            workbook.remove_sheet(workbook.get_sheet_by_name(sh))
    workbook.save(excel_file)
    print("successfully removed starting {} worksheets from the excel file".format(no_of_sheet))
    return excel_file
