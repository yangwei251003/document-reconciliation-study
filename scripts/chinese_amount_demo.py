"""Small original parsing experiment; not a settlement or accounting engine."""
import argparse,re
DIGIT = {'零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '两': 2}

UNIT = {'拾': 10, '十': 10, '佰': 100, '百': 100, '仟': 1000, '千': 1000}

def cn2num(s):
    s = s.replace('整', '').replace('正', '')
    total = 0
    section = 0
    number = 0
    for ch in s:
        if ch in DIGIT:
            number = DIGIT[ch]
        elif ch in UNIT:
            section += (number if number else 1) * UNIT[ch]
            number = 0
        elif ch == '万':
            section = (section + number) * 10000
            total += section
            section = 0
            number = 0
        elif ch == '亿':
            total = (total + section + number) * 100000000
            section = 0
            number = 0
        elif ch in '圆元':
            total += section + number
            section = 0
            number = 0
        elif ch == '角':
            total += number / 10
            number = 0
        elif ch == '分':
            total += number / 100
            number = 0
    return round(total + section + number, 2)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('text');a=p.parse_args()
    if not a.text or not re.fullmatch('[零壹贰叁肆伍陆柒捌玖一二三四五六七八九两拾十佰百仟千万亿圆元角分整正]+',a.text):p.error('Only the documented Chinese amount characters are accepted.')
    print(format(cn2num(a.text),'.2f'))
