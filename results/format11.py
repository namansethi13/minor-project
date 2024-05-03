import pandas as pd
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, RGBColor
import uuid
import os


class f11:
    def __init__(self, file_data, all_subjects, faculty_name, shift, semester, passing):
        self.file_data = file_data
        self.df = pd.DataFrame()
        self.faculty_name = faculty_name
        self.shift = shift
        self.all_subjects = all_subjects
        self.file_name = str(uuid.uuid4())
        self.semester = int(semester)
        if semester % 2 == 0:
            self.semester_month = "Jan-Jun"
        else:
            self.semester_month = "Jul-Dec"

    def write_to_doc(self):
        self.word_file_path = os.path.join(os.path.dirname(
            __file__), "buffer_files", f"{self.file_name}.docx")
        sub_count = sum_a = sum_b = failed = 0
        doc = Document()
        for section in doc.sections:

            section.left_margin = section.right_margin = Inches(0.2)

            section.top_margin = section.bottom_margin = Inches(0)

        header_lines = [
            "",
            'Maharaja Surajmal Institute',
            'Department of _______',
            'Date: …………',
            f"Faculty Name: - Dr. {self.faculty_name}                        Shift-{self.shift}                                Max Marks: 100 ",
            f"Result Analysis ({self.semester_month} YYYY)"
        ]

        for line in header_lines:
            paragraph = doc.add_heading(line)
            if line == 'Date: …………':
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
            elif line == 'Result Analysis (MMM-MMM YYYY)':
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            elif line == f"Faculty Name: - Dr. {self.faculty_name}                        Shift-{self.shift}                                Max Marks: 100 ":
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY_MED
            else:
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        for paragraph in doc.paragraphs:
            paragraph_format = paragraph.paragraph_format
            paragraph_format.space_before = Pt(0)
            for run in paragraph.runs:
                font = run.font
                font.name = 'Times New Roman'
                font.size = Pt(
                    20) if paragraph.text == 'Maharaja Surajmal Institute' else Pt(14)
                font.bold = True
                font.color.rgb = RGBColor(0, 0, 0)
        row_count = 0
        for dfname, data in self.file_data.items():
            for section, subjects in data["section-subject"].items():
                row_count += len(subjects)
        table = doc.add_table(rows=3+row_count, cols=14)
        table.style = 'TableGrid'
        first_row = ['S.No', 'Paper Code', 'Subjects Taught', 'Students Appeared', '', 'Passed', '', 'Pass%', '',
                     '>=90%', '', "89.99-75%", '', "74.99-60%", '', "59.99-50%", '', "49.99-40%", '', "<40%", '', "Highest Marks"]
        for i in range(len(first_row)):
            table.cell(0, i).text = first_row[i]

        for dfname, data in self.file_data.items():

            all_columns = data["all_columns"]
            result_df = data["result_df"]
            print("result df from the f1 file \n", result_df)

            for section, subjects in data["section-subject"].items():
                
        table.cell(row_count+1, 0).text = ""
        table.cell(row_count+1, 1).text = ""
        table.cell(row_count+1, 2).text = "Total Students & Pass %"
        table.cell(row_count+1, 3).text = str(sum_a+sum_b)
        table.cell(row_count+1, 4).text = str(sum_a+sum_b-failed)
        table.cell(
            row_count+1, 5).text = f"{(sum_a+sum_b-failed)/(sum_a+sum_b)*100:.2f}%"
        table.cell(
            row_count+1, 6).text = f"No. of students & average % above 60%{sum_a}\n({sum_a/(sum_a+sum_b)*100:.2f}%)"
        table.cell(row_count+1, 6).merge(table.cell(row_count+1, 8))
        table.cell(
            row_count+1, 9).text = f"No. of students & average % below 60%{sum_b}\n({sum_b/(sum_a+sum_b)*100:.2f}%)"
        table.cell(row_count+1, 9).merge(table.cell(row_count+1, 12))

        for i in range(0, row_count+3):
            for j in range(14):
                table.cell(
                    i, j).paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                for run in table.cell(i, j).paragraphs[0].runs:
                    font = run.font
                    font.name = 'Times New Roman'
                    font.size = Pt(10)
                    font.bold = True
                    font.color.rgb = RGBColor(0, 0, 0)

        footer_lines = [
            '',
            '“I do hereby solemnly affirm and declare that the facts stated in the above result are true to the best of my knowledge and belief”',
            f"""Dr.{self.faculty_name}    		                 (Dr.ABC)       				(Mr. ABC)	
Assistant Professor 		Convenor-Result Analysis Committee         	HOD-____"""
        ]
        for line in footer_lines:
            paragraph = doc.add_paragraph(line)
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            paragraph_format = paragraph.paragraph_format
            paragraph_format.space_before = Pt(0)
            for run in paragraph.runs:
                font = run.font
                font.name = 'Times New Roman'
                font.size = Pt(10)
                if line != '“I do hereby solemnly affirm and declare that the facts stated in the above result are true to the best of my knowledge and belief”':
                    font.bold = True
                font.color.rgb = RGBColor(0, 0, 0)
        doc.save(self.word_file_path)
        return f"{self.file_name}.docx"
