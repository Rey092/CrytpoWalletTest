# -*- coding: utf-8 -*-


def camel_case_split(text):
    try:
        words = [[text[0]]]

        for c in text[1:]:
            if words[-1][-1].islower() and c.isupper():
                words.append(list(c))
            else:
                words[-1].append(c)

        return " ".join(["".join(word).capitalize() for word in words])
    except TypeError:
        return text
