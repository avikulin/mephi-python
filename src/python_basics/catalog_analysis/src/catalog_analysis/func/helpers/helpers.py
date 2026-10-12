from typing import List


def clear(collection: List):
    if collection is None:
        raise ValueError("Collection is None, which is not allowed")
    
    # оверхэд на конструктор списка, зато без side-effects
    return [item for item in collection if item is not None]