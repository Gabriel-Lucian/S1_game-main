"""Loads given file lines to a list an returns it"""


def categorize(wordList) -> dict:
    """Categorizes the given words"""
    result = {
        "easy": [],
        "medium": [],
        "hard": [],
    }

    for word in wordList:
        if len(word) < 5:
            result["easy"].append(word)
        elif len(word) < 7:
            result["medium"].append(word)
        else:
            result["hard"].append(word)

    return result


def text_loader(file_name: str) -> dict:
    """Loads given file lines to a list an returns it"""
    word_list = []

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            word_list.append(line.strip())

        file.close()
    except FileNotFoundError:
        return ["file", "not", "found", "error"]

    return categorize(word_list)
