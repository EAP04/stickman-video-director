# Controle de Qualidade — Makuva TV

Checklist de qualidade por vídeo. Este é o **gate de entrega**: um vídeo só é publicado no YouTube após passar em todos os itens abaixo. Nenhum arquivo existente foi alterado — este documento consolida regras que já estavam espalhadas por `cronograma_postagem.md` e pelos testes de regressão em `tests/scenarios/`.

## Checklist por vídeo

| # | Item | Critério de aprovação | Status |
|---|------|----------------------|--------|
| 1 | Consistência do personagem | Mesma cabeça, membros e linha entre os 3 clipes | ☐ |
| 2 | Sem texto na cena | Nenhum número, balão de fala ou caixa de diálogo visível | ☐ |
| 3 | Narração em português de Moçambique | Áudio apenas, tom conversacional, sem legendas queimadas | ☐ |
| 4 | Legendas sincronizadas | Sincronizadas com a narração, adicionadas na edição | ☐ |
| 5 | Thumbnail | Cores verde/vermelho/amarelo, contraste para mobile, safe zones respeitadas | ☐ |
| 6 | Duração total | ≤ 60 segundos (YouTube Shorts) | ☐ |
| 7 | Proporção | 9:16 vertical | ☐ |
| 8 | Estilo visual | Style 2 · Ambientes Variados, ambiente diferenciado por vídeo | ☐ |
| 9 | Cores | Máximo 3 cores de destaque, nomes comuns (sem hex/RGB) | ☐ |
| 10 | Direitos autorais | Música, SFX e narração com direito de uso assegurado | ☐ |
| 11 | Checklist de upload | Todos os itens de `configuracoes_canal.md` preenchidos | ☐ |

## Gate de entrega

- Se **todos** os itens acima estiverem aprovados → liberar para publicação (Fase E do pipeline).
- Se **algum** item estiver pendente → corrigir e reavaliar antes de publicar.

## Referências

- `makuva_tv/05_controle/cronograma_postagem.md` — checklist antes de publicar e schedule
- `makuva_tv/00_canal/configuracoes_canal.md` — Regras de produção e Checklist de upload no YouTube
- `tests/scenarios/b-common-production-quality.md` — casos de regressão de qualidade B
- `tests/scenarios/b1-production-quality.md` — casos de regressão B1
- `tests/scenarios/b3-design-motion.md` — casos de revisão comportamental B3
