
from openai import OpenAI

from src.config.openai import OPENAI_API_KEY
from src.prompts import prompts


class ModelOpenAI:
    def __init__(self):

        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.chunks = []
        self.metadatas = []
        self.embeddings = []
        self.model_type = "text-embedding-ada-002"

    @property
    def data(self):
        return self.embeddings, self.chunks, self.metadatas

    def embed(self, data=""):
        embedding = self.openai_client.embeddings.create(
            input=data, model=self.model_type)
        return embedding.data[0].embedding

    def generate(self):
        info = "        - - - > Embedding"
        step = (100 / len(self.chunks))
        for i, chunk in enumerate(self.chunks):
            self.embeddings.append(self.embed(chunk))
            print(f"{info} - {int(i*step)}%", end='\r', flush=True)

        print(f"{info} - 100%", end='\r', flush=True)
        print("\n", end='', flush=True)

        return self.data

    def query_to_docs(self, result) -> str:

        ids_container = result['ids']
        documents_container = result['documents']
        metadatas_container = result['metadatas']

        formatted_list = []
        result = zip(ids_container, documents_container, metadatas_container)
        for ids, doc, metas in result:
            for id, chunk, meta in zip(ids, doc, metas):
                formatted_list.append(
                    "\n{}\n[{}]: {}".format(id, meta["source"], chunk))

        return "\n".join(formatted_list)

    def question(self, question: str, documents: str) -> str:
        chat_completion = self.completions(
            prompts.generic(documents), question)
        return chat_completion.choices[0].message.content

    def completions(self, prompt, question):
        return self.openai_client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"{prompt}"},
                {"role": "user", "content": f"{question}"}
            ],
            model="gpt-3.5-turbo",
            max_tokens=500,
            temperature=0
        )

    def keys_generation(self, documents):
        prompt = prompts.keywords(documents)
        chat_completion = self.completions(prompt, documents)
        keys = chat_completion.choices[0].message.content.split(",")
        return [key.strip().rstrip('.').rstrip('\n') for key in keys]

    def names_generation(self, documents):
        prompt = prompts.names(documents)
        chat_completion = self.completions(prompt, documents)
        names = chat_completion.choices[0].message.content.split(",")
        return [item for item in names if item != '0']

    def resume_generation(self, documents):
        prompt = prompts.resume(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def title_generation(self, documents):
        prompt = prompts.publisher(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def intention_generation(self, documents):
        prompt = prompts.intention(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def humor_generation(self, documents):
        prompt = prompts.humor(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def objective_generation(self, documents):
        prompt = prompts.objective(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def type_text_generation(self, documents):
        prompt = prompts.type_text(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def subject_generation(self, documents):
        prompt = prompts.subject(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def registration_generation(self, documents):
        prompt = prompts.registration(documents)
        chat_completion = self.completions(prompt, documents)
        return chat_completion.choices[0].message.content

    def metadata_generation(self):

        print("        - - - > ", end='', flush=True)

        for i in range(len(self.chunks)):

            chunk = self.chunks[i]
            metadata = self.metadatas[i]

            # anotation = self.registration_generation(chunk)   # noqa: E501
            # intentions = self.intention_generation(chunk)
            # type_text = self.type_text_generation(chunk)
            # objective = self.objective_generation(chunk)
            description = self.resume_generation(chunk)
            # subject = self.subject_generation(chunk)
            # humor = self.humor_generation(chunk)
            # title = self.title_generation(chunk)
            # names = self.names_generation(chunk)
            # keys = self.keys_generation(chunk)

            metadata_filled = {
                # "title": title,
                # "humor": humor,
                # "type": type_text,
                # "subject": subject,
                # "objective": objective,
                # "anotation": anotation,
                # "keys": ", ".join(keys),
                # "intentions": intentions,
                # "names":  ", ".join(names),
                "description": description,
            }

            registration = self.registration_generation(
                self.text_metadata(metadata_filled))
            metadata_filled = {**metadata_filled, "registration": registration}

            self.metadatas[i] = {**metadata, **metadata_filled}
            print(self.metadatas[i]['registration'])

            # with concurrent.futures.ThreadPoolExecutor() as executor:

            #     anotation = executor.submit(self.registration_generation, chunk).result()   # noqa: E501
            #     intentions = executor.submit(self.intention_generation, chunk).result()   # noqa: E501
            #     type_text = executor.submit(self.type_text_generation, chunk).result()  # noqa: E501
            #     objective = executor.submit(self.objective_generation, chunk).result()  # noqa: E501
            #     description = executor.submit(self.resume_generation, chunk).result()  # noqa: E501
            #     subject = executor.submit(self.subject_generation, chunk).result()  # noqa: E501
            #     humor = executor.submit(self.humor_generation, chunk).result()  # noqa: E501
            #     title = executor.submit(self.title_generation, chunk).result()  # noqa: E501
            #     names = executor.submit(self.names_generation, chunk).result()  # noqa: E501
            #     keys = executor.submit(self.keys_generation, chunk).result()  # noqa: E501

            #     metadata_filled = {
            #         "title": title,
            #         "humor": humor,
            #         "type": type_text,
            #         "subject": subject,
            #         "objective": objective,
            #         "keys": ", ".join(keys),
            #         "intentions": intentions,
            #         "names":  ", ".join(names),
            #         "description": description,
            #         "anotation": anotation,
            #     }

            #     registration = executor.submit(self.registration_generation, self.text_metadata(metadata_filled)).result()  # noqa: E501
            #     metadata_filled = { **metadata_filled, "registration": registration}  # noqa: E501

            #     self.metadatas[i] = { **metadata, **metadata_filled }
            #     print(self.metadatas[i]['registration'])

            print(".", end='', flush=True)

        print("\n", end='', flush=True)
        return self.metadatas[i]

    def text_metadata(self, metadata):
        text_metadata = ""
        for k, v in metadata.items():
            text_metadata += f"{k}: {v}\n"
        return text_metadata
