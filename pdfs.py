#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fpdf import FPDF
import Tkinter, Tkconstants, tkFileDialog
    
    
def fpdf():
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font('Arial', 'B', 16)
	pdf.cell(40, 10, 'Reporte')
	pdf.output('reporte.pdf', 'F')
	import os
    	try:
        	os.startfile('reporte.pdf')
    	except Exception:
        	os.system("xdg-open \"%s\"" % 'reporte.pdf')

def reporte():
	print "hola mundo"
