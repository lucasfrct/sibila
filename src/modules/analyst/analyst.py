# flake8: noqa: E501
from typing import List

from src.modules.legislation import legislation as Legislation

class Analyst:
    def __init__(self):
        self.clauses = []
        self.clause: str = ""
        
        self.correlation: float = 1.5

    
    def add_clause(self, clause: str = ""):
        """
        Adciona uma Cláusula na lista de cláusulas para análise

        Args:
            clause (string): Texto com a cláusula a ser analizada.
        """
        self.clauses.append(clause)
        self.clause = clause

    def predict(self) -> str:
        inference = self.clauses[0]
        return inference

    def legislative_correlation(self) -> List[dict]:
        """
        Correlação legislativa: procura leis que tem relação com essa cláusula.

        Args:
            clause (string): Texto com a cláusula a ser analizada.

        Returns:
            List[str]: retorna alista de leis correlacionadas.
        """
        laws: List[dict] = []
        
        laws.extend(Legislation.federal_constitution().query(self.clause, 5, self.correlation))
        # laws.extend(Legislation.dnpdc_proposition().query(self.clause, 5, self.correlation))
        
        return laws 

    def hipothesis_of_inadequate_execution(self, clause: str = ""):
        """enumera as hipótesis de execuçao inadequada da cláusula"""
        pass

    def injuctive_relief_against_execution_of_an_illega_act(self, valuse: str = ""):
        """tutela inibitória de execuçao de ilícito"""
        pass

    def redibitory_vides(self, clause: str = ""):
        """Vícios redibitórios"""
        pass

    def null_hypothesis(self, clause: str = ""):
        """hipótese de nulidade"""
        pass

    def writing_erros(self, clause: str = ""):
        """erros de redaçao"""
        pass

    def hyposufficiency_conditions(self, clause: str = ""):
        """condicoes de hipossuficiencia"""
        pass

    def conditions_of_compliance(self, clause: str = ""):
        """condiçao de cumprimento"""
        pass

    def future_interests(self, cluase: str):
        """intereses futuros"""
        pass

    def factual_interests(self, clause: str = ""):
        """interesses atuais"""
        pass
