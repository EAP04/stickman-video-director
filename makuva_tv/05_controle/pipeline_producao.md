# Pipeline de Produção — Makuva TV

Este documento padroniza o fluxo end-to-end de cada vídeo do Makuva TV, da proposta à publicação no YouTube. Ele consolida as peças que já existiam espalhadas pelo repositório e não altera nenhum arquivo existente — apenas referencia o que já está em uso.

## Visão geral do fluxo

Cada vídeo segue 5 fases:

```
Fase A — Proposta de direção
      ↓ (confirmação)
Fase B — Prompts de geração
      ↓ (execução manual pelo usuário)
Fase C — Pós-produção (edição)
      ↓
Fase D — Controle de qualidade
      ↓ (gate)
Fase E — Publicação no YouTube
```

## Fase A — Proposta de direção (`proposta_direcao.md`)

Para cada vídeo `video_NNN_<tema>_N/` em `makuva_tv/02_roteiros/`:

1. Preencher `proposta_direcao.md` com:
   - Título em português (≤60 caracteres, com gancho e hashtag `#MakuvaTV`)
   - Mensagem central e gancho (0–3s)
   - Duração alvo: 30 segundos (3 clipes de ~10s)
   - Formato: 9:16 vertical (YouTube Shorts)
   - Estilo visual: **Style 2 · Ambientes Variados** (fundo branco com ambiente diferenciado por vídeo)
   - Cores de destaque: máximo 3 (verde vivo, vermelho forte, amarelo brilhante)
   - Ambiente de fundo: descritivo em português (veja `guia_estilo_visual.md`)
   - Perfil da voz: narrador adulto, português de Moçambique, tom conversacional
   - Estrutura narrativa: 3 clipes com propósito, cena do palitinho e VO
   - Continuidade entre clipes
   - BGM e som
2. Marcar a seção **Confirmação necessária** antes de passar para a Fase B.

Referência: `makuva_tv/plano_200_videos.md` define o padrão de cada vídeo (gancho 0–3s, desenvolvimento 3–25s, punchline 25–30s).

## Fase B — Prompts de geração (`prompts_fase_b.md`)

1. Escrever 3 prompts em inglês, um por clipe, dentro de blocos de código triplo (```).
2. Cada prompt deve conter:
   - Personagem consistente (mesma cabeça oca, membros pretos, linha média uniforme)
   - Ambiente do vídeo (conforme `guia_estilo_visual.md`)
   - Proporção 9:16, duração ~10 segundos
   - Sem texto, números, balões de fala ou caixas de diálogo
   - Cores apenas com nomes comuns (branco, preto, azul, vermelho, amarelo, verde) — sem hex/RGB/Pantone
3. Incluir seção **Regras de geração (não alterar)** e **Após gerar** (download MP4, edição, narração, legendas, SFX, thumbnail).

Ferramentas de geração (execução manual pelo usuário): Google Flow, Runway, Luma ou Kling. O assistente não acessa navegador nem gera vídeos automaticamente.

## Fase C — Pós-produção (`instrucoes_producao.md`)

1. Baixar os 3 clipes (MP4).
2. Montar no CapCut, Premiere ou editor de preferência.
3. Adicionar:
   - Narração em português de Moçambique (áudio apenas, sem legendas queimadas na cena)
   - Legendas sincronizadas
   - Efeito sonoro (opcional)
   - Thumbnail com cores verde, vermelho, amarelo
4. Salvar clipes e edições em `makuva_tv/03_producao/video_NNN_<tema>_N/`.

## Fase D — Controle de qualidade (gate antes de publicar)

Passar por todos os itens de `controle_qualidade.md`. Só publicar após aprovação em todos.

## Fase E — Publicação no YouTube

1. Seguir o **Checklist de upload no YouTube (por vídeo)** em `makuva_tv/00_canal/configuracoes_canal.md`.
2. Publicar 3×/semana (segunda, quarta, sexta, 18h horário de Moçambique) — veja `makuva_tv/05_controle/cronograma_postagem.md`.
3. Adicionar à playlist da categoria correspondente (veja `makuva_tv/00_canal/playlists_sugeridas.md`).
4. Registrar no `plano_lancamento.md` (status, data, link, métricas).

## Arquivos relacionados

| Arquivo | Caminho | Uso |
|---------|---------|-----|
| Proposta de direção | `makuva_tv/02_roteiros/video_*/proposta_direcao.md` | Fase A |
| Prompts Fase B | `makuva_tv/02_roteiros/video_*/prompts_fase_b.md` | Fase B |
| Instruções produção | `makuva_tv/02_roteiros/video_*/instrucoes_producao.md` | Fase C |
| Controle de qualidade | `makuva_tv/05_controle/controle_qualidade.md` | Fase D |
| Configurações canal | `makuva_tv/00_canal/configuracoes_canal.md` | Fase E (checklist upload) |
| Cronograma | `makuva_tv/05_controle/cronograma_postagem.md` | Fase E (schedule) |
| Playlists | `makuva_tv/00_canal/playlists_sugeridas.md` | Fase E (playlists) |
| Guia de estilo | `makuva_tv/00_canal/guia_estilo_visual.md` | Estilo visual (Fases A–B) |
| Organização | `makuva_tv/05_controle/organizacao_arquivos.md` | Estrutura e backup |
| Plano lançamento | `makuva_tv/05_controle/plano_lancamento.md` | Controle operacional |
