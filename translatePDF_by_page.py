# GitHub project: https://github.com/danielcmcg/Unity-UI-Nested-Drag-and-Drop

# https://github.com/ssut/py-googletrans
from googletrans import Translator

import docx
import io

# https://github.com/pdfminer/pdfminer.six
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

'''start translator'''
translator = Translator()

'''create docx'''
doc = docx.Document()

# based on:
# https://stackoverflow.com/questions/53171973/importing-a-pdf-file-with-text-into-a-csv-file-with-python
# https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
 
            text = fake_file_handle.getvalue()
            yield text
 
            converter.close()
            fake_file_handle.close()

def extract_text(pdf_path):
    for page in extract_text_by_page(pdf_path):
        translation = translator.translate(page, src='en', dest='pt')
        doc.add_paragraph(translation.text)

if __name__ == '__main__':
    print(extract_text('TestDocument.pdf'))
	
'''save doc'''
doc.save('translatedDocument.docx')
print('end')
