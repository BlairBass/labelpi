from reportlab.graphics.barcode import code39
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

import calendar
import time

from script.Printer import Printer


def generate_barcode(value = None, callback=None, configuration=None, qty=1, printer=None):
    # Generates a Code39 barcode from the passed value, saves it as a PDF and prints it
    # Finally, the transferred callback is called
    filename = "/tmp/" + str(calendar.timegm(time.gmtime())) + ".labelpi.pdf"
    c = canvas.Canvas(filename)
    c.setPageSize((25 * mm, 54 * mm))
    #c.setPageSize((54*mm, 25*mm))
    c.setPageRotation(90)

    barcode = code39.Standard39(value, barHeight=14*mm, checksum=0, barWidth=1.15,
                                humanReadable=True, ratio=3.0)

    barcode.drawOn(c, -1.5 * mm, 6 * mm)
    c.showPage()
    c.save()
    if printer is not None:
      printer.print_file(filename=filename, callback=callback, qty=qty)
