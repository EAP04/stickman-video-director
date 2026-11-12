import re
import glob
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE = r"C:\laragon\www\stickman-video-director\makuva_tv\02_roteiros"

# Estilos
TITULO_FONT = Font(bold=True, size=14, color="FFFFFF")
TITULO_FILL = PatternFill("solid", fgColor="1F4E79")
HEADER_FONT = Font(bold=True, size=11, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="2E75B6")
CELL_FONT = Font(size=10)
CELL_FILL_ALT = PatternFill("solid", fgColor="F2F2F2")
BORDER = Border(
    left=Side(style="thin", color="BFBFBF"),
    right=Side(style="thin", color="BFBFBF"),
    top=Side(style="thin", color="BFBFBF"),
    bottom=Side(style="thin", color="BFBFBF"),
)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)

def extrair_texto(caminho):
    if not os.path.exists(caminho):
        return ""
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

def extrair_campo(texto, campo):
    """Extrai valor de um campo tipo '- **Campo:** valor'"""
    padrao = rf"- \*\*{re.escape(campo)}\*\*:\s*(.+)"
    m = re.search(padrao, texto)
    return m.group(1).strip() if m else ""

def extrair_tabela_vo(texto):
    """Extrai a tabela VO da proposta_direcao.md"""
    linhas = texto.split("\n")
    vo = {}
    na_tabela = False
    for linha in linhas:
        if "| Clipe |" in linha and "VO" in linha:
            na_tabela = True
            continue
        if na_tabela:
            if linha.startswith("|----"):
                continue
            if linha.startswith("|") and linha.endswith("|"):
                partes = [p.strip() for p in linha.strip("|").split("|")]
                if len(partes) >= 6:
                    clip_num = partes[0].replace("Clipe ", "")
                    vo[clip_num] = {
                        "tempo": partes[1],
                        "proposito": partes[2],
                        "cena": partes[3],
                        "vo": partes[4],
                    }
            else:
                na_tabela = False
    return vo

def extrair_prompts(texto):
    """Extrai os 3 prompts em inglês do prompts_fase_b.md"""
    prompts = []
    blocos = re.findall(r"```\n(.*?)\n```", texto, re.DOTALL)
    for b in blocos:
        prompts.append(b.strip())
    return prompts

def extrair_nome_categoria(nome_pasta):
    """Extrai categoria e numero da pasta video_NNN_categoria_slug_N"""
    # video_01_luz_viu -> categoria luz_viu, numero ''
    # video_21_kombi_chapas_2 -> categoria kombi_chapas, numero 2
    partes = nome_pasta.split("_")
    # Formato: video NNN categoria_slug [N]
    # Remover 'video' e NNN
    resto = "_".join(partes[2:])
    # Verificar se termina com _N (numero)
    m = re.match(r"(.+)_(\d+)$", resto)
    if m:
        return m.group(1), m.group(2)
    return resto, ""

def extrair_titulo_descricao(texto):
    """Extrai título e descrição da proposta_direcao.md"""
    titulo = extrair_campo(texto, "Título em português")
    # Remover aspas e emoji se houver
    titulo = titulo.strip('"').strip()
    # Descricao não está como campo, mas podemos usar a mensagem central
    mensagem = extrair_campo(texto, "Mensagem")
    gancho = extrair_campo(texto, "Gancho")
    return titulo, mensagem, gancho

def coletar_dados():
    pastas = sorted(glob.glob(os.path.join(BASE, "video_*")))
    dados = []
    for pasta in pastas:
        nome_pasta = os.path.basename(pasta)
        # Extrair numero do vídeo do nome da pasta
        m_vid = re.match(r"video_(\d+)_", nome_pasta)
        num_video = int(m_vid.group(1)) if m_vid else 0

        categoria, sufixo = extrair_nome_categoria(nome_pasta)

        prop_path = os.path.join(pasta, "proposta_direcao.md")
        prompt_path = os.path.join(pasta, "prompts_fase_b.md")

        prop_texto = extrair_texto(prop_path)
        prompt_texto = extrair_texto(prompt_path)

        titulo, mensagem, gancho = extrair_titulo_descricao(prop_texto)
        vo = extrair_tabela_vo(prop_texto)
        prompts = extrair_prompts(prompt_texto)

        estilo = extrair_campo(prop_texto, "Estilo")
        formato = extrair_campo(prop_texto, "Formato")
        idioma = extrair_campo(prop_texto, "Idioma da narração")
        ambiente = extrair_campo(prop_texto, "Ambiente de fundo")

        dados.append({
            "num": num_video,
            "pasta": nome_pasta,
            "categoria": categoria,
            "sufixo": sufixo,
            "titulo": titulo,
            "mensagem": mensagem,
            "gancho": gancho,
            "estilo": estilo,
            "formato": formato,
            "idioma": idioma,
            "ambiente": ambiente,
            "vo": vo,
            "prompts": prompts,
        })
    return dados

def main():
    dados = coletar_dados()
    dados.sort(key=lambda x: x["num"])

    wb = Workbook()

    # ============ ABA 1: RESUMO DO PROJETO ============
    ws = wb.active
    ws.title = "Resumo do Projeto"
    ws.sheet_view.showGridLines = False

    ws["A1"] = "MAKUVA TV — PROJETO COMPLETO DE VÍDEOS SHORTS"
    ws["A1"].font = TITULO_FONT
    ws["A1"].fill = TITULO_FILL
    ws.merge_cells("A1:H1")

    resumo = [
        ("Canal", "Makuva TV"),
        ("Formato", "YouTube Shorts — 9:16 vertical"),
        {"Duração por vídeo": "~30 segundos (3 clipes de ~10s cada)"},
        {"Total de vídeos": f"{len(dados)} vídeos"},
        {"Categorias": "20 categorias (10 vídeos cada)"},
        {"Estilo visual": "Style 2 · Ambientes Variados (fundo branco com ambiente diferenciado por vídeo, palitinho consistente)"},
        {"Personagem": "Palitinho: cabeça circular oca, membros pretos, linha média uniforme"},
        {"Idioma da narração": "Português de Moçambique (voz off, sem texto/balões na cena)"},
        {"Cores de destaque": "Verde, vermelho, amarelo (nomes comuns apenas)"},
        {"Ferramentas de geração": "Google Flow, Runway, Luma ou Kling"},
        {"Edição": "CapCut ou Premiere"},
        {"Publicação": "YouTube Shorts + playlist por categoria"},
        {"Estrutura narrativa": "Clipe 1: Golden Hook | Clipe 2: Unveil Insider Secrets | Clipe 3: Ultimate Truth + Elevation"},
        {"Arquivos por vídeo": "proposta_direcao.md, prompts_fase_b.md, instrucoes_producao.md"},
        {"Pasta dos roteiros": "makuva_tv/02_roteiros/video_NNN_categoria_slug_N/"},
        {"Playground HTML": "makuva_tv/google_flow_playground.html (objeto VIDEOS com todos os prompts)"},
        {"Status": "100% concluído — 200 vídeos roteirizados"},
        {"Git commit": "5dd8dc6 — 586 arquivos, 31.651 inserções"},
        {"Branch": "main (1 commit à frente do origin/main)"},
    ]

    r = 3
    for item in resumo:
        if isinstance(item, tuple):
            chave, valor = item
        else:
            chave, valor = list(item.items())[0]
        ws.cell(row=r, column=1, value=chave).font = Font(bold=True, size=10)
        ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor="DDEBF7")
        ws.cell(row=r, column=1).border = BORDER
        ws.cell(row=r, column=1).alignment = WRAP
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
        ws.cell(row=r, column=2, value=valor).font = CELL_FONT
        ws.cell(row=r, column=2).alignment = WRAP
        ws.cell(row=r, column=2).border = BORDER
        for c in range(3, 5):
            ws.cell(row=r, column=c).border = BORDER
        r += 1

    ws.column_dimensions["A"].width = 25
    ws.column_dimensions["B"].width = 40
    ws.column_dimensions["C"].width = 40
    ws.column_dimensions["D"].width = 40

    # ============ ABA 2: CATÁLOGO COMPLETO ============
    ws2 = wb.create_sheet("Catalogo 200 Vídeos")
    headers2 = ["Nº", "Categoria", "Sufixo", "Pasta", "Título (PT)", "Ambiente de Fundo", "Mensagem / História", "Clipe 1 VO", "Clipe 2 VO", "Clipe 3 VO"]
    for c, h in enumerate(headers2, 1):
        cell = ws2.cell(row=1, column=c, value=h)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER
        cell.border = BORDER

    r = 2
    for d in dados:
        vo = d["vo"]
        ws2.cell(row=r, column=1, value=d["num"]).alignment = CENTER
        ws2.cell(row=r, column=2, value=d["categoria"]).alignment = CENTER
        ws2.cell(row=r, column=3, value=d["sufixo"] if d["sufixo"] else "1").alignment = CENTER
        ws2.cell(row=r, column=4, value=d["pasta"]).font = CELL_FONT
        ws2.cell(row=r, column=5, value=d["titulo"]).font = CELL_FONT
        ws2.cell(row=r, column=6, value=d["ambiente"]).font = CELL_FONT
        ws2.cell(row=r, column=7, value=d["mensagem"]).font = CELL_FONT
        ws2.cell(row=r, column=8, value=vo.get("1", {}).get("vo", "")).font = CELL_FONT
        ws2.cell(row=r, column=9, value=vo.get("2", {}).get("vo", "")).font = CELL_FONT
        ws2.cell(row=r, column=10, value=vo.get("3", {}).get("vo", "")).font = CELL_FONT
        for c in range(1, 11):
            ws2.cell(row=r, column=c).border = BORDER
            ws2.cell(row=r, column=c).alignment = WRAP
            if r % 2 == 0:
                ws2.cell(row=r, column=c).fill = CELL_FILL_ALT
        r += 1

    larguras2 = [6, 22, 8, 30, 35, 45, 50, 30, 30, 30]
    for i, w in enumerate(larguras2, 1):
        ws2.column_dimensions[get_column_letter(i)].width = w
    ws2.freeze_panes = "A2"

    # ============ ABA 3: DETALHES DOS CLIPE ============
    ws3 = wb.create_sheet("Detalhes dos Clipes")
    headers3 = ["Vídeo", "Categoria", "Clipe", "Tempo", "Objetivo Narrativo", "Cena do Palitinho", "VO (Português)", "Prompt (Inglês)"]
    for c, h in enumerate(headers3, 1):
        cell = ws3.cell(row=1, column=c, value=h)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER
        cell.border = BORDER

    r = 2
    for d in dados:
        vo = d["vo"]
        prompts = d["prompts"]
        for clip in ["1", "2", "3"]:
            v = vo.get(clip, {})
            p = prompts[int(clip)-1] if len(prompts) >= int(clip) else ""
            ws3.cell(row=r, column=1, value=d["num"]).alignment = CENTER
            ws3.cell(row=r, column=2, value=d["categoria"]).alignment = CENTER
            ws3.cell(row=r, column=3, value=int(clip)).alignment = CENTER
            ws3.cell(row=r, column=4, value=v.get("tempo", "")).font = CELL_FONT
            ws3.cell(row=r, column=5, value=v.get("proposito", "")).font = CELL_FONT
            ws3.cell(row=r, column=6, value=v.get("cena", "")).font = CELL_FONT
            ws3.cell(row=r, column=7, value=v.get("vo", "")).font = CELL_FONT
            ws3.cell(row=r, column=8, value=p).font = CELL_FONT
            for c in range(1, 9):
                ws3.cell(row=r, column=c).border = BORDER
                ws3.cell(row=r, column=c).alignment = WRAP
                if r % 2 == 0:
                    ws3.cell(row=r, column=c).fill = CELL_FILL_ALT
            r += 1

    larguras3 = [8, 22, 7, 12, 30, 40, 30, 80]
    for i, w in enumerate(larguras3, 1):
        ws3.column_dimensions[get_column_letter(i)].width = w
    ws3.freeze_panes = "A2"

    # ============ ABA 4: CENARIOS E HISTORIA ============
    ws4 = wb.create_sheet("Cenarios e Historia")
    headers4 = ["Vídeo", "Categoria", "Título", "Gancho (0-3s)", "Conflito", "Revelação / Insider", "Resolução + Piada", "Chamada para Ação (CTA)"]
    for c, h in enumerate(headers4, 1):
        cell = ws4.cell(row=1, column=c, value=h)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER
        cell.border = BORDER

    # Mapear CTAs por categoria (baseado nos arquivos)
    ctas = {
        "kombi_chapas": "Já ficou preso no kombi no trânsito?",
        "tdm_internet": "Já teve internet lenta demais?",
        "banco_filas": "Já chegou ao banco e ele fechou?",
        "familia_domingo": "Já chegou atrasado ao almoço da família?",
        "xiga_taxi": "Já chamou xiga e ele não apareceu?",
        "pao_mercado": "Já foi ao mercado e o pão acabou?",
        "edm_luz": "Já ficou no escuro por falta de luz?",
        "vizinho_barulhento": "Já teve vizinho barulhento?",
        "escola_professores": "Já chegou na escola e o professor não veio?",
        "hospital_saude": "Já foi ao hospital e estava lotado?",
        "casamento_dote": "Já passou por negociação de dote?",
        "igreja_pastor": "Já foi à igreja no domingo?",
        "policia_transito": "Já foi parado pela polícia de trânsito?",
        "feira_matola": "Já comprou na feira do Matola?",
        "namoro_whatsapp": "Já se declarou pelo WhatsApp?",
        "emprego_entrevista": "Já foi a uma entrevista de emprego?",
        "agua_chafariz": "Já buscou água no chafariz?",
        "celular_rede": "Já ficou sem rede no celular?",
        "bairro_esquina": "Já conversou na esquina do bairro?",
        "festa_fim_semana": "Já foi a uma festa de fim de semana?",
    }

    r = 2
    for d in dados:
        vo = d["vo"]
        cta = ctas.get(d["categoria"], "Comente se já passou por isso!")
        ws4.cell(row=r, column=1, value=d["num"]).alignment = CENTER
        ws4.cell(row=r, column=2, value=d["categoria"]).alignment = CENTER
        ws4.cell(row=r, column=3, value=d["titulo"]).font = CELL_FONT
        ws4.cell(row=r, column=4, value=d["gancho"]).font = CELL_FONT
        ws4.cell(row=r, column=5, value=vo.get("1", {}).get("cena", "")).font = CELL_FONT
        ws4.cell(row=r, column=6, value=vo.get("2", {}).get("cena", "")).font = CELL_FONT
        ws4.cell(row=r, column=7, value=vo.get("3", {}).get("cena", "")).font = CELL_FONT
        ws4.cell(row=r, column=8, value=cta).font = CELL_FONT
        for c in range(1, 9):
            ws4.cell(row=r, column=c).border = BORDER
            ws4.cell(row=r, column=c).alignment = WRAP
            if r % 2 == 0:
                ws4.cell(row=r, column=c).fill = CELL_FILL_ALT
        r += 1

    larguras4 = [8, 22, 35, 40, 40, 40, 40, 40]
    for i, w in enumerate(larguras4, 1):
        ws4.column_dimensions[get_column_letter(i)].width = w
    ws4.freeze_panes = "A2"

    # ============ ABA 5: OBJETOS E ELEMENTOS VISUAIS ============
    ws5 = wb.create_sheet("Objetos e Elementos Visuais")
    objetos = [
        ("Personagem principal", "Palitinho (stick figure)", "Cabeça circular oca, membros pretos, linha média uniforme", "Fundo branco com elementos de ambiente", "Todos os vídeos"),
        ("Fundo", "Branco puro com ambiente por cena", "Mobiliário mínimo cinza claro, elementos variam por categoria (kombi, banco, padaria, quarto, etc.)", "Ambiente diferente por vídeo", "Todos os vídeos (Style 2)"),
        ("Destaque amarelo", "Objeto pequeno amarelo", "Ticket, pão, placa, vela, livro, cruz, etc.", "Um objeto por cena", "Vários vídeos"),
        ("Destaque vermelho", "Elemento vermelho", "Trânsito parado, banco fechado, sem pão, luz sumida, etc.", "Conflito visual", "Vários vídeos"),
        ("Destaque verde", "Elemento verde", "Cores de marca do canal", "Thumbnails, playlists", "Branding"),
        ("Narração VO", "Áudio em português de Moçambique", "Frases curtas, coloquiais, acento natural", "3 frases por vídeo", "Todos os vídeos"),
        ("Legendas", "Uma linha por vez", "Preta com contorno branco (ou vice-versa)", "Parte central inferior", "Montagem no CapCut/Premiere"),
        ("SFX", "Efeitos sonoros leves", "Kombi, celular, banco, almoço, xiga, luz, mercado, vizinho, escola, hospital", "Opcional", "Montagem"),
        ("BGM", "Música instrumental leve", "Tema cotidiano, sem tirar atenção da narração", "Fundo do vídeo", "Montagem"),
        ("Thumbnail", "Palitinho + cores verde/vermelho/amarelo", "Emoji relacionado ao tema", "Safe zone do YouTube", "Publicação"),
    ]
    for c, h in enumerate(["Elemento", "Descrição", "Detalhe Técnico", "Uso / Posicionamento", "Onde Aplica"], 1):
        cell = ws5.cell(row=1, column=c, value=h)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER
        cell.border = BORDER

    r = 2
    for obj in objetos:
        for c, val in enumerate(obj, 1):
            ws5.cell(row=r, column=c, value=val).font = CELL_FONT
            ws5.cell(row=r, column=c).border = BORDER
            ws5.cell(row=r, column=c).alignment = WRAP
            if r % 2 == 0:
                ws5.cell(row=r, column=c).fill = CELL_FILL_ALT
        r += 1

    larguras5 = [20, 30, 50, 35, 30]
    for i, w in enumerate(larguras5, 1):
        ws5.column_dimensions[get_column_letter(i)].width = w

    # ============ ABA 6: INSTRUCOES PRODUCAO ============
    ws6 = wb.create_sheet("Instrucoes Producao")
    instrucoes = [
        ("Passo 1", "Confirmar proposta", "Ler proposta_direcao.md e concordar com roteiro, estilo e cores."),
        ("Passo 2", "Gerar clipes", "Copiar cada prompt de prompts_fase_b.md para Google Flow/Runway/Luma/Kling. Gerar 3 MP4 de ~10s."),
        ("Passo 3", "Montar vídeo", "Importar clipes 1→2→3 no CapCut/Premiere. Adicionar VO em português de Moçambique, legendas sincronizadas, SFX opcional. Exportar 9:16, máx 60s."),
        ("Passo 4", "Publicar YouTube", "Título curto com emoji, descrição curta em PT-MZ, thumbnail com cores verde/vermelho/amarelo, publicar como Shorts, adicionar à playlist da categoria."),
        ("O que o assistente NÃO faz", "Limitações", "Não acessa YouTube, não faz login, não gera vídeo automaticamente, não edita/exporta MP4."),
        ("O que o assistente FAZ", "Recursos", "Escreve roteiros, ajusta cores/personagem/estilo, cria prompts, ajuda com legendas e descrições."),
    ]
    for c, h in enumerate(["Passo", "Ação", "Detalhes"], 1):
        cell = ws6.cell(row=1, column=c, value=h)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER
        cell.border = BORDER

    r = 2
    for inst in instrucoes:
        for c, val in enumerate(inst, 1):
            ws6.cell(row=r, column=c, value=val).font = CELL_FONT
            ws6.cell(row=r, column=c).border = BORDER
            ws6.cell(row=r, column=c).alignment = WRAP
            if r % 2 == 0:
                ws6.cell(row=r, column=c).fill = CELL_FILL_ALT
        r += 1

    larguras6 = [10, 25, 80]
    for i, w in enumerate(larguras6, 1):
        ws6.column_dimensions[get_column_letter(i)].width = w

    # ============ ABA 7: CHECKLIST PUBLICACAO ============
    ws7 = wb.create_sheet("Checklist Publicacao")
    checklist = [
        "Vídeo exportado em MP4 9:16 (1080x1920), máximo 60s",
        "Narração gravada em português de Moçambique",
        "Legendas sincronizadas, uma linha por vez",
        "Título curto com emoji (ex: 'O kombi ficou preso no trânsito 🚌')",
        "Descrição curta em português de Moçambique + CTA para inscrever-se",
        "Thumbnail com palitinho e cores verde/vermelho/amarelo",
        "Publicado como YouTube Shorts",
        "Adicionado à playlist correspondente da categoria",
        "Hashtags: #MakuvaTV + categoria",
        "Comente/responda aos comentários nos primeiros dias",
    ]
    for c, h in enumerate(["#", "Item de Checklist", "Status (✓/✗)"], 1):
        cell = ws7.cell(row=1, column=c, value=h)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER
        cell.border = BORDER

    for i, item in enumerate(checklist, 1):
        ws7.cell(row=i+1, column=1, value=i).alignment = CENTER
        ws7.cell(row=i+1, column=2, value=item).font = CELL_FONT
        ws7.cell(row=i+1, column=3, value="").alignment = CENTER
        for c in range(1, 4):
            ws7.cell(row=i+1, column=c).border = BORDER
            ws7.cell(row=i+1, column=c).alignment = WRAP

    ws7.column_dimensions["A"].width = 5
    ws7.column_dimensions["B"].width = 90
    ws7.column_dimensions["C"].width = 15

    # Salvar
    caminho_saida = r"C:\laragon\www\stickman-video-director\MAKUVA_TV_PROJETO_COMPLETO.xlsx"
    wb.save(caminho_saida)
    print(f"Excel gerado com sucesso: {caminho_saida}")
    print(f"Total de vídeos processados: {len(dados)}")

if __name__ == "__main__":
    main()