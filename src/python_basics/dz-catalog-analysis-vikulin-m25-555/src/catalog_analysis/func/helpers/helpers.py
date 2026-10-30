from typing import List, Set


def protect_not_empty(collection: List|Set):
    if not collection:
        # предохранитель от пустого списка и None на входе
        raise ValueError("Input list must be not empty")

def clear(collection: List):
    if collection is None:
        raise ValueError("Collection is None, which is not allowed")
    
    # оверхэд на конструктор списка, зато без side-effects
    return [item for item in collection if item is not None]