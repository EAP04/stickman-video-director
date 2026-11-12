import os
import re

BASE = r"C:\laragon\www\stickman-video-director\makuva_tv\02_roteiros"

# Mapeamento: número do vídeo -> ambiente específico
AMBIENTES_LUZ_VIU = {
    1: "Quarto de dormir com cama, abajur de cabeceira e janela com cortina, fundo branco com mobiliário mínimo cinza claro",
    45: "Sala de estar com sofá, tapete, abajur de pé e janela, fundo branco com mobiliário mínimo cinza claro",
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

def modificar_proposta(caminho, numero, ambiente):
    texto = ler(caminho)

    # Muda o estilo
    texto = texto.replace(
        "- **Estilo:** Style 1 · Classic Minimalist (fundo branco, palito simples)",
        "- **Estilo:** Style 2 · Ambientes Variados (fundo branco com ambiente por cena, palito simples)"
    )
    texto = texto.replace(
        "- **Estilo:** Style 1 · Classic Minimalist (fundo branco)",
        "- **Estilo:** Style 2 · Ambientes Variados (fundo branco com ambiente por cena, palito simples)"
    )

    # Muda a descrição do estilo visual
    texto = texto.replace(
        "- **Estilo visual:** Style 1 Classic Minimalist, tema claro (fundo branco)",
        "- **Estilo visual:** Style 2 Ambientes Variados, tema claro com ambiente diferenciado por vídeo"
    )

    # Adiciona ambiente na seção de cores usadas (ou cria se não existir)
    if "**Ambiente de fundo:**" not in texto:
        # Insere após a linha de Cores usadas no vídeo
        texto = texto.replace(
            "- **Cores usadas no vídeo:**",
            f"- **Ambiente de fundo:** {ambiente}\n- **Cores usadas no vídeo:**"
        )

    # Atualiza a confirmação
    texto = texto.replace(
        "- [ ] Você quer manter o estilo Style 1 (fundo branco, palito simples)",
        "- [ ] Você quer manter o estilo Style 2 (ambiente diferenciado por vídeo, palito consistente)"
    )

    escrever(caminho, texto)
    print(f"  proposta_direcao.md atualizado para vídeo {numero} (ambiente: {ambiente[:40]}...)")


def modificar_prompts(caminho, numero, ambiente):
    texto = ler(caminho)

    # Para cada clipe, substituir "pure white background" e "on white background" pelo ambiente
    # Clipe 1: "on pure white background" -> "em [ambiente]"
    texto = texto.replace(
        "Minimalist 2D animated stick figure on pure white background.",
        f"Minimalist 2D animated stick figure in {ambiente.lower()}."
    )

    # Clipe 2 e 3: "Same minimalist 2D animated stick figure on white background"
    texto = texto.replace(
        "Same minimalist 2D animated stick figure on white background.",
        f"Same minimalist 2D animated stick figure in {ambiente.lower()}."
    )

    # Clipe 3: "background returns to pure white" / "background turns pitch black"
    texto = texto.replace(
        "background returns to pure white",
        f"background returns to {ambiente.lower()}"
    )
    texto = texto.replace(
        "background turns pitch black",
        f"background turns dark {ambiente.lower()}"
    )

    escrever(caminho, texto)
    print(f"  prompts_fase_b.md atualizado para vídeo {numero} (ambiente: {ambiente[:40]}...)")


def main():
    pastas = sorted([
        os.path.join(BASE, d) for d in os.listdir(BASE)
        if d.startswith("video_") and "luz_viu" in d
    ])

    print(f"Encontrados {len(pastas)} vídeos da categoria Luz Viu")

    for pasta in pastas:
        numero = extrair_numero_video(pasta)
        ambiente = AMBIENTES_LUZ_VIU.get(numero, "ambiente interno com iluminação variada")

        print(f"\nProcessando vídeo {numero}: {os.path.basename(pasta)}")

        prop = os.path.join(pasta, "proposta_direcao.md")
        prom = os.path.join(pasta, "prompts_fase_b.md")

        if os.path.exists(prop):
            modificar_proposta(prop, numero, ambiente)
        else:
            print(f"  AVISO: proposta_direcao.md não encontrado")

        if os.path.exists(prom):
            modificar_prompts(prom, numero, ambiente)
        else:
            print(f"  AVISO: prompts_fase_b.md não encontrado")

    print("\nConcluído!")


if __name__ == "__main__":
    main()