import re

FLAGS = re.MULTILINE | re.DOTALL

class RegExCleaner():

    def __init__(self, expressions=[]):
        self.expressions = expressions

    @staticmethod
    def _compile(expressions):
        regexps = []
        for pattern, repl in expressions.items():
            regexps.append((re.compile(pattern, flags=FLAGS), repl))
        return regexps

    @classmethod
    def reddits(cls):
        r"""Create class with specific patterns"""

        words ={
            r'e.g.':r' ExempliGratia ',
            r'i.e.':r' IdEst ',
            r'n.b.':r' NotaBene ',
            r'N.B.':r' NotaBene ',
            r'p.s.':r' PostScript ',
            r'P.S.':r' PostScript ',
            r'U.S. ':r' US ',
            r'U.S ':r' US ',
            r'U.S.A ':r' USA ',
            r'p.m.':r'PM',
            r'P.M.':r'PM',
            r'a.m.':r'AM',
            r'A.M.':r'AM',
            r'R.I.P.':r'RIP',
            r'r.i.p.':r'RIP',

            r"TL:DR":r"TLDR",
            r"TL;DR":r"TLDR",
            r"tl;drs":r"TLDR",
            r"tl;dr":r"TLDR",

            r' 24/7 ':r' <ALLTIME> ',
            r' <3 ':r' <HEART> ',

            r"&nbsp;":r"",
            r"&nbsp":r"",
            r"&amp;#x200B;":r" ",
            r"&amp;": r"",
            r'&lt;' :r' ',
            r'&gt;' :r' ',
            r'&le;' :r' ',
            r'&ge;' :r' ',
        }
        expressions = {
            r'\(?https?:/\/\S+\)?' : r' <LINK> ',         # https  <LINK>
            r'/r/\S+' : r' <SubReddit> ',                 # SubReddit names
            r'/u/\S+' : r' <UserName> ',                  # UserName names 
            r"[‘’`´ʹʻʽʾʿˈˊʹ΄՚᾿‛′Ꞌꞌ＇]":r"'",
            r"\B'|'\B":r"",
            r"(\S)\*+(\W|$)":r"\1\2",  r"(\W|^)\*+(\S)":r"\1\2",
            r"(\W|^)[-+]?[.\d]*[\d]*[:,.\d]+(?!(D|st|nd|rd|th|u|U))": r" <NUMBER> ",
            r"'(s|S|ve|VE|ll|LL|d|D|re|RE)(\W)":r" '\1\2",
            r"(.)\1{2,}":r"\1\1",
            r'([\.\!\?,])+': r' \1 ',
            r'[HhAa]{4,}\W' : r'haha ',
            r'(:|=)-?(D|\))+(\W|$)' : r' <SMILE> ',
            r'(:|=)-?[pP]+(\W|$)' : r' <TONGUE> ',
            r'\W;-?\)+(\W|$)' : r' <WINK> ',
            r'[^A-Za-z0-9\'<>\.,\*\!\?\$€¥ÆÐƎƏƐƔĲŊŒẞÞǷȜæðǝəɛɣĳŋœĸſßþƿȝĄƁÇĐƊĘĦĮƘŁØƠŞȘŢȚŦŲƯY̨Ƴąɓçđɗęħįƙłøơşșţțŧųưy̨ƴÁÀÂÄǍĂĀÃÅǺĄÆǼǢƁĆĊĈČÇĎḌĐƊÐÉÈĖÊËĚĔĒĘẸƎƏƐĠĜǦĞĢƔáàâäǎăāãåǻąæǽǣɓćċĉčçďḍđɗðéèėêëěĕēęẹǝəɛġĝǧğģɣĤḤĦIÍÌİÎÏǏĬĪĨĮỊĲĴĶƘĹĻŁĽĿNŃN̈ŇÑŅŊÓÒÔÖǑŎŌÕŐỌØǾƠŒĥḥħıíìiîïǐĭīĩįịĳĵķƙĸĺļłľŀŉńn̈ňñņŋóòôöǒŏōõőọøǿơœŔŘŖŚŜŠŞȘṢẞŤŢṬŦÞÚÙÛÜǓŬŪŨŰŮŲỤƯẂẀŴẄǷÝỲŶŸȲỸƳŹŻŽẒŕřŗſśŝšşșṣßťţṭŧþúùûüǔŭūũűůųụưẃẁŵẅƿýỳŷÿȳỹƴźżžẓ]+' : r' ',
        }

        ex = cls.from_vocab(words) + cls.from_dict(expressions)
        return ex

    @classmethod
    def from_dict(cls, custom_dic):
        r"""Create class from dictionary with flexible patterns {pattern : replacing}"""

        return cls(cls._compile(custom_dic))

    @classmethod
    def from_vocab(cls, vocab):
        r"""Create class from vocabulary with fixed patterns {pattern : replacing}"""

        pattern = re.compile("|".join(map(re.escape, vocab.keys())))
        repl = lambda match: vocab[match.group(0)]
        return cls([(pattern, repl)])

    def __add__(self, b):
        return RegExCleaner(self.expressions + b.expressions)

    def __call__(self, s):

        for regex, repl in self.expressions:
            s = regex.sub(repl, s)
        return s
