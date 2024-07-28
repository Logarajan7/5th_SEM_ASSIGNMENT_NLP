

import os
from transformers import pipeline
from fpdf import FPDF
import nltk

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

summarizer = pipeline("summarization")

def summarize_text(text, max_length=130, min_length=30, do_sample=False):
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=do_sample)
    return summary[0]['summary_text']

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Automatic Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_chapter(self, title, body):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(body)

def generate_report(sections, filename='report.pdf'):
    pdf = PDFReport()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    for title, body in sections:
        pdf.add_chapter(title, body)
    pdf.output(filename)

from google.colab import files
uploaded = files.upload()

file_name = list(uploaded.keys())[0]
with open(file_name, 'r') as file:
    text = file.read()

sections = sent_tokenize(text)

summarized_sections = [summarize_text(section) for section in sections]

report_sections = [("Section " + str(i+1), section) for i, section in enumerate(summarized_sections)]

generate_report(report_sections)

files.download('report.pdf')
