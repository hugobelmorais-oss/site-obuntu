# CLAUDE.md

Instruções para o Claude Code neste repositório.

## Contexto do Projeto

Site estático do **OBUNTU** (coletivo cultural da UFPB). Stack: HTML + CSS + JavaScript puro, sem framework nem package manager. Publicado via GitHub Pages.

Ficheiros principais:
- `index.html` — estrutura da página
- `styles.css` — estilos
- `script.js` — lógica e integração com Google Drive API (Apps Script)

---

## Diretrizes de Comportamento

Diretrizes para reduzir erros comuns de codificação LLM. Derivadas das recomendações de Andrej Karpathy.

**Compromisso:** estas diretrizes privilegiam cautela sobre velocidade. Para tarefas triviais, usa o bom senso.

### 1. Pensar Antes de Codificar

**Não assumir. Não esconder confusão. Expor trade-offs.**

Antes de implementar:
- Enuncia explicitamente as tuas suposições. Se incerto, pergunta.
- Se existirem múltiplas interpretações, apresenta-as — não escolhas silenciosamente.
- Se existir uma abordagem mais simples, diz. Questiona quando justificado.
- Se algo não estiver claro, para. Nomeia o que é confuso. Pergunta.

### 2. Simplicidade Primeiro

**Código mínimo que resolve o problema. Nada especulativo.**

- Sem funcionalidades além do pedido.
- Sem abstrações para código de uso único.
- Sem "flexibilidade" ou "configurabilidade" não solicitada.
- Sem tratamento de erros para cenários impossíveis.
- Se escreveres 200 linhas e podia ser 50, reescreve.

Pergunta: "Um engenheiro sénior diria que isto é demasiado complicado?" Se sim, simplifica.

### 3. Alterações Cirúrgicas

**Toca apenas no que é necessário. Limpa apenas a tua própria bagunça.**

Ao editar código existente:
- Não "melhores" código adjacente, comentários ou formatação.
- Não refatores coisas que não estão partidas.
- Segue o estilo existente, mesmo que farias de forma diferente.
- Se notares código morto não relacionado, menciona — não apagues.

Quando as tuas alterações criam órfãos:
- Remove imports/variáveis/funções que as TUAS alterações tornaram desnecessários.
- Não removes código morto pré-existente a não ser que pedido.

O teste: cada linha alterada deve traçar diretamente ao pedido do utilizador.

### 4. Execução Orientada a Objetivos

**Define critérios de sucesso. Itera até verificado.**

Transforma tarefas em objetivos verificáveis:
- "Adicionar validação" → "Escreve testes para inputs inválidos, depois faz passar"
- "Corrigir o bug" → "Escreve um teste que o reproduz, depois faz passar"
- "Refatorar X" → "Garante que os testes passam antes e depois"

Para tarefas multi-passo, enuncia um plano breve:
```
1. [Passo] → verificar: [check]
2. [Passo] → verificar: [check]
3. [Passo] → verificar: [check]
```

Critérios de sucesso fortes permitem iterar de forma independente. Critérios fracos ("faz funcionar") requerem clarificação constante.

---

**Estas diretrizes funcionam se:** menos alterações desnecessárias nos diffs, menos reescritas por excesso de complicação, e perguntas de clarificação aparecem antes da implementação em vez de após erros.
