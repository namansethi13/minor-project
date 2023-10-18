import pandas as pd

class One:
    pdf = None

    def __init__(self, pdf):
        print("in class one")
        self.pdf = pdf

    def normalize(self):
        print("in normalize")
        df = pd.read_csv(self.pdf)
        df['english'] = [10, 20, 30]
        normalized_csv = df.to_csv(index=False)

        return normalized_csv
