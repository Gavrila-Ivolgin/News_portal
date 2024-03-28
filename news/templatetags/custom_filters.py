#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
import re
import string

register = template.Library()


@register.filter()
def censor(text):
    """
    Фильтр, который заменяет буквы нежелательных слов в заголовках и текстах статей на символ "*"
    :param text: проверяемый объект <str>
    :return: объект <str> с замененным текстом "*"
    """
    filename = "dict_words.txt"
    text_user = str(text).split()  # ['новость', 'об', 'хорошей', 'погоде']

    try:
        with open(filename, "r", encoding="utf-8", errors="ignor") as file:

            list_words = file.read().lower().split()  # <class 'str'> # ['отличный', 'передовой', ... 'хорошей']

            censor_text = []

            if text_user:
                for word in text_user:
                    # Убираем из проверяемого слова знаки препинания
                    word_clear = re.sub(r'[^\w\s]', '', word)

                    if word_clear.lower() in list_words:
                        censor_word = word_clear[:1] + str(len(word_clear[1:]) * '*')
                        censor_text.append(censor_word)
                    else:
                        censor_text.append(word)

            return " ".join(censor_text)

    except Exception as e:
        print(e)





