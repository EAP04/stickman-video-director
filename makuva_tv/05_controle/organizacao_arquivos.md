# Organização de Arquivos e Backup — Makuva TV

Padroniza a estrutura de pastas já em uso no repositório e adiciona regras de backup. Nenhum arquivo existente foi alterado.

## Estrutura de pastas

```
makuva_tv/
├── 00_canal/              # Identidade visual, configurações, guias
│   ├── configuracoes_canal.md
│   ├── identidade_visual.md
│   ├── playlists_sugeridas.md
│   ├── guia_estilo_visual.md          (novo)
│   ├── otimizacao_shorts.md           (novo)
│   └── direitos_autorais.md           (novo)
├── 01_ativos/               # Logos e thumbnails
│   ├── logos/
│   └── thumbnails/
├── 02_roteiros/             # Roteiros e prompts por vídeo
│   ├── video_NNN_<tema>_N/            # 181 vídeos
│   │   ├── proposta_direcao.md
│   │   ├── prompts_fase_b.md
│   │   └── instrucoes_producao.md
│   ├── cat_XX_<tema>/
│   │   └── categoria.md               # 20 categorias × 10 conceitos
│   ├── ideias_futuras.md
│   ├── kits_memes_piadas.md
│   └── plano_200_videos.md
├── 03_producao/             # Clipes, narrações, edições (não versionado)
│   └── video_NNN_<tema>_N/
├── 04_publicados/           # Vídeos publicados no YouTube
├── 05_controle/             # Cronograma, métricas, controle
│   ├── cronograma_postagem.md
│   ├── pipeline_producao.md           (novo)
│   ├── controle_qualidade.md          (novo)
│   ├── organizacao_arquivos.md        (novo)
│   └── plano_lancamento.md            (novo)
```

## Regras por pasta

| Pasta | Conteúdo | Versionado? |
|-------|----------|-------------|
| `00_canal/` | Identidade visual, configurações, guias de estilo | Sim (git) |
| `01_ativos/` | Logos SVG, thumbnails SVG | Sim (git) |
| `02_roteiros/` | `proposta_direcao.md`, `prompts_fase_b.md`, `instrucoes_producao.md` por vídeo; `categoria.md` por categoria | Sim (git) |
| `03_producao/` | Clipes MP4, arquivos de narração, edições em CapCut/Premiere | **Não** (backup externo) |
| `04_publicados/` | Registros de vídeos publicados | Sim (git) |
| `05_controle/` | Cronograma, métricas, pipeline, qualidade, lançamento | Sim (git) |

## Versionamento (git)

- Commit por lote de vídeos concluídos, não um commit por vídeo.
- Mensagem de commit no formato: `feat(makuva): <descrição>`
- Push para `origin/main` após cada lote.
- Nunca commitar clipes MP4 ou arquivos de produção pesados (pesam demais no repositório).

## Backup

- Clipes MP4, narrações e edições em `03_producao/` devem ser copiados para um local externo ao repositório (disco externo ou nuvem).
- O repositório git versiona apenas textos (`.md`) e assets leves (SVG).
- Antes de apagar qualquer clipe de produção, confirmar que o vídeo já está publicado no YouTube e que o backup externo existe.

## Arquivos relacionados

- `makuva_tv/README.md` — organização e uso das pastas
- `makuva_tv/02_roteiros/plano_200_videos.md` — plano mestre de 200 vídeos
