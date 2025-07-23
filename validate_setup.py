#!/usr/bin/env python3
"""
Script de Teste e Validação da Configuração Local do Sibila
"""

import sys
import os
import subprocess

def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário")
        return False
    print("✅ Python version OK")
    return True

def check_dependencies():
    """Verifica dependências essenciais"""
    dependencies = [
        ('Flask', 'flask'),
        ('Python-dotenv', 'dotenv'),
        ('SQLite3', 'sqlite3'),
        ('PDFPlumber', 'pdfplumber'),
        ('Ollama', 'ollama'),
        ('OpenAI', 'openai'),
        ('Requests', 'requests'),
    ]
    
    results = {}
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"✅ {name}: OK")
            results[name] = True
        except ImportError:
            print(f"❌ {name}: Missing")
            results[name] = False
    
    return results

def check_environment():
    """Verifica configuração do ambiente"""
    env_file = '.env'
    if os.path.exists(env_file):
        print("✅ Arquivo .env encontrado")
        return True
    else:
        print("❌ Arquivo .env não encontrado")
        print("   Execute: cp .env.example .env")
        return False

def check_ollama_service():
    """Verifica se Ollama está rodando"""
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:11434/api/tags'], 
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            print("✅ Ollama service: Running")
            return True
        else:
            print("❌ Ollama service: Not responding")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Ollama service: Not available")
        print("   Execute: ollama serve")
        return False

def check_project_structure():
    """Verifica estrutura do projeto"""
    required_files = [
        'main.py',
        'requirements.txt',
        'src/server.py',
        'src/routes/routes.py',
        '.env.example'
    ]
    
    all_good = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}: Found")
        else:
            print(f"❌ {file_path}: Missing")
            all_good = False
    
    return all_good

def main():
    """Executa todos os testes"""
    print("=" * 50)
    print("VALIDAÇÃO DA CONFIGURAÇÃO LOCAL - SIBILA")
    print("=" * 50)
    
    print("\n1. Verificando Python...")
    python_ok = check_python_version()
    
    print("\n2. Verificando estrutura do projeto...")
    structure_ok = check_project_structure()
    
    print("\n3. Verificando arquivo de ambiente...")
    env_ok = check_environment()
    
    print("\n4. Verificando dependências Python...")
    deps = check_dependencies()
    
    print("\n5. Verificando serviços externos...")
    ollama_ok = check_ollama_service()
    
    # Resumo
    print("\n" + "=" * 50)
    print("RESUMO DA VALIDAÇÃO")
    print("=" * 50)
    
    if all([python_ok, structure_ok, env_ok]):
        print("✅ Configuração básica: OK")
    else:
        print("❌ Configuração básica: Problemas encontrados")
    
    missing_deps = [name for name, status in deps.items() if not status]
    if missing_deps:
        print(f"❌ Dependências faltando: {', '.join(missing_deps)}")
        print("   Execute: pip install -r requirements.txt")
    else:
        print("✅ Todas as dependências: OK")
    
    if not ollama_ok:
        print("❌ Ollama não está rodando")
        print("   Execute: ollama serve")
    
    print("\n📖 Para guia completo, consulte: SETUP_LOCAL.md")
    
    # Instruções de próximos passos
    if python_ok and structure_ok and env_ok:
        if missing_deps:
            print("\n🔧 PRÓXIMOS PASSOS:")
            print("1. pip install -r requirements.txt")
            print("2. ollama serve")
            print("3. ollama pull llama3")
            print("4. python main.py")
        elif not ollama_ok:
            print("\n🔧 PRÓXIMOS PASSOS:")
            print("1. ollama serve")
            print("2. ollama pull llama3")  
            print("3. python main.py")
        else:
            print("\n🚀 TUDO PRONTO! Execute: python main.py")

if __name__ == "__main__":
    main()