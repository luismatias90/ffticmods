# Solo Ramza Manager

Troca a classe do Ramza em **FINAL FANTASY TACTICS - The Ivalice Chronicles (versão Enhanced)** por qualquer classe do jogo (genéricas, de personagens únicos ou de chefes/inimigos), com todas as skills da classe custando 0 JP. Feito para runs solo Ramza.

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

1. **Feche o Reloaded-II** e abra o `SoloRamzaManager.exe`.
2. Confira o painel **Configuração**. O jogo e o Reloaded-II são detectados sozinhos; se não forem, use *Procurar...*
3. Clique em **Extrair / atualizar** (leva uns 10 segundos, só lê o jogo). Repita depois de updates do jogo.
4. Escolha uma classe nas abas **Genéricas**, **Personagens únicos** ou **Chefes / Inimigos ⚠**. O painel da direita mostra as skills (com o custo de JP antes → depois), equipamentos e atributos.
5. Clique em **Aplicar no Ramza**. O mod é instalado e ativado no perfil do `FFT_enhanced.exe`.
6. Abra o jogo **pelo Reloaded-II**.

Para trocar de classe, é só escolher outra e aplicar de novo. **Restaurar jogo original** remove o mod.

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
- `ramza_manager/mod_builder.py`: calcula e gera o mod (JobData/AbilityData/SpawnData XML + ModConfig).
- `ramza_manager/nxd_db.py`: extrai as tabelas nex (`ability`, `job`, `jobcommand`) do jogo para SQLite e gera os `.nxd` editados (custo de JP e nome da classe).
- `ramza_manager/class_catalog.py`: quais classes aparecem e em que aba.
- `ramza_manager/app.py`: interface (PySide6).
- `data/`: tabelas XML de referência do jogo original.
- `tools/FF16Tools/`: FF16Tools.CLI (Nenkai, MIT).

Os dados extraídos e as configurações ficam em `%LOCALAPPDATA%\SoloRamzaManager`.

## Créditos e licença

- Partes do código e as tabelas de referência vêm do **The Ivalice Chronicles Mod Studio** (GPL-3). Por isso este projeto também é **GPL-3** (ver `LICENSE`).
- **FF16Tools** e **fftivc.utility.modloader**, por Nenkai.
- **Reloaded-II**, por Sewer56.
