#!/usr/bin/env python3
"""Faithful Python mirror of zcode_embed_ime/lib/zcode_logic.dart (ZCode class).

Purpose: validate the Dart splicer logic on this VM, where no Dart/Flutter
toolchain exists. Every function below is a line-for-line transliteration of
the Dart source (same tables, same order of rules, same indices). If this
mirror disagrees with the Dart file, the Dart file wins and this file must be
re-transliterated.

Usage:
  python3 zcode_mirror.py yabona bodogsan budugsen tang mongol mo
  python3 zcode_mirror.py --lexicon   # NG-word ANG check over the trimmed lexicon
"""
import sys

dagbr = {
    "in": "ᡬᡬᡧ ", "yin": "ᡬᡬᡧ ", "on": "ᡭᡧ ", "o": "ᡳ ",
    "ban": "ᡳᡪᡧ ", "iyan": "ᡬᡬᡪᡧ ", "iyen": "ᡬᡬᡪᡧ ",
    "bar": "ᡳᡪᢝ ", "iyar": "ᡬᡬᡪᢝ ", "iyer": "ᡬᡬᡪᢝ ",
    "yi": "ᡬᡫ ", "ji": "ᡬᡫ ", "gi": "ᡬᡫ ", "i": "ᡫ ",
    "to": "ᢘᡳ ", "do": "ᢙᡳ ", "tor": "ᢘᡭᢝ ", "dor": "ᢙᡭᢝ ",
    "tahi": "ᢘᡪᢊᡬᡦ ", "dahi": "ᢙᡪᢊᡬᡦ ", "toni": "ᢘᡭᡱᡫ ",
    "doni": "ᢙᡭᡱᡫ ", "tai": "ᢘᡪᡫ ", "loga": "ᢏᡭᢉᡨ ",
    "luge": "ᢏᡭᢊᡪᡨ ", "aca": "ᡥᢚᡧ ", "dagan": "ᢙᡪᡱᡱᡪᡧ ",
    "degen": "ᢙᡪᢊᡪᡧ ", "tagan": "ᢘᡪᡱᡱᡪᡧ ", "tegen": "ᢘᡪᢊᡪᡧ ",
    "nogod": "ᡯᡭᡱᡱᡭᡭᡧ ", "nugud": "ᡯᡭᢋᡭᡭᡧ ", "od": "ᡭᡭᡧ ",
    "oo": "ᡭᡳ ", "uu": "ᡭᡳ ", "nar": "ᡯᡪᢝ ", "mini": "ᢌᡬᡱᡫ ",
    "cini": "ᢚᡬᡱᡫ ", "ni": "ᡯᡫ ",
}

aArr = ["ᡥᡧ", "", "", "ᡥᡪ", "ᡪᡪ", "", "ᡪ", "ᡪᡪ", "", "ᡧ", "ᡪᡨ", "ᡨ"]
eArr = ["ᡥᡨ", "", "", "ᡥ", "ᡪᡪ", "", "ᡪ", "ᡪᡪ", "", "ᡪᡨ", "ᡧ", "ᡨ"]
iArr = ["ᡫ", "", "", "ᡥᡬ", "", "", "ᡬ", "ᡬᡬ", "ᡪᡬ", "ᡫ", "ᡬᡦ", ""]
oArr = ["ᡥᡭ", "ᡥᡭ", "", "ᡥᡭ", "", "", "ᡭ", "ᡪᡭ", "", "ᡳ", "ᡭ", ""]
uArr = ["ᡥᡭᡦ", "", "", "ᡥᡭᡬ", "", "", "ᡭ", "ᡭᡬ", "ᡪᡭᡬ", "ᡳ", "ᡭ", "ᡭᡦ"]
nArr = ["ᡯ", "", "", "ᡯ", "", "", "ᡪ", "ᡱ", "", "ᡧ", "ᡰ", ""]
bArr = ["ᡳ", "", "", "ᡳ", "ᡴ", "", "ᡳ", "ᡴ", "", "ᡲ", "", ""]
pArr = ["ᡶ", "", "", "ᡶ", "ᡷ", "", "ᡶ", "ᡷ", "", "ᡵ", "", ""]
hArr = ["ᡸ", "", "", "ᡸ", "ᢊ", "ᢋ", "ᡪᡪ", "ᢊ", "ᢋ", "ᢇ", "ᢇ", ""]
gArr = ["ᢈ", "", "ᡪᡪ", "ᢈ", "ᢊ", "ᢋ", "ᡱᡱ", "ᢊ", "ᢋ", "ᢇ", "ᢉ", "ᡬᡨ"]
mArr = ["ᢌ", "", "", "ᢌ", "", "", "ᢎ", "", "", "ᢍ", "", ""]
lArr = ["ᢏ", "", "", "ᢏ", "", "", "ᢑ", "", "", "ᢐ", "", ""]
sArr = ["ᢔ", "", "", "ᢔ", "", "", "ᢔ", "", "", "ᢓ", "", ""]
xArr = ["ᢗ", "", "", "ᢗ", "", "", "ᢗ", "", "", "ᢖ", "", ""]
tArr = ["ᢘ", "", "", "ᢘ", "", "", "ᢙ", "ᢘ", "", "ᢘᡦ", "", ""]
dArr = ["ᢙ", "", "", "ᢘ", "", "", "ᡭᡪ", "ᢙ", "", "ᡭᡧ", "ᢙᡦ", ""]
cArr = ["ᢚ", "", "", "ᢚ", "", "", "ᢚ", "", "", "ᢚᡦ", "", ""]
jArr = ["ᡬ", "", "", "ᡬ", "", "", "ᢛ", "", "", "ᢛᡦ", "", ""]
yArr = ["ᢜ", "", "", "ᢜ", "", "", "ᢜ", "", "", "ᡫ", "", ""]
rArr = ["ᢞ", "", "", "ᢞ", "", "", "ᢞ", "", "", "ᢝ", "", ""]
wArr = ["ᢟ", "", "", "ᢟ", "", "", "ᢟ", "", "", "ᢟᡦ", "", ""]
fArr = ["ᢡ", "", "", "ᢡ", "ᢢ", "", "ᢡ", "ᢢ", "", "ᢠ", "", ""]
kArr = ["ᢤ", "", "", "ᢤ", "ᢥ", "", "ᢤ", "ᢥ", "", "ᢣ", "", ""]
qArr = ["ᢚ", "", "", "ᢚ", "", "", "ᢚ", "", "", "ᢚᡦ", "", ""]
zArr = ["ᢧ", "", "", "ᢧ", "", "", "ᢧ", "", "", "ᢧᡦ", "", ""]
vArr = ["ᡥᡭ", "ᡥᡭ", "", "ᡥᡭ", "", "", "ᡭ", "ᡪᡭ", "", "ᡳ", "ᡭ", ""]
upperAArr = ["ᡥᡧ", "", "", "ᡪᡪ", "", "", "ᡪᡪ", "", "", "ᡧ", "", ""]
upperEArr = ["ᢟ", "", "", "ᢟ", "", "", "ᢟ", "", "", "ᢟᡦ", "", ""]
upperIArr = ["ᡫ", "", "", "ᡥᡬ", "", "", "ᡬ", "ᡬᡬ", "ᡪᡬ", "ᡫ", "ᡬᡦ", ""]
upperOArr = ["ᡥᡭ", "ᡥᡭ", "", "ᡥᡭ", "", "", "ᡭ", "ᡪᡭ", "", "ᡭ", "ᡭ", ""]
upperUArr = ["ᡥᡭᡦ", "", "", "ᡥᡭᡬ", "", "", "ᡭᡬ", "", "", "ᡭᡦ", "", ""]
upperNArr = ["ᡯ", "", "", "ᡯ", "", "", "ᡱ", "ᡪ", "", "ᡧ", "ᡰ", ""]
upperBArr = ["ᡳ", "", "", "ᡳ", "ᡴ", "", "ᡳ", "ᡴ", "", "ᡲ", "", ""]
upperPArr = ["ᡶ", "", "", "ᡶ", "ᡷ", "", "ᡶ", "ᡷ", "", "ᡵ", "", ""]
upperHArr = ["ᡸ", "", "", "ᡸ", "ᢊ", "ᢋ", "ᡪᡪ", "ᢊ", "ᢋ", "ᢇ", "ᢇ", ""]
upperGArr = ["ᢈ", "", "ᡪᡪ", "ᢈ", "ᢊ", "ᢋ", "ᡱᡱ", "ᢊ", "ᢋ", "ᢇ", "ᢉ", "ᡬᡨ"]
upperMArr = ["ᢌ", "", "", "ᢌ", "", "", "ᢎ", "", "", "ᢍ", "", ""]
upperLArr = ["ᢏᢨ", "", "", "ᢏᢨ", "", "", "ᢑᢨ", "", "", "ᢑᢨᡦ", "", ""]
upperSArr = ["ᢔ", "", "", "ᢔ", "", "", "ᢔ", "", "", "ᢓ", "", ""]
upperXArr = ["ᢗ", "", "", "ᢗ", "", "", "ᢗ", "", "", "ᢖ", "", ""]
upperTArr = ["ᢙ", "", "", "ᢙ", "", "", "ᢙ", "ᢘ", "", "ᢙᡦ", "", ""]
upperDArr = ["ᢘ", "", "", "ᢙ", "", "", "ᢘ", "", "", "ᢘᡦ", "", ""]
upperCArr = ["ᢦ", "", "", "ᢦ", "", "", "ᢦ", "", "", "ᢦᡦ", "", ""]
upperJArr = ["ᡬ", "", "", "ᡬ", "", "", "ᢛ", "", "", "ᢛᡦ", "", ""]
upperYArr = ["ᢜ", "", "", "ᢜ", "", "", "ᢜ", "", "", "ᡫ", "", ""]
upperRArr = ["ᢞ", "", "", "ᢞ", "", "", "ᢞ", "", "", "ᢝ", "", ""]
upperWArr = ["ᢟ", "", "", "ᢟ", "", "", "ᢟ", "", "", "ᢟᡦ", "", ""]
upperFArr = ["ᢡ", "", "", "ᢡ", "ᢢ", "", "ᢡ", "ᢢ", "", "ᢠ", "", ""]
upperKArr = ["ᢤ", "", "", "ᢤ", "ᢥ", "", "ᢤ", "ᢥ", "", "ᢣ", "", ""]
upperQArr = ["ᢦ", "", "", "ᢦ", "", "", "", "", "", "ᢦᡦ", "", ""]
upperZArr = ["ᢨ", "", "", "ᢨ", "", "", "ᢨ", "", "", "ᢨᡦ", "", ""]
upperVArr = ["ᡭ", "ᡭ", "", "ᡭ", "", "", "ᡭ", "ᡪᡭ", "", "ᡳ", "ᡭ", ""]

wordMap = {
    "a": aArr, "e": eArr, "i": iArr, "o": oArr, "u": uArr, "n": nArr,
    "b": bArr, "p": pArr, "h": hArr, "g": gArr, "m": mArr, "l": lArr,
    "s": sArr, "x": xArr, "t": tArr, "d": dArr, "c": cArr, "j": jArr,
    "y": yArr, "r": rArr, "w": wArr, "f": fArr, "k": kArr, "q": qArr,
    "z": zArr, "v": vArr,
    "A": upperAArr, "E": eArr, "I": iArr, "O": upperOArr, "U": upperUArr,
    "N": nArr, "B": bArr, "P": pArr, "H": hArr, "G": gArr, "M": mArr,
    "L": upperLArr, "S": sArr, "X": xArr, "T": upperTArr, "D": upperDArr,
    "C": upperCArr, "J": jArr, "Y": yArr, "R": rArr, "W": wArr,
    "F": fArr, "K": kArr, "Q": qArr, "Z": upperZArr, "V": vArr,
}

databases = {
    "aav": "ᡥᡪᡴᡭ", "america": "ᡥᡪᢎᢟᢞᡬᢤᡪᡨ", "ch": "ᡭᡭ",
    "chi": "ᡭᡭᡫ", "cihola": "ᢚᡬᡪᡪᡭᢑᡧ", "cino": "ᢚᡬᡱᡳᡨ",
    "do": "ᢙᡳ", "du": "ᢙᡳ", "eej": "ᡥᢛᡫ", "eyer": "ᡬᡬᡪᢝ",
    "europe": "ᡥᢟᡭᡬᢞᡭᡶᡪᡨ", "eyen": "ᡬᡬᡪᡧ", "gowa": "ᢈᡭᡳᡨ",
    "hebei": "ᡥᢨᢟᡳᢟᡫ", "in": "ᡬᡬᡧ", "kino": "ᢤᡬᡱᡭ",
    "kod": "ᢥᡭᢙᡦ", "mongo": "ᢌᡭᡪᢊᡱᡱᡭᢐ", "no": "ᡳ",
    "on": "ᡭᡧ", "oo": "ᡭᡳ", "radio": "ᢞᡪᢙᡬᡭ", "sh": "ᢗ",
    "shi": "ᢗᡫ", "su": "ᢔᡭᡦ", "tatar": "ᢘᡪᢘᡪᢝ",
    "yunikod": "ᢜᡭᡬᡱᡬᢥᡭᢙᡦ", "zh": "ᢨ", "zhi": "ᢨᡫ",
    "english": "ᡥᡪᡪᢊᢊᢑᡫ", "england": "ᡥᡪᡪᢊᢊᢑᡫ",
    "degen": "ᢙᡪᢊᡪᡧ", "deng": "ᢙᢟᡪᡬᡨ", "dan": "ᢙᡪᡧ",
    "den": "ᢙᡪᡧ", "din": "ᢙᡬᡧ", "o": "ᡥᡭ", "u": "ᡥᡭᡬ",
    "i": "ᡥᡫ", "naima": "ᡯᡪᡬᢎᡧ", "dung": "ᢙᡭᡬᡪᡬᡨ",
    "don": "ᢙᡭᡧ", "dungsigor": "ᢙᡭᡬᡪᢊᢔᡬᡱᡱᡭᢝ",
    "agola": "ᡥᡪᡱᡱᡭᢑᡧ", "sig": "ᢔᡬᢇ", "sih": "ᢔᡬᢇ",
    "tig": "ᢘᡬᢇ", "tere": "ᢘᡪᢞᡧ",
}

# ANG_BUG_FIX: set True to mirror the Dart fix in middle() (see zcode_logic.dart).
# When True, the "solving g before a or o" rule does NOT overwrite the ANG form
# (U+188A) of a G that belongs to an "ng" digraph (previous letter is 'n').
ANG_BUG_FIX = False


def first_and_last(latin):
    result_first = ""
    result_last = []
    first_str = latin[0]
    second_str = latin[1]
    last_str = latin[-1]
    prelast_str = latin[-2]
    if first_str in wordMap:
        result_first = wordMap[first_str][3]
        x = first_str
        if x in ("b", "p", "k", "f"):
            y = second_str
            if y in ("o", "u", "v", "U"):
                result_first = wordMap[x][4]
        if x in ("h", "g"):
            y = second_str
            if y in ("e", "i", "w"):
                result_first = wordMap[x][4]
        if x in ("h", "g"):
            y = second_str
            if y in ("u", "U"):
                result_first = wordMap[x][5]
        if last_str in wordMap:
            p_temp = wordMap[last_str][9]
            if p_temp:
                result_last.append(p_temp)
        x = prelast_str
        if x in ("b", "p", "k", "f"):
            y = last_str
            if y == "a":
                if result_last:
                    result_last.clear()
                result_last.append(wordMap[y][10])
        if x in ("h", "g"):
            y = last_str
            if y == "e":
                if result_last:
                    result_last.clear()
                result_last.append(wordMap[y][9])
        if x in ("b", "p", "k", "f", "h", "g"):
            y = last_str
            if y == "i":
                if result_last:
                    result_last.clear()
                result_last.append(wordMap[y][10])
        if x in ("b", "p", "k", "f"):
            y = last_str
            if y in ("o", "v"):
                if result_last:
                    result_last.clear()
                result_last.append(wordMap[y][10])
        if x in ("b", "p", "k", "f", "h", "g"):
            y = last_str
            if y == "u":
                if result_last:
                    result_last.clear()
                result_last.append(wordMap[y][10])
        if x in ("i", "e", "u", "U"):
            y = last_str
            if y in ("g", "h"):
                if result_last:
                    result_last.clear()
                result_last.append(wordMap[y][11])
        if x == "n":
            y = last_str
            if y == "g":
                if result_last:
                    result_last.clear()
                result_last.append(wordMap[y][11])
        if x in ("n", "m", "l", "y", "r"):
            y = last_str
            if y in ("a", "e"):
                if result_last:
                    result_last.clear()
                result_last.append(wordMap[y][11])
        if x in ("c", "v", "z", "q", "d"):
            y = last_str
            if y == "e":
                if result_last:
                    result_last.clear()
                result_last.append(wordMap[y][10])
        if x in ("h", "g"):
            y = last_str
            if y == "a":
                if result_last:
                    result_last.clear()
                result_last.append(wordMap[y][11])
        if x in ("n", "m", "h", "g"):
            y = last_str
            if y == "a":
                if len(latin) == 2:
                    if result_last:
                        result_last.clear()
                    result_last.append(wordMap[y][9])
    return result_first, result_last


def middle(s):
    result_mid = ""
    for i in range(1, len(s) - 1):
        x = s[i]
        if x not in wordMap:
            continue
        m = wordMap[x][6]
        yy = s[i - 1]
        if yy in ("a", "o", "v"):
            if x == "g":
                m = wordMap[x][2]
        if yy not in ("a", "o", "v"):
            if x == "g":
                m = wordMap[x][7]
        # solving g before a or o
        if x == "g":
            y = s[i + 1]
            if y in ("a", "o", "v"):
                # ANG FIX: a G directly after 'n' ("ng") before 'a'/'o'
                # takes the ANG shape U+188A U+1871 U+1871 (desktop Fix 1,
                # G.gMiddleAngGa): the ANG form plus the double-tooth
                # form. The old code overwrote the ANG form with the
                # double-tooth form alone, dropping the ANG.
                if ANG_BUG_FIX and yy == "n":
                    m = wordMap[x][7] + wordMap[x][6]
                else:
                    m = wordMap[x][6]
        if x in ("n", "d"):
            y = s[i + 1]
            if y in ("a", "e", "i", "o", "v", "u", "A", "E", "U"):
                m = wordMap[x][7]
        if x in ("N", "T", "D"):
            m = wordMap[x][7]
        if x in ("b", "p", "k", "f"):
            y = s[i + 1]
            if y in ("o", "u", "v", "U"):
                m = wordMap[x][7]
        if x in ("h", "g"):
            y = s[i + 1]
            if y in ("e", "i", "w"):
                m = wordMap[x][7]
        if x in ("h", "g"):
            y = s[i + 1]
            if y == "u":
                m = wordMap[x][8]
        if x == "u" and i == 1:
            m = wordMap[x][7]
        if x == "i":
            y = s[i - 1]
            if y in ("a", "e", "o", "v"):
                m = wordMap[x][7]
        if x == "g":
            y = s[i - 1]
            w = s[i + 1]
            if y == "i":
                if w not in ("a", "e", "i", "o", "u") and y != "v":
                    for j in range(1, i + 1):
                        z = s[i + 1 - j]
                        if z in ("a", "o", "v", "A"):
                            m = wordMap[x][2]
        if x in ("h", "g"):
            y = s[i + 1]
            if y == "a":
                if i == len(s) - 2:
                    m = wordMap[x][10]
        if x == "n":
            y = s[i + 1]
            if y in ("a", "e"):
                if i == len(s) - 2:
                    m = wordMap[x][10]
        if x in ("m", "l", "y", "r"):
            y = s[i + 1]
            if y in ("a", "e"):
                if i == len(s) - 2:
                    m = wordMap[x][9]
        result_mid = result_mid + m
    return result_mid


def get_ends_class(word):
    new_words = []
    i_ret = 0
    if word == oArr[0]:
        new_words.append(eArr[3] + uArr[9])
        new_words.append(oArr[9])
        new_words.append(oArr[6])
    elif word == eArr[3] + uArr[11]:
        new_words.append(eArr[3] + uArr[9])
        new_words.append(uArr[3])
    elif len(word) > 2:
        sc_last = word[-1]
        s_pre_last = word[-2]
        sub_word_pre = word[:-2]
        if sc_last == aArr[11]:
            if s_pre_last == nArr[10]:
                sub_word_pre += nArr[7] + aArr[9]
                i_ret = 1
            elif s_pre_last == mArr[9]:
                sub_word_pre += mArr[6] + aArr[9]
                i_ret = 2
            elif s_pre_last == lArr[9]:
                sub_word_pre += lArr[6] + aArr[9]
                i_ret = 3
            elif s_pre_last == yArr[9]:
                sub_word_pre += yArr[6] + aArr[9]
                i_ret = 4
            elif s_pre_last == rArr[9]:
                sub_word_pre += rArr[6] + aArr[9]
                i_ret = 5
        elif s_pre_last == wArr[6] and sc_last == aArr[9]:
            sub_word_pre += oArr[9] + aArr[11]
            i_ret = 6
        if i_ret != 0:
            new_words.append(sub_word_pre)
    return new_words


def excute(latin):
    result = []
    word_length = len(latin)
    result_first = ""
    result_mid = ""
    result_last = []
    if word_length == 1 and latin in wordMap:
        result_first = wordMap[latin][0]
    elif word_length == 2:
        result_first, result_last = first_and_last(latin)
    else:
        result_first, result_last = first_and_last(latin)
        result_mid = middle(latin)
    if result_last:
        for item in result_last:
            result.append(result_first + result_mid + item)
    else:
        result.append(result_first)
    return result


def excute_ex(latin):
    result = []
    res_words = excute(latin)
    for w in res_words:
        if len(w) > 0:
            result.append(w)
            new_word = get_ends_class(w)
            if new_word:
                result.extend(new_word)
    database = databases.get(latin)
    if database is not None:
        trim = database.strip()
        if trim in result:
            result.remove(trim)
        result.insert(0, trim)
    tein = dagbr.get(latin)
    if tein is not None:
        trim = tein.strip()
        if trim in result:
            result.remove(trim)
        result.insert(0, trim)
    return result


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--lexicon":
        # ANG check over the full 499,925-word dictionary: for every word whose
        # Z52 form contains NG+G (U+186C followed by G), does the typed-latin
        # splicer produce the ANG form? Needs latin keys, so use dictionary.txt.
        import os
        n_total = n_ang = 0
        dict_path = os.path.expanduser("~/workspace/paiza/data/dictionary.txt")
        with open(dict_path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 2:
                    continue
                latin, z52 = parts[0], parts[1]
                # NG+G in the dictionary form: U+186C (ᡬ) followed by a G form
                # (U+188A ANG, or U+186A U+186A double-tooth, or U+1871 U+1871?)
                # The audit counts words where the Z52 has "ng" spelled with ANG.
                if "ᡬ" in z52 and "ᢊ" in z52:
                    n_total += 1
        print(f"dictionary words containing both NG-mark and ANG form: {n_total}")
        sys.exit(0)
    for latin in args:
        print(f"{latin}: {excute_ex(latin)}")
