# Guia de Estilo Visual — Makuva TV (Style 2 · Ambientes Variados)

Este guia consolida o estilo visual aplicado aos 181 vídeos do Makuva TV. Nenhum arquivo existente foi alterado — este documento apenas reúne em um só lugar as regras que já estavam em uso nos arquivos `proposta_direcao.md` e `prompts_fase_b.md` de cada vídeo.

## Personagem (palito)

| Elemento | Especificação |
|----------|---------------|
| Cabeça | Círculo oco (hollow circular head) |
| Membros | Traço preto, linha média uniforme |
| Consistência | Mesma cabeça, mesmos membros, mesma linha entre os 3 clipes |
| Limite de ociosidade | Nenhum membro ocioso por mais de 2–3 segundos |
| Estilo | 2D minimalista, linhas simples e pretas, animação suave |

## Paleta de cores

- **Cores de destaque:** máximo 3 por vídeo (verde vivo, vermelho forte, amarelo brilhante)
- **Fundo:** branco com mobiliário mínimo cinza claro
- **Notação:** apenas nomes comuns de cor (branco, preto, azul, vermelho, amarelo, verde)
- **Proibido:** hex, RGB ou Pantone

## Ambientes (Style 2)

Cada vídeo tem um ambiente de fundo diferente, em vez de fundo branco vazio:

- **Fundo base:** branco com mobiliário mínimo cinza claro
- **Ambiente por vídeo/categoria:** diferenciado conforme o tema (ex: interior de kombi, feira, chafariz, sala de aula, quarto, consultório médico)
- As descrições dos ambientes estão mapeadas por categoria em `aplicar_ambientes_todos.py` (dicionário `AMBIENTES`, versões PT para `proposta_direcao.md` e EN para `prompts_fase_b.md`)

## Formato técnico

| Item | Especificação |
|------|---------------|
| Proporção | 9:16 vertical (YouTube Shorts) |
| Duração | ~30 segundos (3 clipes de ~10s) |
| Texto na cena | Nenhum (sem números, balões de fala ou caixas de diálogo) |
| Idioma dos prompts | Inglês (para Google Flow, Runway, Luma, Kling) |
| Idioma da narração | Português de Moçambique |

## Regras proibidas (cenas)

- Não usar texto, números ou interface na cena
- Não usar balões de fala ou caixas de diálogo
- Não usar notação de cor técnica (hex, RGB, Pantone)
- Não deixar membros ociosos por mais de 2–3 segundos

## Referências técnicas

- `skills/directing-stickman-videos/references/style-catalog.md` — catálogo de estilos visuais e fórmulas de prompt
- `skills/directing-stickman-videos/references/autopilot-production-qa.md` — piso de qualidade da produção B
