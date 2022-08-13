from script.Barcode import generate_barcode
from script.Printer import Printer

printer = Printer(None)
#printer = None

generate_barcode(value="00316", callback=None, printer=printer, configuration=None, qty=1)