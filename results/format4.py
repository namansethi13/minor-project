from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, RGBColor
import uuid
import os


class f4():
    def __init__(self, data):
        self.data = data
        print(data)
        self.file_name = str(uuid.uuid4())
        
    def write_to_doc(self):
        word_file_path = os.path.join(os.path.dirname(
            __file__), "buffer_files", f"{self.file_name}.docx")
        doc = Document()
        for section in doc.sections:

            section.left_margin = section.right_margin = Inches(0.2)

            section.top_margin = section.bottom_margin = Inches(0)

        header_lines = [
            'Maharaja Surajmal Institute',
            'Department of _______',
            f'Programme: {self.data[0]["course"]}',

        ]

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
                font.bold = True
                font.color.rgb = RGBColor(0, 0, 0)
        doc.save(word_file_path)
        return f"{self.file_name}.docx"