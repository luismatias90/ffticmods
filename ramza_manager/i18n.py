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
        "lbl_jp": "Custo de JP das skills:",
        "tip_jp": "0 = grátis. Se o jogo não deixar aprender com 0, use 1.",
        "search_class": "Buscar classe ou skillset...",
        "chk_bag": "Trocar os itens do bônus da Deluxe Edition pela minha lista",
        "bag_help": (
            "<b>Como funciona:</b> o jogo entrega os itens do <b>bônus da Deluxe Edition</b> no inventário. "
            "Este app troca o conteúdo desse bônus pela sua lista (as cores preta/vermelha do Ramza "
            "continuam). Funciona só com a Deluxe e, em geral, vale para <b>jogo novo</b>: um save que já "
            "recebeu o bônus não recebe de novo. <i>Experimental: teste primeiro com uma lista pequena.</i>"
        ),
        "search_item": "Buscar item ou tipo (ex.: Elixir, Sword, Ring)...",
        "lbl_qty": "Quantidade:",
        "btn_add": "Adicionar →",
        "lbl_my_list": "<b>Minha lista</b>",
        "col_item": "Item",
        "col_type": "Tipo",
        "col_qty": "Qtd",
        "btn_remove": "Remover selecionado",
        "btn_clear": "Limpar",
        "btn_deluxe": "Padrão da Deluxe",
        "status_not_found": "não encontrado",
        "status_reloaded_missing": "não encontrado — instale e aponte a pasta",
        "status_installed": "instalado",
        "status_modloader_missing": "não encontrado na pasta Mods do Reloaded-II",
        "status_dotnet_needed": "necessário para ler os dados do jogo",
        "status_data_ready": "prontos",
        "status_data_missing": "clique em 'Extrair / atualizar' (uns 10 segundos)",
        "status_all_ok": "Tudo pronto: jogo, Reloaded-II, Mod Loader, .NET 9 e dados do jogo",
        "status_missing": "Falta configurar {n} item(ns) — veja abaixo",
        "mod_none": "Mod atual: <b>nenhum</b> (jogo original)",
        "mod_original_class": "original (Squire)",
        "mod_bag_count": "{n} item(ns) no bônus",
        "mod_bag_original": "bônus original",
        "mod_active": "Mod atual: Ramza = <b>{klass}</b> · Bolsa: <b>{bag}</b>",
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
            "<th>Crescimento*</th></tr>{rows}</table>"
            "<p class='muted'>* crescimento: quanto menor, mais o atributo sobe por nível.</p>"
        ),
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
        "empty_bag_title": "Lista vazia",
        "empty_bag_body": "Adicione itens na aba 'Itens iniciais', ou desmarque a troca do bônus.",
        "nothing_title": "Nada para aplicar",
        "nothing_body": (
            "Marque a troca de classe e/ou a troca dos itens. Para voltar ao jogo original, "
            "use 'Restaurar jogo original'."
        ),
        "experimental_title": "Classe experimental",
        "experimental_body": "{name} é uma classe de chefe/inimigo e pode travar o jogo.\nAplicar mesmo assim?",
        "log_building": "Gerando mod...",
        "log_applying": "Aplicando...",
        "log_installed": "Mod instalado em {path}",
        "done_title": "Mod aplicado",
        "done_intro": "Pronto!",
        "done_class": "• Ramza agora é {name}.",
        "done_bag": "• Bônus da Deluxe trocado por {n} item(ns). Comece um jogo novo para recebê-los.",
        "done_ok": "O mod já está ativado no Reloaded-II. Abra o jogo pelo Reloaded-II.",
        "done_no_app": (
            "Não achei o FFT_enhanced.exe no Reloaded-II. Adicione o jogo lá e ative os mods "
            "'{mod}' e 'FFTIVC Mod Loader'."
        ),
        "restore_need": "Aponte a pasta do Reloaded-II primeiro.",
        "log_removed": "Mod removido. Jogo original.",
        "log_not_installed": "O mod não estava instalado.",
        "restored_title": "Restaurado",
        "restored_body": "O mod foi removido: Ramza e bônus voltaram ao original.",
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
            "skills (custo de JP antes → depois), equipamentos e atributos. "
            "As três classes próprias do Ramza passam a ser essa. Ele continua no nível 1.</li>"
            "<li>O custo de JP padrão é <b>0</b>. Se o jogo não deixar aprender, mude para <b>1</b> e aplique de novo.</li>"
            "<li>Opcional, na aba <b>Itens iniciais</b>: monte a bolsa. Só vale na "
            "<b>Deluxe Edition</b> e em <b>jogo novo</b>. Teste primeiro com poucos itens.</li>"
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
        "cc_label": "{name} — {skillset} (base: {base}, {n} skills)",
        "cc_preview_empty": (
            "<h2>Minhas classes</h2>"
            "<p>Crie uma classe com um <b>skillset misto</b>: escolha uma <b>classe base</b> "
            "(que você pode ajustar: atributos, equipamentos, Move/Jump, esquiva e inatas) e monte o skillset com "
            "habilidades de qualquer classe do jogo — até 16 de ação e 6 de reação/suporte/movimento.</p>"
            "<p>Clique em <b>Nova classe...</b> para começar. Com <b>Exportar...</b> você gera um arquivo "
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
    },
    LANG_EN: {
        "window_title": "Solo Ramza Manager {version} — FFT: The Ivalice Chronicles (Enhanced)",
        "banner_subtitle": "Final Fantasy Tactics · The Ivalice Chronicles — solo Ramza run manager",
        "lang_tip": "Language of the app and the wizard",
        "tab_class": "Ramza's class",
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
        "lbl_jp": "Skill JP cost:",
        "tip_jp": "0 = free. If the game won't let you learn at 0, use 1.",
        "search_class": "Search class or skillset...",
        "chk_bag": "Replace the Deluxe Edition bonus items with my list",
        "bag_help": (
            "<b>How it works:</b> the game delivers the <b>Deluxe Edition bonus</b> items into the inventory. "
            "This app replaces that bonus with your list (Ramza's black/red colors stay). "
            "It only works with the Deluxe Edition and, in general, only on a <b>new game</b>: a save that "
            "already received the bonus will not receive it again. <i>Experimental: try a short list first.</i>"
        ),
        "search_item": "Search item or type (e.g. Elixir, Sword, Ring)...",
        "lbl_qty": "Quantity:",
        "btn_add": "Add →",
        "lbl_my_list": "<b>My list</b>",
        "col_item": "Item",
        "col_type": "Type",
        "col_qty": "Qty",
        "btn_remove": "Remove selected",
        "btn_clear": "Clear",
        "btn_deluxe": "Deluxe default",
        "status_not_found": "not found",
        "status_reloaded_missing": "not found — install it and point to the folder",
        "status_installed": "installed",
        "status_modloader_missing": "not found in the Reloaded-II Mods folder",
        "status_dotnet_needed": "required to read the game data",
        "status_data_ready": "ready",
        "status_data_missing": "click 'Extract / update' (about 10 seconds)",
        "status_all_ok": "Ready: game, Reloaded-II, Mod Loader, .NET 9 and game data",
        "status_missing": "{n} item(s) still need setup — see below",
        "mod_none": "Current mod: <b>none</b> (original game)",
        "mod_original_class": "original (Squire)",
        "mod_bag_count": "{n} item(s) in the bonus",
        "mod_bag_original": "original bonus",
        "mod_active": "Current mod: Ramza = <b>{klass}</b> · Bag: <b>{bag}</b>",
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
            "<th>Growth*</th></tr>{rows}</table>"
            "<p class='muted'>* growth: the lower the number, the more the stat rises per level.</p>"
        ),
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
        "empty_bag_title": "Empty list",
        "empty_bag_body": "Add items on the 'Starting items' tab, or uncheck the bonus swap.",
        "nothing_title": "Nothing to apply",
        "nothing_body": (
            "Check the class change and/or the item swap. To go back to the original game, "
            "use 'Restore the original game'."
        ),
        "experimental_title": "Experimental class",
        "experimental_body": "{name} is a boss/enemy class and may freeze the game.\nApply anyway?",
        "log_building": "Building mod...",
        "log_applying": "Applying...",
        "log_installed": "Mod installed at {path}",
        "done_title": "Mod applied",
        "done_intro": "Done!",
        "done_class": "• Ramza is now {name}.",
        "done_bag": "• Deluxe bonus replaced with {n} item(s). Start a new game to receive them.",
        "done_ok": "The mod is already enabled in Reloaded-II. Launch the game from Reloaded-II.",
        "done_no_app": (
            "FFT_enhanced.exe is not in Reloaded-II. Add the game there and enable "
            "'{mod}' and 'FFTIVC Mod Loader'."
        ),
        "restore_need": "Point to the Reloaded-II folder first.",
        "log_removed": "Mod removed. Original game.",
        "log_not_installed": "The mod was not installed.",
        "restored_title": "Restored",
        "restored_body": "The mod was removed: Ramza and the bonus are back to the original.",
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
            "skills (JP cost before → after), equipment and stats. "
            "Ramza's three own classes become that class. He still starts at level 1.</li>"
            "<li>The default JP cost is <b>0</b>. If the game won't let you learn, set it to <b>1</b> and apply again.</li>"
            "<li>Optional, on the <b>Starting items</b> tab: build the bag. This only works with the "
            "<b>Deluxe Edition</b> and a <b>new game</b>. Try a short list first.</li>"
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
        "cc_label": "{name} — {skillset} (base: {base}, {n} skills)",
        "cc_preview_empty": (
            "<h2>My classes</h2>"
            "<p>Create a class with a <b>mixed skillset</b>: pick a <b>base class</b> "
            "(which you can tweak: stats, equipment, Move/Jump, evasion and innates) and build the skillset from "
            "abilities of any class in the game — up to 16 action and 6 reaction/support/movement.</p>"
            "<p>Click <b>New class...</b> to start. <b>Export...</b> creates a <b>.ramzaclass.json</b> "
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
