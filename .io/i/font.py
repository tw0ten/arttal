import os
import sys
import fontforge
font = fontforge.font()
font.copyright = "https://github.com/tw0ten/arttal"
font.version = "0"
font.os2_panose = (2, 0, 0, 9, 0, 0, 0, 0, 0, 0)


def font_generate(name="art"):
    assert sum(name.count(i) for i in ['"', ' ', '-', '/']) == 0

    font.familyname = name

    path = f"o/font/{name}"
    os.mkdir(path)

    variants = [
        # ("Thin", 100, -3),
        # ("ExtraLight", 200, -2),
        # ("Light", 300, -1),
        ("Regular", 400, 0),
        # ("Medium", 500, 1),
        # ("SemiBold", 600, 2),
        # ("Bold", 700, 3),
        # ("ExtraBold", 800, 4),
        # ("Black", 900, 5),
    ]

    os.mkdir(f"{path}/ttf")
    for (variant, weight, scale) in variants:
        f = font

        f.weight = variant

        f.fontname = f"{name}-{variant}"
        f.fullname = name if scale == 0 else f"{name} ({variant})"

        file = f"{path}/ttf/{variant}.ttf"
        print("# font", file)
        f.validate()
        f.generate(file)

        if scale == 0:
            file = f"{path}/font.otf"
            print("# font", file)
            f.generate(file)

    file = f"{path}/font-face.css"
    print("# font", file)
    open(file, "w").write(
        "\n".join(
            ["@font-face { "
             + f"font-family: \"{name}\"; src: url(\"font.otf\");"
             + " }"] +
            ["@font-face { " +
             "; ".join([
                 f"font-family: \"{name}\"",
                 f"font-weight: {weight}",
                 f"src: url(\"ttf/{variant}.ttf\")",
                 ""]) +
             "}" for (variant, weight, _) in variants]))

    print(f"font \"{name}\"")


def is_caseable(i): return \
    (not i.upper() == i.lower()) \
    and len(i.upper()) == len(i.lower())


m = [[] for i in range(2 ** 8)]

m[0b00000000] += [' ',  ' ', '​']
m[0b00000001] += ['ー', '々', '〻']
m[0b00000011] += ['1']
m[0b00000100] += ['\'']+['‘', '’']
m[0b00000101] += ['0']
m[0b00000110] += ['`']
m[0b00000111] += ['°']
m[0b00001010] += ['*', '×']
m[0b00001011] += ['+']
m[0b00010000] += ['-']+['—', '…'] + ['−', '–']
m[0b00010001] += ['=']
m[0b00010011] += ['2']
m[0b00010101] += ['#']
m[0b00011010] += ['^']
m[0b00100000] += [',']
m[0b00100010] += ['/'] + ['÷']
m[0b00101000] += [')']
m[0b00101001] += ['?']
m[0b00101010] += ['y', 'Y']+['й', 'Й'] + ['я', 'Я'] + ['η', 'Η'] + ['¥']
m[0b00101100] += \
    ['u', 'U']+['у', 'У'] + ['ū', 'Ū']+['ų', 'Ų']+['ў', 'Ў'] + \
    ['ю', 'Ю']+['ü', 'Ü']
m[0b00110000] += ['>']
m[0b00110001] += [';']
m[0b00110010] += \
    ['i', 'I']+['и', 'И']+['і', 'І']+['į', 'Į'] + \
    ['υ', 'Υ']+['ι', 'Ι']
m[0b00110011] += ['3']
m[0b00110100] += ['ь', 'Ь'] + ['ъ', 'Ъ']
m[0b00110101] += ['5']
m[0b00110110] += ['ы', 'Ы']
m[0b00111000] += ['}']
m[0b00111100] += ['9']
m[0b01000000] += ['.']
m[0b01000001] += ['!']
m[0b01000010] += ['a', 'A']+['а', 'А']+['α', 'Α']+['ą', 'Ą'] + ['ä', 'Ä']
m[0b01000011] += ['7']
m[0b01000100] += [':']
m[0b01000101] += ['o', 'O']+['о', 'О']+['ω', 'Ω']+['ο', 'Ο']
m[0b01000110] += ['4']
m[0b01001100] += ['$', '¤']
m[0b01010010] += ['f', 'F']+['ф', 'Ф']+['φ', 'Φ']
m[0b01010100] += ['n', 'N']+['н', 'Н']+['ν', 'Ν'] + ['ñ', 'Ñ']
m[0b01010101] += ['k', 'K']+['к', 'К']+['κ', 'Κ']
m[0b01010110] += ['ŋ', 'Ŋ']
m[0b01011000] += ['p', 'P']+['п', 'П']+['π', 'Π']
m[0b01011100] += ['↑']
m[0b01100000] += ['"', '“', '”', '„'] + ['«', '»']
m[0b01100010] += ['l', 'L']+['л', 'Л']+['λ', 'Λ'] + ['£']
m[0b01100100] += ['v', 'V']+['в', 'В'] + ['β', 'Β']
m[0b01100110] += ['w', 'W']
m[0b01101100] += ['d', 'D']+['д', 'Д'] + ['δ', 'Δ']
m[0b01110000] += ['&']
m[0b01110010] += ['6']
m[0b01110100] += ['↓']
m[0b01110110] += ['%']
m[0b01110111] += ['8']
m[0b01111001] += ['♪']
m[0b10000010] += ['(']
m[0b10000011] += ['t', 'T']+['т', 'Т']+['τ', 'Τ']
m[0b10000100] += ['b', 'B']+['б', 'Б']
m[0b10000101] += ['s', 'S']+['с', 'С']+['ς', 'σ', 'Σ'] + ['ß', 'ẞ']
m[0b10000110] += ['c', 'C'] + ['ц', 'Ц']
m[0b10001000] += ['\\']
m[0b10001100] += ['g', 'G']+['г', 'Г'] + ['γ', 'Γ']
m[0b10010000] += ['<']
m[0b10010010] += ['{']
m[0b10010100] += \
    ['e', 'E']+['э', 'Э']+['ε', 'Ε']+['ę', 'Ę'] + \
    ['е', 'Е']+['ė', 'Ė'] + \
    ['ö', 'Ö']+['ё', 'Ё'] + \
    ['€']
m[0b10011000] += ['r', 'R']+['ρ', 'Ρ'] + ['р', 'Р']
m[0b10100000] += ['@']
m[0b10100011] += ['[']
m[0b10101000] += ['j', 'J'] + ['ж', 'Ж']+['ž', 'Ž']
m[0b10101001] += [']']
m[0b10101010] += ['x', 'X']+['ξ', 'Ξ']
m[0b10101011] += ['|'] + ['·']
m[0b10110000] += ['_']
m[0b11000010] += ['ч', 'Ч']+['č', 'Č']
m[0b11000011] += ['þ', 'Þ']+['θ', 'Θ']
m[0b11000100] += ['h', 'H']+['х', 'Х']+['χ', 'Χ']
m[0b11000101] += ['ш', 'Ш']+['š', 'Š'] + ['щ', 'Щ']
m[0b11001100] += ['m', 'M']+['м', 'М']+['μ', 'Μ']
m[0b11100101] += ['q', 'Q']
m[0b11100110] += ['ʍ']
m[0b11101000] += ['z', 'Z']+['з', 'З']+['ζ', 'Ζ']
m[0b11111110] += ['~']
m[0b11111111] += ['�', ".notdef"]

_m = []
for i in m:
    for j in i:
        _m.append(j)
        assert _m.count(j) == 1


def glyph_for_char(i):
    for chars in range(len(m)):
        for char in range(len(m[chars])):
            if m[chars][char] == i:
                return chars
    assert False
    return None


font.descent = 0
font.ascent = 128 * 12


def file_for_glyphs(*i):
    name = "+".join(["{:08b}".format(i) for i in i])
    sys.stdout.flush()
    os.system(f"i/art {name}")
    sys.stdout.flush()
    return name


def add_glyph(char, file, width=1):
    i = -1
    try:
        i = ord(char)
        try:
            font.removeGlyph(i)
            print("# glyph override")
        except Exception:
            None
    except Exception:
        None
    print("glyph {:04X} {}".format(i, file))
    v = font.createChar(i, char)
    try:
        v.importOutlines(f"o/art/{file}/.svg")
    except Exception as e:
        print("! error", e)
    v.width = int(font.ascent / 2 * width)


for i in range(len(m)):
    file = file_for_glyphs(i)
    add_glyph(chr(0xE000 + i), file)
    i = m[i]
    for c in range(len(i)):
        print(f"# m '{i[c]}'")
        add_glyph(i[c], file)


assert len({g.width for g in font.glyphs() if g.width > 0}) == 1
font_generate("art.mono")

file = "o/m"
print(f"m {file}")
open(file, "w").write("".join([(i[0] if len(i) > 0 else " ") for i in m]))


font.addLookup("liga", "gsub_ligature", (), (("liga", (("dflt", ("dflt")),)),))
font.addLookupSubtable("liga", "liga_subtable")


def add_ligature(target="ab", replacement='c'):
    print(f"# ligature \"{target}\" '{replacement}'")
    for (t, r) in ([
        # ab c
            (target.lower(), replacement.lower()),
        # Ab C
            (target[0].upper() + target[1:].lower(), replacement.upper()),
        # AB C
            (target.upper(), replacement.upper())]
        if is_caseable(target)
            else [(target, replacement)]):
        print(f"ligature \"{t}\" '{r}'")
        font[r].addPosSub("liga_subtable", tuple(t))


def with_repeat(chars="", repeat='ー'):
    if not chars:
        return ""
    o = f"{chars[0]}"
    for i in range(1, len(chars)):
        o += repeat if chars[i] == chars[i - 1] else chars[i]
    return o


def add_expander(target='a', replacement="bc", repeat=True):
    if repeat:
        replacement = with_repeat(replacement)
    for (t, r) in ([
        # a bc
            (target.lower(), replacement.lower()),
        # A BC
            (target.upper(), replacement.upper())]
        if is_caseable(target)
            else [(target, replacement)]):
        print(f"# expander '{t}' \"{r}\"")
        add_glyph(
            t,
            file_for_glyphs(*[glyph_for_char(i) for i in r]),
            width=len(r))


add_ligature("ng", 'ŋ')
add_ligature("th", 'þ')
add_ligature("wh", 'ʍ')
add_ligature("ch", 'ч')
add_ligature("sh", 'ш')

add_ligature("ph", 'f')

add_ligature("нг", 'ŋ')
add_ligature("кс", "x")


add_expander('ñ', "nn")
add_expander('ẞ', "ss")

add_expander('я', "йа")
add_expander('ё', "йо")
add_expander('ю', "йу")

add_expander('ä', "ae")
add_expander('ö', "oe")
add_expander('ü', "ue")

add_expander('æ', "ae")
add_expander('œ', "oe")

add_expander('ą', "aa")
add_expander('ę', "ee")
add_expander('į', "ii")
add_expander('ū', "uu")
add_expander('ų', "uu")
add_expander('ō', "oo")
add_expander('ē', "ee")

add_expander('ž', "zh")

add_expander('ψ', "πσ")

add_expander('¢', "¤%")
add_expander('€', "¤E")
add_expander('¥', "¤Y")
add_expander('£', "¤L")

add_expander('…', "...", repeat=False)
add_expander('—', "--", repeat=False)
add_expander('©', "(C)")
add_expander('®', "(R)")

add_expander('。', ". ")
add_expander('　', "  ", repeat=False)
add_expander('，', ", ")
add_expander('！', "! ")
add_expander('？', "? ")
add_expander('；', "; ")
add_expander('：', ": ")
add_expander('（', " (")
add_expander('）', ") ")
add_expander('［', " [")
add_expander('］', "] ")
add_expander('【', " [")
add_expander('】', "] ")

add_expander('²', "^2")


def japanese():
    vowels = ['a', 'i', 'u', 'e', 'o']
    hiragana = \
        [(['あ', 'い', 'う', 'え', 'お'], ""),
         (['ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ'], ""),
         (['か', 'き', 'く', 'け', 'こ'], 'K'),
         (['ゕ', None, None, 'ゖ', None], 'k'),
         (['が', 'ぎ', 'ぐ', 'げ', 'ご'], 'G'),
         (['さ', 'し', 'す', 'せ', 'そ'], 'S'),
         (['ざ', 'じ', 'ず', 'ぜ', 'ぞ'], 'Z'),
         (['た', 'ち', 'つ', 'て', 'と'], 'T'),
         ([None, None, 'っ', None, None], 't'),
         (['だ', 'ぢ', 'づ', 'で', 'ど'], 'D'),
         (['な', 'に', 'ぬ', 'ね', 'の'], 'N'),
         (['は', 'ひ', 'ふ', 'へ', 'ほ'], 'H'),
         (['ば', 'び', 'ぶ', 'べ', 'ぼ'], 'B'),
         (['ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ'], 'P'),
         (['ま', 'み', 'む', 'め', 'も'], 'M'),
         (['や', None, 'ゆ', None, 'よ'], 'Y'),
         (['ゃ', None, 'ゅ', None, 'ょ'], 'y'),
         (['ら', 'り', 'る', 'れ', 'ろ'], 'R'),
         (['わ', 'ゐ', 'ゔ', 'ゑ', 'を'], 'W'),
         (['ゎ', None, None, None, None], 'w')]
    katakana = \
        [(['ア', 'イ', 'ウ', 'エ', 'オ'], ""),
         (['ァ', 'ィ', 'ゥ', 'ェ', 'ォ'], ""),
         (['カ', 'キ', 'ク', 'ケ', 'コ'], 'K'),
         (['ヵ', None, None, 'ヶ', None], 'k'),
         (['ガ', 'ギ', 'グ', 'ゲ', 'ゴ'], 'G'),
         (['サ', 'シ', 'ス', 'セ', 'ソ'], 'S'),
         (['ザ', 'ジ', 'ズ', 'ゼ', 'ゾ'], 'Z'),
         (['タ', 'チ', 'ツ', 'テ', 'ト'], 'T'),
         ([None, None, 'ッ', None, None], 't'),
         (['ダ', 'ヂ', 'ヅ', 'デ', 'ド'], 'D'),
         (['ナ', 'ニ', 'ヌ', 'ネ', 'ノ'], 'N'),
         (['ハ', 'ヒ', 'フ', 'ヘ', 'ホ'], 'H'),
         (['バ', 'ビ', 'ブ', 'ベ', 'ボ'], 'B'),
         (['パ', 'ピ', 'プ', 'ペ', 'ポ'], 'P'),
         (['マ', 'ミ', 'ム', 'メ', 'モ'], 'M'),
         (['ヤ', None, 'ユ', None, 'ヨ'], 'Y'),
         (['ャ', None, 'ュ', None, 'ョ'], 'y'),
         (['ラ', 'リ', 'ル', 'レ', 'ロ'], 'R'),
         (['ワ', 'ヰ', None, 'ヱ', 'ヲ'], 'W'),
         (['ヮ', None, None, None, None], 'w'),
         (['ヷ', 'ヸ', 'ヴ', 'ヹ', 'ヺ'], 'V')]

    def kana(m):
        c2n = len(vowels)
        for i in range(len(m)):
            (kana, c1o) = m[i]
            assert len(kana) == c2n
            for i in range(c2n):
                if kana[i] is not None:
                    c1 = c1o
                    c2 = vowels[i]
                    add_expander(kana[i], f"{c1}{c2}")

    add_expander('々', "ーー", repeat=False)
    kana(hiragana)
    add_expander('ん', "n")
    kana(katakana)
    add_expander('ン', "n")


japanese()


font_generate()
