# flake8: noqa: E501

import sys

from src.utils.colors import colors
from src.utils import writer as Writer
from src.models.ollama import ModelOllama
from src.models.open_ai import ModelOpenAI
from src.modules.analyst.analyst import Analyst


# Coleta dos dados - rotular dados
# Pré processamento
# - limpeza do texto
# - tokenizaçao
# - remoçao de palavra de parada
# - normalização (acentuaçao, ortografia, conversão para minúsculas)
# - lemarizaçao (extrair o lema da palavra)
# - stemming (extrair radical da palavras)
# Extraçao de características
# - análise sintática (tags e entidades)
# - janela de context (tags e entidades)
# - bag of words (matrix de )
# - TF-IDF (Term Frequency-Inverse Document Frequency).
# - Embeddings de palavras

class Agent:

    def __init__(self):

        self.ollama = ModelOllama()
        self.openai = ModelOpenAI()
        self.analyst = Analyst()

    def welcome(self):
        print("\n", f"{colors.WARNING}Como posso ajudar? {colors.ENDC}", "\n")

    def available(self):
        print("\n", f"{colors.WARNING}Quer perguntar mais alguma coisa? {
              colors.ENDC}", "\n")

    def question(self, question):
        answer = self.openai.question(question, "")
        self.write(answer)
        self.available()
        return answer

    def write(self, content, delay=0.01):
        """ escreve a resposta num terminal com delay. """
        Writer.delay(content, delay)

    def run(self):
        self.welcome()
        for line in sys.stdin:
            self.question(line)

    def analyze(self):
        
        self.analyst.add_clause( """ 
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
            """)
        
        predic = self.analyst.predict()

        promt_errors = """"
        O documento é uma contrato de plano de saúde sobre a jurisdiçao brasileira de orgãos como, ANS, CFM, JusBrasil, ANVISA, CDC, 
        levante no mínimo 3 erros jurídicos diferentes entre si nessa cláusula quando houver erros. me forneça a resposta num formato json cru, sem comentários, com o campo tags, sendo este um array com no mínimo 3 tags relacionadas a justificativa encontrada, outro campo com a justificativa sendo uma string descrevendo o erro encontrado. outro campo com o sentimento, positivo ou negativo da justificativa. outro campo com a intenção geral a justificativa em poucas palavras. outro campo chamado adendo que escreve o novo trecho para a cláusula adicionando a correção com base na justiticafiva encontrada de modo a ser parte da narrativa do texto original tomando atenção para que não haja repetição de idéias ou cacofonia no texto. Para cada erro crie um objeto { tags: [], justificativa: '', sentimento: '', intenção: '', adendo: ''}. para a resposta siga o formato: [ { tags: [...], justificativa: '', sentimento: '', intencao: '', adendo: '' }, ... ] 
        """
        answer = self.ollama.question(promt_errors, predic)
        # answer = self.openai.question(f"{promt_errors}\n{answer}", predic)
        # answer = self.openai.question(f"{promt_errors}", predic)
        self.write(answer)
