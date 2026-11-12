"""
Regenera google_flow_playground.html lendo os prompts dos arquivos individuais
prompts_fase_b.md (já atualizados para Style 2 com ambientes) e proposta_direcao.md.

Para cada vídeo extrai:
  - Título e descrição de proposta_direcao.md
  - 3 prompts (um por clipe) de prompts_fase_b.md (dentro de blocos ```)
  - Gera novo HTML com objeto VIDEOS atualizado
"""

import os
import re

BASE = r"C:\laragon\www\stickman-video-director\makuva_tv\02_roteiros"
SRC_HTML = r"C:\laragon\www\stickman-video-director\makuva_tv\google_flow_playground.html"
DST_HTML = r"C:\laragon\www\stickman-video-director\makuva_tv/google_flow_playground.html"


def ler(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        return f.read()


def extrair_clipes(conteudo_md):
    """Extrai nome e prompt de cada clipe de prompts_fase_b.md."""
    # Encontra cabeçalhos ## Clipe N — Nome (tempo)
    # Aceita qualquer tipo de traço (hífen, en-dash, em-dash)
    secoes = re.split(r"^##\s*", conteudo_md, flags=re.MULTILINE)
    clipes = []
    for secao in secoes:
        m_head = re.match(r"Clipe \d+[\s‒–—―−-]+(.+)", secao.strip())
        if not m_head:
            continue
        nome_tempo = m_head.group(1).strip()
        # Extrair prompt do bloco de código triplo nesta seção
        m_prompt = re.search(r"```\n(.*?)\n```", secao, re.DOTALL)
        if not m_prompt:
            continue
        bloco = m_prompt.group(1)
        linhas = [l.strip() for l in bloco.split("\n") if l.strip()]
        prompt = " ".join(linhas)
        clipes.append({"nome_tempo": nome_tempo, "prompt": prompt})
    return clipes


def extrair_titulo_descricao(conteudo_prop):
    """Extrai título em português e descrição de proposta_direcao.md."""
    titulo = None
    descricao = None

    m_titulo = re.search(r"\*\*Título em português:\*\*\s*(.+)", conteudo_prop)
    if m_titulo:
        titulo = m_titulo.group(1).strip().strip('"').strip("'")

    m_desc = re.search(r"\*\*Descricao:\*\*\s*(.+)", conteudo_prop)
    if not m_desc:
        m_desc = re.search(r"\*\*Descrição:\*\*\s*(.+)", conteudo_prop)
    if m_desc:
        descricao = m_desc.group(1).strip()

    return titulo, descricao


def extrair_numero_video(pasta):
    nome = os.path.basename(pasta)
    m = re.match(r"video_(\d+)_", nome)
    return int(m.group(1)) if m else None


def js_string(s):
    """Escapa uma string para uso em JavaScript."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def main():
    # Ler HTML original para obter o esqueleto (antes e depois do objeto VIDEOS)
    html_original = ler(SRC_HTML)

    inicio = html_original.index("const VIDEOS = {")
    fim = html_original.index("};", inicio) + 2

    esqueleto_antes = html_original[:inicio]
    esqueleto_depois = html_original[fim:]

    # Coletar todos os diretórios de vídeo
    pastas = sorted([
        os.path.join(BASE, d) for d in os.listdir(BASE)
        if d.startswith("video_") and os.path.isdir(os.path.join(BASE, d))
    ])

    entradas = []
    total_videos = 0

    for pasta in pastas:
        numero = extrair_numero_video(pasta)
        if numero is None:
            continue

        prop_path = os.path.join(pasta, "proposta_direcao.md")
        prom_path = os.path.join(pasta, "prompts_fase_b.md")

        if not os.path.exists(prop_path) or not os.path.exists(prom_path):
            print(f"  AVISO: vídeo {numero} falta arquivos, pulando")
            continue

        conteudo_prop = ler(prop_path)
        conteudo_prom = ler(prom_path)

        titulo, descricao = extrair_titulo_descricao(conteudo_prop)
        if not titulo:
            titulo = f"Vídeo {numero}"
        if not descricao:
            descricao = f"Vídeo {numero} do Makuva TV"

        clipes = extrair_clipes(conteudo_prom)
        if len(clipes) < 3:
            print(f"  AVISO: vídeo {numero} tem apenas {len(clipes)} clipes, pulando")
            continue

        # Montar clipes JS
        clipes_js = []
        for c in clipes[:3]:
            # Separar nome e tempo: "Nome (0–10s)"
            m_nt = re.match(r"(.+?)\s*\((0–10s|10–20s|20–30s)\)", c["nome_tempo"])
            if m_nt:
                nome = m_nt.group(1).strip()
                tempo = m_nt.group(2)
            else:
                nome = c["nome_tempo"]
                tempo = ""
            clipes_js.append(
                f"      {{\n"
                f"        nome: \"{js_string(nome)} ({tempo})\",\n"
                f"        tempo: \"{tempo}\",\n"
                f"        prompt: \"{js_string(c['prompt'])}\"\n"
                f"      }}"
            )

        entrada = (
            f"  video_{numero}: {{\n"
            f"    titulo: \"{js_string(titulo)}\",\n"
            f"    descricao: \"{js_string(descricao)}\",\n"
            f"    clipes: [\n"
            f"{chr(10).join(clipes_js)}\n"
            f"    ]\n"
            f"  }}"
        )
        entradas.append(entrada)
        total_videos += 1

    videos_js = ",\n".join(entradas)

    novo_html = (
        esqueleto_antes
        + "const VIDEOS = {\n"
        + videos_js
        + "\n};\n"
        + esqueleto_depois
    )

    # Atualizar o texto "Style 1" no preview-box para "Style 2"
    novo_html = novo_html.replace(
        'Style 1 · Classic Minimalist',
        'Style 2 · Ambientes Variados'
    )

    escrever(DST_HTML, novo_html)
    print(f"\nPlayground regenerado: {DST_HTML}")
    print(f"Total de vídeos: {total_videos}")


def escrever(arquivo, texto):
    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(texto)


if __name__ == "__main__":
    main()