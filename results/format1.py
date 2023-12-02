import pandas as pd
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, RGBColor
import uuid


class f1:
    def __init__(self, file_data,all_subjects,faculty_name,shift):
        self.file_data = file_data
        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.all_subjects=all_subjects
        self.faculty_name=faculty_name
        self.shift=shift
        self.file_name = str(uuid.uuid4())
        if self.shift == 1:
            self.shift = "I"
        else:
            self.shift = "II"
        # self.all_subjects = {
        #     '020102': 'Applied Maths',
        #         '020104': 'Web Based Programming',
        #         '020106': 'Data Structures & Algorithm Using C',
        #         '020108': 'DBMS',
        #         '020110': 'EVS',
        #         '020136': 'SAUE',
        #         '020172': 'Practical IV-WBP Lab',
        #         '020174': 'Practical- V DS Lab',
        #         '020176': 'Practical- VI DBMS Lab',
        #         '020202': 'Computer Networks',
        #         '020204': 'Operating Systems',
        #         '020206': 'Computer Graphics',
        #         '020208': 'Software Engineering',
        #         '020210': 'Business Communication',
        #         '020236': 'SAUE',
        #         '020272': 'Practical- VII CN Lab',
        #         '020274': 'Practical- VIII OS Lab',
        #         '020276': 'Practical- IX CG Lab',
        #         }

    def process_data(self,subjects):
        for file_name, column_names in self.file_data.items():
            df1 = pd.read_excel(file_name, skiprows=5)
            df1 = df1.iloc[:-10, 3:-4]
            
            df1 = df1[df1.iloc[:, 0].isin(column_names)]
            df1 = df1.iloc[:, [i for i in range(0, len(df1.columns), 3)]]

            df1.columns = column_names

            self.df = pd.concat([self.df, df1], ignore_index=True, sort=False)
        self.df = self.df[subjects]
        self.df.to_excel('f1.xlsx', index=False)
    def read_from_filtered_excel(self, course_name, subject_code):

    # Assuming the column you want to work with is named 'YourColumnName'
        index=0
        column_names = list()
        sum_a = sum_b = 0
        for i in range(len(subject_code)):
            column_names.append(
                subject_code[i]+" "+self.all_subjects[subject_code[i]]+" (Total)")

        for i, column_name in enumerate(column_names):
            self.filtered_df.at[i, 'S.No'] = f'{i+1:.0f}'
            self.filtered_df.at[i, 'Paper Code'] = str(
                course_name[i] + str(column_name[3:6]))
            index+=1
            self.filtered_df.at[i, 'Subjects Taught'] = str(
                column_name[7:-8])

            non_empty_values = self.df[column_name[0:6]].dropna()

            total_students = non_empty_values.shape[0]
            self.filtered_df.at[i, 'Students Appeared'] = f'{total_students:.0f}'

            passed_students = non_empty_values[non_empty_values >= 40].shape[0]
            self.filtered_df.at[i, 'Passed'] = f'{passed_students:.0f}'
            self.filtered_df.at[i, 'Pass %'] = f"{(passed_students / total_students) * 100:.2f}"

            countA1 = non_empty_values[non_empty_values >= 90].shape[0]
            countA2 = non_empty_values[(non_empty_values >= 75) & (non_empty_values <= 89)].shape[0]
            countA3 = non_empty_values[(non_empty_values >= 60) & (non_empty_values <= 74)].shape[0]
            sum_a += countA1 + countA2 + countA3

            countB1 = non_empty_values[(non_empty_values >= 50) & (non_empty_values <= 59)].shape[0]
            countB2 = non_empty_values[(non_empty_values >= 40) & (non_empty_values <= 49)].shape[0]
            countB3 = non_empty_values[(non_empty_values >= 1) & (non_empty_values <= 39)].shape[0]
            sum_b += countB1 + countB2 + countB3
            self.filtered_df.at[i, '>=90%'] = str(
                f"{countA1}\n({countA1 / total_students * 100:.2f})")
            self.filtered_df.at[i,
                                '89.99 - 75%'] = f"{countA2}\n({countA2 / total_students * 100:.2f})"
            self.filtered_df.at[i,
                                '74.99 - 60%'] = f"{countA3}\n({countA3 / total_students * 100:.2f})"
            self.filtered_df.at[i,
                                '------------- 59.99 – 50%'] = f"{countB1}\n({countB1 / total_students * 100:.2f})"
            self.filtered_df.at[i,
                                '----B------ 49.99-40%'] = f"{countB2}\n({countB2 / total_students * 100:.2f})"
            self.filtered_df.at[i,
                                '----------<40%'] = f"{countB3}\n({countB3 / total_students * 100:.2f})"
            self.filtered_df.at[i,
                                'C=B-A'] = f'{(countB1+countB2+countB3-countA1):.0f}'
            self.filtered_df.at[i,
                                'Highest Marks'] = f'{self.df[column_name[0:6]].max():.0f}'
            print(self.filtered_df)

        second_last_row = pd.Series({
            "S.No": "",
            "Paper Code": "",
            "Subjects Taught": "Total Students & Pass %",
            "Students Appeared": (self.filtered_df["Students Appeared"].astype(int)).sum(),
            "Passed": (self.filtered_df["Passed"].astype(int)).sum(),
            "Pass %": f'{((self.filtered_df["Passed"].astype(int)).sum() / (self.filtered_df["Students Appeared"].astype(int)).sum()) * 100:.2f}',
            '>=90%': f"No. of Students and average %age above 60% {sum_a} ({sum_a / (self.filtered_df['Students Appeared'].astype(int)).sum() * 100:.2f}))",
            "89.99 - 75%": "",
            "74.99 - 60%": "",
            "------------- 59.99 – 50%": f"No. of Students and average %age below 60% {sum_b} ({sum_b / (self.filtered_df['Students Appeared'].astype(int)).sum() * 100:.2f}))",
            "----B------ 49.99-40%": "",
            "----------<40": "",
            "C=B-A": "",
            "Highest Marks": "",
        })
        last_row = pd.Series({
            "S.No": "",
            "Paper Code": "*Relaxation of 2% in addition to C who are regular and punctual during teaching\ndays from 2Aug-9Nov (availed upto 6 leave) excluding the time period of mid-term\nexams from 8Oct.-13Oct.18*\nThis has been shifted to pt. 4 of Faculty Performance criterion.",
            "Subjects Taught": "",
            "Students Appeared": "",
            "Passed": "",
            "Pass %": "",
            '>=90%': "",
            "89.99 - 75%": "",
            "74.99 - 60%": "",
            "------------- 59.99 – 50%": "",
            "----B------ 49.99-40%": "",
            "----------<40%": "",
            "C=B-A": "",
            "Highest Marks": "",
        })

# Append the new row to the DataFrame
        self.filtered_df = self.filtered_df._append(
            second_last_row, ignore_index=True)
        self.filtered_df = self.filtered_df._append(
            last_row, ignore_index=True)
        print(self.filtered_df)
    def write_to_doc(self):
        self.word_file_path = f"results/buffer_files/{self.file_name}.docx"
        excel_data_df = self.filtered_df
        doc = Document()
        for section in doc.sections:

            section.left_margin = section.right_margin = Inches(0.4)

            section.top_margin = section.bottom_margin = Inches(0)

        # Add lines to the header
        header_lines = [
            "",
            'Maharaja Surajmal Institute',
            'Department of _______',
            'Date: …………',
            f"Faculty Name: - Dr. {self.faculty_name}                        Shift-{self.shift}                                Max Marks: 100 ",
            'Result Analysis (MMM-MMM YYYY)'
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


        # Set the font to Times New Roman
        for paragraph in doc.paragraphs:
            paragraph_format = paragraph.paragraph_format
            paragraph_format.space_before = Pt(0)
            for run in paragraph.runs:
                font = run.font
                font.name = 'Times New Roman'
                font.size = Pt(
                    20) if paragraph.text == 'Maharaja Surajmal Institute' else Pt(14)
                font.bold = True
                font.color.rgb = RGBColor(0, 0, 0)  # RGB values for black

        doc.add_table(
            excel_data_df.shape[0]+1, excel_data_df.shape[1], style='Table Grid')
        table = doc.tables[0]
        # add the header rows.
        for j in range(excel_data_df.shape[-1]):
            cell = table.cell(0, j)
            cell.text = excel_data_df.columns[j]
            cell.paragraphs[0].runs[0].bold = True
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(10)

# Add the rest of the data frame with bold, Times New Roman, and text size 10

        for i in range(excel_data_df.shape[0]):
            for j in range(excel_data_df.shape[-1]):
                cell = table.cell(i+1, j)
                cell.text = str(excel_data_df.values[i, j])
                cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
                cell.paragraphs[0].runs[0].font.size = Pt(10)
                cell.paragraphs[0].runs[0].bold = True
                cell.paragraphs[0].runs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        def merge_cells(table, start_row, start_col, end_row, end_col):
            for row in range(start_row, end_row + 1):
                for col in range(start_col, end_col + 1):
                    cell = table.cell(row, col)
                    if row == start_row and col == start_col:
                        continue  # Skip the first cell, as it will be the merged cell
                    cell.text = cell.text.strip()

    # Merge the cells
            table.cell(start_row, start_col).merge(
                table.cell(end_row, end_col))


# Specify the range of cells to merge (indices are zero-based)
        merge_cells(table, start_row=len(self.filtered_df)-1, start_col=6,
                    end_row=len(self.filtered_df)-1, end_col=8)  # Merging columns 7 to 9
        merge_cells(table, start_row=len(self.filtered_df)-1, start_col=9,
                    end_row=len(self.filtered_df)-1, end_col=12)  # Merging columns 10 to 13
        merge_cells(table, start_row=len(self.filtered_df), start_col=9, end_row=len(
            self.filtered_df), end_col=12)  # Merging columns 10 to 13
        merge_cells(table, start_row=len(self.filtered_df), start_col=1, end_row=len(
            self.filtered_df), end_col=8)  # Merging columns 14 to 15
# Add the footer
        footer_lines = [
            "",
            f'C= No. of Students securing 90 or above is deducted from the total no. of students securing below 60 marks and accordingly the %age below 60% (aggregate) is computed ',
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
                font.color.rgb = RGBColor(0, 0, 0)  # RGB values for black

        doc.save(self.word_file_path)
        return f"{self.file_name}.docx"


# Example usage:
file_data = {
    "sem2.xlsx": ["B", '020102', '020104', '020106', '020108', '020110', '020136', '020172', '020174', '020176'],
    "sem3.xlsx": ["A", '020202', '020204', '020206', '020208', '020210', '020236', '020272', '020274']
}
subjects=["020102", '020104', '020106', "020202", '020204']
# 
# f1.process_data(subjects=subjects)
# f1.read_from_filtered_excel(course_name="BCA", subject_code=subjects)
# f1.write_to_doc()


