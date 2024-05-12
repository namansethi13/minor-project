from openpyxl import load_workbook
import pandas as pd
from openpyxl.styles import Font
from openpyxl.styles import Font, Alignment, Border, Side
import os
import re

class ElectiveDf:
    subject_name_mapping = {}
    def __init__(self, input_file,subject_name_mapping, exclude_subject_dict,credits_mapping,is_elective,elective_obj):
        if bool(exclude_subject_dict):
            self.exclude_subject_code = list(exclude_subject_dict.keys())[0]
            self.exclude_columns=[exclude_subject_dict[self.exclude_subject_code]]
        else:
            self.exclude_subject_code,self.exclude_columns= "",[]
        
        self.subject_name_mapping = subject_name_mapping
        self.input_file = input_file
        # self.output_file = output_file
        self.df = None
        self.subject_column_renaming = {}
        # self.footers_to_add = footers_to_add
        # self.headers_to_add = headers_to_add
        self.total_subjects = len(subject_name_mapping)
        self.credits_mapping=credits_mapping
        self.df = pd.read_csv(self.input_file)
        print("input file columns")
        print(self.df.columns)
        credits_list = []
        for name in self.df.columns[4:]:
            if ".1" in name:
                continue
            if ".2" in name:
                continue
            names = name.split('/')[0].strip()
            credits_list.append(names)
        list_of_credits = []
        pattern = r'\((\d+)\)'
        for subject in credits_list:
            match = re.search(pattern, subject)
            if match:
                list_of_credits.append(match.group(1))

        list_of_credits = [int(i) for i in list_of_credits]
        for name in self.df.columns:
            if "/" in name:
                elective_subjects = name.split("/")
                if ".1" in elective_subjects[-1]:
                    for i,e in enumerate(elective_subjects):
                        if ".1" not in e:
                            elective_subjects[i] = e+".1"
                if ".2" in elective_subjects[-1]:
                    for i,e in enumerate(elective_subjects):
                        if ".2" not in e:
                            elective_subjects[i] = e+".2"
                    
                col = self.df[name]
                self.df = self.df.drop(name, axis=1)
                for subject in enumerate(elective_subjects):
                    self.df[subject[1]] = col
        enrollment_list = self.df["Enrollment Number"].tolist()
        enrollment_list = [f"{int(enrollment):011d}" for enrollment in enrollment_list[1:]]
        self.elective_obj = elective_obj["elective_list"]
        for elective_between in self.elective_obj:
            for elective , students in elective_between.items():
                for i,entry in enumerate(self.df[elective]):
                    if i == 0:
                        continue
                    if enrollment_list[i-1] not in  students:
                        self.df.loc[i,elective] = None
                        self.df.loc[i,f"{elective}.1"] = None
                        self.df.loc[i,f"{elective}.2"] = None
        self.df.rename(columns=self.subject_name_mapping , inplace=True)
        print(self.df.columns)
        new_df=self.df.iloc[:,10:15]   
        self.df['Total'] = 0
        
        credits_mapping=self.credits_mapping

        
        for subject, credits in credits_mapping.items():
            
            self.df['Total'] += self.df.apply(lambda row: (float(row[subject]) * credits)
                                   if row[subject] is not None and str(row[subject]).strip().isdigit() else 0, axis=1) 
        self.df['CGPA%'] = 0.0
        credits_mapping=self.credits_mapping

        for subject, credits in credits_mapping.items():
           self.df['CGPA%'] += self.df.apply(lambda row: (float(row[subject]) * credits)
                                  if row[subject] is not None and str(row[subject]).strip().isdigit() else 0, axis=1)

        print("hereeeeeeeeee")
        # total_credits = sum(credits_mapping.values()) -
        total_credits = sum(list_of_credits) 
        self.df['CGPA%'] /= total_credits.__round__(4)
        self.df['Reapper Paper Codes'] = ''
        print(self.df)
        def is_numeric(value):
            try:
                int(value)
                return True
            except ValueError:
                return False
                
        def filter_reappear(row):
            return ','.join(set([col.split('(')[0].strip() for col in self.df.columns[4:-4]
                             if 'Total' in col and pd.notna(row[col]) and is_numeric(row[col]) and 1 <= int(row[col].strip()) < 40
                             and col not in self.exclude_columns
                             and self.exclude_subject_code not in col
                             and not any(row[col].strip() == 'Absent Paper Codes' for col in self.df.columns[4:-2]
                                         if 'External' in col and col not in self.exclude_columns) and row[col] != '0']))
        self.df['Reapper Paper Codes'] = self.df.apply(filter_reappear, axis=1)
        self.df['Reapper Paper Codes'] = self.df['Reapper Paper Codes'].apply(
            lambda x: ','.join([s[3:6] for s in x.split(',')]))
        self.df['Absent Paper Codes'] = ''
        
        def filter_absent(row):
            return ','.join(set([col.split('(')[0].strip() for col in self.df.columns[4:-4]
                             if 'External' in col and pd.notna(row[col]) and str(row[col]).strip() == '0' and col not in self.exclude_columns]))


        self.df['Absent Paper Codes'] = self.df.apply(filter_absent, axis=1)
        self.df['Absent Paper Codes'] = self.df['Absent Paper Codes'].apply(
            lambda x: ','.join([s[3:6] for s in x.split(',')]))
        self.df.to_csv(os.path.join(os.path.dirname(__file__), "buffer_files", "temp.csv"))
        reappear_lists = self.df['Reapper Paper Codes'].apply(
            lambda x: x.split(',') if pd.notna(x) else [])
        absent_lists = self.df['Absent Paper Codes'].apply(
            lambda x: x.split(',') if pd.notna(x) else [])

        common_subjects = set.intersection(
            *map(set, reappear_lists.tolist() + absent_lists.tolist()))

        def update_columns(row, column_name):
            return ','.join([subject for subject in row if subject not in common_subjects])

        self.df['Reapper Paper Codes'] = reappear_lists.apply(
            lambda row: update_columns(row, 'Reapper Paper Codes'))
        self.df['Absent Paper Codes'] = absent_lists.apply(
            lambda row: update_columns(row, 'Absent Paper Codes'))
        self.temp = self.subject_name_mapping
        credits_mapping=self.credits_mapping
        for key , value in self.temp.items():
            self.subject_column_renaming[value] = value

        for key , value in self.subject_column_renaming.items():

            if "internal" in value.lower():

                value = value.replace("Internal",str(credits_mapping[key.replace("Internal" , "Total")]))

                
                self.subject_column_renaming[key] = value
            else:
                value = ""
                
        
        self.df.rename(columns=self.subject_column_renaming, inplace=True)
    def get_df(self):
        return self.df