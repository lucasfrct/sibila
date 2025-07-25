# Sistema de Auto-Migração Sibila

Este documento descreve o sistema de auto-migração aprimorado que inicializa automaticamente junto com a aplicação.

## Resumo das Melhorias

### ✅ O que foi implementado:

1. **Auto-migração na inicialização**: O sistema agora executa automaticamente quando a aplicação inicia
2. **Migração diferencial**: Aplica apenas as diferenças/novos schemas, não recria tabelas existentes
3. **Tratamento robusto de erros**: A aplicação continua mesmo se algumas migrações falharem
4. **Verificação de integridade**: Valida se o schema está correto antes e após migrações
5. **Log detalhado**: Fornece feedback claro sobre o status das migrações
6. **Compatibilidade com dependências**: Funciona mesmo quando algumas dependências estão faltando

## Como Funciona

### Inicialização Automática

Quando você executa `python main.py`, o sistema:

1. **Verifica a saúde do banco**: Testa conectividade básica
2. **Executa migração legacy**: Para compatibilidade com bancos existentes (se disponível)
3. **Executa migrações versionadas**: Aplica apenas as migrações pendentes
4. **Verifica integridade**: Confirma que o schema está correto
5. **Inicia o servidor**: Só depois de garantir que o banco está pronto

### Migração Diferencial

O sistema é inteligente e:

- ✅ **Aplica apenas diferenças**: Não recria tabelas que já existem
- ✅ **Mantém dados existentes**: Preserva informações já armazenadas
- ✅ **Rastreia o que foi aplicado**: Usa a tabela `schema_migrations` para controle
- ✅ **Permite rollback**: Cada migração pode ser revertida se necessário

## Estrutura do Sistema

### Arquivos Principais

```
src/
├── routines/
│   └── migrate.py              # Rotinas de migração aprimoradas
├── migrations/
│   ├── migration_base.py       # Classe base para migrações
│   ├── migration_manager.py    # Gerenciador principal (aprimorado)
│   ├── migration_001_initial.py # Schema inicial
│   └── migration_002_*.py      # Migrações adicionais
└── modules/database/
    └── sqlitedb.py            # Conexão com banco
main.py                        # Ponto de entrada (com auto-migração)
migrate_cli.py                 # Ferramenta CLI para gerenciar migrações
```

### Funcionalidades da CLI

```bash
# Verificar status das migrações
python migrate_cli.py status

# Aplicar migrações pendentes manualmente
python migrate_cli.py migrate

# Reverter última migração
python migrate_cli.py rollback

# Criar nova migração
python migrate_cli.py create "Descrição da migração"
```

## Tabelas Criadas

### Schema Inicial (Migration 001)
- `documents_info`: Metadados de documentos
- `paragraphs_metadatas`: Conteúdo de parágrafos com metadados
- Índices para melhor performance

### Schema de Exemplo (Migration 002)
- `user_preferences`: Preferências do usuário
- `application_settings`: Configurações da aplicação
- Dados padrão inseridos automaticamente

### Controle de Migração
- `schema_migrations`: Rastreia migrações aplicadas

## Logs de Exemplo

### Primeira Execução (Banco Novo)
```
INFO: 🚀 Starting Sibila Application...
INFO: ✓ Database connectivity test passed
INFO: === Starting Auto-Migration on Startup ===
INFO: Step 1: Running legacy table creation...
INFO: Step 2: Running versioned migration system...
INFO: Migration status: 0 applied, 2 pending
INFO: 📋 Found 2 pending migrations to apply
INFO: 📦 Applying migration 001...
INFO: ✓ Migration 001 applied successfully
INFO: 📦 Applying migration 002...
INFO: ✓ Migration 002 applied successfully
INFO: ✅ All 2 migrations applied successfully
INFO: ✓ Database is ready for use
INFO: === Auto-Migration Startup Complete ===
INFO: 🌐 Starting Flask server...
```

### Execução Subsequente (Banco Atualizado)
```
INFO: 🚀 Starting Sibila Application...
INFO: ✓ Database connectivity test passed
INFO: === Starting Auto-Migration on Startup ===
INFO: Step 1: Running legacy table creation...
INFO: Step 2: Running versioned migration system...
INFO: Migration status: 2 applied, 0 pending
INFO: ✓ No pending migrations - database is up to date
INFO: ✓ Database is ready for use
INFO: === Auto-Migration Startup Complete ===
INFO: 🌐 Starting Flask server...
```

### Nova Migração Disponível
```
INFO: 🚀 Starting Sibila Application...
INFO: ✓ Database connectivity test passed
INFO: === Starting Auto-Migration on Startup ===
INFO: Step 1: Running legacy table creation...
INFO: Step 2: Running versioned migration system...
INFO: Migration status: 2 applied, 1 pending
INFO: 📋 Found 1 pending migrations to apply
INFO: 📦 Applying migration 003...
INFO: ✓ Migration 003 applied successfully
INFO: ✅ All 1 migrations applied successfully
INFO: ✓ Database is ready for use
INFO: === Auto-Migration Startup Complete ===
INFO: 🌐 Starting Flask server...
```

## Criando Novas Migrações

### 1. Use a CLI (Recomendado)
```bash
python migrate_cli.py create "Adicionar tabela de usuários"
```

### 2. Edite o arquivo gerado
```python
# src/migrations/migration_003_adicionar_tabela_usuarios.py

from src.migrations.migration_base import Migration

class Migration003(Migration):
    """Adicionar tabela de usuários"""
    
    def __init__(self):
        super().__init__("003", "Adicionar tabela de usuários")
    
    def up(self, conn) -> bool:
        """Aplicar a migração"""
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error in Migration003.up(): {e}")
            return False
    
    def down(self, conn) -> bool:
        """Reverter a migração"""
        try:
            conn.execute("DROP TABLE IF EXISTS users")
            conn.commit()
            return True
        except Exception as e:
            print(f"Error in Migration003.down(): {e}")
            return False
```

### 3. Reinicie a aplicação
O sistema detectará automaticamente a nova migração e a aplicará.

## Tratamento de Erros

### Falhas de Migração
- ⚠️ **Aplicação continua**: Mesmo se uma migração falhar, a aplicação tenta iniciar
- 📝 **Logs detalhados**: Erros são registrados com stack trace completo
- 🔄 **Recuperação manual**: Use CLI para diagnosticar e corrigir problemas

### Dependências Faltando
- ⚠️ **Migração legacy opcional**: Se dependências estão faltando, pula a migração legacy
- ✅ **Sistema principal funciona**: Migrações versionadas funcionam independentemente
- 📝 **Avisos claros**: Sistema informa quando componentes não estão disponíveis

## Vantagens do Sistema

### Para Desenvolvimento
- 🚀 **Setup automático**: Banco sempre pronto ao iniciar a aplicação
- 🔄 **Sincronização simples**: Novos desenvolvedores obtêm schema atualizado automaticamente
- 🐛 **Debug fácil**: Logs claros mostram exatamente o que aconteceu

### Para Produção
- 🛡️ **Deploy seguro**: Migrações aplicadas automaticamente durante deploy
- 📊 **Monitoramento**: Status claro de migrações aplicadas
- 🔙 **Rollback disponível**: Pode reverter migrações se necessário

### Para Manutenção
- 📈 **Evolução gradual**: Adicione mudanças incrementalmente
- 🔍 **Rastreabilidade**: Histórico completo de mudanças no schema
- ⚡ **Performance**: Apenas diferenças são aplicadas, não recriações completas

## Compatibilidade

### Bancos Existentes
- ✅ **Totalmente compatível**: Funciona com bancos criados pelo sistema legacy
- ✅ **Sem perda de dados**: Preserva todas as informações existentes
- ✅ **Migração suave**: Transição transparente para o novo sistema

### Versões Futuras
- ✅ **Extensível**: Fácil adicionar novas migrações
- ✅ **Versionado**: Controle preciso de versões do schema
- ✅ **Flexível**: Suporta mudanças complexas de schema

## Conclusão

O sistema de auto-migração aprimorado garante que:

1. **A aplicação sempre inicia com o banco correto** 📊
2. **Apenas diferenças são aplicadas** ⚡
3. **O processo é robusto e tolerante a falhas** 🛡️
4. **Desenvolvedores têm controle total** 🎛️
5. **A manutenção é simplificada** 🔧

O resultado é um sistema que "simplesmente funciona" e evolui junto com a aplicação de forma transparente e confiável.