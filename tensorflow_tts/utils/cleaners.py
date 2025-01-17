# -*- coding: utf-8 -*-
# Copyright (c) 2017 Keith Ito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re

from tensorflow_tts.utils.korean import tokenize as ko_tokenize
from tensorflow_tts.utils.number_norm import normalize_numbers
from unidecode import unidecode

try:
    from german_transliterate.core import GermanTransliterate
except:
    pass

# Regular expression matching whitespace:
_whitespace_re = re.compile(r"\s+")

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [
    (re.compile("\\b%s\\." % x[0], re.IGNORECASE), x[1])
    for x in [
        ("wlh", "wallahi"),
        ("isa", "inshaallah"),
        ("slm", "salam"),
        ("aslm", "assalamu alaikum"),
        ("aslm", "assalam alaikum"),
        ("wslm", "wa'alaikumu salam"),
        ("w/slm", "wa'alaikumu salam"),
        ("saw", "salallahu alaihi wasalam"),
        ("as", "alaihi salam"),
        ("sw", "subhanahu wata’allah"),
        ("ra", "radiyallahu anhu"),
        ("ra", "radiyallahu anha"),
        ("alhmd", "alhamdulillah"),
        ("ykk", "yakake"),
        ("ykk", "yakike"),
        ("ngd", "nagode"),
        ("gsky", "gaskiya"),
        ("lfy", "lafiya"),
        ("lpy", "lafiya"),
        ("gdy", "godiya"),
        ("hkr", "hakuri"),
        ("alh", "alhaji"),
        ("haj", "hajiya"),
        ("hkr", "hakuri"),
        ("mal", "mallam"),
        ("mal", "malama"),
        ("srk", "sarki"),
        ("klu", "kalau"),
        ("lbr", "labari"),
        ("lbr", "labarai"),
        ("bb", "babu"),
        ("lit", "litinin"),
        ("lrb", "laraba"),
        ("lhd", "lahadi"),
        ("asb", "asabar"),
        ("tlt", "talata"),
        ("min", "minti"),
        ("kyye", "kiyaye"),
        ("wnn", "wannan"),
        ("y", "ya"),
        ("yy", "yaya"),
        ("lkc", "lokaci"),
        ("lkcn", "lokacin"),
        ("mgn", "magana"),
        ("hk", "haka"),
        ("ahk", "ahaka"),
        ("ynz", "yanzu"),
        ("bbu", "babu"),
        ("dmw", "damuwa"),
        ("bkt", "bukata"),
        ("hausw", "hausawa"),
        ("2rai", "turai"),
        ("2ra", "tura"),
        ("lau", "kalau"),
        ("dftn", "dafatan"),
        ("mgd", "mungode")
    ]
]


def expand_abbreviations(text):
    for regex, replacement in _abbreviations:
        text = re.sub(regex, replacement, text)
    return text


def expand_numbers(text):
    return normalize_numbers(text)


def lowercase(text):
    return text.lower()


def collapse_whitespace(text):
    return re.sub(_whitespace_re, " ", text)


def convert_to_ascii(text):
    return unidecode(text)


def basic_cleaners(text):
    """Basic pipeline that lowercases and collapses whitespace without transliteration."""
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text


def transliteration_cleaners(text):
    """Pipeline for non-English text that transliterates to ASCII."""
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text


def english_cleaners(text):
    """Pipeline for English text, including number and abbreviation expansion."""
    #text = convert_to_ascii(text)
    text = lowercase(text)
    text = expand_numbers(text)
    text = expand_abbreviations(text)
    text = collapse_whitespace(text)
    return text


def korean_cleaners(text):
    """Pipeline for Korean text, including number and abbreviation expansion."""
    text = ko_tokenize(
        text
    )  # '존경하는' --> ['ᄌ', 'ᅩ', 'ᆫ', 'ᄀ', 'ᅧ', 'ᆼ', 'ᄒ', 'ᅡ', 'ᄂ', 'ᅳ', 'ᆫ']
    return text

def german_cleaners(text):
    """Pipeline for German text, including number and abbreviation expansion."""
    try:
        text = GermanTransliterate(replace={';': ',', ':': ' '}, sep_abbreviation=' -- ').transliterate(text)
    except NameError:
        raise ModuleNotFoundError("Install german_transliterate package to use german_cleaners")
    return text
