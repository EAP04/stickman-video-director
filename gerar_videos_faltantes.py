# -*- coding: utf-8 -*-
"""
Gera os 19 vídeos faltantes (182-200) para completar o plano de 200 vídeos do Makuva TV.
Cada vídeo recebe: proposta_direcao.md, prompts_fase_b.md, instrucoes_producao.md
Seguindo o padrao Style 2 · Ambientes Variados ja aplicado aos 181 vídeos existentes.
Prompts em ingles puro para Google Flow/Runway/Luma/Kling.
"""

import os

BASE = r"C:\laragon\www\stickman-video-director\makuva_tv\02_roteiros"

# (numero, sufixo, titulo, mensagem, gancho, ambiente_pt, ambiente_en, cores,
#  vo1_pt, vo2_pt, vo3_pt, cena1_pt, cena2_pt, cena3_pt, cena1_en, cena2_en, cena3_en,
#  sfx_pt, sfx_en, categoria_playlist)
VIDEOS = [
    # luz_viu (completar para 4)
    (182, "luz_viu_3", "A luz voltou quando fechei os olhos",
     "O palitinho esta no quarto, a luz apaga e volta sozinha.",
     "O palitinho fecha os olhos, a luz apaga, abre os olhos e a luz esta de volta.",
     "Quarto simples com cama, abajur e interruptor na parede, fundo branco com mobiliario minimo cinza claro",
     "Simple bedroom with bed, bedside lamp and wall switch, white background with minimal light gray furniture",
     "branco, preto, amarelo",
     "O palitinho fecha os olhos", "A luz apagou", "A luz voltou de novo",
     "The stick figure closes his eyes", "The lights go out", "The stick figure opens his eyes and the lights are back on",
     "The stick figure closes his eyes in the bedroom", "The bedroom lights go out", "The stick figure opens his eyes and the lights are back on",
     "Interruptor de luz", "light switch", "Luz e Quarto"),
    (183, "luz_viu_4", "O interruptor nao acende a luz",
     "O palitinho aperta o interruptor, mas a luz nao acende.",
     "O palitinho chega ao interruptor, aperta, nada acontece, aperta de novo, ainda nada.",
     "Quarto com abajur na mesa de cabeceira e interruptor na parede, fundo branco com mobiliario minimo cinza claro",
     "Bedroom with bedside lamp on nightstand and wall switch, white background with minimal light gray furniture",
     "branco, preto, vermelho",
     "O palitinho chega ao interruptor", "Apertei e nada aconteceu", "Vou usar o celular como lanterna",
     "The stick figure goes to the switch", "I pressed it and nothing happened", "I will use the phone as a flashlight",
     "The stick figure goes to the wall switch", "The stick figure presses the switch, nothing turns on", "The stick figure picks up the phone to use as flashlight",
     "Interruptor", "wall switch", "Luz e Quarto"),

    # kombi_lotada (completar para 4)
    (184, "kombi_lotada_3", "O kombi quebrou no meio da rua",
     "O kombi para no meio da rua, o motorista diz que quebrou, todo mundo desce.",
     "O kombi esta andando, para de repente, o motorista avisa que quebrou e todos precisam sair.",
     "Interior de kombi/chapa com bancos, corrimãos e passageiros, fundo branco com mobiliario minimo cinza claro",
     "Interior of kombi/chapa minibus with seats, handrails and passengers, white background with minimal light gray furniture",
     "branco, preto, vermelho",
     "O kombi esta andando", "O kombi parou", "Vou andar a pe",
     "The kombi is moving", "The kombi stopped", "I will walk on foot",
     "The kombi is driving on the street", "The kombi stops in the middle of the road, driver says it broke down", "Passengers get out and the stick figure walks",
     "Motor de kombi", "kombi engine", "Kombi e Chapa"),
    (185, "kombi_lotada_4", "Todo mundo desceu do kombi",
     "O kombi esta lotado, para no ponto, todo mundo precisa descer de uma vez.",
     "O kombi esta cheio de gente, chega ao ponto, motorista diz que todo mundo desce, tumulto para sair.",
     "Parada de kombi na rua com bancos de espera e movimento de pessoas, fundo branco com mobiliario minimo cinza claro",
     "Kombi stop on the street with waiting benches and people movement, white background with minimal light gray furniture",
     "branco, preto, amarelo",
     "O kombi esta lotado", "Chegamos ao ponto", "Todo mundo sai correndo",
     "The kombi is full", "We arrived at the stop", "Everyone gets out running",
     "The kombi is full of passengers", "The kombi stops at the stop", "Everyone gets off in a hurry",
     "Buzinar de kombi", "kombi horn", "Kombi e Chapa"),

    # falta_rede (completar para 5)
    (186, "falta_rede_2", "Sem sinal no celular",
     "O palitinho tenta fazer uma ligacao, mas nao tem sinal.",
     "O palitinho esta no celular, tenta ligar, aparece sem sinal, fica sem conexao.",
     "Rua do bairro com poste de luz e placas, fundo branco com mobiliario minimo cinza claro",
     "Street in the neighborhood with lamppost and signs, white background with minimal light gray furniture",
     "branco, preto, vermelho",
     "O palitinho tenta ligar", "Sem sinal no celular", "Vou andar ate achar sinal",
     "The stick figure tries to call", "No signal on the phone", "I will walk to find signal",
     "The stick figure holds the phone", "The phone shows no signal", "The stick figure walks looking for signal",
     "Sinal de celular", "cell phone signal", "Falta de Rede"),
    (187, "falta_rede_3", "Barranco sem rede",
     "O palitinho esta no morro/bairro alto, o celular nao pega nada.",
     "O palitinho chega ao local alto do bairro, tenta usar o celular, nao tem rede nenhuma.",
     "Vista do bairro com casas e morro, fundo branco com mobiliario minimo cinza claro",
     "Neighborhood view with houses and hill, white background with minimal light gray furniture",
     "branco, preto, amarelo",
     "O palitinho chega ao morro", "Nao pega rede nenhuma", "Vou descer para achar sinal",
     "The stick figure arrives at the hill", "It does not pick up any signal", "I will go down to find signal",
     "The stick figure at the top of the neighborhood", "The phone with no signal at all", "The stick figure walks down the hill",
     "Vento", "wind", "Falta de Rede"),
    (188, "falta_rede_4", "O chip nao pega",
     "O palitinho coloca um chip novo, mas continua sem sinal.",
     "O palitinho troca o chip no celular, tenta ligar, ainda nao pega nada.",
     "Quarto com mesa e celular sobre ela, fundo branco com mobiliario minimo cinza claro",
     "Room with table and phone on it, white background with minimal light gray furniture",
     "branco, preto, vermelho",
     "O palitinho troca o chip", "Continua sem sinal", "Vou ligar para a operadora",
     "The stick figure changes the chip", "Still no signal", "I will call the operator",
     "The stick figure with phone and chip on the table", "The phone still has no signal", "The stick figure dials on the screen",
     "Chip de celular", "SIM card", "Falta de Rede"),
    (189, "falta_rede_5", "O wi-fi do vizinho nao conecta",
     "O palitinho tenta se conectar no wi-fi do vizinho, mas a senha esta errada.",
     "O palitinho busca redes wi-fi, acha do vizinho, digita a senha, nao conecta.",
     "Sala de estar com janela para a rua e roteador, fundo branco com mobiliario minimo cinza claro",
     "Living room with street window and router, white background with minimal light gray furniture",
     "branco, preto, amarelo",
     "O palitinho busca redes wi-fi", "Senha errada, nao conecta", "Vou pagar meu proprio internet",
     "The stick figure searches for wi-fi networks", "Wrong password, does not connect", "I will pay for my own internet",
     "The stick figure searching for wi-fi networks", "The stick figure types the password on the phone", "The stick figure gives up and walks away",
     "Notificacao de wi-fi", "wi-fi notification", "Falta de Rede"),

    # familia_almoco_domingo (completar para 5)
    (190, "familia_almoco_domingo_2", "O sogro fala demais no almoço",
     "No almoço de domingo, o sogro nao para de falar e todo mundo ouve.",
     "A familia esta almoçando, o sogro começa a contar uma historia longa, ninguem consegue comer.",
     "Sala de jantar com mesa, cadeiras, pratos e comida, fundo branco com mobiliario minimo cinza claro",
     "Dining room with table, chairs, plates and food, white background with minimal light gray furniture",
     "branco, preto, vermelho",
     "A familia esta almoçando", "O sogro comeca a falar", "Ninguem consegue comer",
     "The family is having lunch", "The father-in-law starts talking", "No one can eat",
     "Dining table with family eating", "The father-in-law talking loudly to everyone", "The stick figure with fork stopped",
     "Talheres no prato", "cutlery on plate", "Familia e Domingo"),
    (191, "familia_almoco_domingo_3", "A prima chegou sem avisar",
     "No almoço de domingo, a prima aparece de surpresa e ninguem esperava.",
     "A familia esta almoçando, a campainha toca, e a prima entra sem ter sido convidada.",
     "Sala de estar com sofa, mesa de centro e porta de entrada, fundo branco com mobiliario minimo cinza claro",
     "Living room with sofa, coffee table and entrance door, white background with minimal light gray furniture",
     "branco, preto, amarelo",
     "A familia esta almoçando", "A campainha toca", "A prima apareceu sem avisar",
     "The family is having lunch", "The doorbell rings", "The cousin showed up without warning",
     "Table with family having lunch", "The doorbell ringing at the door", "The cousin entering the living room",
     "Campainha", "doorbell", "Familia e Domingo"),
    (192, "familia_almoco_domingo_4", "A tia trouxe comida demais",
     "A tia chega ao almoço de domingo com varias panelas de comida.",
     "A tia entra na sala carregando panelas e mais panelas, a mesa ja estava cheia.",
     "Sala de jantar com mesa ja posta e porta de entrada, fundo branco com mobiliario minimo cinza claro",
     "Dining room with set table and entrance door, white background with minimal light gray furniture",
     "branco, preto, vermelho",
     "A mesa ja estava cheia", "A tia entra com panelas", "Onde vamos colocar tanta comida?",
     "The table was already full", "The aunt enters with pots", "Where will we put so much food?",
     "Dining table with plates", "The aunt carrying several pots", "The stick figure looking at so many pots",
     "Panelas batendo", "pots clinking", "Familia e Domingo"),
    (193, "familia_almoco_domingo_5", "O primo sentou no lugar errado",
     "No almoço de domingo, o primo senta no lugar do avo e ninguem ousa dizer nada.",
     "A familia esta sentada para almoçar, o primo ocupa a cadeira do avo, silencio constrangedor.",
     "Sala de jantar com cadeiras ao redor da mesa, fundo branco com mobiliario minimo cinza claro",
     "Dining room with chairs around the table, white background with minimal light gray furniture",
     "branco, preto, amarelo",
     "Todos estao sentados", "O primo sentou na cadeira do avo", "Ninguem fala nada",
     "Everyone is sitting", "The cousin sat in the grandfather's chair", "No one says anything",
     "Chairs around the table", "The cousin sitting in the wrong chair", "The grandfather standing looking at the chair",
     "Silencio constrangedor", "awkward silence", "Familia e Domingo"),

    # xiga_matola (completar para 5)
    (194, "xiga_matola_2", "O motorista de xiga nao sabe o caminho",
     "O motorista da xiga para e pergunta caminho ao passageiro.",
     "O palitinho entra na xiga, o motorista para no meio do caminho e pergunta para onde ir.",
     "Interior de xiga com motorista, passageiro e painel, fundo branco com mobiliario minimo cinza claro",
     "Interior of xiga taxi with driver, passenger and dashboard, white background with minimal light gray furniture",
     "branco, preto, vermelho",
     "O palitinho entra na xiga", "O motorista para o carro", "Para onde o senhor quer ir?",
     "The stick figure gets into the xiga", "The driver stops the car", "Where do you want to go, sir?",
     "The stick figure in the back seat", "The driver stopping the xiga", "The driver asking for directions",
     "Motor do xiga", "xiga engine", "Xiga e Taxi"),
    (195, "xiga_matola_3", "O preço da xiga sobe no caminho",
     "O motorista combina um preço, mas cobra mais quando chega ao destino.",
     "O palitinho combina 50 meticais, o motorista leva, e ao chegar cobra 100.",
     "Rua da cidade com xiga em movimento e placas de trânsito, fundo branco com mobiliario minimo cinza claro",
     "City street with moving xiga taxi and traffic signs, white background with minimal light gray furniture",
     "branco, preto, amarelo",
     "Combinamos 50 meticais", "Chegamos ao destino", "Agora sao 100 meticais",
     "We agreed on 50 meticais", "We arrived at the destination", "Now it is 100 meticais",
     "The stick figure and the driver talking", "The xiga stopping at the destination", "The driver extending his hand to charge",
     "Buzinar", "honking", "Xiga e Taxi"),
    (196, "xiga_matola_4", "O xiga parou no meio da rua",
     "O xiga quebra no meio do caminho, todos precisam descer e continuar a pe.",
     "O xiga esta andando, para de repente, o motorista diz que nao tem jeito, todos saem andando.",
     "Rua com xiga parado e passageiros descendo, fundo branco com mobiliario minimo cinza claro",
     "Street with xiga stopped and passengers getting out, white background with minimal light gray furniture",
     "branco, preto, vermelho",
     "O xiga esta andando", "O xiga quebrou", "Vou continuar a pe",
     "The xiga is moving", "The xiga broke down", "I will continue on foot",
     "The xiga driving on the street", "The xiga stopped in the middle of the road", "Passengers getting out and walking",
     "Motor parado", "engine stopped", "Xiga e Taxi"),
    (197, "xiga_matola_5", "Nao tem troco no xiga",
     "O passageiro paga com nota grande, o motorista nao tem troco.",
     "O palitinho paga a corrida com uma nota de 200, o motorista diz que nao tem troco.",
     "Interior de xiga com motorista e passageiro pagando, fundo branco com mobiliario minimo cinza claro",
     "Interior of xiga taxi with driver and passenger paying, white background with minimal light gray furniture",
     "branco, preto, amarelo",
     "Paguei com nota de 200", "Nao tenho troco", "Fica assim mesmo entao",
     "I paid with a 200 note", "I have no change", "Keep it like that then",
     "The stick figure giving the note to the driver", "The driver looking at the note without change", "The stick figure getting out of the xiga",
     "Dinheiro de papel", "paper money", "Xiga e Taxi"),

    # igreja_pastor (completar para 3)
    (198, "igreja_pastor_3", "O celular tocou na igreja",
     "Durante o culto, o celular de alguem toca alto e o pastor olha para o lado.",
     "A igreja esta em culto, o celular toca com uma musica alta, todos olham para quem esta.",
     "Interior de igreja com bancos, pastor na frente e congregacao, fundo branco com mobiliario minimo cinza claro",
     "Church interior with benches, pastor in front and congregation, white background with minimal light gray furniture",
     "branco, preto, vermelho",
     "A congregacao esta orando", "O celular tocou alto", "O pastor olha para o lado",
     "The congregation is praying", "The phone rang loudly", "The pastor looks to the side",
     "Church benches with people", "The phone ringing in someone's hand", "The pastor turning his head",
     "Musica de celular", "cell phone ringtone", "Igreja e Pastor"),

    # fila_banco (completar para 3)
    (199, "fila_banco_3", "A fila do banco nao anda",
     "O palitinho esta na fila do banco, passa o tempo e ninguem e chamado.",
     "O palitinho esta sentado na fila, olha o relogio, a fila nao avança, horas passam.",
     "Agencia do banco com cadeiras de espera, guiche e pessoas na fila, fundo branco com mobiliario minimo cinza claro",
     "Bank branch with waiting chairs, counter and people in line, white background with minimal light gray furniture",
     "branco, preto, amarelo",
     "O palitinho esta na fila", "A fila nao anda", "Ja faz uma hora que estou aqui",
     "The stick figure is in line", "The line does not move", "It has been an hour since I am here",
     "Waiting chairs at the bank", "The stick figure looking at the watch", "The counter empty while the line waits",
     "Relogio", "watch", "Banco e Filas"),

    # casamento_dote (completar para 3)
    (200, "casamento_dote_3", "A negociacao do dote",
     "A familia do noivo negocia o lobolo com a familia da noiva, valores sobem e descem.",
     "As duas familias estao reunidas, comecam a falar do dote, os valores ficam cada vez mais altos.",
     "Sala de estar com duas familias sentadas em cadeiras opostas, fundo branco com mobiliario minimo cinza claro",
     "Living room with two families sitting on opposite chairs, white background with minimal light gray furniture",
     "branco, preto, vermelho",
     "As familias estao reunidas", "Comecamos a falar do dote", "O valor esta ficando alto demais",
     "The families are gathered", "We start talking about the dowry", "The value is getting too high",
     "Two families sitting to talk", "The representative talking about the dowry", "The bride's father listening seriously",
     "Conversa familiar", "family conversation", "Casamento e Dote"),
]


def gerar_proposta_direcao(numero, sufixo, titulo, mensagem, gancho, ambiente_pt, cores, vo1_pt, vo2_pt, vo3_pt, cena1_pt, cena2_pt, cena3_pt):
    cores_lista = [c.strip() for c in cores.split(",")]
    return f"""# Proposta de Direção — Vídeo {numero} do Makuva TV: {sufixo}

## 1. Dados gerais
- **Canal:** Makuva TV
- **Título em português:** "{titulo}"
- **Duração:** 30 segundos (3 clipes de ~10s)
- **Formato:** 9:16 vertical (YouTube Shorts)
- **Modo:** A · Director Mode
- **Estilo:** Style 2 · Ambientes Variados (fundo branco com ambiente por cena, palito simples)
- **Idioma da narração:** Português de Moçambique

## 2. Mensagem central e gancho
- **Mensagem:** {mensagem}
- **Gancho (0–3s):** {gancho}

## 3. Configurações técnicos
- **Proporção:** 9:16
- **Duração alvo:** 30 segundos (3 clipes)
- **Estilo visual:** Style 2 Ambientes Variados, tema claro com ambiente diferenciado por vídeo
- **Cores de destaque (máximo 3):** {cores}
- **Ambiente de fundo:** {ambiente_pt}
- **Cores usadas no vídeo:** Fundo branco, traço preto, destaque {cores_lista[0]} no clipe 1
- **Não usar:** Notação de cor técnica (hex, RGB), balões de fala, texto na cena

## 4. Perfil da voz (narrador)
- **Identidade:** Narrador adulto, descontraído, próximo do povo moçambicano
- **Acento:** Português de Moçambique
- **Tom:** Conversacional, leve, cômico sem exagero
- **Entrega:** Ritmo médio, pausas naturais, sem raspidez
- **Onde usar:** Narração em voz off (áudio apenas, sem balões de fala)

## 5. Estrutura narrativa (3 clipes)

| Clipe | Tempo | Propósito narrativo | Cena do palitinho | VO (português) |
|-------|-------|---------------------|-------------------|----------------|
| 1 | 0–10s | Golden Hook — estabelecer conflito | {cena1_pt} | "{vo1_pt}" |
| 2 | 10–20s | Unveil Insider Secrets — revelar a reality | {cena2_pt} | "{vo2_pt}" |
| 3 | 20–30s | Ultimate Truth + Elevation — piada final | {cena3_pt} | "{vo3_pt}" |

## 6. Continuidade entre clipes
- Clipe 1 termina com {vo1_pt} → Clipe 2 começa com {vo2_pt}
- Clipe 2 termina com {vo2_pt} → Clipe 3 começa com {vo3_pt}
- Clipe 3 termina com {vo3_pt} → convite para comentar relacionado ao tema

## 7. BGM e som
- **Música:** Instrumental leve, tema cotidiano, sem tirar atenção da narração
- **SFX:** Relacionado ao tema (opcional, leve)
- **Narração:** Áudio apenas, sem legendas queimadas na cena (legendas adicionadas na edição)

## 8. Confirmação necessária
Antes de gerar os prompts de vídeo (Fase B), confirme:
- [ ] Você concorda com este roteiro de 30 segundos
- [ ] Você quer manter o estilo Style 2 (ambiente diferenciado por vídeo, palito consistente)
- [ ] Você quer manter as cores verde, vermelho, amarelo como destaques
- [ ] Você vai gerar os clipes em Google Flow, Runway, Luma ou Kling?

Após sua confirmação, passo os prompts prontos da Fase B para você copiar e colar.
"""


def gerar_prompts_fase_b(numero, sufixo, nome1_pt, nome2_pt, nome3_pt, prompt1_en, prompt2_en, prompt3_en, cores, sfx_en):
    cores_lista = [c.strip() for c in cores.split(",")]
    cores_str = ", ".join(cores_lista)
    return f"""# Prompts Fase B — Vídeo {numero}: {sufixo}

Copie e cole cada prompt separadamente na ferramenta de geração de vídeo (Google Flow, Runway, Luma ou Kling). Cada prompt gera um clipe de ~10 segundos.

## Clipe 1 — {nome1_pt} (0–10s)

```
{prompt1_en}
```

## Clipe 2 — {nome2_pt} (10–20s)

```
{prompt2_en}
```

## Clipe 3 — {nome3_pt} (20–30s)

```
{prompt3_en}
```

## Regras de geração (não alterar)
- Proporção: 9:16 vertical
- Duração: ~10 segundos por clipe
- Nenhum texto, número ou interface na cena
- Personagem consistente (mesma cabeça, mesmos membros, mesma linha)
- Nenhum membro ocioso por mais de 2–3 segundos
- Cores apenas com nomes comuns: {cores_str}
- Não usar hex, RGB ou Pantone

## Após gerar
Baixe os 3 clipes (MP4) e monte no CapCut, Premiere ou editor que preferir. Adicione:
1. Narração em português de Moçambique
2. Legendas sincronizadas
3. Efeito sonoro de {sfx_en} (opcional)
4. Thumbnail com cores verde, vermelho, amarelo
"""


def gerar_instrucoes_producao(numero, sufixo, titulo, vo1_pt, vo2_pt, vo3_pt, sfx_pt, categoria_playlist):
    return f"""# Instruções — Produzir o Vídeo {numero} do Makuva TV ({sufixo})

## Passo 1 — Confirmar a proposta
Leia o arquivo `proposta_direcao.md` e o roteiro do vídeo {numero}. Se concordar com o roteiro, estilo e cores, prossiga para o passo 2.

## Passo 2 — Gerar os clipes
1. Abra o gerador de vídeo que você escolher (Google Flow, Runway, Luma ou Kling).
2. Faça login com sua conta (você mesmo, eu não consigo acessar).
3. Copie o **Clipe 1** do arquivo `prompts_fase_b.md` e cole na ferramenta.
4. Gere o vídeo, baixe o MP4.
5. Repita para o **Clipe 2** e **Clipe 3**.

## Passo 3 — Montar o vídeo
1. Abra o CapCut (celular ou computador) ou Premiere.
2. Importe os 3 clipes na ordem: 1 → 2 → 3.
3. Grave ou adicione narração em português de Moçambique:
   - "{vo1_pt}"
   - "{vo2_pt}"
   - "{vo3_pt}"
4. Adicione legendas em português, uma linha por vez, sincronizadas com a fala.
5. Adicione efeito sonoro de {sfx_pt} (opcional).
6. Exporte em MP4 vertical 9:16, no máximo 60 segundos.

## Passo 4 — Publicar no YouTube (Makuva TV)
1. Acesse o YouTube com sua conta.
2. Clique em Criar → Enviar vídeo.
3. Selecione o MP4 montado.
4. Título: "{titulo}"
5. Descrição: curta, em português de Moçambique, peça para inscrever-se.
6. Thumbnail: use cores verde, vermelho, amarelo com o palitinho.
7. Publique como Shorts.
8. Adicione à playlist "{categoria_playlist}" (crie esta playlist no YouTube Studio).

## O que eu não consigo fazer
- Não consigo acessar o YouTube nem fazer login por você.
- Não consigo gerar os clipes de vídeo no Google Flow/Runway/Luma.
- Não consigo editar ou exportar o MP4.

## O que eu consigo fazer
- Escrever o roteiro do próximo vídeo.
- Ajustar cores, personagem ou estilo.
- Criar mais prompts de geração.
- Ajudar com legendas e descrições para o YouTube.

Quando estiver pronto para o **Vídeo {numero + 1}**, é só avisar.
"""


def montar_prompt(cena_en, ambiente_en):
    """Monta o prompt em inglês seguindo o padrão dos vídeos existentes."""
    return (f"Minimalist 2D animated stick figure on white background with {ambiente_en}. "
            f"{cena_en}. Hollow circular head, black stick limbs, uniform medium line weight. "
            f"Simple black lines, smooth 2D animation style. 9:16 vertical aspect ratio, 10 seconds duration. "
            f"No speech bubbles, no text, no dialogue boxes.")


def main():
    criados = 0
    pulados = 0

    for (numero, sufixo, titulo, mensagem, gancho, ambiente_pt, ambiente_en, cores,
         vo1_pt, vo2_pt, vo3_pt, cena1_pt, cena2_pt, cena3_pt, cena1_en, cena2_en, cena3_en,
         sfx_pt, sfx_en, categoria_playlist) in VIDEOS:

        pasta = os.path.join(BASE, f"video_{numero}_{sufixo}")

        if os.path.exists(pasta):
            print(f"  AVISO: vídeo {numero} já existe, pulando")
            pulados += 1
            continue

        os.makedirs(pasta, exist_ok=True)

        # 1. proposta_direcao.md
        with open(os.path.join(pasta, "proposta_direcao.md"), "w", encoding="utf-8") as f:
            f.write(gerar_proposta_direcao(
                numero, sufixo, titulo, mensagem, gancho, ambiente_pt, cores,
                vo1_pt, vo2_pt, vo3_pt, cena1_pt, cena2_pt, cena3_pt))

        # 2. prompts_fase_b.md (prompts em inglês puro)
        prompt1 = montar_prompt(cena1_en, ambiente_en)
        prompt2 = montar_prompt(cena2_en, ambiente_en)
        prompt3 = montar_prompt(cena3_en, ambiente_en)

        with open(os.path.join(pasta, "prompts_fase_b.md"), "w", encoding="utf-8") as f:
            f.write(gerar_prompts_fase_b(
                numero, sufixo,
                vo1_pt, vo2_pt, vo3_pt,
                prompt1, prompt2, prompt3, cores, sfx_en))

        # 3. instrucoes_producao.md
        with open(os.path.join(pasta, "instrucoes_producao.md"), "w", encoding="utf-8") as f:
            f.write(gerar_instrucoes_producao(
                numero, sufixo, titulo, vo1_pt, vo2_pt, vo3_pt, sfx_pt, categoria_playlist))

        criados += 1
        print(f"  OK: vídeo {numero} ({sufixo}) criado em {pasta}")

    print(f"\nConcluído: {criados} vídeos criados, {pulados} pulados (já existiam).")
    print(f"Total de vídeos: 181 + {criados} = {181 + criados}")


if __name__ == "__main__":
    main()