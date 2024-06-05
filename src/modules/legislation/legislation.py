# flake8: noqa: E501

import logging
import traceback

from src.modules.legislation import federal_constitution_retrieval as FederalConstitutionRetrieval

def federal_constitution():
    return FederalConstitutionRetrieval

def dnpdc_proposition():
    """ proposiçoes do DNPDC """
    return FederalConstitutionRetrieval

def procon_proposition():
    """ proposiçoes do PROCON """
    return FederalConstitutionRetrieval

def sne_proposition():
    """ proposiçoes do SNE """
    return FederalConstitutionRetrieval

def inspection_based_revision_model():
    """ modelo revisional baseado em inspação """
    return FederalConstitutionRetrieval



