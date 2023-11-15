import pandas as pd
from openpyxl import load_workbook

class ResultProcessor:

    exclude_columns = [
        'SAUE (Internal)',
    ]

    # exclude_subject_code = "20136"
    exclude_subject_code = ""
    subject_name_mapping = {}
    # subject_name_mapping = {
    #     '020102(4)': 'Applied Maths (Internal)',
    #     '020102(4).1': 'Applied Maths (External)',
    #     '020102(4).2': 'Applied Maths (Total)',
    #     '020104(4)': 'Web Based Programming (Internal)',
    #     '020104(4).1': 'Web Based Programming (External)',
    #     '020104(4).2': 'Web Based Programming (Total)',
    #     '020106(4)': 'Data Structures & Algorithm Using C (Internal)',
    #     '020106(4).1': 'Data Structures & Algorithm Using C (External)',
    #     '020106(4).2': 'Data Structures & Algorithm Using C (Total)',
    #     '020108(4)': 'DBMS (Internal)',
    #     '020108(4).1': 'DBMS (External)',
    #     '020108(4).2': 'DBMS (Total)',
    #     '020110(2)': 'EVS (Internal)',
    #     '020110(2).1': 'EVS (External)',
    #     '020110(2).2': 'EVS (Total)',
    #     '020136(2)': 'SAUE (Internal)',
    #     '020136(2).1': 'SAUE (External)',
    #     '020136(2).2': 'SAUE (Total)',
    #     '020172(2)': 'Practical IV-WBP Lab (Internal)',
    #     '020172(2).1': 'Practical IV-WBP Lab (External)',
    #     '020172(2).2': 'Practical IV-WBP Lab (Total)',
    #     '020174(2)': 'Practical- V DS Lab (Internal)',
    #     '020174(2).1': 'Practical- V DS Lab (External)',
    #     '020174(2).2': 'Practical- V DS Lab (Total)',
    #     '020176(2)': 'Practical- VI DBMS Lab (Internal)',
    #     '020176(2).1': 'Practical- VI DBMS Lab (External)',
    #     '020176(2).2': 'Practical- VI DBMS Lab (Total)',
    # }


    def __init__(self, input_file, output_file , subject_name_mapping, exclude_subject_code):
        self.exclude_subject_code = exclude_subject_code
        self.subject_name_mapping = subject_name_mapping
        self.input_file = input_file
        self.output_file = output_file
        self.df = None
    
    def read_data(self):
        # Read the CSV file
        self.df = pd.read_csv(self.input_file)

    def rename_columns(self):
        # Rename the columns using the subject_name_mapping
        self.df.rename(columns=self.subject_name_mapping, inplace=True)
    
    def process_reappear(self):
        self.df['Reappear'] = ''

        def is_numeric(value):
            try:
                int(value)
                return True
            except ValueError:
                return False

        def filter_reappear(row):
            return ', '.join(set([col.split('(')[0].strip() for col in self.df.columns[3:-2]
                                  if 'Total' in col and is_numeric(row[col]) and int(row[col].strip()) < 40 and int(row[col].strip()) >= 1
                                  and col not in self.exclude_columns
                                  and self.exclude_subject_code not in col
                                  and not any(row[col].strip() == 'Absent' for col in self.df.columns[3:-2]
                                              if 'External' in col and col not in self.exclude_columns
                                              and self.exclude_subject_code not in col) and row[col] != '0']))  # Only include non-zero values

        self.df['Reappear'] = self.df.apply(filter_reappear, axis=1)

    
    def process_absents(self):
        self.df['Absent'] = ''

        def filter_absent(row):
            return ', '.join(set([col.split('(')[0].strip() for col in self.df.columns[3:-2]
                                  if 'External' in col and row[col].strip() == '0' and col not in self.exclude_columns
                                  and self.exclude_subject_code not in col]))

        self.df['Absent'] = self.df.apply(filter_absent, axis=1)

    def _calculate_cgpa(self):
        # Initialize CGPA as a floating-point number
        self.df['CGPA'] = 0.0

        credits_mapping = {
            'Applied Maths (Total)': 4,
            'Web Based Programming (Total)': 4,
            'Data Structures & Algorithm Using C (Total)': 4,
            'DBMS (Total)': 4,
            'EVS (Total)': 2,
            'SAUE (Total)': 2,
            'Practical IV-WBP Lab (Total)': 2,
            'Practical- V DS Lab (Total)': 2,
            'Practical- VI DBMS Lab (Total)': 2,
        }

        # Loop through the columns and update CGPA
        for subject, credits in credits_mapping.items():
            self.df['CGPA'] += self.df.apply(lambda row: (float(row[subject]) * credits)
                                             if row[subject] and str(row[subject]).strip().isdigit() else 0, axis=1)

        # Calculate CGPA as the sum divided by the total credits
        total_credits = sum(credits_mapping.values())
        self.df['CGPA'] /= total_credits
        self.df['CGPA'] = self.df['CGPA'].round(5)


    def save_result(self):
        # Save the DataFrame to a new Excel file, excluding the header rows
        saved_file = self.df.iloc[3:].to_excel( self.output_file, index=False, sheet_name='ResultSheet', engine='xlsxwriter')
        return saved_file

    def add_headers_to_excel(self, headers):
        # Load the existing workbook
        workbook = load_workbook(self.output_file)

    # Get the active sheet
        sheet = workbook.active

    # Shift existing rows down to make space for headers
        # Add one additional row for separation
        sheet.insert_rows(1, amount=len(headers) + 1)

    # Write headers to the sheet
        for i, header_row in enumerate(headers):
            for j, header_value in enumerate(header_row, start=1):
                sheet.cell(row=i + 1, column=j, value=header_value)

    # Save the modified workbook
        workbook.save(self.output_file)
    def update_reappear_absent_columns(self):
    # Split the "Reappear" and "Absent" column values into a list of subjects for each row
        reappear_lists = self.df['Reappear'].apply(lambda x: x.split(', ') if pd.notna(x) else [])
        absent_lists = self.df['Absent'].apply(lambda x: x.split(', ') if pd.notna(x) else [])

    # Find common subjects across all rows
        common_subjects = set.intersection(*map(set, reappear_lists.tolist() + absent_lists.tolist()))

    # Update "Reappear" and "Absent" columns
        def update_columns(row, column_name):
            return ', '.join([subject for subject in row if subject not in common_subjects])

        self.df['Reappear'] = reappear_lists.apply(lambda row: update_columns(row, 'Reappear'))
        self.df['Absent'] = absent_lists.apply(lambda row: update_columns(row, 'Absent'))

    def add_footers_to_excel(self, footer):
        # Load the existing workbook
        workbook = load_workbook(self.output_file)

    # Get the active sheet
        sheet = workbook.active

    # Calculate the starting row for appending the footer
        start_row = sheet.max_row + 2  # Add some additional space between data and footer

    # Write footer to the sheet
        for i, footer_row in enumerate(footer):
            for j, footer_value in enumerate(footer_row, start=1):
                sheet.cell(row=start_row + i, column=j, value=footer_value)

    # Save the modified workbook
        workbook.save(self.output_file)


# Usage

