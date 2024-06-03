# flake8: noqa: E501


from src.routines import migrate

from src.modules.document.paragraph_metadata import ParagraphMetadata
from src.modules.document import paragraph_metadata_retrieval as PragraphRetrieval
from src.modules.document import paragraph_metadata_repository as PragraphRepository


def run():
    p = ParagraphMetadata()
    p.content = """ 
            2.1 Poderão se inscrever no Plano, nas seguintes categorias:   
            2.1.1 Beneficiário Titular: pessoa física contratante 
            2.1.2 Beneficiários Dependentes: considerados como tais aqueles também admitidos pelo regime previdenciário oficial vigente, a saber: 
                a)  cônjuge;  
                b)  companheiro, havendo união estável, na forma da lei, sem eventual concorrência com o cônjuge, salvo por decisão judicial; 
                c)  filhos,  adotivos  ou  não,  e  enteados  não  emancipados,  de  qualquer  condição, menores de 18 (dezoito) anos incompletos;  
                d)  filhos de qualquer idade comprovadamente inválidos; 
                e)  pais comprovadamente dependentes econômicos; 
                f) menor que, por determinação judicial, se ache sob a guarda e responsabilidade  do  beneficiário  titular  ou  sob  sua  tutela,  desde  que  não possua bens  ou  meios  suficientes para  o  próprio  sustento  e  educação, devendo tal condição ser comprovada.  
            2.2  A  adesão  dos  Beneficiários  Dependentes  fica  condicionada  à  participação  do Titular.  
            2.3  A  inclusão  do  Beneficiário  Titular  e  de  seus  respectivos  Dependentes  será processada  mediante  preenchimento  de  Termo  de  Adesão,  que  vinculará  a  este contrato para todos os fins de direito.  
            2.3.1  As  inclusões  de  novos  Dependentes  dar-se-á  por  celebração  de  Termo  de Adesão que vinculará a este contrato para todos os fins de direito.  
            2.4 No momento da contratação, nas inclusões posteriores e quando a CONTRATADA julgar necessário, a CONTRATANTE obriga-se fornecer à CONTRATADA documentos comprobatórios do vínculo do Titular com a CONTRATANTE,  bem  como  da  relação  de  dependência  entre  os  Dependentes  e  o Titular.  
            2.5 É assegurada a inclusão:  a)  do recém-nascido, filho natural ou adotivo do Beneficiário, isento do cumprimento  dos  períodos  de  carência  já  cumpridos  pelo  beneficiário  e  não cabendo  qualquer  alegação  de  doença  ou  lesão  preexistente,  desde  que  a inscrição  ocorra  no  prazo  máximo  de  30  (trinta)  dias  após  o  nascimento  ou adoção, e que o beneficiário (pai ou mãe) tenha cumprido o prazo de carência de 300 (trezentos) dias para parto a termo; b)  do filho adotivo, menor de 12 (doze) anos, com aproveitamento dos períodos de carência já cumpridos pelo Beneficiário adotante, cabendo a exigência de 3 Cobertura Parcial Temporária para os casos de Doença ou Lesão Pré-Existente.  
            2.5.1 Ultrapassado o prazo previsto no item antecedente, será obrigatório o cumprimento integral dos respectivos prazos de carência.   
            2.5.2  O  Dependente  que  vier  a  perder  a  condição  de  dependência  poderá  assinar Contrato em seu próprio nome, em até 30 (trinta) dias a contar da data da perda do direito  de  Beneficiário  Dependente,  aproveitando  as  carências  já  cumpridas  neste Contrato.  
            2.6  O  Beneficiário  Titular  é  responsável  pela  constante  atualização  dos  dados cadastrais  informados,  em  relação  a  si  e  aos  seus  Dependentes,  inclusive  com  o envio  de  documentos  quando  se  fizer  necessário,  incluindo  eventual  alteração  de endereço, que deverá ser comunicada imediatamente à CONTRATADA.  
            2.7  O  CONTRATANTE  e  a  CONTRATADA  poderão  negociar,  entre  si,  a  ampliação do  rol  de  dependentes,  independente  de  alteração  no  rol  do  regime  previdenciário oficial,  desde  que  respeitados  os  limites  de  parentesco  definidos  na  legislação vigente.
        """
            
    p.generate_phrases()
    p.generate_lines()
    p.generate_chunks()
    p.new_uuid()
    p.export_dataset()
    # print("Documentos: ", PragraphRepository.save(p))
    # print("DOC Retrieval: ", PragraphRetrieval.save(p))
    # print("DOC Retrieval: ", PragraphRetrieval.save_with_embedings(p))
    
    # print("QUERY: ", [a.content for a in PragraphRetrieval.query("rol do regime", 10)]) 
    # print("QUERY: ", [a.content for a in PragraphRetrieval.query_with_embeddings("rol do regime", 10)])
    

if __name__ == "__main__":
    migrate.tables()
    run()
