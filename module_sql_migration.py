#!./pdf_python/bin/python
# -*- coding: utf-8 -*-

import os
import re
from model import Book, Chapter, Verse, session

class ReadTheBible:
    path = ''

    def __init__(self, path):
        self.path = path

    def read_bible_ini(self):
        try:
            bqtini = open(os.path.join(self.path,'Bibleqt.ini'), 'r')
        except:
            print "oops, it seems file doesn't exists"
            return
        for line in bqtini:
            uline = line.decode('utf-8', 'replace')
            if "PathName" in uline:
                path_name = uline.split(' = ')[1].rstrip()
            if "FullName" in uline:
                full_name = uline.split(' = ')[1].rstrip()
            if "ShortName" in uline:
                short_names = uline.split(' = ')[1].rstrip()
            if "ChapterQty" in uline:
                chapter_qty = uline.split(' = ')[1].rstrip()
                self.read_the_book(path_name, full_name, short_names)
        bqtini.close()

    def read_the_book(self, path, f_name, sh_names):
        try:
            module = open(os.path.join(self.path, path), 'r')
        except:
            print "oops, the module %s doesn't exists" % (os.path.join(self.path, path))
            return
        book = Book()
        book.name = f_name
        book.shortname = sh_names

        reg = re.compile(ur'(\d+)')
        tag_remove = re.compile(ur'<.*?>')
        re_strong = re.compile(ur' [0-9]+')
        chapt_number = 1
        for line in module:
            uline = line.decode('utf-8', 'replace')
            if u'<h4>' in uline:
                uline = tag_remove.sub('', uline)
                chapter = Chapter()
                chapter.name = uline
                chapter.number = chapt_number
                chapt_number += 1
                book.chapters.append(chapter)
                session.add(chapter)
            if u'<p>' in uline:
                uline = tag_remove.sub('', uline)
                uline = re_strong.sub('', uline)
                verse = Verse()
                verse.number = int(reg.findall(uline)[0])
                verse.text = uline
                chapter.verses.append(verse)
                session.add(verse)
                session.add(chapter)

        session.add(book)
        session.commit()
        module.close()


if __name__ == "__main__":
    module_path = os.path.join(os.getcwd(), 'jub')
    module_read = ReadTheBible(module_path)
    module_read.read_bible_ini()

