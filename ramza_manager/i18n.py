"""Textos da interface em português (Brasil) e inglês."""

from __future__ import annotations

LANG_PT = "pt"
LANG_EN = "en"
LANGS = (LANG_PT, LANG_EN)

_language = LANG_PT

STRINGS: dict[str, dict[str, str]] = {
    LANG_PT: {
        "window_title": "Solo Ramza Manager {version} — FFT: The Ivalice Chronicles (Enhanced)",
        "banner_subtitle": "Final Fantasy Tactics · The Ivalice Chronicles — gerenciador de runs solo do Ramza",
        "lang_tip": "Idioma do aplicativo e do assistente",
        "tab_class": "Classe do Ramza",
        "tab_sprite": "Sprite do Ramza",
        "tab_bag": "Itens iniciais (bolsa)",
        "btn_apply": "Aplicar no jogo",
        "btn_restore": "Restaurar jogo original",
        "setup_title": "Configuração",
        "btn_hide_details": "Ocultar detalhes ▴",
        "btn_show_details": "Detalhes ▾",
        "btn_wizard": "Assistente",
        "row_game": "Jogo:",
        "row_reloaded": "Reloaded-II:",
        "row_modloader": "FFTIVC Mod Loader:",
        "row_dotnet": ".NET 9 Runtime:",
        "row_data": "Dados do jogo:",
        "btn_browse": "Procurar...",
        "btn_download": "Baixar",
        "btn_extract": "Extrair / atualizar",
        "chk_class": "Trocar a classe do Ramza",
        "search_class": "Buscar classe ou skillset...",
        "chk_bag": "Somar estes itens ao inventário ao gravar no save",
        "bag_help": (
            "<b>Como funciona:</b> os itens são <b>somados ao inventário</b> do slot quando você clica em "
            "<b>Gravar no save</b>, na aba <b>Save do jogo</b> (até 99 de cada). Funciona em qualquer edição "
            "e em qualquer save, não só em jogo novo. Gravar de novo soma de novo."
        ),
        "search_item": "Buscar item ou tipo (ex.: Elixir, Sword, Ring)...",
        "lbl_qty": "Quantidade:",
        "btn_add": "Adicionar →",
        "lbl_my_list": "<b>Minha lista</b>",
        "lbl_my_list_n": "Minha lista ({n})",
        "col_item": "Item",
        "col_type": "Tipo",
        "col_qty": "Qtd",
        "btn_remove": "Remover selecionado",
        "btn_clear": "Limpar",
        "status_not_found": "não encontrado",
        "status_reloaded_missing": "não encontrado — instale e aponte a pasta",
        "status_installed": "instalado",
        "status_modloader_missing": "não encontrado na pasta Mods do Reloaded-II",
        "status_dotnet_needed": "necessário para ler os dados do jogo",
        "status_data_ready": "prontos",
        "status_data_missing": "clique em 'Extrair / atualizar' (uns 10 segundos)",
        "status_all_ok": "Tudo pronto: jogo, Reloaded-II, Mod Loader, .NET 9 e dados do jogo",
        "status_missing": "Falta configurar {n} item(ns) — veja abaixo",
        "mod_none": "<b>Nenhum mod</b> — jogo original",
        "mod_original_class": "original (Squire)",
        "mod_sprite_original": "original",
        "mod_active": "Ramza: <b>{klass}</b><br>Sprite: <b>{sprite}</b>",
        "preview_empty": (
            "<h2>Escolha uma classe</h2>"
            "<p>Selecione uma classe na lista para ver skills, equipamentos e atributos.</p>"
            "<p>Ao aplicar, as três classes próprias do Ramza (Cap. 1, Cap. 2–3 e Cap. 4) viram a "
            "classe escolhida. Ele continua começando no nível 1 e evolui normalmente. "
            "O resto do jogo não muda.</p>"
        ),
        "none_f": "nenhuma",
        "none_m": "nenhum",
        "warn_experimental": (
            "<p class='warn'><b>⚠ Experimental:</b> classe de chefe/inimigo. Pode ter "
            "animações faltando ou travar o jogo com o sprite do Ramza. Salve antes de testar.</p>"
        ),
        "preview_skillset": (
            "<p><b>Skillset:</b> {name} · <b>Move</b> {move} · <b>Jump</b> {jump} · "
            "<b>Evasão</b> {evade}% · <span class='muted'>Job {job}</span></p>"
        ),
        "own_skillset": "próprio",
        "h_action": "<h3>Habilidades de ação</h3>",
        "h_rsm": "<h3>Reação / Suporte / Movimento</h3>",
        "innate": "<p><b>Habilidades inatas:</b> {names}</p>",
        "equip": "<p><b>Equipamentos:</b> {names}</p>",
        "h_stats": (
            "<h3>Atributos</h3><table cellspacing=4><tr><th></th><th>Multiplicador</th>"
            "<th>Crescimento*</th><th>Nível {level}**</th></tr>{rows}</table>"
            "<p class='muted'>* crescimento: quanto menor, mais o atributo sobe por nível.<br>"
            "** simulação considerando que todos os níveis foram ganhos nesta classe "
            "(o crescimento vale para a classe em que o nível foi ganho). "
            "HP/MP variam numa faixa porque o valor inicial é sorteado.</p>"
        ),
        "sim_level": "Simular atributos no nível:",
        "sim_level_tip": "Mostra HP, MP, Speed, PA e MA que o Ramza teria nesse nível com esta classe.",
        "status_line": "<p><b>Status inato/inicial:</b> {names}</p>",
        "h_gear": "<h3>Equipamento inicial ajustado</h3>",
        "class_label": "{name} — {skillset} ({n} skills)",
        "tip_job": "Job {job} · skillset {cmd}",
        "cat_generic": "Genéricas",
        "cat_unique": "Personagens únicos",
        "cat_boss": "Chefes / Inimigos ⚠",
        "dlg_game_folder": "Pasta do jogo (onde fica FFT_enhanced.exe)",
        "dlg_bad_folder": "Pasta inválida",
        "dlg_no_exe": "Não encontrei FFT_enhanced.exe nessa pasta.",
        "dlg_reloaded_folder": "Pasta do Reloaded-II (onde fica Reloaded-II.exe)",
        "dlg_no_reloaded": "Não encontrei Reloaded-II.exe nessa pasta.",
        "err_title": "Erro",
        "dlg_no_game": "Jogo não encontrado",
        "dlg_no_game_body": "Aponte a pasta do jogo primeiro.",
        "dlg_dotnet_title": ".NET 9",
        "dlg_dotnet_body": "Instale o .NET 9 Runtime (botão 'Baixar') e tente de novo.",
        "log_extract": "Extraindo tabelas do jogo (só leitura)...",
        "need_setup_title": "Falta configurar",
        "need_extract": "• Extraia os dados do jogo (botão 'Extrair / atualizar').",
        "need_reloaded": "• Instale o Reloaded-II e aponte a pasta dele.",
        "close_reloaded_title": "Feche o Reloaded-II",
        "close_reloaded_body": "Feche o Reloaded-II antes de continuar, senão ele desfaz a ativação do mod.",
        "close_reloaded_restore": "Feche o Reloaded-II antes de restaurar.",
        "pick_class_title": "Escolha uma classe",
        "pick_class_body": (
            "Selecione uma classe na aba 'Classe do Ramza', ou desmarque 'Trocar a classe do Ramza'."
        ),
        "nothing_title": "Nada para aplicar",
        "nothing_body": (
            "Marque a troca de classe e/ou de sprite. Os itens vão para o save, na aba 'Save do jogo'. "
            "Para voltar ao jogo original, "
            "use 'Restaurar jogo original'."
        ),
        "pick_sprite_title": "Escolha um sprite",
        "pick_sprite_body": "Selecione um sprite na aba 'Sprite do Ramza', ou desmarque a troca de sprite.",
        "done_sprite": "• O sprite de batalha do Ramza agora é {name}.",
        "log_sprite": "Lendo o sprite {name} do jogo...",
        "sprite_no_pack": "Não encontrei data/enhanced/{pack}. Aponte a pasta do jogo.",
        "sprite_extract_fail": "Não consegui ler o sprite {name} (código {code}).",
        "chk_sprite": "Trocar o sprite de batalha do Ramza",
        "page_sprite_desc": (
            "O Ramza passa a ser desenhado com o sprite escolhido nos capítulos 1, 2–3 e 4. "
            "As cores e o retrato do menu também mudam (Lettie e a maioria dos aldeões não têm retrato "
            "próprio e mantêm o do Ramza). Algumas cenas de evento podem continuar com o visual original."
        ),
        "sprite_help": (
            "<b>Como funciona:</b> a classe não muda o desenho do Ramza. Esta opção copia a folha "
            "de sprite de outro personagem (a clássica e a HD que o modo Enhanced desenha) por cima "
            "das três folhas dele. Só entram sprites humanos: "
            "monstro usa outra animação e pode travar. Algumas cenas da história continuam com o Ramza original."
        ),
        "search_sprite": "Buscar sprite...",
        "sprite_cat_all": "Todos",
        "sprite_cat_unique": "Personagens",
        "sprite_cat_generic": "Classes e genéricos",
        "sprite_no_match": "Nenhum sprite encontrado.",
        "nav_pick_sprite": "Escolha um sprite",
        "experimental_title": "Classe experimental",
        "experimental_body": "{name} é uma classe de chefe/inimigo e pode travar o jogo.\nAplicar mesmo assim?",
        "log_building": "Gerando mod...",
        "log_applying": "Aplicando...",
        "log_installed": "Mod instalado em {path}",
        "done_title": "Mod aplicado",
        "done_intro": "Pronto!",
        "done_class": "• Ramza agora é {name}. Depois do primeiro save, dê JP a ele na aba 'Save do jogo'.",
        "done_ok": "O mod já está ativado no Reloaded-II. Abra o jogo pelo Reloaded-II.",
        "done_no_app": (
            "Não achei o FFT_enhanced.exe no Reloaded-II. Adicione o jogo lá e ative os mods "
            "'{mod}' e 'FFTIVC Mod Loader'."
        ),
        "restore_need": "Aponte a pasta do Reloaded-II primeiro.",
        "log_removed": "Mod removido. Jogo original.",
        "log_not_installed": "O mod não estava instalado.",
        "restored_title": "Restaurado",
        "restored_body": "O mod foi removido: o Ramza voltou ao original.",
        "nxd_no_pac": "Nenhum .pac encontrado em data/enhanced. O jogo está instalado?",
        "nxd_scanning": "Procurando tabelas em {name}...",
        "nxd_ff16_fail": "FF16Tools falhou ao ler {name} (código {code}). O .NET 9 Runtime está instalado?",
        "nxd_missing": "Não encontrei nos arquivos do jogo: {names}",
        "nxd_warn": "Aviso: tabelas ausentes (ignoradas): {names}",
        "nxd_sqlite": "Convertendo tabelas para SQLite...",
        "nxd_sqlite_fail": "FF16Tools nxd-to-sqlite falhou (código {code}).",
        "nxd_ready": "Dados do jogo prontos.",
        "nxd_generating": "Gerando .nxd: {tables}",
        "nxd_to_nxd_fail": "FF16Tools sqlite-to-nxd falhou (código {code}).",
        "nxd_not_generated": "FF16Tools não gerou {name}.",
        "wiz_title": "Assistente de configuração — Solo Ramza Manager",
        "wiz_back": "Voltar",
        "wiz_next": "Avançar",
        "wiz_finish": "Concluir",
        "wiz_skip": "Abrir o app mesmo assim",
        "wiz_check": "Verificar de novo",
        "wiz_extract": "Extrair agora",
        "wiz_step_lang": "Idioma",
        "wiz_step_overview": "O que instalar",
        "wiz_step_dotnet": ".NET 9",
        "wiz_step_reloaded": "Reloaded-II",
        "wiz_step_loader": "Mod Loader",
        "wiz_step_game": "Pasta do jogo",
        "wiz_step_extract": "Dados do jogo",
        "wiz_step_use": "Como usar",
        "wiz_lang_title": "Idioma  ·  Language",
        "wiz_lang_body": (
            "<p>Escolha o idioma do <b>aplicativo</b> e deste <b>assistente</b>. "
            "Dá para trocar depois, no canto da janela principal.</p>"
            "<p>Choose the language for the <b>app</b> and this <b>wizard</b>. "
            "You can change it later from the corner of the main window.</p>"
        ),
        "wiz_overview_title": "Antes de usar",
        "wiz_overview_body": (
            "<p>O Solo Ramza Manager troca a classe do Ramza em "
            "<b>FINAL FANTASY TACTICS - The Ivalice Chronicles (Enhanced)</b> "
            "por um mod do Reloaded-II. Os arquivos do jogo não são alterados.</p>"
            "<p>Instale isto uma vez, nesta ordem:</p>"
            "<ol>"
            "<li><b>.NET 9 Runtime</b> — para ler as tabelas do jogo.</li>"
            "<li><b>Reloaded-II</b> — o carregador de mods.</li>"
            "<li><b>FFTIVC Mod Loader</b> — e o <b>FFT_enhanced.exe</b> adicionado no Reloaded-II.</li>"
            "<li><b>Pasta do jogo</b> — e abrir o jogo uma vez pela Steam.</li>"
            "<li><b>Extrair os dados</b> — o app lê o jogo (uns 10 segundos).</li>"
            "</ol>"
            "<p>No último passo está como escolher a classe, a bolsa e aplicar o mod.</p>"
        ),
        "wiz_dotnet_title": ".NET 9 Runtime",
        "wiz_dotnet_body": (
            "<p>O app usa o FF16Tools para ler as tabelas do jogo. Esse programa precisa do "
            "<b>.NET 9 Runtime</b> (o Runtime, não o SDK).</p>"
            "<ol>"
            "<li>Clique em <b>Baixar</b> e instale o .NET 9 Runtime.</li>"
            "<li>Volte aqui e clique em <b>Verificar de novo</b>.</li>"
            "</ol>"
        ),
        "wiz_dotnet_ok": "O .NET 9 Runtime está instalado.",
        "wiz_dotnet_bad": "O .NET 9 Runtime não foi encontrado.",
        "wiz_reloaded_title": "Reloaded-II",
        "wiz_reloaded_body": (
            "<ol>"
            "<li>Clique em <b>Baixar</b> e extraia o Reloaded-II numa pasta "
            "(por exemplo <b>C:\\Reloaded-II</b>).</li>"
            "<li>Abra o <b>Reloaded-II.exe</b> uma vez, para ele criar as pastas internas.</li>"
            "<li>Clique em <b>Procurar...</b> e aponte essa pasta — a mesma onde está o Reloaded-II.exe.</li>"
            "</ol>"
        ),
        "wiz_reloaded_ok": "Reloaded-II encontrado.",
        "wiz_reloaded_bad": "Aponte a pasta onde está o Reloaded-II.exe.",
        "wiz_loader_title": "Jogo no Reloaded-II e Mod Loader",
        "wiz_loader_body": (
            "<p>Isto é feito dentro do Reloaded-II:</p>"
            "<ol>"
            "<li>Clique em <b>+ (Add an Application)</b> e escolha o <b>FFT_enhanced.exe</b> "
            "na pasta do jogo.</li>"
            "<li>Abra <b>Download Mods</b>, procure por <b>fftivc</b> e instale o "
            "<b>FFTIVC Mod Loader</b>. Se preferir, baixe o release no botão abaixo.</li>"
            "<li>Feche o Reloaded-II ao terminar. Ele precisa estar fechado para o app ativar o mod.</li>"
            "</ol>"
        ),
        "wiz_app_ok": "FFT_enhanced.exe já está adicionado no Reloaded-II.",
        "wiz_app_bad": "O FFT_enhanced.exe ainda não foi adicionado no Reloaded-II.",
        "wiz_loader_ok": "FFTIVC Mod Loader instalado.",
        "wiz_loader_bad": "FFTIVC Mod Loader não está na pasta Mods.",
        "wiz_game_title": "Pasta do jogo",
        "wiz_game_body": (
            "<p>Aponte a pasta onde está o <b>FFT_enhanced.exe</b>. Na Steam, em geral é:</p>"
            "<p><b>…\\steamapps\\common\\FINAL FANTASY TACTICS - The Ivalice Chronicles</b></p>"
            "<p>Depois, abra o jogo <b>uma vez pela Steam</b> (não pelo Reloaded-II) para criar "
            "as pastas de save. O assistente não consegue confirmar esse passo.</p>"
        ),
        "wiz_game_ok": "FFT_enhanced.exe encontrado.",
        "wiz_game_bad": "Aponte a pasta do jogo.",
        "wiz_extract_title": "Extrair os dados do jogo",
        "wiz_extract_body": (
            "<p>O app lê as tabelas do jogo (só leitura, uns 10 segundos) e guarda uma cópia local. "
            "Os arquivos do jogo não mudam. Repita este passo depois de um update do jogo.</p>"
            "<p>Precisa do .NET 9 e da pasta do jogo já apontada.</p>"
        ),
        "wiz_extract_ok": "Dados do jogo prontos.",
        "wiz_extract_bad": "Os dados ainda não foram extraídos.",
        "wiz_extract_running": "Extraindo… pode levar uns 10 segundos.",
        "wiz_use_title": "Como configurar a run",
        "wiz_use_body": (
            "<ol>"
            "<li><b>Feche o Reloaded-II</b> antes de aplicar qualquer coisa.</li>"
            "<li>Na aba <b>Classe do Ramza</b>, escolha uma classe. O painel da direita mostra "
            "skills (com o custo de JP), equipamentos e atributos. "
            "As três classes próprias do Ramza passam a ser essa. Ele continua no nível 1.</li>"
            "<li>As skills custam o JP normal. Depois do primeiro save, use a aba <b>Save do jogo</b> "
            "para dar 9999 JP ao Ramza (e ajustar Bravura e Fé).</li>"
            "<li>Opcional, na aba <b>Sprite do Ramza</b>: escolha outro sprite de batalha. "
            "Cores e retrato mudam junto; algumas cenas podem continuar com o Ramza.</li>"
            "<li>Opcional, na aba <b>Itens iniciais</b>: monte a lista de itens. Eles são somados ao "
            "inventário quando você grava o save na aba <b>Save do jogo</b>.</li>"
            "<li>Clique em <b>Aplicar no jogo</b>. Abra o jogo <b>pelo Reloaded-II</b>.</li>"
            "<li><b>Restaurar jogo original</b> remove o mod.</li>"
            "</ol>"
            "<p>Classes de chefe/inimigo (⚠) podem travar com o sprite do Ramza. Salve antes de testar.</p>"
            "<p>Para trocar o idioma depois, use o seletor <b>PT-BR / EN</b> no canto da janela, "
            "ou abra este assistente de novo pelo botão <b>Assistente</b>.</p>"
        ),
        "cat_custom": "✦ Minhas classes",
        "cc_btn_new": "Nova classe...",
        "cc_btn_edit": "Editar...",
        "cc_btn_dup": "Duplicar",
        "cc_btn_delete": "Excluir",
        "cc_btn_import": "Importar...",
        "cc_btn_export": "Exportar...",
        "cc_btn_new_plus": "+ Nova classe...",
        "cc_new_tip": "Crie uma classe com skillset misto (Ctrl+N)",
        "cc_builtin_note": "★ Classe pronta — ao editar, uma cópia é salva nas suas classes.",
        "cc_user_note": "Sua classe — clique duas vezes na lista para editar.",
        "nav_caption": "O QUE VAI MUDAR",
        "nav_tip": "Ctrl+{n}",
        "apply_tip": "Gera o mod e instala no Reloaded-II (Ctrl+Enter)",
        "btn_log_show": "Registro ▴",
        "btn_log_hide": "Registro ▾",
        "status_ready": "Pronto.",
        "status_busy": "Trabalhando… aguarde.",
        "installed_caption": "INSTALADO AGORA",
        "nav_off": "Desligado — sem alteração",
        "nav_pick_class": "Escolha uma classe",
        "nav_bag_n": "{n} item(ns) na lista",
        "page_class_desc": "Escolha a classe que o Ramza vai usar: uma do jogo ou uma criada por você.",
        "page_bag_desc": "Monte a lista de itens que entram no inventário do save.",
        "filter_all": "Todas",
        "list_no_match": "Nenhuma classe encontrada. Tente outra busca ou outro filtro.",
        "lbl_items_catalog": "Itens do jogo",
        "tip_remove": "Remove os itens selecionados (Delete)",
        "cc_label": "{name} — {skillset} (base: {base}, {n} skills)",
        "cc_preview_empty": (
            "<h2>Minhas classes</h2>"
            "<p>Crie uma classe com um <b>skillset misto</b>: escolha uma <b>classe base</b> "
            "(que você pode ajustar: atributos, equipamentos, Move/Jump, esquiva e inatas) e monte o skillset com "
            "habilidades de qualquer classe do jogo — até 16 de ação e 6 de reação/suporte/movimento.</p>"
            "<p>As classes com <b>★</b> vêm prontas (Red Mage, Paladin, Sage...). Clique em <b>Nova classe...</b> para criar a sua. Com <b>Exportar...</b> você gera um arquivo "
            "<b>.ramzaclass.json</b> para mandar a outras pessoas; quem recebe usa <b>Importar...</b>.</p>"
            "<p class='muted'>O skillset misto vai só nos skillsets próprios do Ramza, então inimigos e "
            "outros personagens não mudam.</p>"
        ),
        "cc_preview_meta": "<p><b>Classe base:</b> {base} · <b>Autor:</b> {author}</p>",
        "cc_no_author": "—",
        "cc_special_warn": (
            "<b>⚠ Atenção:</b> {names} têm mecânica própria (itens, arremesso, pulo ou Arithmeticks) "
            "e podem se comportar diferente fora do skillset original. Teste antes da run."
        ),
        "cc_copy_name": "{name} (cópia)",
        "cc_delete_title": "Excluir classe",
        "cc_delete_body": "Excluir a classe \"{name}\" da biblioteca? O mod já aplicado não muda.",
        "cc_import_title": "Importar classes",
        "cc_export_title": "Exportar classe",
        "cc_file_filter": "Classe do Solo Ramza (*.ramzaclass.json);;JSON (*.json)",
        "cc_imported": "Importada(s): {names}",
        "cc_pick_first": "Selecione uma classe em 'Minhas classes' primeiro.",
        "cc_exported": "Classe exportada em {path}",
        "cc_exported_body": "Arquivo salvo:\n{path}\n\nMande esse arquivo para quem quiser usar a classe.",
        "cc_invalid_title": "Classe incompleta",
        "cc_need_name": "Dê um nome para a classe.",
        "cc_need_skills": "Adicione pelo menos uma habilidade ao skillset.",
        "cc_err_format": "não é um arquivo de classe do Solo Ramza Manager.",
        "cc_err_version": "feito numa versão mais nova do app (formato {version}). Atualize o Solo Ramza Manager.",
        "cc_err_field": "campo '{field}' ausente ou inválido.",
        "cc_err_read": "não consegui ler {name}: {error}",
        "cc_err_base": "Classe base inválida (Job {job}).",
        "cc_warn_dropped": "habilidade {id} não existe como {slot} neste jogo e foi removida.",
        "cc_warn_limit": "mais de {n} habilidades de {slot}; as excedentes foram removidas.",
        "cc_slot_action": "ação",
        "cc_slot_rsm": "reação/suporte/movimento",
        "cc_new_title": "Nova classe",
        "cc_edit_title": "Editar classe",
        "cc_name": "Nome da classe:",
        "cc_skillset": "Nome do skillset:",
        "cc_skillset_ph": "(igual ao nome da classe)",
        "cc_base": "Classe base:",
        "cc_copy_base": "Copiar skills da base",
        "cc_copy_base_tip": "Adiciona às listas as habilidades do skillset original da classe base.",
        "cc_author": "Autor:",
        "cc_desc": "Descrição:",
        "cc_desc_ph": "Opcional. Aparece no jogo no lugar da descrição da classe.",
        "cc_base_hint": (
            "A classe base dá o ponto de partida de atributos, equipamentos, Move/Jump, esquiva e inatas "
            "(ajuste na aba 'Atributos e equipamento'). O skillset abaixo substitui o dela. "
            "Dê dois cliques numa habilidade para adicionar ou remover."
        ),
        "cc_search": "Buscar habilidade, skillset ou tipo...",
        "cc_filter_all": "Todas",
        "cc_up": "↑",
        "cc_down": "↓",
        "cc_actions_count": "<b>Ação</b> ({n}/{max})",
        "cc_rsm_count": "<b>Reação / Suporte / Movimento</b> ({n}/{max})",
        "cc_full_title": "Skillset cheio",
        "cc_full_body": (
            "O skillset aceita até {a} habilidades de ação e {r} de reação/suporte/movimento. "
            "Não couberam: {names}"
        ),
        "cc_page_skills": "Skillset",
        "cc_page_job": "Atributos e equipamento",
        "cc_builtin_tip": "Classe de fábrica. Editar cria uma cópia sua em 'Minhas classes'.",
        "cc_builtin_copied": "Classe de fábrica editada: a versão alterada foi salva como '{name}'.",
        "cc_builtin_no_delete": "As classes de fábrica (★) vêm com o app e não podem ser excluídas.",
        "cc_save": "Salvar",
        "cc_cancel": "Cancelar",
        "cc_box_stats": "Atributos",
        "cc_col_mult": "Multiplicador",
        "cc_col_growth": "Crescimento",
        "cc_stats_hint": (
            "Multiplicador: % aplicado ao atributo (100 = normal, maior = mais forte). "
            "Crescimento: quanto <b>menor</b>, mais o atributo sobe por nível."
        ),
        "cc_box_move": "Movimento e esquiva",
        "cc_evasion": "Esquiva (C-Ev)",
        "cc_no_mev": (
            "Esquiva mágica não é da classe no jogo: vem de escudos, capas e acessórios."
        ),
        "cc_box_innate": "Habilidades inatas (sempre ativas, fora dos slots)",
        "cc_box_equip": "Equipamentos permitidos",
        "cc_equip_weapon": "Armas",
        "cc_equip_shield": "Escudo",
        "cc_equip_head": "Cabeça",
        "cc_equip_body": "Corpo",
        "cc_equip_accessory": "Acessórios",
        "cc_reset_base": "Voltar tudo para a classe base",
        "cc_base_value": "base: {value}",
        "cc_slot_innate": "inata",
        "cc_warn_equip": "tipo de equipamento desconhecido '{flag}' foi ignorado.",
        "cc_warn_range": "{field} fora da faixa {low}–{high}; ajustado.",
        "cc_changed": "<p><b>Alterado em relação à base:</b> {names}</p>",
        "cc_field_innates": "inatas",
        "cc_field_equip": "equipamentos",
        "wiz_checklist_title": "Situação agora",
        "tab_save": "Save do jogo",
        "page_save_desc": "Edita um save manual: JP, Bravura e Fé do Ramza e itens no inventário.",
        "nav_save_caption": "EDITAR SAVE",
        "nav_save_slot": "{title}",
        "nav_save_none": "Gravado na hora, fora do 'Aplicar'",
        "save_help": (
            "<b>Como usar:</b> com o mod aplicado, comece o jogo e salve num slot manual "
            "(o primeiro save aparece depois da primeira batalha). <b>Feche o jogo</b>, escolha o slot aqui "
            "e grave. O JP vai para a classe própria do Ramza, que o mod trocou pela classe escolhida: "
            "use no menu <i>Learn</i>. As skills custam o JP normal do jogo. "
            "Os itens da aba <b>Itens iniciais</b> são somados ao inventário. "
            "O app guarda uma cópia do save antes de gravar. "
            "<i>Carregue o slot manual: o autosave/continuar não recebe a edição.</i>"
        ),
        "save_file_row": "Arquivo:",
        "save_not_found": "save não encontrado — abra o jogo e salve uma vez, ou use Procurar...",
        "btn_save_reload": "Recarregar",
        "dlg_save_file": "Escolha o enhanced.png",
        "save_slots": "Slots",
        "save_slot_n": "Slot {n}",
        "save_slot_line": "{title}\nRamza Nv {level} · JP {jp} · Bravura {brave} · Fé {faith}",
        "save_slot_no_ramza": "{title}\n(Ramza não encontrado neste slot)",
        "save_no_slots": "Nenhum slot salvo.",
        "save_pick_slot": "Escolha um slot.",
        "save_ramza": "Ramza — nível {level}",
        "save_jp": "JP da classe do Ramza:",
        "save_jp_tip": "JP disponível para aprender as skills da classe do Ramza (máx. 9999).",
        "btn_save_jp_max": "9999",
        "save_brave": "Bravura:",
        "save_brave_tip": "Bravura permanente (0–100): dano de punhos e de algumas armas, chance de reação.",
        "save_faith": "Fé:",
        "save_faith_tip": "Fé permanente (0–100): força das magias que o Ramza lança e recebe.",
        "btn_save_write": "Gravar no save",
        "save_confirm_title": "Gravar no save",
        "save_confirm_items": "\nItens somados:\n{items}\n",
        "save_items_n": "Itens: {n} tipo(s) da aba 'Itens iniciais' serão somados ao inventário.",
        "save_items_none": "Itens: nenhum (monte a lista na aba 'Itens iniciais').",
        "save_confirm_body": (
            "Gravar no slot {title}?\n\nJP: {jp}\nBravura: {brave}\nFé: {faith}\n{items}\n"
            "Uma cópia do save original fica guardada."
        ),
        "close_game_title": "Feche o jogo",
        "close_game_body": "Feche o jogo antes de gravar: ele regrava o save e a edição se perde.",
        "save_done_title": "Save gravado",
        "save_done_body": "Pronto! Abra o jogo e carregue o slot.\n\nCópia do save original:\n{backup}",
        "log_save_reading": "Lendo o save...",
        "log_save_read": "{n} slot(s) lido(s) de {name}.",
        "log_save_writing": "Gravando o save...",
        "log_save_written": "Slot {title} gravado. Backup: {backup}",
        "save_err_slot": "O slot {n} está vazio.",
        "save_err_no_ramza": "Não achei o Ramza no slot {n}.",
        "save_err_png": "O arquivo não parece um save do jogo (.png).",
        "save_err_unpack": "Não consegui abrir {name} com o FF16Tools.",
        "save_err_pack": "Não consegui montar o save novo com o FF16Tools.",
        "save_err_verify": "O save novo não bateu com a edição; nada foi gravado.",
        "jp_total": "<p>Total para aprender tudo: <span class='jp'>{total} JP</span></p>",
        "jp_total_over": (
            "<p>Total para aprender tudo: <span class='jp'>{total} JP</span> — mais que os {max} JP "
            "do save; o resto vem das batalhas.</p>"
        ),
    },
    LANG_EN: {
        "window_title": "Solo Ramza Manager {version} — FFT: The Ivalice Chronicles (Enhanced)",
        "banner_subtitle": "Final Fantasy Tactics · The Ivalice Chronicles — solo Ramza run manager",
        "lang_tip": "Language of the app and the wizard",
        "tab_class": "Ramza's class",
        "tab_sprite": "Ramza's sprite",
        "tab_bag": "Starting items (bag)",
        "btn_apply": "Apply to the game",
        "btn_restore": "Restore the original game",
        "setup_title": "Setup",
        "btn_hide_details": "Hide details ▴",
        "btn_show_details": "Details ▾",
        "btn_wizard": "Wizard",
        "row_game": "Game:",
        "row_reloaded": "Reloaded-II:",
        "row_modloader": "FFTIVC Mod Loader:",
        "row_dotnet": ".NET 9 Runtime:",
        "row_data": "Game data:",
        "btn_browse": "Browse...",
        "btn_download": "Download",
        "btn_extract": "Extract / update",
        "chk_class": "Change Ramza's class",
        "search_class": "Search class or skillset...",
        "chk_bag": "Add these items to the inventory when writing the save",
        "bag_help": (
            "<b>How it works:</b> the items are <b>added to the slot's inventory</b> when you click "
            "<b>Write to save</b> on the <b>Game save</b> tab (up to 99 of each). Works with any edition "
            "and any save, not just a new game. Writing again adds them again."
        ),
        "search_item": "Search item or type (e.g. Elixir, Sword, Ring)...",
        "lbl_qty": "Quantity:",
        "btn_add": "Add →",
        "lbl_my_list": "<b>My list</b>",
        "lbl_my_list_n": "My list ({n})",
        "col_item": "Item",
        "col_type": "Type",
        "col_qty": "Qty",
        "btn_remove": "Remove selected",
        "btn_clear": "Clear",
        "status_not_found": "not found",
        "status_reloaded_missing": "not found — install it and point to the folder",
        "status_installed": "installed",
        "status_modloader_missing": "not found in the Reloaded-II Mods folder",
        "status_dotnet_needed": "required to read the game data",
        "status_data_ready": "ready",
        "status_data_missing": "click 'Extract / update' (about 10 seconds)",
        "status_all_ok": "Ready: game, Reloaded-II, Mod Loader, .NET 9 and game data",
        "status_missing": "{n} item(s) still need setup — see below",
        "mod_none": "<b>No mod</b> — original game",
        "mod_original_class": "original (Squire)",
        "mod_sprite_original": "original",
        "mod_active": "Ramza: <b>{klass}</b><br>Sprite: <b>{sprite}</b>",
        "preview_empty": (
            "<h2>Choose a class</h2>"
            "<p>Select a class in the list to see skills, equipment and stats.</p>"
            "<p>When you apply, Ramza's three own classes (Ch. 1, Ch. 2–3 and Ch. 4) become the "
            "chosen class. He still starts at level 1 and levels up normally. "
            "The rest of the game is unchanged.</p>"
        ),
        "none_f": "none",
        "none_m": "none",
        "warn_experimental": (
            "<p class='warn'><b>⚠ Experimental:</b> boss/enemy class. It may be missing "
            "animations or freeze the game with Ramza's sprite. Save before you try it.</p>"
        ),
        "preview_skillset": (
            "<p><b>Skillset:</b> {name} · <b>Move</b> {move} · <b>Jump</b> {jump} · "
            "<b>Evasion</b> {evade}% · <span class='muted'>Job {job}</span></p>"
        ),
        "own_skillset": "own",
        "h_action": "<h3>Action abilities</h3>",
        "h_rsm": "<h3>Reaction / Support / Movement</h3>",
        "innate": "<p><b>Innate abilities:</b> {names}</p>",
        "equip": "<p><b>Equipment:</b> {names}</p>",
        "h_stats": (
            "<h3>Stats</h3><table cellspacing=4><tr><th></th><th>Multiplier</th>"
            "<th>Growth*</th><th>Level {level}**</th></tr>{rows}</table>"
            "<p class='muted'>* growth: the lower the number, the more the stat rises per level.<br>"
            "** simulated as if every level was gained in this class "
            "(growth applies to the class the level was gained in). "
            "HP/MP show a range because the starting value is random.</p>"
        ),
        "sim_level": "Simulate stats at level:",
        "sim_level_tip": "Shows the HP, MP, Speed, PA and MA Ramza would have at this level with this class.",
        "status_line": "<p><b>Innate/starting status:</b> {names}</p>",
        "h_gear": "<h3>Adjusted starting gear</h3>",
        "class_label": "{name} — {skillset} ({n} skills)",
        "tip_job": "Job {job} · skillset {cmd}",
        "cat_generic": "Generic",
        "cat_unique": "Unique characters",
        "cat_boss": "Bosses / Enemies ⚠",
        "dlg_game_folder": "Game folder (where FFT_enhanced.exe is)",
        "dlg_bad_folder": "Invalid folder",
        "dlg_no_exe": "FFT_enhanced.exe was not found in that folder.",
        "dlg_reloaded_folder": "Reloaded-II folder (where Reloaded-II.exe is)",
        "dlg_no_reloaded": "Reloaded-II.exe was not found in that folder.",
        "err_title": "Error",
        "dlg_no_game": "Game not found",
        "dlg_no_game_body": "Point to the game folder first.",
        "dlg_dotnet_title": ".NET 9",
        "dlg_dotnet_body": "Install the .NET 9 Runtime (Download button) and try again.",
        "log_extract": "Extracting game tables (read only)...",
        "need_setup_title": "Setup incomplete",
        "need_extract": "• Extract the game data ('Extract / update').",
        "need_reloaded": "• Install Reloaded-II and point to its folder.",
        "close_reloaded_title": "Close Reloaded-II",
        "close_reloaded_body": "Close Reloaded-II before continuing, or it will undo the mod activation.",
        "close_reloaded_restore": "Close Reloaded-II before restoring.",
        "pick_class_title": "Choose a class",
        "pick_class_body": "Select a class on the 'Ramza's class' tab, or uncheck 'Change Ramza's class'.",
        "nothing_title": "Nothing to apply",
        "nothing_body": (
            "Check the class change and/or the sprite change. Items go into the save, on the 'Game save' tab. "
            "To go back to the original game, "
            "use 'Restore the original game'."
        ),
        "pick_sprite_title": "Pick a sprite",
        "pick_sprite_body": "Select a sprite on the 'Ramza's sprite' tab, or uncheck the sprite change.",
        "done_sprite": "• Ramza's battle sprite is now {name}.",
        "log_sprite": "Reading the {name} sprite from the game...",
        "sprite_no_pack": "data/enhanced/{pack} was not found. Point to the game folder.",
        "sprite_extract_fail": "Could not read the {name} sprite (code {code}).",
        "chk_sprite": "Change Ramza's battle sprite",
        "page_sprite_desc": (
            "Ramza is drawn with the chosen sprite in chapters 1, 2–3 and 4. "
            "The colors and the menu portrait change too (Lettie and most townsfolk have no portrait "
            "of their own and keep Ramza's). Some event scenes can still show the original Ramza."
        ),
        "sprite_help": (
            "<b>How it works:</b> changing his class does not change how Ramza is drawn. "
            "This copies another character's sprite sheet (the classic one and the HD one the "
            "Enhanced mode draws) over his three sheets. Only human "
            "sprites are listed: a monster sheet uses different animations and can freeze the game. "
            "Some story scenes still show the original Ramza."
        ),
        "search_sprite": "Search sprites...",
        "sprite_cat_all": "All",
        "sprite_cat_unique": "Characters",
        "sprite_cat_generic": "Jobs and generics",
        "sprite_no_match": "No sprite found.",
        "nav_pick_sprite": "Pick a sprite",
        "experimental_title": "Experimental class",
        "experimental_body": "{name} is a boss/enemy class and may freeze the game.\nApply anyway?",
        "log_building": "Building mod...",
        "log_applying": "Applying...",
        "log_installed": "Mod installed at {path}",
        "done_title": "Mod applied",
        "done_intro": "Done!",
        "done_class": "• Ramza is now {name}. After the first save, give him JP in the 'Game save' tab.",
        "done_ok": "The mod is already enabled in Reloaded-II. Launch the game from Reloaded-II.",
        "done_no_app": (
            "FFT_enhanced.exe is not in Reloaded-II. Add the game there and enable "
            "'{mod}' and 'FFTIVC Mod Loader'."
        ),
        "restore_need": "Point to the Reloaded-II folder first.",
        "log_removed": "Mod removed. Original game.",
        "log_not_installed": "The mod was not installed.",
        "restored_title": "Restored",
        "restored_body": "The mod was removed: Ramza is back to the original.",
        "nxd_no_pac": "No .pac found in data/enhanced. Is the game installed?",
        "nxd_scanning": "Looking for tables in {name}...",
        "nxd_ff16_fail": "FF16Tools failed to read {name} (code {code}). Is the .NET 9 Runtime installed?",
        "nxd_missing": "Not found in the game files: {names}",
        "nxd_warn": "Warning: missing tables (ignored): {names}",
        "nxd_sqlite": "Converting tables to SQLite...",
        "nxd_sqlite_fail": "FF16Tools nxd-to-sqlite failed (code {code}).",
        "nxd_ready": "Game data is ready.",
        "nxd_generating": "Building .nxd: {tables}",
        "nxd_to_nxd_fail": "FF16Tools sqlite-to-nxd failed (code {code}).",
        "nxd_not_generated": "FF16Tools did not produce {name}.",
        "wiz_title": "Setup wizard — Solo Ramza Manager",
        "wiz_back": "Back",
        "wiz_next": "Next",
        "wiz_finish": "Finish",
        "wiz_skip": "Open the app anyway",
        "wiz_check": "Check again",
        "wiz_extract": "Extract now",
        "wiz_step_lang": "Language",
        "wiz_step_overview": "What to install",
        "wiz_step_dotnet": ".NET 9",
        "wiz_step_reloaded": "Reloaded-II",
        "wiz_step_loader": "Mod Loader",
        "wiz_step_game": "Game folder",
        "wiz_step_extract": "Game data",
        "wiz_step_use": "How to use",
        "wiz_lang_title": "Idioma  ·  Language",
        "wiz_lang_body": (
            "<p>Escolha o idioma do <b>aplicativo</b> e deste <b>assistente</b>. "
            "Dá para trocar depois, no canto da janela principal.</p>"
            "<p>Choose the language for the <b>app</b> and this <b>wizard</b>. "
            "You can change it later from the corner of the main window.</p>"
        ),
        "wiz_overview_title": "Before you start",
        "wiz_overview_body": (
            "<p>Solo Ramza Manager changes Ramza's class in "
            "<b>FINAL FANTASY TACTICS - The Ivalice Chronicles (Enhanced)</b> "
            "with a Reloaded-II mod. The game files themselves are not modified.</p>"
            "<p>Install the following once, in this order:</p>"
            "<ol>"
            "<li><b>.NET 9 Runtime</b> — to read the game tables.</li>"
            "<li><b>Reloaded-II</b> — the mod loader.</li>"
            "<li><b>FFTIVC Mod Loader</b> — and add <b>FFT_enhanced.exe</b> in Reloaded-II.</li>"
            "<li><b>Game folder</b> — then launch the game once from Steam.</li>"
            "<li><b>Extract the data</b> — the app reads the game (about 10 seconds).</li>"
            "</ol>"
            "<p>The last step explains how to pick a class, set the bag and apply the mod.</p>"
        ),
        "wiz_dotnet_title": ".NET 9 Runtime",
        "wiz_dotnet_body": (
            "<p>The app uses FF16Tools to read the game tables. That program needs the "
            "<b>.NET 9 Runtime</b> (the Runtime, not the SDK).</p>"
            "<ol>"
            "<li>Click <b>Download</b> and install the .NET 9 Runtime.</li>"
            "<li>Come back and click <b>Check again</b>.</li>"
            "</ol>"
        ),
        "wiz_dotnet_ok": "The .NET 9 Runtime is installed.",
        "wiz_dotnet_bad": "The .NET 9 Runtime was not found.",
        "wiz_reloaded_title": "Reloaded-II",
        "wiz_reloaded_body": (
            "<ol>"
            "<li>Click <b>Download</b> and extract Reloaded-II to a folder "
            "(for example <b>C:\\Reloaded-II</b>).</li>"
            "<li>Open <b>Reloaded-II.exe</b> once so it can create its folders.</li>"
            "<li>Click <b>Browse...</b> and select that folder — the one that contains Reloaded-II.exe.</li>"
            "</ol>"
        ),
        "wiz_reloaded_ok": "Reloaded-II found.",
        "wiz_reloaded_bad": "Point to the folder that contains Reloaded-II.exe.",
        "wiz_loader_title": "Game in Reloaded-II and Mod Loader",
        "wiz_loader_body": (
            "<p>Do this inside Reloaded-II:</p>"
            "<ol>"
            "<li>Click <b>+ (Add an Application)</b> and choose <b>FFT_enhanced.exe</b> "
            "in the game folder.</li>"
            "<li>Open <b>Download Mods</b>, search for <b>fftivc</b> and install "
            "<b>FFTIVC Mod Loader</b>. Or download the release with the button below.</li>"
            "<li>Close Reloaded-II when you are done. It has to be closed for this app to enable the mod.</li>"
            "</ol>"
        ),
        "wiz_app_ok": "FFT_enhanced.exe is already added in Reloaded-II.",
        "wiz_app_bad": "FFT_enhanced.exe has not been added in Reloaded-II yet.",
        "wiz_loader_ok": "FFTIVC Mod Loader is installed.",
        "wiz_loader_bad": "FFTIVC Mod Loader is not in the Mods folder.",
        "wiz_game_title": "Game folder",
        "wiz_game_body": (
            "<p>Point to the folder that contains <b>FFT_enhanced.exe</b>. On Steam it is usually:</p>"
            "<p><b>…\\steamapps\\common\\FINAL FANTASY TACTICS - The Ivalice Chronicles</b></p>"
            "<p>Then launch the game <b>once from Steam</b> (not from Reloaded-II) so it can create "
            "the save folders. The wizard cannot confirm that step.</p>"
        ),
        "wiz_game_ok": "FFT_enhanced.exe found.",
        "wiz_game_bad": "Point to the game folder.",
        "wiz_extract_title": "Extract the game data",
        "wiz_extract_body": (
            "<p>The app reads the game tables (read only, about 10 seconds) and keeps a local copy. "
            "The game files are not changed. Repeat this step after a game update.</p>"
            "<p>.NET 9 and the game folder have to be set first.</p>"
        ),
        "wiz_extract_ok": "Game data is ready.",
        "wiz_extract_bad": "The game data has not been extracted yet.",
        "wiz_extract_running": "Extracting… this can take about 10 seconds.",
        "wiz_use_title": "How to set up the run",
        "wiz_use_body": (
            "<ol>"
            "<li><b>Close Reloaded-II</b> before you apply anything.</li>"
            "<li>On the <b>Ramza's class</b> tab, pick a class. The panel on the right shows "
            "skills (with their JP cost), equipment and stats. "
            "Ramza's three own classes become that class. He still starts at level 1.</li>"
            "<li>Skills cost their normal JP. After the first save, use the <b>Game save</b> tab "
            "to give Ramza 9999 JP (and adjust Bravery and Faith).</li>"
            "<li>Optional, on the <b>Ramza's sprite</b> tab: pick another battle sprite. "
            "Colors and portrait change with it; some scenes can still show Ramza.</li>"
            "<li>Optional, on the <b>Starting items</b> tab: build the item list. The items are added to "
            "the inventory when you write the save on the <b>Game save</b> tab.</li>"
            "<li>Click <b>Apply to the game</b>. Launch the game <b>from Reloaded-II</b>.</li>"
            "<li><b>Restore the original game</b> removes the mod.</li>"
            "</ol>"
            "<p>Boss/enemy classes (⚠) can freeze with Ramza's sprite. Save before you try them.</p>"
            "<p>To change the language later, use the <b>PT-BR / EN</b> selector in the corner of the window, "
            "or open this wizard again with the <b>Wizard</b> button.</p>"
        ),
        "cat_custom": "✦ My classes",
        "cc_btn_new": "New class...",
        "cc_btn_edit": "Edit...",
        "cc_btn_dup": "Duplicate",
        "cc_btn_delete": "Delete",
        "cc_btn_import": "Import...",
        "cc_btn_export": "Export...",
        "cc_btn_new_plus": "+ New class...",
        "cc_new_tip": "Create a class with a mixed skillset (Ctrl+N)",
        "cc_builtin_note": "★ Ready-made class — editing saves a copy to your classes.",
        "cc_user_note": "Your class — double-click it in the list to edit.",
        "nav_caption": "WHAT WILL CHANGE",
        "nav_tip": "Ctrl+{n}",
        "apply_tip": "Builds the mod and installs it into Reloaded-II (Ctrl+Enter)",
        "btn_log_show": "Log ▴",
        "btn_log_hide": "Log ▾",
        "status_ready": "Ready.",
        "status_busy": "Working… please wait.",
        "installed_caption": "INSTALLED NOW",
        "nav_off": "Off — unchanged",
        "nav_pick_class": "Pick a class",
        "nav_bag_n": "{n} item(s) in the list",
        "page_class_desc": "Pick the class Ramza will use: one from the game or one you made.",
        "page_bag_desc": "Build the list of items that go into the save's inventory.",
        "filter_all": "All",
        "list_no_match": "No class found. Try another search or filter.",
        "lbl_items_catalog": "Game items",
        "tip_remove": "Removes the selected items (Delete)",
        "cc_label": "{name} — {skillset} (base: {base}, {n} skills)",
        "cc_preview_empty": (
            "<h2>My classes</h2>"
            "<p>Create a class with a <b>mixed skillset</b>: pick a <b>base class</b> "
            "(which you can tweak: stats, equipment, Move/Jump, evasion and innates) and build the skillset from "
            "abilities of any class in the game — up to 16 action and 6 reaction/support/movement.</p>"
            "<p>Classes marked <b>★</b> come ready-made (Red Mage, Paladin, Sage...). Click <b>New class...</b> to make your own. <b>Export...</b> creates a <b>.ramzaclass.json</b> "
            "file you can send to other people; they load it with <b>Import...</b>.</p>"
            "<p class='muted'>The mixed skillset only goes into Ramza's own skillsets, so enemies and "
            "other characters are not affected.</p>"
        ),
        "cc_preview_meta": "<p><b>Base class:</b> {base} · <b>Author:</b> {author}</p>",
        "cc_no_author": "—",
        "cc_special_warn": (
            "<b>⚠ Heads up:</b> {names} have their own mechanics (items, throwing, jumping or Arithmeticks) "
            "and may behave differently outside their original skillset. Test before your run."
        ),
        "cc_copy_name": "{name} (copy)",
        "cc_delete_title": "Delete class",
        "cc_delete_body": "Delete the class \"{name}\" from the library? The mod already applied won't change.",
        "cc_import_title": "Import classes",
        "cc_export_title": "Export class",
        "cc_file_filter": "Solo Ramza class (*.ramzaclass.json);;JSON (*.json)",
        "cc_imported": "Imported: {names}",
        "cc_pick_first": "Select a class in 'My classes' first.",
        "cc_exported": "Class exported to {path}",
        "cc_exported_body": "File saved:\n{path}\n\nSend this file to anyone who wants to use the class.",
        "cc_invalid_title": "Incomplete class",
        "cc_need_name": "Give the class a name.",
        "cc_need_skills": "Add at least one ability to the skillset.",
        "cc_err_format": "this is not a Solo Ramza Manager class file.",
        "cc_err_version": "made with a newer version of the app (format {version}). Update Solo Ramza Manager.",
        "cc_err_field": "field '{field}' is missing or invalid.",
        "cc_err_read": "could not read {name}: {error}",
        "cc_err_base": "Invalid base class (Job {job}).",
        "cc_warn_dropped": "ability {id} does not exist as {slot} in this game and was removed.",
        "cc_warn_limit": "more than {n} {slot} abilities; the extra ones were removed.",
        "cc_slot_action": "action",
        "cc_slot_rsm": "reaction/support/movement",
        "cc_new_title": "New class",
        "cc_edit_title": "Edit class",
        "cc_name": "Class name:",
        "cc_skillset": "Skillset name:",
        "cc_skillset_ph": "(same as the class name)",
        "cc_base": "Base class:",
        "cc_copy_base": "Copy base skills",
        "cc_copy_base_tip": "Adds the abilities of the base class's original skillset to the lists.",
        "cc_author": "Author:",
        "cc_desc": "Description:",
        "cc_desc_ph": "Optional. Shown in game instead of the class description.",
        "cc_base_hint": (
            "The base class is the starting point for stats, equipment, Move/Jump, evasion and innates "
            "(tweak them in the 'Stats and equipment' tab). The skillset below replaces its own. "
            "Double-click an ability to add or remove it."
        ),
        "cc_search": "Search ability, skillset or type...",
        "cc_filter_all": "All",
        "cc_up": "↑",
        "cc_down": "↓",
        "cc_actions_count": "<b>Action</b> ({n}/{max})",
        "cc_rsm_count": "<b>Reaction / Support / Movement</b> ({n}/{max})",
        "cc_full_title": "Skillset full",
        "cc_full_body": (
            "The skillset holds up to {a} action and {r} reaction/support/movement abilities. "
            "Didn't fit: {names}"
        ),
        "cc_page_skills": "Skillset",
        "cc_page_job": "Stats and equipment",
        "cc_builtin_tip": "Built-in class. Editing it creates your own copy in 'My classes'.",
        "cc_builtin_copied": "Built-in class edited: your version was saved as '{name}'.",
        "cc_builtin_no_delete": "Built-in classes (★) ship with the app and cannot be deleted.",
        "cc_save": "Save",
        "cc_cancel": "Cancel",
        "cc_box_stats": "Stats",
        "cc_col_mult": "Multiplier",
        "cc_col_growth": "Growth",
        "cc_stats_hint": (
            "Multiplier: % applied to the stat (100 = normal, higher = stronger). "
            "Growth: the <b>lower</b> it is, the more the stat rises per level."
        ),
        "cc_box_move": "Movement and evasion",
        "cc_evasion": "Evasion (C-Ev)",
        "cc_no_mev": (
            "Magic evasion is not a class stat in the game: it comes from shields, cloaks and accessories."
        ),
        "cc_box_innate": "Innate abilities (always on, outside the slots)",
        "cc_box_equip": "Allowed equipment",
        "cc_equip_weapon": "Weapons",
        "cc_equip_shield": "Shield",
        "cc_equip_head": "Head",
        "cc_equip_body": "Body",
        "cc_equip_accessory": "Accessories",
        "cc_reset_base": "Reset everything to the base class",
        "cc_base_value": "base: {value}",
        "cc_slot_innate": "innate",
        "cc_warn_equip": "unknown equipment type '{flag}' was ignored.",
        "cc_warn_range": "{field} outside {low}–{high}; adjusted.",
        "cc_changed": "<p><b>Changed from the base:</b> {names}</p>",
        "cc_field_innates": "innates",
        "cc_field_equip": "equipment",
        "wiz_checklist_title": "Status right now",
        "tab_save": "Game save",
        "page_save_desc": "Edits a manual save: Ramza's JP, Bravery and Faith, and inventory items.",
        "nav_save_caption": "EDIT SAVE",
        "nav_save_slot": "{title}",
        "nav_save_none": "Written right away, not by 'Apply'",
        "save_help": (
            "<b>How to use:</b> with the mod applied, start the game and save to a manual slot "
            "(the first save shows up after the first battle). <b>Close the game</b>, pick the slot here "
            "and write. The JP goes to Ramza's own class, which the mod replaced with the chosen class: "
            "spend it in the <i>Learn</i> menu. Skills cost the game's normal JP. "
            "Items from the <b>Starting items</b> tab are added to the inventory. "
            "The app keeps a copy of the save before writing. "
            "<i>Load the manual slot: the autosave/continue doesn't get the edit.</i>"
        ),
        "save_file_row": "File:",
        "save_not_found": "save not found — open the game and save once, or use Browse...",
        "btn_save_reload": "Reload",
        "dlg_save_file": "Pick enhanced.png",
        "save_slots": "Slots",
        "save_slot_n": "Slot {n}",
        "save_slot_line": "{title}\nRamza Lv {level} · JP {jp} · Bravery {brave} · Faith {faith}",
        "save_slot_no_ramza": "{title}\n(Ramza not found in this slot)",
        "save_no_slots": "No saved slots.",
        "save_pick_slot": "Pick a slot.",
        "save_ramza": "Ramza — level {level}",
        "save_jp": "Ramza's class JP:",
        "save_jp_tip": "JP available to learn the skills of Ramza's class (max. 9999).",
        "btn_save_jp_max": "9999",
        "save_brave": "Bravery:",
        "save_brave_tip": "Permanent Bravery (0–100): damage of fists and some weapons, reaction chance.",
        "save_faith": "Faith:",
        "save_faith_tip": "Permanent Faith (0–100): strength of spells Ramza casts and receives.",
        "btn_save_write": "Write to save",
        "save_confirm_title": "Write to save",
        "save_confirm_items": "\nItems added:\n{items}\n",
        "save_items_n": "Items: {n} kind(s) from the 'Starting items' tab will be added to the inventory.",
        "save_items_none": "Items: none (build the list on the 'Starting items' tab).",
        "save_confirm_body": (
            "Write to slot {title}?\n\nJP: {jp}\nBravery: {brave}\nFaith: {faith}\n{items}\n"
            "A copy of the original save is kept."
        ),
        "close_game_title": "Close the game",
        "close_game_body": "Close the game before writing: it rewrites the save and the edit would be lost.",
        "save_done_title": "Save written",
        "save_done_body": "Done! Open the game and load the slot.\n\nCopy of the original save:\n{backup}",
        "log_save_reading": "Reading the save...",
        "log_save_read": "{n} slot(s) read from {name}.",
        "log_save_writing": "Writing the save...",
        "log_save_written": "Slot {title} written. Backup: {backup}",
        "save_err_slot": "Slot {n} is empty.",
        "save_err_no_ramza": "Couldn't find Ramza in slot {n}.",
        "save_err_png": "The file doesn't look like a game save (.png).",
        "save_err_unpack": "Couldn't open {name} with FF16Tools.",
        "save_err_pack": "Couldn't build the new save with FF16Tools.",
        "save_err_verify": "The new save didn't match the edit; nothing was written.",
        "jp_total": "<p>Total to learn everything: <span class='jp'>{total} JP</span></p>",
        "jp_total_over": (
            "<p>Total to learn everything: <span class='jp'>{total} JP</span> — more than the save's "
            "{max} JP; the rest comes from battles.</p>"
        ),
    },
}


def get_language() -> str:
    return _language


def set_language(lang: str) -> None:
    global _language
    if lang not in LANGS:
        raise ValueError(lang)
    _language = lang


def t(key: str, **kwargs: object) -> str:
    text = STRINGS[_language].get(key) or STRINGS[LANG_PT].get(key) or key
    if kwargs:
        return text.format(**kwargs)
    return text
