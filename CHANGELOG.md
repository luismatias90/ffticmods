# Changelog

## 0.6.0 — 2026-10-05

### Português

**JP pelo save, não mais custo 0**

- As skills voltam a custar o JP normal do jogo. Antes o custo 0 valia para qualquer unidade com essas skills; agora nenhuma outra unidade é afetada.
- O seletor *Custo de JP das skills* saiu. A prévia da classe mostra o custo de cada skill e o total para aprender tudo, e avisa quando passa de 9999.

**Simulador de atributos por nível**

- A prévia da classe tem um campo *Simular atributos no nível*: digite o nível (1–99) e a tabela de atributos mostra o HP, MP, Speed, PA e MA que o Ramza teria, calculados pelo multiplicador e pelo crescimento da classe. HP/MP aparecem como faixa, porque o valor inicial é sorteado.

**Aba Save do jogo**

- Nova aba (`Ctrl+4`) que edita o Ramza num save manual: JP da classe dele (até 9999), Bravura e Fé (0–100).
- Acha o `enhanced.png` sozinho, lista os slots com nível, JP, Bravura e Fé, e grava com o FF16Tools.
- Guarda uma cópia do save em `%LOCALAPPDATA%\SoloRamzaManager\save_backups` antes de cada gravação, confere o resultado antes de substituir o original e mantém a miniatura.
- Não grava com o jogo aberto, porque ele regravaria o save ao sair.

**Itens iniciais pelo save, não mais pelo bônus Deluxe**

- Os itens da aba **Itens iniciais** são somados ao inventário do slot ao gravar o save, até 99 de cada. Funciona em qualquer edição e em qualquer save, não só em jogo novo na Deluxe.
- O mod não mexe mais no pacote de bônus da Deluxe Edition (`systembonus*.nxd`), e o botão **Padrão da Deluxe** saiu.

### English

**JP from the save, no more 0 cost**

- Skills cost the game's normal JP again. The 0 cost used to apply to any unit with those skills; now no other unit is affected.
- The *Skill JP cost* selector is gone. The class preview shows each skill's cost and the total to learn everything, and warns when it goes over 9999.

**Stat simulator by level**

- The class preview has a *Simulate stats at level* field: type a level (1–99) and the stats table shows the HP, MP, Speed, PA and MA Ramza would have, computed from the class multiplier and growth. HP/MP show a range because the starting value is random.

**Game save tab**

- New tab (`Ctrl+4`) that edits Ramza in a manual save: his class JP (up to 9999), Bravery and Faith (0–100).
- Finds `enhanced.png` on its own, lists the slots with level, JP, Bravery and Faith, and writes through FF16Tools.
- Keeps a copy of the save in `%LOCALAPPDATA%\SoloRamzaManager\save_backups` before each write, checks the result before replacing the original, and keeps the thumbnail.
- Won't write while the game is open, since it would rewrite the save on exit.

**Starting items through the save, no more Deluxe bonus**

- Items from the **Starting items** tab are added to the slot's inventory when writing the save, up to 99 of each. Works with any edition and any save, not just a new game on the Deluxe.
- The mod no longer touches the Deluxe Edition bonus pack (`systembonus*.nxd`), and the **Deluxe default** button is gone.

## 0.5.0 — 2026-10-02

### Português

**Sprite do Ramza**

- Dá para trocar o sprite de batalha do Ramza (capítulos 1, 2–3 e 4) pelo de outro personagem humano ou de uma classe genérica.
- O mod troca a folha clássica e a HD que o modo Enhanced desenha, além das cores de roupa na tabela `CharCLUT`.
- O retrato do menu também troca, quando o personagem tem um. A Lettie e a maioria dos aldeões não têm retrato próprio e ficam com o do Ramza.
- Sprites de monstro ficam de fora: a grade de animação é outra e trava com os movimentos do Ramza.

**Classes para importar**

- A pasta `biblioteca_classes` traz 11 classes prontas, em `.ramzaclass.json`, para importar pelo botão **Importar...**: Alchemist, Arcane Archer, Druid, Freelancer, Glass Cannon, Rogue, Shogun, Time Knight, Troubadour, Warlock e White Monk. O `index.json` resume cada uma.

**Interface**

- Visual novo, no estilo dos menus de *The Ivalice Chronicles*: janelas azul-noite com moldura dupla dourada, texto creme e a mão-cursor dos menus no item selecionado.
- A navegação virou uma barra lateral com três passos (classe, sprite e itens iniciais). Cada passo mostra o que será aplicado, e o cartão **Instalado agora** mostra o que já está no jogo.
- Os filtros de classe viraram botões com a contagem de cada categoria.
- O registro saiu do pé da janela. A barra de status mostra a última mensagem, e o botão **Registro** abre o histórico.
- Atalhos: `Ctrl+1`, `Ctrl+2` e `Ctrl+3` trocam de passo, `Ctrl+Enter` aplica o mod, `Ctrl+N` cria uma classe, `Ctrl+F` busca e `Delete` remove o item selecionado da bolsa.
- Enquanto o app extrai os dados ou monta o mod, o cursor vira ampulheta.

**Correções**

- O campo **Descrição** do editor de classes não aparece mais com fundo preto de console.

### English

**Ramza's sprite**

- Ramza's battle sprite (chapters 1, 2–3 and 4) can be swapped for another human character or a generic class.
- The mod replaces both the classic sheet and the HD sheet the Enhanced mode draws, plus the outfit colors in the `CharCLUT` table.
- The menu portrait changes too, when that character has one. Lettie and most villagers have no portrait of their own and keep Ramza's.
- Monster sprites are left out: their animation grid is different and locks up with Ramza's movements.

**Classes to import**

- The `biblioteca_classes` folder ships 11 ready-made classes as `.ramzaclass.json` files, imported with the **Import...** button: Alchemist, Arcane Archer, Druid, Freelancer, Glass Cannon, Rogue, Shogun, Time Knight, Troubadour, Warlock and White Monk. `index.json` summarizes each one.

**Interface**

- New look, in the style of *The Ivalice Chronicles* menus: night-blue windows with a double gold frame, cream text, and the menu hand cursor on the selected item.
- Navigation is now a sidebar with three steps (class, sprite and starting items). Each step shows what will be applied, and the **Installed now** card shows what is already in the game.
- Class filters are now buttons that show how many classes are in each category.
- The log no longer sits at the bottom of the window. The status bar shows the latest message, and the **Log** button opens the history.
- Shortcuts: `Ctrl+1`, `Ctrl+2` and `Ctrl+3` switch steps, `Ctrl+Enter` applies the mod, `Ctrl+N` creates a class, `Ctrl+F` searches and `Delete` removes the selected bag item.
- The cursor turns into an hourglass while the app extracts game data or builds the mod.

**Fixes**

- The **Description** field in the class editor no longer shows up with a black console background.
