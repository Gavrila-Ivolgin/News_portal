#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter()
def censor(text):
    """
    Фильтр, который заменяет буквы нежелательных слов в заголовках и текстах статей на символ "*"
    :param text: проверяемый объект <str>
    :return: объект <str> с замененным текстом "*"
    """
    list =

    print(str(text).lower())
    return str(text).lower()
