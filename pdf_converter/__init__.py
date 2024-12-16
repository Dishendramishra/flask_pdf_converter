#%%
from pdf2docx import Converter
import os
from pathlib import Path



def convert_pdf(filename):
    
    p = Path(filename)
    output_filename = p.with_suffix('.docx')
    
    cv = Converter(filename)
    cv.convert(output_filename, start=0, end=None)
    cv.close()
    
    return output_filename.name