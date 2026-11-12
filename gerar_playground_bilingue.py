import re

# Gera versão bilíngue do playground: prompt em inglês (para copiar) + tradução em português (para entender)
# Lê google_flow_playground.html original, mantém prompts em inglês e adiciona tradução abaixo de cada um

SRC = r"C:\laragon\www\stickman-video-director\makuva_tv\google_flow_playground.html"
DST = r"C:\laragon\www\stickman-video-director\makuva_tv\google_flow_playground_bilingue.html"

TERMOS = {
    # Estrutura base (mais longos primeiro)
    "Minimalist 2D animated stick figure on pure white background":
        "Figurinha palitinho animada 2D minimalista em fundo branco puro",
    "Same minimalist 2D animated stick figure":
        "Mesma figurinha palitinho animada 2D minimalista",
    "Same stick figure":
        "Mesma figurinha palitinho",
    "White stick figure":
        "Figurinha palitinho branca",

    # Personagem e estilo
    "Hollow circular head, black stick limbs, uniform medium line weight":
        "Cabeça circular oca, membros de pau pretos, traço médio uniforme",
    "Hollow circular head":
        "Cabeça circular oca",
    "black stick limbs":
        "membros de pau pretos",
    "uniform medium line weight":
        "traço médio uniforme",
    "Simple black lines":
        "Linhas pretas simples",
    "smooth 2D animation style":
        "estilo de animação 2D suave",
    "vibrant colors":
        "cores vibrantes",
    "Simple black lines, vibrant colors, smooth 2D animation style":
        "Linhas pretas simples, cores vibrantes, estilo de animação 2D suave",

    # Técnico
    "9:16 vertical aspect ratio":
        "Proporção 9:16 vertical",
    "10 seconds duration":
        "duração de 10 segundos",
    "No speech bubbles, no text, no dialogue boxes":
        "Sem balões de fala, sem texto, sem caixas de diálogo",

    # Backgrounds
    "on black background":
        "em fundo preto",
    "on white background":
        "em fundo branco",
    "inside kombi":
        "dentro do kombi",

    # Termos gerais
    "Stick figure":
        "Figurinha palitinho",
    "Figure":
        "Figura",
    "stick figure":
        "figurinha palitinho",
    "no face details":
        "sem detalhes no rosto",
    "smooth 2D animation":
        "animação 2D suave",

    # Cenas específicas
    "looks at wall":
        "olha para a parede",
    "sitting in moving":
        "sentado em movimento",
    "turns down":
        "vira em",
    "exits":
        "sai",
    "sits at":
        "sentado em",
    "holding plate":
        "segurando prato",
    "raises hand":
        "levanta a mão",
    "sitting in waiting room":
        "sentado na sala de espera",
    "looks at display board":
        "olha para o painel de exibição",
    "sits at table":
        "sentado na mesa",
    "at market stall":
        "na barraca do mercado",
    "on motorcycle":
        "na motocicleta",
    "waves to stop":
        "acena para parar",
    "left at home":
        "deixado em casa",

    # Verbos e ações
    "lies down to sleep": "deita para dormir",
    "reaches for light switch": "estende a mão para o interruptor de luz",
    "switches off light": "desliga a luz",
    "background turns pitch black": "fundo fica preto absoluto",
    "stands up slowly": "levanta-se lentamente",
    "walks forward with hands outstretched": "caminha para frente com as mãos estendidas",
    "looks around in the dark": "olha ao redor no escuro",
    "Holds a small phone light or candle": "segura uma luz de celular pequena ou vela",
    "switches on light": "liga a luz",
    "background returns to pure white": "fundo retorna ao branco puro",
    "looks directly at camera and smiles": "olha diretamente para a câmera e sorri",
    "yellow shirt accent": "destaque de camisa amarela",

    "enters a minibus taxi (kombi)": "entra em um minibus táxi (kombi)",
    "struggles to close the door": "dificulta para fechar a porta",
    "looks around at crowded interior": "olha ao redor do interior lotado",
    "looks at wristwatch": "olha para o relógio de pulso",
    "taps foot impatiently": "bate o pé impacientemente",
    "looks out window as minibus stops repeatedly": "olha pela janela enquanto o minibus para repetidamente",
    "to pick up more passengers": "para pegar mais passageiros",
    "exits the kombi looking exhausted and desperate": "sai do kombi parecendo exausto e desesperado",
    "Background shows a setting sun behind the figure": "Fundo mostra um pôr do sol atrás da figura",
    "(yellow accent on horizon)": "(destaque amarelo no horizonte)",
    "wipes sweat from forehead": "limpa o suor da testa",
    "looks at camera with tired expression": "olha para a câmera com expressão cansada",
    "yellow sunset accent": "destaque amarelo do pôr do sol",

    "enters bakery": "entra na padaria",
    "asks for bread price": "pede o preço do pão",
    "price went up": "o preço subiu",
    "figure looks annoyed": "figura parece irritada",
    "Small red price accent visible": "Pequeno destaque vermelho de preço visível",
    "asks for less bread due to price": "pede menos pão devido ao preço",
    "still too expensive": "ainda muito caro",
    "figure sighs": "figura suspira",
    "leaves bakery without bread": "sai da padaria sem pão",
    "walks away empty-handed": "afasta-se de mãos vazias",

    "enters bank building": "entra no prédio do banco",
    "takes a queue ticket from machine": "pega um bilhete de fila da máquina",
    "looks at long line of people": "olha para a longa fila de pessoas",
    "holding ticket inside bank": "segurando o bilhete dentro do banco",
    "looks up at display board": "olha para o painel de exibição",
    "numbers barely change": "números quase não mudam",
    "display board showing a completely different number": "painel de exibição mostrando um número completamente diferente",
    "shrugs, turns around and walks out of bank": "encosta os ombros, vira-se e sai do banco",
    "Small red number accent on board visible": "Pequeno destaque vermelho de número no painel visível",

    "lies in bed": "deita na cama",
    "pulls blanket over head": "puxa o cobertor sobre a cabeça",
    "covers ears": "tapa os ouvidos",
    "looks annoyed as loud music starts next door": "parece irritado enquanto a música alta começa ao lado",
    "sits up in bed": "sentar na cama",
    "bangs on wall with fist": "bate na parede com o punho",
    "music note or speaker icon appears on other side of wall getting louder": "ícone de nota musical ou alto-falante aparece do outro lado da parede ficando mais alto",
    "small red sound accent": "pequeno destaque vermelho de som",
    "sits on edge of bed looking exhausted with dark circles under eyes": "sentada na beira da cama parecendo exausta com olheiras",
    "Window shows sunrise with yellow light": "Janela mostra nascer do sol com luz amarela",
    "looks at camera with tired defeated expression": "olha para a câmera com expressão cansada e derrotada",
    "yellow sunrise accent": "destaque amarelo do nascer do sol",

    "is at home trying to rest": "está em casa tentando descansar",
    "neighbor makes loud noise": "vizinho faz barulho alto",
    "figure cannot rest": "figura não consegue descansar",
    "Neighbor keeps making loud noise": "Vizinho continua fazendo barulho alto",
    "figure looks annoyed, covers ears": "figura parece irritada, tapa os ouvidos",
    "closes the window": "fecha a janela",
    "tries to block the noise": "tenta bloquear o barulho",
    "looks resigned": "parece resignado",

    "arrives at school, looks for teacher, classroom is empty": "chega na escola, procura o professor, sala de aula está vazia",
    "Small yellow book accent visible": "Pequeno destaque amarelo de livro visível",
    "Teacher does not arrive": "Professor não chega",
    "figure looks at empty classroom, waits in vain": "figura olha para a sala de aula vazia, espera em vão",
    "leaves the school, walks away looking resigned": "sai da escola, caminha para longe parecendo resignado",

    "arrives at hospital looking sick": "chega ao hospital parecendo doente",
    "goes to reception to see doctor": "vai à recepção para ver o médico",
    "receptionist says doctor does not see patients today": "recepcionista diz que o médico não atende pacientes hoje",
    "Small yellow ticket accent visible": "Pequeno destaque amarelo de bilhete visível",
    "Doctor is not available today": "Médico não está disponível hoje",
    "figure waits then looks disappointed": "figura espera então parece decepcionado",
    "leaves without being seen": "sai sem ser atendido",
    "leaves hospital, walks away down the road looking unwell and resigned": "sai do hospital, caminha pela estrada para longe parecendo doente e resignado",
    "will come back another day": "vai voltar outro dia",

    "holds phone, internet connection drops": "segura o telefone, a conexão de internet cai",
    "page stops loading": "página para de carregar",
    "Small yellow signal accent visible": "Pequeno destaque amarelo de sinal visível",
    "Phone shows no signal": "Telefone não mostra sinal",
    "figure taps screen trying to reconnect": "figura toca na tela tentando reconectar",
    "nothing works": "nada funciona",
    "turns airplane mode on and off": "liga e desliga o modo avião",
    "tries to reconnect, looks resigned": "tenta reconectar, parece resignado",

    "sits inside kombi": "senta dentro do kombi",
    "kombi starts moving then stops in traffic": "kombi começa a se mover então para no trânsito",
    "figure looks around": "figura olha ao redor",
    "Small yellow kombi accent visible": "Pequeno destaque amarelo do kombi visível",
    "Kombi is stuck in traffic, not moving": "Kombi está preso no trânsito, não se movendo",
    "figure waits looking impatient": "figura espera parecendo impaciente",
    "gets out of kombi, walks away on the road looking resigned": "sai do kombi, caminha pela estrada para longe parecendo resignado",
    "going on foot": "indo a pé",
}


def traduzir_texto(texto):
    """Traduz um texto em inglês para português usando dicionário de termos."""
    resultado = texto
    for termo, traducao in sorted(TERMOS.items(), key=lambda x: -len(x[0])):
        resultado = resultado.replace(termo, traducao)
    return resultado


def extrair_objeto_videos(conteudo):
    """Extrai o objeto VIDEOS do JavaScript no HTML."""
    inicio = conteudo.index("const VIDEOS = {")
    fim = conteudo.index("};", inicio) + 2
    return conteudo[inicio:fim]


def gerar_bloco_bilingue(bloco_original):
    """Gera um bloco VIDEOS onde cada prompt tem o original em inglês + tradução em português."""
    # Extrair cada prompt individualmente
    def substituir_prompt(match):
        prompt_original = match.group(1)
        traducao = traduzir_texto(prompt_original)
        return (
            f'prompt: "INGLES: {prompt_original}\\n\\n'
            f'PORTUGUES: {traducao}"'
        )

    # Substituir cada prompt no bloco
    bloco_bilingue = re.sub(
        r'prompt:\s*"([^"]*)"',
        substituir_prompt,
        bloco_original
    )
    return bloco_bilingue


def main():
    with open(SRC, "r", encoding="utf-8") as f:
        conteudo = f.read()

    bloco_original = extrair_objeto_videos(conteudo)
    bloco_bilingue = gerar_bloco_bilingue(bloco_original)

    conteudo_bil = conteudo.replace(bloco_original, bloco_bilingue)

    # Atualizar título e subtítulo
    conteudo_bil = conteudo_bil.replace(
        "<title>Makuva TV — Prompts Google Flow</title>",
        "<title>Makuva TV — Prompts Google Flow (Bilíngue PT/EN)</title>"
    )
    conteudo_bil = conteudo_bil.replace(
        '<div class="sub">Prompts prontos para o Google Flow</div>',
        '<div class="sub">Prompt em inglês (para copiar) + tradução em português (para entender)</div>'
    )
    conteudo_bil = conteudo_bil.replace(
        "<b>Como usar:</b> selecione o vídeo abaixo, veja os 3 prompts de cada clipe, clique em <b>Copiar</b> e cole no Google Flow. Gere cada clipe separadamente (~10s, 9:16 vertical).",
        "<b>Como usar:</b> selecione o vídeo abaixo, veja os 3 prompts de cada clipe. O botão <b>Copiar</b> copia apenas o texto em inglês (o que serve para o Google Flow, Runway, Luma ou Kling). A tradução em português está abaixo para você entender o que cada prompt diz."
    )

    # Adicionar lista visível de vídeos
    lista_items = []
    for m in re.finditer(r'video_\d+:\s*\{\s*titulo:\s*"([^"]*)"', bloco_original):
        lista_items.append(f'        <li><strong>{m.group(1)}</strong></li>')

    def chave_num(titulo):
        mm = re.match(r"Vídeo (\d+)", titulo)
        return int(mm.group(1)) if mm else 9999

    # Extrair títulos para ordenar
    titulos = [m.group(1) for m in re.finditer(r'titulo:\s*"([^"]*)"', bloco_original)]
    titulos.sort(key=chave_num)

    lista_items = []
    for t in titulos:
        lista_items.append(f'        <li><strong>{t}</strong></li>')

    lista_section = f'''
  <div class="lista-videos" style="margin-top: 30px; padding: 20px; background: var(--panel); border-radius: var(--radius); border: 1px solid var(--border);">
    <h2 style="margin: 0 0 12px 0; font-size: 18px; color: var(--text);">Lista de Todos os Vídeos ({len(titulos)})</h2>
    <ul style="margin: 0; padding-left: 20px; color: var(--text); font-size: 14px; line-height: 1.8; max-height: 400px; overflow-y: auto;">
{chr(10).join(lista_items)}
    </ul>
  </div>
'''

    conteudo_bil = conteudo_bil.replace(
        '</div>\n<script>',
        lista_section + '</div>\n<script>'
    )

    with open(DST, "w", encoding="utf-8") as f:
        f.write(conteudo_bil)

    print(f"Versão bilíngue gerada: {DST}")
    print(f"Total de vídeos: {len(titulos)}")


if __name__ == "__main__":
    main()