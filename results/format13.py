import pandas as pd
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.shared import Pt, RGBColor
import uuid
import os
import uuid
class f13:
    def __init__(self,request_data,shift,year,faculty_name,semester,section):
        course = request_data["course"]
        self.course = course
        self.shift = shift
        self.semester = semester
        self.section = section
        year = request_data["year"]
        subject = request_data["subject"]
        self.df = request_data["df"]
        last_three_columns = self.df.columns[-3:]
        self.df.dropna(inplace=True)
        self.df.sort_values(by=last_three_columns[-3],ascending=True,inplace=True)
        self.df.insert(0, 'S.No.', range(1, 1 + len(self.df)))
        print('df:',self.df.columns)
        self.subject_name = " ".join(self.df.columns[-1].split(" ")[:-1])
        print('subject_name:',self.subject_name)
        self.file_name = str(uuid.uuid4())
        self.faculty_name = faculty_name
        self.shift = shift
        self.result_year = year
        roman_map = {
            1: 'I',
            2: 'II',
            3: 'III',
            4: 'IV',
            5: 'V',
            6: 'VI',
            7: 'VII',
            8: 'VIII',
            9: 'IX',
            10: 'X'
        }
        self.semester_roman = roman_map[int(semester)]
        enrollment_series = self.df.iloc[:,1]
        str_enrollment_series = f"{int(enrollment_series):011d}"
        df['Enrollment No.'] = str_enrollment_series


    def write_to_doc(self):
        self.word_file_path = os.path.join(os.path.dirname(
            __file__), "buffer_files", f"{self.file_name}.docx")
        doc = Document()
        header_lines = [
            "",
            'MAHARAJA SURAJMAL INSTITUTE',
            f"DEPARTMENT OF _________________({self.shift})",
            f"                      {self.shift} Shift       MMM-MMM YYYY",
            f"Class:- {self.course} {self.semester_roman} Sec {self.section} Batch [yyyy-yyyy]",
            f"(Note: Student list is sorted in decreasing order based on internal marks)",
            f"Dr. {self.faculty_name}",
            f" "
        ]
        footer_lines = [f"Faculty                         Result Analysis Committee	             HOD,{self.course} ({self.shift})",
                        f"Dr. ABC"]
        for line in header_lines:
            paragraph = doc.add_heading(line)
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        for paragraph in doc.paragraphs:
            paragraph_format = paragraph.paragraph_format
            paragraph_format.space_before = Pt(0)
            for run in paragraph.runs:
                font = run.font
                font.name = 'Times New Roman'
                font.size = Pt(
                    20) if paragraph.text == 'Maharaja Surajmal Institute' else Pt(14)
                font.size = Pt(12) if "(Note:" in paragraph.text else Pt(14)
                font.bold = True
                font.color.rgb = RGBColor(0, 0, 0)
        doc.add_table(rows=self.df.shape[0]+2, cols=self.df.shape[1])
        table = doc.tables[0]
        table.style = 'TableGrid'
        table.cell(0, 0).merge(table.cell(1, 0)).text = "S.No."
        table.cell(0, 1).merge(table.cell(1,1)).text = "Enrollment No."
        table.cell(0, 2).merge(table.cell(1,2)).text = "Name"
        table.cell(0, 3).merge(table.cell(0,5)).text =  self.subject_name
        table.cell(1,3).text = "Int"
        table.cell(1,4).text = "Ext"
        table.cell(1,5).text = "Total"
        sno = list(self.df.iloc[:,0])
        print(sno)
        enroll_no = list(self.df.iloc[:,1])
        name = list(self.df.iloc[:,2])
        int_marks = list(self.df.iloc[:,-3])
        ext_marks = list(self.df.iloc[:,-2])
        total_marks = list(self.df.iloc[:,-1])
        for i in range(self.df.shape[0]):
            table.cell(i+2,0).text = str(sno[i])
            table.cell(i+2,1).text = str(enroll_no[i])
            table.cell(i+2,2).text = str(name[i])
            table.cell(i+2,3).text = str(int_marks[i])
            table.cell(i+2,4).text = str(ext_marks[i])
            table.cell(i+2,5).text = str(total_marks[i])


        for row in table.rows:
                    for cell in row.cells:
                        paragraphs = cell.paragraphs
                        for paragraph in paragraphs:
                            paragraph_format = paragraph.paragraph_format
                            paragraph_format.space_before = Pt(0)
                            paragraph_format.space_after = Pt(0)
                            paragraph_format.line_spacing = 1
                            paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
                            for run in paragraph.runs:
                                font = run.font
                                font.name = 'Times New Roman'
                                font.size = Pt(11)
                                font.bold = True
                                font.color.rgb = RGBColor(0, 0, 0)

        doc.add_paragraph()



        for line in footer_lines:
            paragraph = doc.add_heading(line)
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

        for paragraph in doc.paragraphs:
            paragraph_format = paragraph.paragraph_format
            paragraph_format.space_before = Pt(0)
            for run in paragraph.runs:
                font = run.font
                font.name = 'Times New Roman'
                font.size = Pt(
                    20) if paragraph.text == 'MAHARAJA SURAJMAL INSTITUTE' else Pt(14)
                font.bold = True
                if paragraph.text == 'Class-wise Result Analysis':
                    font.underline = True
                font.color.rgb = RGBColor(0, 0, 0)

        
        doc.save(self.word_file_path)
        return f"{self.file_name}"

