#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.sax
import os


class MovieHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.type = ""
        self.index = -1
        self.tag = ""

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        if tag == 'd':
            self.index = self.index + 1
            self.tag = tag
            params = attributes['p'].split(',')

            dialogue = 'Dialogue: 3,'
            start = float(params[0])
            mode = params[1]
            timestr = timeofStartEnd(start, mode)
            if mode in ['1', '2', '3']:
                dialogue = dialogue + timestr + 'AcplayDefault,,0000,0000,0000,,{\move(2080, 64, -160, 64)}'
            else:
                dialogue = dialogue + timestr + 'AcplayDefault,,0000,0000,0000,,{\\a6\pos(960, 193)}'
            assparam.append(dialogue)



    # 元素结束事件处理
    def endElement(self, tag):
        print()

    # 内容事件处理
    def characters(self, content):
        if self.tag == 'd':
            assparam[self.index] = assparam[self.index] + str(content) + '\n'


def timeofStartEnd(timestr, mode):
    startint = int(float(timestr))
    startdeci = float('%.2f'%(float(timestr) - startint))
    startdeci = (str(startdeci))[2:4]
    if len(str(startdeci)) <2:
        startdeci = str(startdeci) + '0'
    if mode in ['1', '2', '3']:
        endint = startint + 8
    else:
        endint = startint + 4
    starthour = int(startint/3600)
    startminute = int((startint-600*starthour)/60)
    startsecond = int(startint - 3600 * starthour - startminute * 60)
    endhour = int(endint/3600)
    endminute = int((endint - 3600 * endhour)/60)
    endsecond = int(endint - 3600*endhour - endminute*60)
    if startminute < 10:
        startminute = '0' + str(startminute)
    if startsecond <10 :
        startsecond = '0' + str(startsecond)
    if endminute < 10:
        endminute = '0' + str(endminute)
    if endsecond < 10:
        endsecond = '0' + str(endsecond)
    return str(starthour) + ':' + str(startminute) + ':' + str(startsecond) + '.' + str(startdeci) + ',' \
           + str(endhour) + ':' + str(endminute) + ':' + str(endsecond) + '.' + str(startdeci) + ','





def formScriptInfo():
    return '[Script Info]\nScriptType: v4.00+\nCollisions: Normal\nPlayResX: 1920\nPlayResY: 1080\n\n'


def formV4Styles():
    return '[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, ' \
           'BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, ' \
           'Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: AcplayDefault, Microsoft YaHei, 64, ' \
           '&H00FFFFFF, &H00FFFFFF, &H00000000, &H00000000, 0, 0, 0, 0, 100, 100, 0.00, 0.00, 1, 1, 0, 2, 20, 20, 20, '\
           '0\n\n'


def formEvents():
    return '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'




assparam = []


def danmaku2ass(filepath):
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler(Handler)
    # parser.parse("D:\\danmaku\\av\\10547999\\P2_生物股长深情演唱《YELL》现场版，听着耳朵简直要怀孕了.xml")
    parser.parse(filepath)
    [fname, fename] = os.path.splitext(filepath)
    with open(fname+'.ass', 'w', encoding='utf-8') as file:
        file.write(formScriptInfo())
        file.write(formV4Styles())
        file.write(formEvents())
        for x in assparam:
            file.write(x)


danmaku2ass('D:\Entertainment\Variety\黑傻羞乃木坂合集18.04\【单推乃团字幕组】乃木坂46六周年46小时TV 最佳歌曲前半战 100-61名 - 1.【单推乃团字幕组】乃木坂46六周年46小时TV 最佳歌曲前半战 100-61(Av22157128,P1).xml')

# print(formScriptInfo())
# print(formV4Styles())

# print(timeofStartEnd('274.71', '8'))




