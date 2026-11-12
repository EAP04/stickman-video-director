"""
Apply Style 2 (Ambientes Variados) to ALL videos in makuva_tv/02_roteiros/.

For each video directory:
  1. Parses the directory name to get video number and category suffix.
  2. Maps the suffix to one of 20 canonical categories.
  3. Looks up the environment description (PT for proposta_direcao.md, EN for prompts_fase_b.md).
  4. Updates proposta_direcao.md: style line, style visual line, Ambiente de fundo field, confirmation checkbox.
  5. Updates prompts_fase_b.md: replaces "on pure white background" / "on white background" with
     environment-aware English text.

Skips videos already on Style 2 (video_01_luz_viu and video_45_luz_viu_5).
"""

import os
import re

BASE = r"C:\laragon\www\stickman-video-director\makuva_tv\02_roteiros"

# Skip these - already migrated to Style 2
SKIP_VIDEO_NUMBERS = {1, 45}

# Map directory suffix -> canonical category name
CANONICAL_MAP = {
    "kombi_chapas": "kombi_chapas",
    "kombi_lotada": "kombi_chapas",
    "tdm_internet": "tdm_internet",
    "banco_filas": "banco_filas",
    "fila_banco": "banco_filas",
    "familia_domingo": "familia_domingo",
    "familia_almoco_domingo": "familia_domingo",
    "xiga_taxi": "xiga_taxi",
    "xiga_matola": "xiga_taxi",
    "pao_mercado": "pao_mercado",
    "preco_pao": "pao_mercado",
    "edm_luz": "edm_luz",
    "luz_viu": "edm_luz",
    "vizinho_barulhento": "vizinho_barulhento",
    "escola_professores": "escola_professores",
    "hospital_saude": "hospital_saude",
    "casamento_dote": "casamento_dote",
    "igreja_pastor": "igreja_pastor",
    "policia_transito": "policia_transito",
    "feira_matola": "feira_matola",
    "namoro_whatsapp": "namoro_whatsapp",
    "emprego_entrevista": "emprego_entrevista",
    "agua_chafariz": "agua_chafariz",
    "falta_rede": "tdm_internet",
    "celular_rede": "celular_rede",
    "bairro_esquina": "bairro_esquina",
    "festa_fim_semana": "festa_fim_semana",
}

# Environment descriptions per canonical category.
# PT for proposta_direcao.md, EN for prompts_fase_b.md.
AMBIENTES = {
    "kombi_chapas": {
        "pt": "Interior de kombi/chapa com bancos, corrimãos e passageiros, fundo branco com mobiliário mínimo cinza claro",
        "en": "minibus taxi interior with seats, handrails and passengers",
    },
    "tdm_internet": {
        "pt": "Escritório doméstico com roteador Wi-Fi, modem e mesa de computador, fundo branco com mobiliário mínimo cinza claro",
        "en": "home office with Wi-Fi router, modem and computer desk",
    },
    "banco_filas": {
        "pt": "Interior de banco com área de fila, balcão de atendimento e cadeiras de espera, fundo branco com mobiliário mínimo cinza claro",
        "en": "bank interior with queue area, service counter and waiting chairs",
    },
    "familia_domingo": {
        "pt": "Sala de jantar familiar com mesa, cadeiras e pratos de comida, fundo branco com mobiliário mínimo cinza claro",
        "en": "family dining room with table, chairs and plates of food",
    },
    "xiga_taxi": {
        "pt": "Interior de táxi com assento do motorista, painel e vista da rua, fundo branco com mobiliário mínimo cinza claro",
        "en": "taxi interior with driver seat, dashboard and street view",
    },
    "pao_mercado": {
        "pt": "Balcão de padaria com exposição de pão, prateleiras e balcão da loja, fundo branco com mobiliário mínimo cinza claro",
        "en": "bakery counter with bread display, shelves and shop counter",
    },
    "edm_luz": {
        "pt": "Quarto de dormir com cama, abajur de cabeceira e janela com cortina, fundo branco com mobiliário mínimo cinza claro",
        "en": "bedroom with bed, bedside lamp and window with curtains",
    },
    "vizinho_barulhento": {
        "pt": "Corredor de apartamento com porta, ruídos do vizinho e interior do prédio, fundo branco com mobiliário mínimo cinza claro",
        "en": "apartment hallway with door, neighbor sounds and building interior",
    },
    "escola_professores": {
        "pt": "Sala de aula com quadro negro, carteiras e mesa do professor, fundo branco com mobiliário mínimo cinza claro",
        "en": "classroom with blackboard, desks and teacher desk",
    },
    "hospital_saude": {
        "pt": "Sala de exame de clínica com cama, equipamento médico e armários, fundo branco com mobiliário mínimo cinza claro",
        "en": "clinic examination room with bed, medical equipment and cabinets",
    },
    "casamento_dote": {
        "pt": "Local de casamento com cadeiras, decorações e montagem de celebração, fundo branco com mobiliário mínimo cinza claro",
        "en": "wedding venue with chairs, decorations and celebration setup",
    },
    "igreja_pastor": {
        "pt": "Interior de igreja com bancos, altar e decorações religiosas, fundo branco com mobiliário mínimo cinza claro",
        "en": "church interior with pews, altar and religious decorations",
    },
    "policia_transito": {
        "pt": "Blitz policial com farda do agente, sinal de trânsito e rua, fundo branco com mobiliário mínimo cinza claro",
        "en": "police checkpoint with officer uniform, traffic sign and street",
    },
    "feira_matola": {
        "pt": "Banca de mercado ao ar livre com produtos, caixas e mesa do vendedor, fundo branco com mobiliário mínimo cinza claro",
        "en": "outdoor market stall with produce, crates and vendor table",
    },
    "namoro_whatsapp": {
        "pt": "Quarto de dormir com cama, telefone na mesa de cabeceira e janela, fundo branco com mobiliário mínimo cinza claro",
        "en": "bedroom with bed, phone on nightstand and window",
    },
    "emprego_entrevista": {
        "pt": "Escritório com mesa, cadeira, computador e mesa de reunião, fundo branco com mobiliário mínimo cinza claro",
        "en": "office interior with desk, chair, computer and meeting table",
    },
    "agua_chafariz": {
        "pt": "Rua ao ar livre com chafariz de água, calçada e bairro, fundo branco com mobiliário mínimo cinza claro",
        "en": "outdoor street with water fountain, pavement and neighborhood",
    },
    "celular_rede": {
        "pt": "Sala de estar com sofá, telefone na mão e janela, fundo branco com mobiliário mínimo cinza claro",
        "en": "living room with sofa, phone in hand and window",
    },
    "bairro_esquina": {
        "pt": "Esquina de rua com edifícios, calçada e bairro, fundo branco com mobiliário mínimo cinza claro",
        "en": "street corner with buildings, sidewalk and neighborhood",
    },
    "festa_fim_semana": {
        "pt": "Local de festa com decorações, mesa e montagem de celebração, fundo branco com mobiliário mínimo cinza claro",
        "en": "party venue with decorations, table and celebration setup",
    },
}


def ler(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        return f.read()


def escrever(arquivo, texto):
    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(texto)


def extrair_numero_video(pasta):
    nome = os.path.basename(pasta)
    m = re.match(r"video_(\d+)_", nome)
    return int(m.group(1)) if m else None


def extrair_sufixo(pasta):
    nome = os.path.basename(pasta)
    m = re.match(r"video_\d+_(.+)", nome)
    if not m:
        return None
    sufixo = m.group(1)
    # Strip trailing _N (numeric disambiguator, e.g. kombi_chapas_2 -> kombi_chapas)
    m2 = re.match(r"(.+?)_\d+$", sufixo)
    if m2:
        return m2.group(1)
    return sufixo


def estilo_ja_aplicado(texto):
    return "Style 2 · Ambientes Variados" in texto


def modificar_proposta(caminho, numero, categoria):
    texto = ler(caminho)
    if estilo_ja_aplicado(texto):
        print(f"  proposta_direcao.md já no Style 2, pulando vídeo {numero}")
        return False

    ambiente_pt = AMBIENTES[categoria]["pt"]

    # 1. Style line (two variants)
    texto = texto.replace(
        "- **Estilo:** Style 1 · Classic Minimalist (fundo branco)",
        "- **Estilo:** Style 2 · Ambientes Variados (fundo branco com ambiente por cena, palito simples)",
    )
    texto = texto.replace(
        "- **Estilo:** Style 1 · Classic Minimalist (fundo branco, palito simples)",
        "- **Estilo:** Style 2 · Ambientes Variados (fundo branco com ambiente por cena, palito simples)",
    )

    # 2. Style visual line (two variants)
    texto = texto.replace(
        "- **Estilo visual:** Style 1 Classic Minimalist, tema claro (fundo branco)",
        "- **Estilo visual:** Style 2 Ambientes Variados, tema claro com ambiente diferenciado por vídeo",
    )
    texto = texto.replace(
        "- **Estilo visual:** Style 1 Classic Minimalist, tema claro",
        "- **Estilo visual:** Style 2 Ambientes Variados, tema claro com ambiente diferenciado por vídeo",
    )

    # 3. Add Ambiente de fundo field after "Cores usadas no vídeo" if present,
    #    otherwise after "Cores de destaque" line
    if "**Ambiente de fundo:**" not in texto:
        if "**Cores usadas no vídeo:**" in texto:
            texto = texto.replace(
                "- **Cores usadas no vídeo:**",
                f"- **Ambiente de fundo:** {ambiente_pt}\n- **Cores usadas no vídeo:**",
            )
        elif "**Cores de destaque**" in texto:
            texto = texto.replace(
                "- **Cores de destaque**:",
                f"- **Cores de destaque**:\n- **Ambiente de fundo:** {ambiente_pt}",
            )
        elif "**Cores de destaque (máximo 3):**" in texto:
            texto = texto.replace(
                "- **Cores de destaque (máximo 3):**",
                f"- **Cores de destaque (máximo 3):**\n- **Ambiente de fundo:** {ambiente_pt}",
            )

    # 4. Confirmation checkbox
    texto = texto.replace(
        "- [ ] Você quer manter o estilo Style 1 (fundo branco, palito simples)",
        "- [ ] Você quer manter o estilo Style 2 (ambiente diferenciado por vídeo, palito consistente)",
    )

    escrever(caminho, texto)
    print(f"  proposta_direcao.md atualizado para vídeo {numero} (categoria: {categoria})")
    return True


def modificar_prompts(caminho, numero, categoria):
    texto = ler(caminho)
    if estilo_ja_aplicado(texto):
        print(f"  prompts_fase_b.md já no Style 2, pulando vídeo {numero}")
        return False

    ambiente_en = AMBIENTES[categoria]["en"]

    # Replace "on pure white background" first (specific pattern)
    texto = texto.replace(
        "on pure white background",
        f"on white background with {ambiente_en}",
    )

    # Replace remaining "on white background" not followed by " with"
    texto = re.sub(
        r"on white background(?!\s+with)",
        f"on white background with {ambiente_en}",
        texto,
    )

    # Replace "background returns to pure white"
    texto = texto.replace(
        "background returns to pure white",
        f"background returns to white background with {ambiente_en}",
    )

    # Replace "background turns pitch black"
    texto = texto.replace(
        "background turns pitch black",
        f"background turns dark {ambiente_en}",
    )

    escrever(caminho, texto)
    print(f"  prompts_fase_b.md atualizado para vídeo {numero} (categoria: {categoria})")
    return True


def main():
    pastas = sorted([
        os.path.join(BASE, d) for d in os.listdir(BASE)
        if d.startswith("video_") and os.path.isdir(os.path.join(BASE, d))
    ])

    print(f"Encontrados {len(pastas)} diretórios de vídeo")

    atualizados = 0
    pulados = 0
    erros = 0

    for pasta in pastas:
        numero = extrair_numero_video(pasta)
        sufixo = extrair_sufixo(pasta)

        if numero in SKIP_VIDEO_NUMBERS:
            print(f"\nVídeo {numero}: pulando (já no Style 2)")
            pulados += 1
            continue

        categoria = CANONICAL_MAP.get(sufixo)
        if not categoria:
            print(f"\nAVISO: vídeo {numero} ({os.path.basename(pasta)}) - sufixo '{sufixo}' não mapeado, pulando")
            erros += 1
            continue

        print(f"\nProcessando vídeo {numero}: {os.path.basename(pasta)} (categoria: {categoria})")

        prop = os.path.join(pasta, "proposta_direcao.md")
        prom = os.path.join(pasta, "prompts_fase_b.md")

        if os.path.exists(prop):
            modificar_proposta(prop, numero, categoria)
            atualizados += 1
        else:
            print(f"  AVISO: proposta_direcao.md não encontrado")
            erros += 1

        if os.path.exists(prom):
            modificar_prompts(prom, numero, categoria)
        else:
            print(f"  AVISO: prompts_fase_b.md não encontrado")
            erros += 1

    print(f"\n{'='*50}")
    print(f"Concluído! {atualizados} vídeos atualizados, {pulados} pulados, {erros} erros")


if __name__ == "__main__":
    main()