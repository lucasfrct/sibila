from dotenv import load_dotenv
from openai import OpenAI
import concurrent.futures
import chromadb
import uuid
import os

from document import Doc

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class Embedding:
    def __init__(self):
        
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)

        self.chunks = []
        self.metadatas = []
        self.embeddings = []

        self.model = "text-embedding-ada-002"
        # self.collection = "my_collection"
        self.collection = "train"
        self.path = "./data"
        self.client = chromadb.PersistentClient(path=self.path)
        self.db = self.client.get_or_create_collection(name=self.collection)

    def document(self, doc: Doc):
        self.doc = doc
        self.chunks, self.metadatas = self.doc.chunks_and_metadatas

    def create(self, data = ""):
        embedding = self.openai_client.embeddings.create(input=data, model=self.model)
        return embedding.data[0].embedding

    def generate(self):
        print("        - - - > ", end='', flush=True)
        for i, chunk in enumerate(self.chunks):
            self.embeddings.append(self.create(chunk))
            print(".", end='', flush=True)

        print("\n", end='', flush=True)

    def save(self):
        self.record(self.chunks, self.metadatas, self.embeddings)

    def record(self, chunks, metadatas, embeddings):
        ids = self.create_ids(chunks)
        self.db.add(embeddings=embeddings, documents=chunks, metadatas=metadatas, ids=ids)
        print(f"        - - - > Dados do pdf {self.doc.name} gravados com suceeso! {len(chunks)} Chunks")

    def create_ids(self, chunks):
        return [str(uuid.uuid4()) for _ in chunks]

    @property
    def data(self):
        return self.chunks, self.metadatas, self.embeddings

    def query(self, question):
        query_embedding = self.create(question)
        results = self.db.query(query_embeddings=[query_embedding], n_results=3)
        return results

    def search(self, question):
        formatted_list = []

        relevant_documents = self.query(question)
        for i, doc in enumerate(relevant_documents["documents"][0]):
            formatted_list.append("[{}]: {}".format(relevant_documents["metadatas"][0][i]["source"], doc))
        
        documents_str = "\n".join(formatted_list)
        return documents_str

    def prompt_keywords(self, documents):
        prompt_template = """Você é um assistente de IA com experiencia de um bibliotecário organizado. 
            Você tem uma alta capacidade de organizar idéias, documentos, assuntos e sessões e é capaz de sintetizar muito bem diversos assuntos. 
            Você extrai palavras chaves dos textos com base nos documentos a baixo.
            Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
            Suas repostas são apenas baseadas no documento e não deve inventar, adicionar ou alucinar com qualquer dado extra ao documento.
            Quando o dado não está no documento, você deve responder com não sei, e se estiver no documeto, deve manter o dado com precisão.
            Cite a fonte  quando fornecer a informação. 
            Gere uma lista de 10 palavras chaves separadas por virgula que representem o assunto abordado nos documentos abaixo sem que se perca o sentido ou o conceito apresentado.
            Documentos:
            {documents}
        """
        return prompt_template.format(documents=documents)

    def prompt_resume(self, documents):
        prompt_template = """Você é um assistente de IA com experiencia de um bibliotecário organizado. 
            Você tem uma alta capacidade de organizar idéias, documentos, assuntos e sessões e é capaz de sintetizar muito bem diversos assuntos. 
            Você extrai resumos que capturam a execência dos textos com base nos documentos a baixo.
            Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
            Suas repostas são apenas baseadas no documento e não deve inventar, adicionar ou alucinar com qualquer dado extra ao documento.
            Quando o dado não está no documento, você deve responder com não sei, e se estiver no documeto, deve manter o dado com precisão.
            Cite a fonte  quando fornecer a informação. 
            Gere um resumo de no máximo 50 palavras que representem o assunto abordado nos documentos abaixo sem que se perca o sentido ou o conceito apresentado.
            Documentos:
            {documents}
        """
        return prompt_template.format(documents=documents)

    def prompt_names(self, documents):
        prompt_template = """Você é um assistente de IA com experiencia de um bibliotecário organizado. 
            Você tem uma alta capacidade de organizar idéias, documentos, assuntos e sessões e é capaz de sintetizar muito bem diversos assuntos. 
            Você extrai nomes de pessoas, autores e citações de terceiros nos textos com base nos documentos a baixo.
            Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
            Suas repostas são apenas baseadas no documento e não deve inventar, adicionar ou alucinar com qualquer dado extra ao documento.
            Quando o dado não está no documento, você deve responder com não sei, e se estiver no documeto, deve manter o dado com precisão.
            Cite a fonte  quando fornecer a informação. 
            Gere uma lista de nomes encontrados separadas por virgula que estejam contidos nos documentos abaixo.
            Caso não encontre nomes, responder estritamente com 0.
            Documentos:
            {documents}
        """
        return prompt_template.format(documents=documents)

    def prompt_publisher(self, documents):
        prompt_template = """Você é um assistente de IA com experiencia de um bibliotecário organizado. 
            Você tem uma alta capacidade de organizar idéias, documentos, assuntos e sessões e é capaz de sintetizar muito bem diversos assuntos. 
            Você extrai título, nomes da editoraas, ano de publicação, numero da edição, autor do livro, ISBN e contatos nos textos com base nos documentos a baixo.
            Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
            Suas repostas são apenas baseadas no documento e não deve inventar, adicionar ou alucinar com qualquer dado extra ao documento.
            Quando o dado não está no documento, você deve responder com não sei, e se estiver no documeto, deve manter o dado com precisão.
            Cite a fonte  quando fornecer a informação. 
            Gere um texto simples com título, subtítulo ou nome da obra, editora, ano de publicaçãao, numero da edição, autores e contatos.
            Caso não encontre essas informçaoes, responder estritamente com "-".
            Documentos:
            {documents}
        """
        return prompt_template.format(documents=documents)

    def prompt_intention(self, documents):
        prompt_template = """Você é um assistente de IA com experiencia de um escritor que resume textos. 
            Você tem uma alta capacidade de organizar idéias, assuntos e é capaz de sintetizar muito bem diversos temas e suas intenções. 
            Você faz resumos que conseguem capturar o sentido do texto e categorizar em um tipo de intenção.
            Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
            Suas repostas são apenas baseadas no documento e não deve inventar, adicionar ou alucinar com qualquer dado extra ao documento.
            Cite a fonte  quando fornecer a informação. 
            Faça uma análise do documento e classifique a inteçao do texto seguindo estritamnte a seguinte lista:
                - Informar
                - Persuadir
                - Entreter
                - Instruir
                - Expressar sentimentos ou opiniões
                - Questionar
                - Convocar ação
                - Descrever
            Caso não encontre essas informçaoes, responder estritamente com "-".
            A classificaçao deve ser feita somente com opçoes da lista e de ve expressar a melhor proximidade possível entre o texto e intençao selecionada
            se o texto tiver mais que uma inteção, colocar as intenções separadas entre virgulas.
            Documentos:
            {documents}
        """
        return prompt_template.format(documents=documents)

    def prompt_humor(self, documents):
        prompt_template = """Você é um assistente de IA versada na detecçao de humor humano em textos. 
            Você tem uma alta capacidade de sintetizar em uma palavra o humor humano prsente no texto. 
            Você responde as dúvidas dos usuários com bases nos documentos a baixo.
            Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
            Suas repostas são apenas baseadas no documento e não deve inventar, adicionar ou alucinar com qualquer dado extra ao documento.
            Quando o dado não está no documento, você deve responder com '-', e se estiver no documeto, deve manter o dado com precisão.
            Cite a fonte  quando fornecer a informação. 
            Categorize o documento abaixo em expressões de humor com base na lista abaixo, separando entre vírgulas os estdados de humor quando houver mais de 1.
                - Feliz
                - Triste
                - Ansioso
                - Irritado
                - Entusiasmado
                - Melancólico
                - Relaxado
                - Frustrado
                - Esperançoso
                - Desapontado
            Documentos:
            {documents}
        """
        return prompt_template.format(documents=documents)

    def prompt_objective(self, documents):
        prompt_template = """Você é um assistente de IA especializado em detectar os objetos centrais de textos. 
            Você tem uma alta capacidade resolutiva, e um pragmatismo exagerado para pontual objetivos em um texto. 
            Você responde as dúvidas dos usuários com bases nos documentos a baixo.
            Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
            Suas repostas são apenas baseadas no documento e não deve inventar, adicionar ou alucinar com qualquer dado extra ao documento.
            Quando o dado não está no documento, você deve responder '-', e se estiver no documeto, deve manter o dado com precisão.
            resuma em no máximo 20 palavras o objetivo desse documento. 
            Documentos:
            {documents}
        """
        return prompt_template.format(documents=documents)

    def prompt_type_text(self, documents):
        prompt_template = """Você é um assistente de IA especilista em língua portuguesa do brasil. 
            Você tem uma alta capacidade de classificar textos conforme a a tipologia sintática. 
            Você responde as dúvidas dos usuários com bases nos documentos a baixo.
            Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
            Suas repostas são apenas baseadas no documento e não deve inventar, adicionar ou alucinar com qualquer dado extra ao documento.
            Quando o dado não está no documento, você deve responder com '-', e se estiver no documeto, deve manter o dado com precisão.
            Classifiques os documentos abaixo conforme a lista:
                - Narrativo
                - Descritivo
                - Dissertativo-argumentativo
                - Expositivo
                - Injuntivo ou instrucional
                - Predominantemente dialógico (diálogos)
                - Relato pessoal
            Se houver mais de uma tipo, separe os tipos entre virgulas.
            Documentos:
            {documents}
        """
        return prompt_template.format(documents=documents)

    def prompt_subject(self, documents):
        prompt_template = """Você é um assistente de IA especialista em classificações de assuntos e gênero de textos. 
            Você tem uma alta capacidade assuntos e gênero de textos em apenas uma palavra. 
            Você responde as dúvidas dos usuários com bases nos documentos a baixo.
            Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
            Suas repostas são apenas baseadas no documento e não deve inventar, adicionar ou alucinar com qualquer dado extra ao documento.
            Quando o dado não está no documento, você deve responder com '-', e se estiver no documeto, deve manter o dado com precisão.
            Categorize os documentos abaixo conforme a lista:

                - Literatura e ficção
                - Ciência e tecnologia
                - História e geografia
                - Arte e cultura
                - Política e economia
                - Saúde e bem-estar
                - Educação e pedagogia
                - Meio ambiente e sustentabilidade
                - Psicologia e comportamento humano
                - Esportes e lazer
            Se houver mais de uma classificaçao, retirno num texto separado por vírgula.
            Documentos:
            {documents}
        """
        return prompt_template.format(documents=documents)

    # ficahmento de tese
    def prompt_registration(self, documents):
        prompt_template = """Você é um assistente de IA especilista em teses de doutordo com alto rigor acadêmico. 
            Você tem uma alta capacidade criar fichamento para teses usando textos, conectando assuntos e expressões anotadas. 
            Você responde as dúvidas dos usuários com bases nos documentos a baixo.
            Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
            Suas repostas são apenas baseadas no documento e não deve inventar, adicionar ou alucinar com qualquer dado extra ao documento.
            Quando o dado não está no documento, você deve responder com '-', e se estiver no documeto, deve manter o dado com precisão.
            Usando o documento abaixo crie uma fichamento de doutorado que expresse a citaçao e depois a idéia central da expressão de cada documento connectando toda informaçoa possível. 
            Documentos:
            {documents}
        """
        return prompt_template.format(documents=documents)

    def prompt_generic(self, documents):
        prompt_template = """Você é um assistente de IA com experiencia de um bibliotecário com um orátória sofisticada e organizada. 
            Você tem uma alta capacidade de organizar idéias, documentos, assuntos e sessões onde discorre coerentemente sobre os assuntos lhe passados. 
            Você responde as dúvidas dos usuários com bases nos documentos a baixo.
            Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
            Suas repostas são apenas baseadas no documento e não deve inventar, adicionar ou alucinar com qualquer dado extra ao documento.
            Quando o dado não está no documento, você deve responder com não sei, e se estiver no documeto, deve manter o dado com precisão.
            Cite a fonte  quando fornecer a informação. 
            Documentos:
            {documents}
        """
        return prompt_template.format(documents=documents)

    def completions(self, prompt, question):
         return self.openai_client.chat.completions.create(
            messages=[
                {"role": "system","content": f"{prompt}"},
                {"role": "user","content": f"{question}"}
            ],
            model="gpt-3.5-turbo",
            max_tokens=500,
            temperature=0
        )

    def keys_generation(self, documents):
        prompt = self.prompt_keywords(documents)
        chat_completion = self.completions(prompt, documents)
        keys = chat_completion.choices[0].message.content.split(",")
        return  [key.strip().rstrip('.').rstrip('\n') for key in keys]

    def names_generation(self, documents):
        prompt = self.prompt_names(documents)
        chat_completion = self.completions(prompt, documents)
        names = chat_completion.choices[0].message.content.split(",")
        return [item for item in names if item != '0']

    def resume_generation(self, documents):
        prompt = self.prompt_resume(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def title_generation(self, documents):
        prompt = self.prompt_publisher(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def intention_generation(self, documents):
        prompt = self.prompt_intention(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def humor_generation(self, documents):
        prompt = self.prompt_humor(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def objective_generation(self, documents):
        prompt = self.prompt_objective(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def type_text_generation(self, documents):
        prompt = self.prompt_type_text(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content
        
    def subject_generation(self, documents):
        prompt = self.prompt_subject(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content
        
    def registration_generation(self, documents):
        prompt = self.prompt_registration(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content
        
    def metadata_generation(self):

        print("        - - - > ", end='', flush=True)

        for i in range(len(self.chunks)):
            
            chunk = self.chunks[i]
            metadata = self.metadatas[i]

            with concurrent.futures.ThreadPoolExecutor() as executor:

                intentions = executor.submit(self.intention_generation, chunk)
                type_text = executor.submit(self.type_text_generation, chunk)
                objective = executor.submit(self.objective_generation, chunk)
                description = executor.submit(self.resume_generation, chunk)
                subject = executor.submit(self.subject_generation, chunk)
                humor = executor.submit(self.humor_generation, chunk)
                title = executor.submit(self.title_generation, chunk)
                names = executor.submit(self.names_generation, chunk)
                keys = executor.submit(self.keys_generation, chunk)
                anotation = executor.submit(self.registration_generation, chunk)

                metadata_filled = { 
                    "title": title.result(),
                    "humor": humor.result(),
                    "type": type_text.result(),
                    "subject": subject.result(),
                    "objective": objective.result(),
                    "keys": ", ".join(keys.result()), 
                    "intentions": intentions.result(),
                    "names":  ", ".join(names.result()), 
                    "description": description.result(),
                    "anotation": anotation.result(),
                }

                # registration = executor.submit(self.registration_generation, self.text_metadata(metadata_filled))
                # metadata_registration = { "registration": registration.result()}

                self.metadatas[i] = {**metadata, **metadata_filled }
                print(self.metadatas[i]['anotation'])

            print(".", end='', flush=True)

        print("\n", end='', flush=True)
        return self.metadatas[i]

    def text_metadata(self, metadata):
        text_metadata = ""
        for k, v in metadata.items():
            text_metadata += f"{k}: {v}\n"
        return text_metadata

    def run(self, question):
        prompt = self.prompt_generic(self.search(question))
        chat_completion = self.completions(prompt, question)
        return chat_completion.choices[0].message.content

