from io import StringIO

from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter, \
    PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.utils import open_filename
#from .image import ImageWriter
#from .layout import LAParams
#from .pdfdevice import TagExtractor

def extract_text(pdf_file, password='', page_numbers=None, maxpages=0,
                 caching=True, codec='utf-8', laparams=None):
    """Parse and return the text contained in a PDF file.

    :param pdf_file: Either a file path or a file-like object for the PDF file
        to be worked on.
    :param password: For encrypted PDFs, the password to decrypt.
    :param page_numbers: List of zero-indexed page numbers to extract.
    :param maxpages: The maximum number of pages to parse
    :param caching: If resources should be cached
    :param codec: Text decoding codec
    :param laparams: An LAParams object from pdfminer.layout. If None, uses
        some default settings that often work well.
    :return: a string containing all of the text extracted.
    """
    if laparams is None:
        laparams = None

    with open_filename(pdf_file, "rb") as fp, StringIO() as output_string:
        rsrcmgr = PDFResourceManager(caching=caching)
        device = TextConverter(rsrcmgr, output_string, codec=codec,
                               laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.get_pages(
                fp,
                page_numbers,
                maxpages=maxpages,
                password=password,
                caching=caching,
        ):
            interpreter.process_page(page)

        return output_string.getvalue()
