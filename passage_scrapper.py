#!./pdf_python/bin/python
# -*- coding: utf-8 -*-

import os
import re
import string
import sys
from model import Book, Chapter, Verse, session
from reportlab.pdfgen import canvas
from reportlab.lib.colors import *
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.platypus import Paragraph, Spacer, Frame, SimpleDocTemplate, PageBreak
from reportlab.platypus import BaseDocTemplate, NextPageTemplate, PageTemplate
from reportlab.lib.styles import ParagraphStyle
from PyPDF2 import PdfFileMerger, PdfFileReader



class MyPresentation:
    HEIGHT = 768
    WIDTH = 1024
    FONTNAME = 'Arial'
    FONTSIZE = 56
    BCKGRDCOLOR =  (0.2, 0.5, 0.3)
    FONTCOLOR = white
    PASSAGE = []


    def __init__(self, fname, passage):
        """ Constructor """
        MyFontObject = ttfonts.TTFont('Arial', 'arial.ttf')
        pdfmetrics.registerFont(MyFontObject)
        self.doc = SimpleDocTemplate(fname, pagesize = (self.WIDTH, self.HEIGHT),
                leftMargin = 40, rightMargin = 40, topMargin = 100, bottomMargin = 30)
        self.story = []
        self.PASSAGE = passage


    def pageCanvas(self, canvas, doc):
        """
        Forming of the page layout (backround color...)
        """
        canvas.saveState()
        canvas.setFont(self.FONTNAME, self.FONTSIZE)
        canvas.setFillColorRGB(self.BCKGRDCOLOR[0], self.BCKGRDCOLOR[1], 
                self.BCKGRDCOLOR[2])
        canvas.rect(0, 0, self.WIDTH, self.HEIGHT, stroke = 0, fill = 1)
        canvas.restoreState()
        canvas.saveState()
        p = canvas.beginPath()
        p.rect(0, self.HEIGHT - 80, self.WIDTH, 80)
        canvas.clipPath(p, stroke = 0)
        canvas.linearGradient(0, self.HEIGHT - 80, self.WIDTH, 
                self.HEIGHT - 80, (black, blue), extend = False)
        canvas.restoreState()
        canvas.saveState()
        canvas.setFillColorRGB(1,1,1)
        canvas.setFont(self.FONTNAME, self.FONTSIZE)
        canvas.drawString(40, 714, "%s.%s:%s" % (self.PASSAGE[0], self.PASSAGE[1],
            self.PASSAGE[2]))
        canvas.restoreState()


    def runBuild(self, str):
        p = ParagraphStyle('test')
        p.textColor = self.FONTCOLOR
        p.borderWidth = 0
        p.fontSize = self.FONTSIZE
        p.fontName = self.FONTNAME
        p.leading = 12 * self.FONTSIZE / 10
        for line in str:
            para = Paragraph("%s" % line, p)
            self.story.append(para)
        self.doc.build(self.story, onFirstPage = self.pageCanvas, onLaterPages =
                self.pageCanvas)




class PassageScrapper:

    def file_to_scrap(self):
        """
        this method is to get the file with initial text as a command-line
        argument or as a raw input filename from user and if it's not in TXT
        and UTF-8, than to convert it and pass further
        """

        if len(sys.argv) == 2:
            filename = sys.argv[1]
        else:
            filename = raw_input('Enter filename: ')

        filename_txt = filename[:string.rfind(filename, '.')] + '.txt'
        if not os.path.exists(os.path.join(os.getcwd(),filename_txt)):
            os.system('libreoffice --headless --convert-to txt:"Text" "' + filename + '"')
        if os.path.exists(os.path.join(os.getcwd(),filename_txt)):
            self.find_the_passages(filename_txt)
        else:
            print "something went wrong. there is no TXT-file"


    def find_the_passages(self, fname):
        """
        this method is to get a list of passages used in initial text
        """

        f = open(fname, 'r')
        ftext = f.read().decode('utf-8','replace')
        p = re.compile(u'\(([0-9]?[а-яА-Яa-zA-Z]+)[ .]{1,2}(\d+):([\d,\-]+)\)')
        passages = p.findall(ftext)
        f.close()

        tmp_list = []

        for passage in passages:
            index = passages.index(passage)
            tmp_list += [ str(index) + ".pdf" ]
            self.create_pdf(passage, tmp_list[-1])

        self.merge_PDF(tmp_list)


    def get_verses_list(self, vrange):
        few = re.compile(u'(\d+)-(\d+)')
        single = re.compile(u'[,]?(\d+)[,]?')
        vlist = []
        if '-' in vrange:
            v = few.findall(vrange)
            for first, last in v:
                vlist += range(int(first), int(last) + 1)
            vrange = few.sub(vrange, '')
        if vrange:
            v = single.findall(vrange)
            for item in v:
                vlist += [int(item)]
        return vlist


    def get_the_passage(self, passage):
        verses_list = self.get_verses_list(passage[2])
        book = "%" + passage[0] + "%" 
        verses = session.query(Verse).join(Chapter).join(Book).filter(Book.shortname.like(book)).filter(Chapter.number == int(passage[1])).filter(Verse.number.in_(verses_list)).all()
        return ([unicode(v.text) for v in verses])


    def create_pdf(self, passage, tmp_file):
        working_dir = os.path.join(os.getcwd(), '_tmp')
        if not os.path.exists(working_dir):
            os.mkdir(working_dir)
        tmp_PDF = MyPresentation(os.path.join(working_dir, tmp_file),
                passage)
        text = self.get_the_passage(passage)
        #print text
        tmp_PDF.runBuild(text)


    def merge_PDF(self, tmp_list):
        merger = PdfFileMerger()
        for filename in tmp_list:
            merger.append(PdfFileReader(file(os.path.join(os.getcwd(), '_tmp', filename), 'rb')))
        merger.write("presentation.pdf")
        os.system('rm -rf _tmp')


if __name__ == "__main__":
    ps = PassageScrapper()
    ps.file_to_scrap()
