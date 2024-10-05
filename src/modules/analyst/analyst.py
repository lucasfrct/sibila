# flake8: noqa: E501
from typing import List

from src.modules.analyst import injuctive_relief_against_execution_of_an_illegal_act_retieval as InjuctiveReliefAgainstExecutionOfAnIllegalActRetieval
from src.modules.analyst import hipothesis_of_inadequate_execution_retrieval as HipothesisOfInadequateExecutionRetrieval
from src.modules.analyst import hipothesis_of_inadequate_execution_scope as HipothesisOfInadequateExecutionScope
from src.modules.analyst import redibitory_vides_retrieval as RidibitoryVidesRetieval
from src.modules.analyst import null_hipothesis_retrieval as NullHipothesisRetieval
from src.modules.legislation import legislation as Legislation


class Analyst:
    def __init__(self):
        self.clauses = []
        self.clause: str = ""
        
        self.correlation: float = 2.5

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
        Correlação legislativa: procura leis que tem relação com a cláusula.
        Returns:
            List[dict]: retorna uma lista de leis correlacionadas.
        """
        laws: List[dict] = []
        
        laws.extend(Legislation.federal_constitution().query(self.clause, 5, self.correlation))
        # laws.extend(Legislation.dnpdc_proposition().query(self.clause, 5, self.correlation))
        
        return laws 

    def hipothesis_of_inadequate_execution(self) -> List[dict]:
        """
        Enumera as hipóteses de execução inadequada da cláusula
        Returns:
            List[dict]: retorna uma lista de hipotesis.
        """
        hipothesis: List[dict] = []
        hipothesis.extend(HipothesisOfInadequateExecutionRetrieval.query(self.clause, 5, self.correlation))
        return HipothesisOfInadequateExecutionScope.execution_out_of_time(hipothesis)
    
    def injuctive_relief_against_execution_of_an_illegal_act(self)-> List[dict]:
        """
        Tutela Inibitória de Execução de Ilícito:
        Trata-se de “ação de conhecimento” de natureza preventiva, destinada a impedir a prática, a repetição ou a continuação do ilícito.
        Deve selecionar uma lista de cláusulas que inibem a execução de algum ato ilícito já conhecido relacionados a cláusula presente.
        
        Returns:
            List[dict]: retorna uma lista de cláusulas com seus inbitórios.
        """
        inhibitory = []
        
        inhibitory.extend(InjuctiveReliefAgainstExecutionOfAnIllegalActRetieval.query(self.clause, 5, self.correlation))

        return inhibitory

    def redibitory_vides(self):
        """
        Vícios redibitórios:
        O vício redibitório é um defeito oculto em coisa objeto de contrato comutativo, tornando-a imprópria ou desvalorizada.
        
        Returns:
            List[dict]: retorna uma lista de cláusulas com seus vícios redibitórios.
        """
        redibitory = []
        
        redibitory.extend(RidibitoryVidesRetieval.query(self.clause, 5, self.correlation))
        
        return redibitory

    def null_hypothesis(self):
        """
         São situações em que um ato jurídico ou um processo é considerado inválido ou sem efeito devido à violação de normas legais. 
         Existem dois tipos principais:
            Nulidade absoluta: 
                Ocorre quando o ato infringe normas de ordem pública, resultando em vício grave e insanável. Pode ser alegada a qualquer tempo e por qualquer interessado, e o juiz pode declará-la de ofício. Exemplos incluem falta de capacidade do agente ou objeto ilícito.
            Nulidade relativa: 
                Acontece quando o ato possui vícios menos graves que afetam interesses particulares, sendo passível de convalidação. Deve ser alegada pela parte interessada dentro de um prazo específico. Exemplos são a coação ou erro na manifestação de vontade.
         Ambas visam garantir a regularidade dos atos jurídicos e proteger os direitos das partes envolvidas.
         
         Returns:
            List[dict]: retorna uma lista de cláusulas com suas hipóteses.
        """
        hipothesys = []
        
        hipothesys.extend(NullHipothesisRetieval.query(self.clause, 5, self.correlation))

        return hipothesys

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
