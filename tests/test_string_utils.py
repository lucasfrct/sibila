import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.utils import string as String


def test_split_to_lines():
    text = "Linha 1\nLinha 2\n\nLinha 3"
    assert String.split_to_lines(text) == ["Linha 1", "Linha 2", "", "Linha 3"]


def test_split_to_phrases():
    text = "Primeira frase. Segunda frase!" 
    assert String.split_to_phrases(text) == ["Primeira frase.", "Segunda frase!"]


def test_clean():
    text = " Olá, mundo!!!\n"
    assert String.clean(text) == "Ola mundo"
