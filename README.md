# Solo Ramza Manager

Swaps Ramza's class in **FINAL FANTASY TACTICS - The Ivalice Chronicles (Enhanced version)** for any class in the game: generic, unique-character, or boss/enemy. It can also use a custom class with a mixed skillset. Skills keep their normal JP cost, and the app edits your save so Ramza gets 9999 JP (plus whatever Bravery, Faith and starting items you want). Built for solo Ramza runs.

**Ready-to-run app:** `dist\SoloRamzaManager\SoloRamzaManager.exe`. On another PC, clone the repository (or download the ZIP from GitHub) and run that `.exe`. It needs the `_internal` folder next to it, so copy the whole `SoloRamzaManager` folder, not just the `.exe`. Python is not required, only the **.NET 9 Runtime** (see below).

## What changes and what doesn't

**Changes (Ramza only):**
- Ramza's three own classes (Squire in Ch. 1, Squire in Ch. 2–3, and Gallant Knight in Ch. 4) become the chosen class. That includes skillset, equipment, stat multipliers and growth, Move/Jump, evasion, innate abilities and the menu name.
- Skillset abilities (action, reaction, support and movement) keep the game's original JP cost. To buy them right away, give Ramza 9999 JP from the **Game save** tab (see below).
- If the class can't use Ramza's starting equipment, it is swapped for a basic compatible item (e.g. Broadsword → Rod for Black Mage).
- Optional: Ramza's battle sprite (chapters 1, 2–3 and 4) becomes another human character's or a generic class's sprite. The mod replaces the classic sheet and the HD sheet the Enhanced mode draws (`system/ffto/g2d/tex_830.bin` to `tex_835.bin`), plus Ramza's colors in the `CharCLUT` table, which Enhanced uses instead of the sheet's palette. The menu portrait changes too (`ui/ffto/common/face`), except for Lettie and most villagers, who have no portrait of their own and keep Ramza's. Some event scenes may still show the original Ramza.

**Doesn't change:**
- Level, EXP and base stats: Ramza starts at level 1 and levels up normally.
- Skill JP costs, for Ramza or for any other unit.
- Ramza's *Traitor* immunity, the story, enemies and other characters.
- The game files. Everything is applied through a Reloaded-II mod, and *Restore the original game* undoes it.

## Prerequisites (one time only)

1. **.NET 9 Runtime** (needed to read the game data): https://dotnet.microsoft.com/download/dotnet/9.0
2. **Reloaded-II**: https://github.com/Reloaded-Project/Reloaded-II/releases/latest
   - Extract it to a folder (e.g. `C:\Reloaded-II`) and open `Reloaded-II.exe`.
   - Click **+ (Add an Application)** and pick `FFT_enhanced.exe` in the game folder.
3. **FFTIVC Mod Loader** (`fftivc.utility.modloader`): in Reloaded-II, search for "fftivc" under *Download Mods*, or download it from https://github.com/Nenkai/fftivc.utility.modloader/releases/latest
4. Launch the game once through Steam so the save folders get created.

## How to use

On first launch, a wizard asks whether the interface should be in **English** or **Portuguese** and walks you through what to install and how to set it up. You can reopen it with the **Wizard** button and switch languages at any time from the corner of the window (PT-BR / EN).

The window has a sidebar with four steps: **Ramza's class**, **Ramza's sprite**, **Starting items** and **Game save** (`Ctrl+1` to `Ctrl+4`). The *What will change* card shows what will be applied, and the *Installed now* card shows what is already in the game.

1. **Close Reloaded-II** and open `SoloRamzaManager.exe`.
2. Check the **Setup** panel. The game and Reloaded-II are detected automatically; if not, use *Browse...*
3. Click **Extract / update** (takes about 10 seconds and only reads the game). Repeat after game updates.
4. Pick a class under **Generic**, **Unique characters**, **Bosses / Enemies ⚠** or **✦ My classes**. The right panel shows the skills with their JP cost (and the total to learn everything), equipment and stats.
5. Optional: pick another battle sprite in **Ramza's sprite**.
6. Click **Apply to the game** (`Ctrl+Enter`). The mod is installed and enabled in the `FFT_enhanced.exe` profile.
7. Launch the game **through Reloaded-II**, start a new game and save to a manual slot.
8. Close the game and, in the **Game save** tab, give Ramza 9999 JP (see below).

To switch classes, pick another one and apply again. **Restore the original game** removes the mod.

### Stat simulator

The class preview has a *Simulate stats at level* field. Type a level (1–99) and the stats table shows the HP, MP, Speed, PA and MA Ramza would have with that class, computed from the class multiplier and growth. HP/MP are shown as a range because the starting value is random.

## Custom classes (mixed skillset)

The **✦ My classes** tab comes with 7 built-in classes, marked with ★:

| Class | Base | Idea |
|---|---|---|
| Red Mage | Black Mage | Basic white and black magic, with sword and light shield |
| Mystic Knight | Knight | Spellblade (status blades) and elemental spells |
| Paladin | Knight | Holy Sword and healing |
| Dark Knight | Knight | Fell Sword, drains and *sap*; more HP/PA, less evasion |
| Sage | White Mage | Advanced white and black magic, high MA, fragile body |
| Ranger | Archer | Aim and Aimed Shot, with bow, crossbow and gun, Move 4 |
| Battle Monk | Monk | Martial arts plus Ramza's battle shouts |

Built-in classes can't be deleted. Editing one saves a copy of your own. They live in `data/classes/` and are generated by `packaging/make_presets.py`.

The `biblioteca_classes` folder has 11 more ready-made classes to bring in with **Import...**: Alchemist, Arcane Archer, Druid, Freelancer, Glass Cannon, Rogue, Shogun, Time Knight, Troubadour, Warlock and White Monk. `index.json` summarizes each one.

You can also create your own class:

1. **New class...** (`Ctrl+N`) opens the editor. Name the class and the skillset, and pick the **base class**, which sets stats, equipment, Move/Jump, evasion and innate abilities.
2. Build the skillset from abilities of **any class** in the game: up to **16 action** abilities and **6 reaction/support/movement** abilities each. Search accepts name, skillset or type, and *Copy base skills* gives you a starting point.
3. In the editor's **Stats and equipment** page, adjust anything you want relative to the base class:
   - HP, MP, Speed, PA and MA **multiplier** and **growth**;
   - **Move**, **Jump** and **class evasion (C-Ev)**;
   - up to 4 **innate abilities** (always active, outside the slots);
   - **allowed equipment** (weapons, shield, head, body, accessories).

   Anything you leave alone matches the base class, and follows the new base if you change it. Magic evasion isn't listed because in the game it doesn't belong to the class: it comes from shields, cloaks and accessories.
4. Select the class in the list and click **Apply to the game**, as with a normal class. Ramza's starting equipment is swapped if the class can't use it.

The mixed skillset goes into Ramza's own skillsets (Mettle, ids 25–27), which only he uses. Enemies and other characters are unaffected. Each ability costs the JP it has in the game.

**Sharing:** **Export...** creates a `.ramzaclass.json` file (a few KB) you can post on Discord, forums, etc. The recipient uses **Import...**. The file is validated on import: abilities that don't exist or are in the wrong slot are dropped with a warning, and an invalid base class is rejected. Your library is stored in `%LOCALAPPDATA%\SoloRamzaManager\classes`.

> Item, Throw, Jump and Arithmeticks abilities have their own mechanics and may behave differently outside their original skillset. The editor warns you when they are in the list. Test before your run.

## Game save: JP, Bravery, Faith and items

The game has no starting-JP table, so JP comes from a save edit. The **Game save** tab opens `enhanced.png` (in `Documents\My Games\FINAL FANTASY TACTICS - The Ivalice Chronicles\Steam\<id>\`), lists the manual slots, and shows Ramza's level, JP, Bravery and Faith in each one. Items from the **Starting items** tab are written here too (see below).

1. With the mod applied, start the game and save to a manual slot. The first save is available after the first battle.
2. **Close the game.** It rewrites the save on exit and would undo the edit. The app refuses to write while the game is running.
3. In the **Game save** tab, pick the slot, click **9999** (or type the JP), set **Bravery** and **Faith** (0–100) and click **Write to save**.
4. Open the game and load that slot. The autosave (*Continue*) doesn't get the edit.

The JP goes to Ramza's own class, the one the mod replaced with your chosen class, and shows up in the *Learn* menu. 9999 is the game's maximum. Some classes cost more than that to learn everything (Summoner, Time Mage, Assassin…), and the preview warns you when that's the case. The rest comes from battles.

Before writing, the app keeps a copy of the save in `%LOCALAPPDATA%\SoloRamzaManager\save_backups`. To roll back, copy the backup over `enhanced.png` (renaming it). The new save is reopened and checked before it replaces the original, and the PNG thumbnail is kept.

## Starting items

In the **Starting items** tab you build the list of items you want: search any item (weapons, armor, accessories, consumables), pick the quantity (1–99) and click **Add →**. Tick **Add these items to the inventory when writing the save**.

The items go into the save along with the JP: in the **Game save** tab, pick the slot and click **Write to save**. The confirmation shows each item with its current → new quantity. Because of that:
- it works with any edition (no Deluxe needed) and any save, not only a new game;
- quantities are **added** to what the slot already has, up to 99 of each item;
- writing again adds again. To write only JP, Bravery and Faith, untick the box in the **Starting items** tab.

### First in-game test
- New game → Orbonne battle: Ramza should show up at level 1 with the class name and skillset.
- Formation menu → *Learn*: the class skills should show up with their normal JP cost.
- Save, close the game, write 9999 JP from the **Game save** tab and load the slot: Ramza should have 9999 JP to spend.

### Boss/enemy classes (⚠)
Lucavi, Ultima Demon and similar classes use animations made for other sprites and may freeze with Ramza's sprite. **Save before testing.** Monsters aren't listed, because Ramza would end up with no menus or equipment.

## Development

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install PySide6 pyinstaller pytest
.\.venv\Scripts\python SoloRamzaManager.pyw        # run
.\.venv\Scripts\python -m pytest                   # tests
.\.venv\Scripts\pyinstaller packaging\SoloRamzaManager.spec --noconfirm --clean   # builds dist\SoloRamzaManager\
```

Release builds take a few extra steps to keep antivirus false positives and Nexus Mods quarantine away:

- **Build from PowerShell, not Git Bash.** Git Bash puts `C:\Program Files\Git\mingw64\bin` on the PATH, and PyInstaller then bundles Git's OpenSSL DLLs (`libcrypto-3-x64.dll`, `libssl-3-x64.dll`) next to Python's.
- **Compile PyInstaller's bootloader from source** instead of using the prebuilt one from PyPI, which many antivirus heuristics flag. With a portable [MinGW-w64](https://winlibs.com/) on the PATH:

  ```powershell
  $venv = (Resolve-Path .venv).Path
  & $venv\Scripts\pip download --no-binary :all: --no-deps pyinstaller==6.22.3 -d $env:TEMP
  tar xzf $env:TEMP\pyinstaller-6.22.3.tar.gz -C $env:TEMP
  Push-Location $env:TEMP\pyinstaller-6.22.3\bootloader
  & $venv\Scripts\python ./waf distclean all --target-arch=64bit --gcc
  cd ..; & $venv\Scripts\pip install --force-reinstall --no-deps .
  Pop-Location
  ```

  Recreating the venv with a plain `pip install pyinstaller` brings the prebuilt bootloader back.
- The spec builds with `noarchive=True`, so there's no `base_library.zip` inside the package (Nexus Mods rejects archives nested in an upload), and it stamps the `.exe` with version info taken from `ramza_manager/__init__.py`.

Layout:
- `ramza_manager/app.py`: main window (PySide6).
- `ramza_manager/wizard.py`: first-run setup wizard.
- `ramza_manager/theme.py`: the *Ivalice Chronicles*-style menu theme.
- `ramza_manager/i18n.py`: Portuguese and English UI strings.
- `ramza_manager/mod_builder.py`: computes and generates the mod (JobData/JobCommandData/AbilityData/SpawnData XML + ModConfig).
- `ramza_manager/nxd_db.py`: extracts the game's nex tables (`ability`, `job`, `jobcommand`) to SQLite and generates the edited `.nxd` files (class name and skillset).
- `ramza_manager/sprites.py`: battle sprite, `CharCLUT` colors and portrait swap.
- `ramza_manager/save_edit.py`: reads and writes Ramza's JP, Bravery, Faith and the inventory in the save (`enhanced.png`); the `fftsave.bin` layout is documented at the top.
- `ramza_manager/stat_sim.py`: stat-by-level simulator.
- `ramza_manager/class_catalog.py`: which classes are listed and under which tab.
- `ramza_manager/custom_class.py`: `.ramzaclass.json` format, validation and custom class library.
- `ramza_manager/class_editor.py`: custom class editor (PySide6).
- `ramza_manager/ff16tools.py`, `reloaded.py`, `game_install.py`, `prereqs.py`: FF16Tools wrapper, Reloaded-II profile, game detection and prerequisite checks.
- `data/`: reference XML tables from the original game, plus the built-in classes in `data/classes/`.
- `biblioteca_classes/`: extra classes to import.
- `tools/FF16Tools/`: FF16Tools.CLI (Nenkai, MIT).

Extracted data, settings, the class library and save backups live in `%LOCALAPPDATA%\SoloRamzaManager`.

See `CHANGELOG.md` for version history.

## Credits and license

- Parts of the code and the reference tables come from **The Ivalice Chronicles Mod Studio** (GPL-3). Because of that, this project is also **GPL-3** (see `LICENSE`).
- **FF16Tools** and **fftivc.utility.modloader**, by Nenkai.
- **Reloaded-II**, by Sewer56.
