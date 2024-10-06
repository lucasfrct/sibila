# flake8: noqa: E501


from src.routines import migrate

from src.modules.analyst import injuctive_relief_against_execution_of_an_illegal_act_retieval as InjuctiveReliefAgainstExecutionOfAnIllegalActRetieval
from src.modules.analyst import hipothesis_of_inadequate_execution_retrieval as HipothesisOfInadequateExecutionRetrieval
from src.modules.legislation import federal_constitution_retrieval as FederalConstitutionRetrieval
from src.modules.analyst import redibitory_vides_retrieval as RidibitoryVidesRetieval
from src.modules.analyst import null_hipothesis_retrieval as NullHipothesisRetieval

from src.modules.analyst.analyst import Analyst

def run():
    
    
    # 4. Lê o arquivo de cláusulas
    
    # Lê o arquivo de cláusulas
    clause_file = open("./seeder/clause.txt", "r", encoding="utf-8")
    clause_content = clause_file.read()
    clause_file.close()
    
    # # Lê o arquivo de constituiçao federal
    # federal_constitution_file = open("./seeder/federal_constitution.txt", "r", encoding="utf-8")
    # federal_constitution_content = federal_constitution_file.read()
    # federal_constitution_file.close()
    
    # Lê o arquivo de hipoteses de execuçao inadequada
    hipothesis_file = open("./seeder/hipothesis.txt", "r", encoding="utf-8")
    hipothesis_content = hipothesis_file.read()
    hipothesis_file.close()
    
    # # Lê o arquivo de hipótese de eceuçao inibitória
    # inhibitory_file = open("./seeder/inhibitory.txt", "r", encoding="utf-8")
    # inhibitory_content = inhibitory_file.read()
    # inhibitory_file.close()
    
    # # Lê o arquivo de redibitório
    # redibitory_file = open("./seeder/redibitory.txt", "r", encoding="utf-8")
    # redibitory_content = redibitory_file.read()
    # redibitory_file.close()
    
    # Lê o arquivo de hipótese de nulidade
    # null_hipothesis_file = open("./seeder/null_hipothesis.txt", "r", encoding="utf-8")
    # null_hipothesis_content = null_hipothesis_file.read()
    # null_hipothesis_file.close()
    
    # ## salvando aem formato vetorial
    # FederalConstitutionRetrieval.save("./doc/constituicao_do_brasil", "Constituiçao Federal do Brasil Art. 6", 1, federal_constitution_content)
    # HipothesisOfInadequateExecutionRetrieval.save("", clause_content, hipothesis_content)
    # InjuctiveReliefAgainstExecutionOfAnIllegalActRetieval.save("Inibitório 1", clause_content, inhibitory_content)
    # RidibitoryVidesRetieval.save("Redibitório 1", clause_content, redibitory_content)
    # NullHipothesisRetieval.save("Hipótese de nulidade 1", clause_content, null_hipothesis_content)
    
    analyst = Analyst()
    # analyst.add_clause(clause_content)
    # analyst.legislative_correlation()
    # analyst.hipothesis_of_inadequate_execution()
    # analyst.injuctive_relief_against_execution_of_an_illegal_act()
    # analyst.redibitory_vides()
    # analyst.null_hypothesis()
    
    # print(analyst.hipothesis_of_inadequate_execution())
    
    # Catalogretrieval.save("./doc.pdf", "Artigo 2", 18, content)
    # print(Catalogretrieval.query("quando o titular é responsável"))
    

if __name__ == "__main__":
    migrate.tables()
    run()
