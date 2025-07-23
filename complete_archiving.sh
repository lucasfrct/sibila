#!/bin/bash

# Script to complete the branch archiving process
# This should be run when you have appropriate permissions to push tags and delete remote branches

echo "Completing branch archiving process..."
echo "====================================="

# Push archive tags to remote
echo "Pushing archive tags to remote..."
git push origin arquive/codex-corrigir-erros-de-digitacao-no-readme
git push origin arquive/codex-refactor-uso-de-métodos-e-imports 
git push origin arquive/codex-renomear-arquivo-para-constituicao_federal.csv
git push origin arquive/codex-revisar-base-de-código-e-sugerir-tarefas
git push origin arquive/copilot-fix-dfde568b-6fad-40de-a58a-bfb835851165

# Delete archived branches from remote
echo "Deleting archived branches from remote..."
git push origin --delete 'codex/renomear-arquivo-para-constituicao_federal.csv'
git push origin --delete 'codex/refactor-uso-de-métodos-e-imports'
git push origin --delete 'codex/corrigir-erros-de-digitação-no-readme'
git push origin --delete 'codex/revisar-base-de-código-e-sugerir-tarefas' 
git push origin --delete 'copilot/fix-dfde568b-6fad-40de-a58a-bfb835851165'

echo "✓ Branch archiving process completed!"
echo ""
echo "Summary:"
echo "- 5 merged branches were archived as tags"
echo "- Archive tags follow the format: arquive/<branch-name>"
echo "- Only main, development, and branches with open PRs remain active"