import pandas as pd

class ExcelToCSVConverter:
    def __init__(self, input_xlsx_file, output_csv_file, subject_codes_dict, subject_credits_dict):
        self.input_xlsx_file = input_xlsx_file
        self.output_csv_file = output_csv_file
        self.subject_codes_dict = subject_codes_dict
        self.subject_credits_dict = subject_credits_dict

    def convert(self):
        try:
            df = pd.read_excel(self.input_xlsx_file)
            print(df)
            df.rename(columns=self.subject_codes_dict, inplace=True)
            print("renamed ",df)
            
        
            expected_columns = list(self.subject_codes_dict.values())
            missing_columns = [col for col in expected_columns if col not in df.columns]

            if missing_columns:
                raise ValueError(f"The following expected columns are missing in the Excel file: {', '.join(missing_columns)}")

            total_credits = sum(self.subject_credits_dict.values())

            df['Total Marks'] = (df[expected_columns] * pd.Series(self.subject_credits_dict)).sum(axis=1)
            df['CGPA'] = (df['Total Marks'] / total_credits) / 10
            df['CGPA'] = df['CGPA'].round(3)

            saved_file =df.to_csv(index=False)
            print("saved file ",saved_file)
            print(f"CSV file '{self.output_csv_file}' has been created with the requested calculations.")
            return saved_file
            
        except FileNotFoundError:
            raise FileNotFoundError(f"The input file '{self.input_xlsx_file}' was not found.")
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

# Usage

