# Solo Ramza Manager

Troca a classe do Ramza em **FINAL FANTASY TACTICS - The Ivalice Chronicles (versão Enhanced)** por qualquer classe do jogo (genéricas, de personagens únicos ou de chefes/inimigos), com todas as skills da classe custando 0 JP. Feito para runs solo Ramza.

**App pronto:** `dist\SoloRamzaManager\SoloRamzaManager.exe`. Em outro PC, basta clonar o repositório (ou baixar o ZIP pelo GitHub) e rodar esse `.exe`. Ele precisa da pasta `_internal` ao lado, então copie a pasta `SoloRamzaManager` inteira, não só o `.exe`. Não precisa de Python; só do **.NET 9 Runtime** (ver abaixo).

## O que muda e o que não muda

**Muda (só no Ramza):**
- As três classes próprias do Ramza (Squire do Cap. 1, Squire dos Cap. 2–3 e Gallant Knight do Cap. 4) viram a classe escolhida, com skillset, equipamentos, multiplicadores e crescimento de atributos, Move/Jump, evasão, habilidades inatas e nome no menu.
- As skills do skillset (ação, reação, suporte e movimento) custam 0 JP. Você aprende tudo no menu *Learn* logo no começo.
- Se a classe não puder usar o equipamento inicial do Ramza, ele troca por um item básico compatível (ex.: Broadsword → Rod para Black Mage).

**Não muda:**
- Nível, EXP e atributos base: o Ramza começa no nível 1 e evolui normalmente.
- A imunidade do Ramza a *Traitor*, a história, os inimigos e os outros personagens.
- Os arquivos do jogo. Tudo é aplicado por um mod do Reloaded-II, e o botão *Restaurar* desfaz.

> Efeito colateral: o custo 0 de JP vale para qualquer unidade que tenha essas skills. Numa run solo isso não faz diferença.

## Pré-requisitos (uma vez só)

1. **.NET 9 Runtime** (necessário para ler os dados do jogo): https://dotnet.microsoft.com/download/dotnet/9.0
2. **Reloaded-II**: https://github.com/Reloaded-Project/Reloaded-II/releases/latest
   - Extraia numa pasta (ex.: `C:\Reloaded-II`) e abra o `Reloaded-II.exe`.
   - Clique em **+ (Add an Application)** e escolha `FFT_enhanced.exe` na pasta do jogo.
3. **FFTIVC Mod Loader** (`fftivc.utility.modloader`): no Reloaded-II, procure por "fftivc" em *Download Mods*, ou baixe em https://github.com/Nenkai/fftivc.utility.modloader/releases/latest
4. Abra o jogo uma vez pela Steam para criar as pastas de save.

## Como usar

Na primeira abertura, um assistente pergunta se a interface fica em **português** ou **inglês** e percorre o que instalar e como configurar. Dá para reabri-lo pelo botão **Assistente**, e trocar o idioma a qualquer momento no canto da janela (PT-BR / EN).

1. **Feche o Reloaded-II** e abra o `SoloRamzaManager.exe`.
2. Confira o painel **Configuração**. O jogo e o Reloaded-II são detectados sozinhos; se não forem, use *Procurar...*
3. Clique em **Extrair / atualizar** (leva uns 10 segundos, só lê o jogo). Repita depois de updates do jogo.
4. Escolha uma classe nas abas **Genéricas**, **Personagens únicos** ou **Chefes / Inimigos ⚠**. O painel da direita mostra as skills (com o custo de JP antes → depois), equipamentos e atributos.
5. Clique em **Aplicar no Ramza**. O mod é instalado e ativado no perfil do `FFT_enhanced.exe`.
6. Abra o jogo **pelo Reloaded-II**.

Para trocar de classe, é só escolher outra e aplicar de novo. **Restaurar jogo original** remove o mod.

## Classes customizadas (skillset misto)

Na sub-aba **✦ Minhas classes** já vêm 7 classes prontas, marcadas com ★:

| Classe | Base | Ideia |
|---|---|---|
| Red Mage | Black Mage | Magia branca e negra básicas, com espada e escudo leve |
| Mystic Knight | Knight | Spellblade (lâmina com status) e magias elementais |
| Paladin | Knight | Holy Sword e curas |
| Dark Knight | Knight | Fell Sword, drenos e *sap*; mais HP/PA e menos esquiva |
| Sage | White Mage | Branca e negra avançadas, MA alto e corpo frágil |
| Ranger | Archer | Aim e Aimed Shot, com arco, besta e arma de fogo, Move 4 |
| Battle Monk | Monk | Artes marciais e os gritos de guerra do Ramza |

As classes de fábrica não podem ser apagadas. Editar uma delas salva uma cópia sua. Elas ficam em `data/classes/` e são geradas por `packaging/make_presets.py`.

Você também pode criar uma classe própria:

1. **Nova classe...** abre o editor. Dê um nome à classe e ao skillset e escolha a **classe base**, que define atributos, equipamentos, Move/Jump, evasão e habilidades inatas.
2. Monte o skillset com habilidades de **qualquer classe** do jogo: até **16 de ação** e **6 de reação/suporte/movimento**. A busca aceita nome, skillset ou tipo, e *Copiar skills da base* é um ponto de partida.
3. Na aba **Atributos e equipamento** do editor, ajuste o que quiser em relação à classe base:
   - **multiplicador** e **crescimento** de HP, MP, Speed, PA e MA;
   - **Move**, **Jump** e **esquiva da classe (C-Ev)**;
   - até 4 **habilidades inatas** (sempre ativas, fora dos slots);
   - **equipamentos permitidos** (armas, escudo, cabeça, corpo, acessórios).

   O que você não mexe continua igual ao da classe base, e segue a nova base se você trocar de base. Esquiva mágica não aparece porque no jogo ela não é da classe: vem de escudos, capas e acessórios.
4. Selecione a classe na lista e clique em **Aplicar no jogo**, como com uma classe normal. O equipamento inicial do Ramza é trocado se a classe não puder usá-lo.

O skillset misto vai nos skillsets próprios do Ramza (Mettle, ids 25–27), que só ele usa. Inimigos e outros personagens não mudam. O custo de JP escolhido vale para as habilidades do skillset, com o mesmo efeito colateral descrito acima.

**Compartilhar:** **Exportar...** gera um arquivo `.ramzaclass.json` (poucos KB) para mandar no Discord, fórum etc. Quem recebe usa **Importar...**. O arquivo é conferido na importação: habilidades que não existem ou estão no slot errado saem com aviso, e uma classe base inválida é recusada. A biblioteca fica em `%LOCALAPPDATA%\SoloRamzaManager\classes`.

> Habilidades de Item, Throw, Jump e Arithmeticks têm mecânica própria e podem se comportar diferente fora do skillset original. O editor avisa quando elas estão na lista. Teste antes da run.

## Itens iniciais (bolsa) — requer Deluxe Edition

Na aba **Itens iniciais (bolsa)** você monta a lista de itens com que quer começar: busque qualquer item (armas, armaduras, acessórios, consumíveis), escolha a quantidade (1–99) e clique em **Adicionar →**. Marque **Trocar os itens do bônus da Deluxe Edition** e clique em **Aplicar no jogo**. A classe e a bolsa são independentes: dá para usar só uma delas, desmarcando a outra.

Como funciona: o jogo entrega os itens do bônus da Deluxe Edition no inventário. O app troca o conteúdo desse bônus pela sua lista, e as cores preta/vermelha do Ramza continuam. Por isso:
- só funciona em cópias com a **Deluxe Edition**;
- vale para **jogo novo**, porque um save que já recebeu o bônus não recebe de novo;
- é **experimental**: teste primeiro com 2 ou 3 itens. Se listas grandes não aparecerem inteiras, reduza.

**Padrão da Deluxe** volta a lista para os itens originais do bônus.

### Primeiro teste no jogo
- Novo jogo → batalha de Orbonne: o Ramza deve aparecer no nível 1 com o nome e o skillset da classe.
- No menu de formação → *Learn*: todas as skills da classe devem custar 0 JP.
- **Se o jogo não deixar aprender com 0 JP**, mude *Custo de JP das skills* para `1` e aplique de novo.

### Classes de chefe/inimigo (⚠)
Lucavi, Ultima Demon e similares usam animações feitas para outros sprites e podem travar com o sprite do Ramza. **Salve antes de testar.** Monstros não aparecem na lista, porque o Ramza ficaria sem menus e equipamentos.

## Para desenvolver

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install PySide6 pyinstaller pytest
.\.venv\Scripts\python SoloRamzaManager.pyw        # rodar
.\.venv\Scripts\python -m pytest                   # testes
.\.venv\Scripts\pyinstaller packaging\SoloRamzaManager.spec --noconfirm   # gera dist\SoloRamzaManager\
```

Estrutura:
- `ramza_manager/mod_builder.py`: calcula e gera o mod (JobData/JobCommandData/AbilityData/SpawnData XML + ModConfig).
- `ramza_manager/nxd_db.py`: extrai as tabelas nex (`ability`, `job`, `jobcommand`) do jogo para SQLite e gera os `.nxd` editados (custo de JP e nome da classe).
- `ramza_manager/class_catalog.py`: quais classes aparecem e em que aba.
- `ramza_manager/custom_class.py`: formato `.ramzaclass.json`, validação e biblioteca de classes customizadas.
- `ramza_manager/class_editor.py`: editor de classe customizada (PySide6).
- `ramza_manager/app.py`: interface (PySide6).
- `data/`: tabelas XML de referência do jogo original.
- `tools/FF16Tools/`: FF16Tools.CLI (Nenkai, MIT).

Os dados extraídos e as configurações ficam em `%LOCALAPPDATA%\SoloRamzaManager`.

## Créditos e licença

- Partes do código e as tabelas de referência vêm do **The Ivalice Chronicles Mod Studio** (GPL-3). Por isso este projeto também é **GPL-3** (ver `LICENSE`).
- **FF16Tools** e **fftivc.utility.modloader**, por Nenkai.
- **Reloaded-II**, por Sewer56.
