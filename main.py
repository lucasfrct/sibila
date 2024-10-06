# flake8: noqa: E501


from src.routines import migrate


def run():

    # Lê o arquivo de cláusulas
    clause_file = open("./seeder/clause.txt", "r", encoding="utf-8")
    clause_content = clause_file.read()
    clause_file.close()

    # # Lê o arquivo de constituiçao federal
    # federal_constitution_file = open("./seeder/federal_constitution.txt", "r", encoding="utf-8")
    # federal_constitution_content = federal_constitution_file.read()
    # federal_constitution_file.close()

    # ## salvando aem formato vetorial
    # FederalConstitutionRetrieval.save("./doc/constituicao_do_brasil", "Constituiçao Federal do Brasil Art. 6", 1, federal_constitution_content


if __name__ == "__main__":
    migrate.tables()
    run()
