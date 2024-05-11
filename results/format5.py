from openpyxl import Workbook
import pandas as pd
from openpyxl.styles import Font
from openpyxl.styles import Font, Alignment, Border, Side
import os
import uuid


class f5:

    def __init__(self,reqdata):
        self.course = reqdata["course"]
        self.shift = reqdata["shift"]
        self.passout_year = reqdata["passout_year"]
        self.file_name = str(uuid.uuid4())
        self.path = os.path.join(os.path.dirname(
            __file__), "buffer_files", f"{self.file_name}.xlsx")
        self.sems = len(reqdata["data"].values())
        self.dataframes = [i for i in reqdata["data"].values()]
        self.no_of_students = 3  # todo: get the number of students from the dataframe
        self.sem_map = {
            1: 'I',
            2: 'II',
            3: 'III',
            4: 'IV',
            5: 'V',
            6: 'VI',
            7: 'VII',
            8: 'VIII'
        }

    def format(self):

        wb = Workbook()
        ws = wb.active

        ws['A1'] = 'Maharaja Surajmal Institute'
        ws['A2'] = 'Department of Computer Application'
        ws['A3'] = 'SECOND SHIFT'
        ws['A4'] = 'BCA Section-'
        ws['A5'] = 'Batch: 2017-20'
        for i in range(1, 6):
            ws.cell(row=i, column=1).alignment = Alignment(horizontal='center')
            ws.merge_cells(start_row=i, start_column=1,
                           end_row=i, end_column=12)
        ws['A8'] = 'S.No.'
        ws['B8'] = 'Enrollment No.'
        ws['C8'] = 'Name of the Student'
        ws['D8'] = 'X %'
        ws['E8'] = 'XII %'
        ws['F8'] = 'Aggregate % of X and XII'
        ws['G8'] = 'Category'
        for i in range(1, self.sems*2+1, 2):
            ws.cell(row=8, column=7+i).value = f'{self.sem_map[(i+1)//2]} Sem%'
            ws.cell(row=8, column=8+i).value = 'Category'
        for i in range(1, 8+self.sems*2+4):
            for j in range(self.no_of_students+1):
                ws.cell(row=8+j, column=i).border = Border(
                    top=Side(style='thin'), bottom=Side(style='thin'), left=Side(style='thin'), right=Side(style='thin'))
        ptr = self.sems*2+7
        ws.cell(row=8, column=ptr +
                1).value = f'Aggregate of {str(",".join(self.sem_map[i] for i in range(1,self.sems+1)))} '
        ws.cell(row=8, column=ptr+2).value = 'Category'
        ws.cell(row=8, column=ptr+3).value = 'Reappear Paper Codes'
        ws.cell(row=8, column=ptr+4).value = 'Absent Paper Codes'
        ptr += 6
        ws.cell(row=8, column=ptr).value = 'Percentage'
        ws.cell(row=8, column=ptr+1).value = 'category'
        for i in range(ptr, ptr+2):
            for j in range(7):
                ws.cell(row=8+j, column=i).border = Border(
                    top=Side(style='thin'), bottom=Side(style='thin'), left=Side(style='thin'), right=Side(style='thin'))
        ws.cell(row=9, column=ptr).value = '>=90%'
        ws.cell(row=10, column=ptr).value = '75 to 89.99%'
        ws.cell(row=11, column=ptr).value = '60 to 74.99%'
        ws.cell(row=12, column=ptr).value = '50 to 59.99%'
        ws.cell(row=13, column=ptr).value = '40 to 49.99%'
        ws.cell(row=14, column=ptr).value = '<40%'
        ws.cell(row=9, column=ptr+1).value = 'O'
        ws.cell(row=10, column=ptr+1).value = 'A'
        ws.cell(row=11, column=ptr+1).value = 'B'
        ws.cell(row=12, column=ptr+1).value = 'C'
        ws.cell(row=13, column=ptr+1).value = 'D'
        ws.cell(row=14, column=ptr+1).value = 'Fail'
        start_row = 8
        end_row = 14
        end_col = ptr+1
        for i in range(start_row, end_row+1):
            for j in range(ptr, end_col+1):
                ws.cell(row=i, column=j).font = Font(color="FF0000")
        start_row = 12+self.no_of_students
        end_row = 12+self.no_of_students+7
        start_col = 3
        end_col = 4
        ws.cell(row=start_row-1, column=start_col).value = 'Summary Based on Columns'
        for i in range(start_row, end_row+1):
            for j in range(start_col, end_col+1):
                ws.cell(row=i, column=j).border = Border(
                    top=Side(style='thin'), bottom=Side(style='thin'), left=Side(style='thin'), right=Side(style='thin'))
        ws.cell(row=12+self.no_of_students, column=3).value = 'Category '
        ws.cell(row=12+self.no_of_students, column=4).value = 'No. of Students'
        ws.cell(row=12+self.no_of_students+1, column=3).value = 'O'
        ws.cell(row=12+self.no_of_students+2, column=3).value = 'A'
        ws.cell(row=12+self.no_of_students+3, column=3).value = 'B'
        ws.cell(row=12+self.no_of_students+4, column=3).value = 'C'
        ws.cell(row=12+self.no_of_students+5, column=3).value = 'D'
        ws.cell(row=12+self.no_of_students+6, column=3).value = 'Fail'
        ws.cell(row=12+self.no_of_students+7,
                column=3).value = 'No. of Absentees'
        wb.save(self.path)
        return f"{self.file_name}.xlsx"