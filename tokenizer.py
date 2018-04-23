#processing library - tokenizer

import json, re, unicodedata, emoji, string


class TOKENIZE():
    def getCLEAN(self, text):
        text = text.replace('\n',' ')
        text = text.replace('...',' TK.PUNCTUAION.ELLIPSES ')
        text = text.replace(u'\ufe0f', 'TK.SPECIALCHAR.UNSPECIFIED')
        text = text.replace(u'\u00a0','') #single quotation mark
        text = text.replace(u'\u2018',' TK.QUOTATION.SINGLE ')
        text = text.replace(u'\u2019',' TK.QUOTATION.SINGLE ')
        text = text.replace(u'\u201c',' TK.QUOTATION.DOUBLE ')
        text = text.replace(u'\u201d',' TK.QUOTATION.DOUBLE ')
        text = text.replace(u'\u2605',' TK.SPECIALCHAR.STAR ')
        text = text.replace(u'\u266a',' TK.SPECIALCHAR.NOTE ')
        return text

    def getLINK(self, text):
        return re.sub('(htt|www).?[^\s]+', ' TK.LINK ', text)

    def getMENTION(self, text):
        return re.sub('@.?[^\s]+', ' TK.MENTION ', text)

    def getRT(self, text):
        if re.search('^RT\s+', text):
            text = 'TK.' + text

        return text

    def getEMOJI(self, text):
        def replacement(match):
            return ' TK.EMOJI.'+match.group(1).upper() + ' '
            
        text = emoji.demojize(text)
        return re.sub(u'\:([a-z_-]+)\:', replacement, text)


    def getCONJUCTION(self, text):
        
        d = {}
 #       d['&'] = ' TK.CONJUNCTION.ANDSYMBOL '
        d['&amp;'] = ' TK.CONJUNCTION.ANDSYMBOL '
    

        for key in d.keys():
            text = text.replace(key, d[key])

        return text

    
    def getPUNCTUATION(self, text):
        d = {}
        d[u'\u2026'] = ' TK.PUNCTUATION.ELLIPSES '
        d['|'] = ' TK.PUNCTUATION.BAR '
        d[' - '] = ' TK.PUNCTUATION.DASH '
        d[u'\u2013'] = ' TK.PUNCTUATION.DASH '
        d[u'\u2014'] = ' TK.PUNCTUATION.DASH '
        
        for key in d.keys():
            text = text.replace(key, d[key])

        return text


    def getQUESTION(self, text):
        d = {}
        for i in range(1,10):
            d['?'*i] = ' TK.QUESTION.QUESTIONMARK' + str(i) + ' '
        for key in d.keys():
            text = text.replace(key, d[key])

        return text

    def getEXCLAMATION(self, text):
        d = {}
        for i in range(1,10):
            d['!'*i] = ' TK.QUESTION.EXCLAMATIONMARK' + str(i) + ' '
        for key in d.keys():
            text = text.replace(key, d[key])

        return text

    def getPRICE(self, text):
        d = {}
        d[u'\u0024'] = ' TK.PRICE.DOLLAR '
        d[u'\u00A2'] = ' TK.PRICE.CENT '
        d[u'\u00A3'] = ' TK.PRICE.POUND '
        d[u'\u00A4'] = ' TK.PRICE.CURRENCY '
        d[u'\u00A5'] = ' TK.PRICE.YEN '
        d[u'\u20AC'] = ' TK.PRICE.EURO '
        
        for key in d.keys():
            text = text.replace(key, d[key])

        return text

    def getMEASURE(self, text):
        d = {}
        d[u'\u2033'] = ' TK.MEASURE.INCH '
        #d[u'\u201d'] = ' TK.MEASURE.INCH '

        for key in d.keys():
            text = text.replace(key, d[key])

        return text

    def getHASHTAG(self, text):
        text = text.split(' ')
        ntext = ''
        for item in text:
            if '#' in item:
                ntext = ntext + item.replace('#',' TK.HASHTAG.').upper() + ' '
            else:
                ntext = ntext + item + ' '
        return ntext

    def is_ascii(self, text):
        return all(ord(c) < 128 for c in text)



def getDATA(filename, include_dates = 'n', format = 'json'):
    TK = TOKENIZE()

    with open(filename,'rU') as f:
        DATA = []
        
        for line in f:
           
            try:
                
                if format == 'text':
                    data = line
                    s = line
#                   s = s.decode('utf-8')
                else:    
                    data = json.loads(line)
                    s = data['text']
          
#                s = data['text']
                s = TK.getCLEAN(s)
                s = TK.getLINK(s)              
                s = TK.getMENTION(s)
                s = TK.getRT(s)
                s = TK.getEMOJI(s)
                s = TK.getCONJUCTION(s)
                s = TK.getPUNCTUATION(s)
                s = TK.getQUESTION(s)
                s = TK.getEXCLAMATION(s)
                s = TK.getPRICE(s)
                s = TK.getMEASURE(s)
                s = TK.getHASHTAG(s)
                
                if TK.is_ascii(s):
                    s = s
                
                else:
                    s = filter(lambda x: x in string.printable, s)
                    
                if 'n' in include_dates:
                
                    if s not in DATA:
                        DATA.append(s)
                    
                else:
                    
                    if [s,data['created_at']] not in DATA:
                        DATA.append([s,data['created_at']])

            except KeyError:
                pass
    return DATA

