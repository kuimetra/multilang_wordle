import customtkinter as ctk
import datetime
import random

app = ctk.CTk()
app.title("Wordle")
app.geometry("420x552")
app.minsize(420, 592)

FONT_13 = ctk.CTkFont(family="Helvetica Neue", size=13)
FONT_15 = ctk.CTkFont(family="Helvetica Neue", size=15)
FONT_16_BOLD = ctk.CTkFont(family="Helvetica Neue", size=16, weight="bold")
FONT_18_BOLD = ctk.CTkFont(family="Helvetica Neue", size=18, weight="bold")
FONT_20_BOLD = ctk.CTkFont(family="Helvetica Neue", size=20, weight="bold")
FONT_30_BOLD = ctk.CTkFont(family="Helvetica Neue", size=30, weight="bold")

ROWS = 6
COLS = 5

BASE_THEMES = {
    "Classic Dark": {
        "BASE": "dark",
        "APP_BG": "#1A1A1A",
        "BOARD_BG": "#2B2B2B",
        "BOARD_TILE": "#121213",
        "TEXT": "#DEE3ED",
        "BUTTON": "#575B5E",
        "BUTTON_HOVER": "#3A3D40",
        "DROPDOWN": "#2B2B2B",
        "WRONG": "#3A3A3C",
        "MISPLACED": "#B2A04C",
        "CORRECT": "#618C55",

        # Keyboard colours
        "KEY": "#818283",
        "HOVER_KEY": "#5A5B5E",

        "GREEN": "#4A7A4C",
        "GREEN_HOVER": "#2B5A2B",
        "RED": "#A94444",
        "RED_HOVER": "#6C2B2B",

        "MESSAGE_BUTTONS": {
            "info": ("#4A90E2", "#357ABD"),
            "warning": ("#E5943A", "#C67C28"),
            "success": ("#7A5AF8", "#6243D6"),
            "confirm_yes": ("#4A7A4C", "#2B5A2B"),
            "confirm_no": ("#A94444", "#6C2B2B"),
        }
    },
    "Classic Light": {
        "BASE": "light",
        "APP_BG": "#FFFFFF",
        "BOARD_BG": "#D4D6DA",
        "BOARD_TILE": "#FFFFFF",
        "TEXT": "#1A1A1A",
        "BUTTON": "#E0E0E0",
        "BUTTON_HOVER": "#C6C6C6",
        "DROPDOWN": "#FFFFFF",
        "WRONG": "#797C7E",
        "MISPLACED": "#C6B566",
        "CORRECT": "#79A96B",

        "KEY": "#E5E5E5",
        "HOVER_KEY": "#CFCFCF",

        "GREEN": "#33A455",
        "GREEN_HOVER": "#22863A",
        "RED": "#C85A5A",
        "RED_HOVER": "#B94A4A",

        "MESSAGE_BUTTONS": {
            "info": ("#3B82F6", "#2563EB"),
            "warning": ("#F59E0B", "#D97706"),
            "success": ("#8B5CF6", "#7C3AED"),
            "confirm_yes": ("#33A455", "#22863A"),
            "confirm_no": ("#C85A5A", "#B94A4A"),
        }
    }
}

THEME_VARIANTS = {
    "High Contrast Dark": {
        "base": "Classic Dark",
        "overrides": {
            "MISPLACED": "#92BFF4",
            "CORRECT": "#E5804A",
        },
        "TEXT_OVERRIDE": {
            "typed": None,
            "submitted": {
                "wrong": None,
                "misplaced": "#1A1A1A",
                "correct": "#1A1A1A"
            }
        }
    },
    "High Contrast Light": {
        "base": "Classic Light",
        "overrides": {
            "MISPLACED": "#92BFF4",
            "CORRECT": "#E5804A",
        },
        "TEXT_OVERRIDE": {
            "typed": None,
            "submitted": {
                "wrong": "#FFFFFF",
                "misplaced": None,
                "correct": None
            }
        }
    },
    "Midnight Blue & Rose": {
        "base": "Classic Dark",
        "overrides": {
            "MISPLACED": "#275495",
            "CORRECT": "#CB5677",
        },
        "TEXT_OVERRIDE": {}
    },
    "Blush & Teal": {
        "base": "Classic Light",
        "overrides": {
            "MISPLACED": "#E194A0",
            "CORRECT": "#3A848D",
        },
        "TEXT_OVERRIDE": {}
    },
}


def build_themes(base_themes, variants):
    """
    Builds the complete themes dictionary by applying variants to base themes.

    Parameters:
    - base_themes: Dictionary of base themes.
    - variants: Dictionary of theme variants.

    Returns:
    - Dictionary of complete themes.
    """
    complete_themes = {name: data.copy() for name, data in base_themes.items()}

    for name, spec in variants.items():
        base = base_themes[spec["base"]].copy()
        base.update(spec["overrides"])
        if "TEXT_OVERRIDE" in spec:
            base["TEXT_OVERRIDE"] = spec["TEXT_OVERRIDE"]
        complete_themes[name] = base

    return complete_themes


themes = build_themes(BASE_THEMES, THEME_VARIANTS)
current_theme = "Classic Dark"

COLOR_APP_BG = themes[current_theme]["APP_BG"]
COLOR_BOARD_BG = themes[current_theme]["BOARD_BG"]
COLOR_BOARD_TILE = themes[current_theme]["BOARD_TILE"]
COLOR_TEXT = themes[current_theme]["TEXT"]
COLOR_BUTTON = themes[current_theme]["BUTTON"]
COLOR_BUTTON_HOVER = themes[current_theme]["BUTTON_HOVER"]
COLOR_DROPDOWN = themes[current_theme]["DROPDOWN"]
COLOR_WRONG = themes[current_theme]["WRONG"]
COLOR_MISPLACED = themes[current_theme]["MISPLACED"]
COLOR_CORRECT = themes[current_theme]["CORRECT"]

COLOR_KEY = themes[current_theme]["KEY"]
COLOR_HOVER_KEY = themes[current_theme]["HOVER_KEY"]

COLOR_GREEN = themes[current_theme]["GREEN"]
COLOR_GREEN_HOVER = themes[current_theme]["GREEN_HOVER"]
COLOR_RED = themes[current_theme]["RED"]
COLOR_RED_HOVER = themes[current_theme]["RED_HOVER"]

current_row = 0
current_col = 0
game_over = False

dict_folder = "dictionaries"
lang_files = {
    "English": f"{dict_folder}/english.csv",
    "Norwegian": f"{dict_folder}/norwegian.csv",
    "Ukrainian": f"{dict_folder}/ukrainian.csv"
}
language_alphabets = {
    "English": set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "Norwegian": set("ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"),
    "Ukrainian": set("АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ")
}

priority = {
    "wrong": 1,
    "misplaced": 2,
    "correct": 3,
}
tile_states = [[None for _ in range(COLS)] for _ in range(ROWS)]

app.configure(fg_color=COLOR_APP_BG)

tiles = []
keyboard_window = None
keyboard_frames = []
info_window = None
info_frames = []
keyboard_state = {}
keyboard_buttons = {}
previous_guesses = set()

MESSAGE_BUTTON_SPECS = {
    "info": "OK",
    "warning": "Retry",
    "success": "Yay!",
}


def show_message(title, message, message_type="info"):
    """
    Shows a message popup.

    Parameters:
    - title: Title of the popup window.
    - message: Message text to display.
    - message_type: Type of message. One of "info", "warning", "success", "confirm".

    Returns:
    - For "confirm" type, returns True if user clicked Yes, False if No.
    - For other types, returns None.
    """
    win = ctk.CTkToplevel()
    win.title(title)
    win.geometry("280x136")
    win.resizable(False, False)
    win.configure(fg_color=COLOR_APP_BG)

    ctk.CTkLabel(win, text=message, text_color=COLOR_TEXT, font=FONT_15, justify="center", wraplength=230,
                 height=54).pack(pady=(25, 7))

    if message_type == "confirm":
        result = False

        def set_result(value):
            nonlocal result
            result = value
            win.destroy()

        frame = ctk.CTkFrame(win, fg_color=COLOR_APP_BG)
        frame.pack()

        yes_fg, yes_hover = get_message_button_colors("confirm_yes")
        no_fg, no_hover = get_message_button_colors("confirm_no")

        ctk.CTkButton(frame, text="Yes", width=75, height=30, text_color="#FFFFFF", fg_color=yes_fg,
                      hover_color=yes_hover, border_color=yes_hover, border_width=2,
                      font=FONT_13, command=lambda: set_result(True)).pack(side="left", padx=(0, 20))

        ctk.CTkButton(frame, text="No", width=75, height=30, text_color="#FFFFFF", fg_color=no_fg,
                      hover_color=no_hover, border_color=no_hover, border_width=2, font=FONT_13,
                      command=lambda: set_result(False)).pack(side="right")

        win.grab_set()
        win.wait_window()
        return result
    else:
        text = MESSAGE_BUTTON_SPECS[message_type]
        fg, hover = get_message_button_colors(message_type)

        ctk.CTkButton(win, text=text, width=75, height=30, text_color="#FFFFFF", fg_color=fg, hover_color=hover,
                      border_color=hover, border_width=2, font=FONT_13, command=win.destroy).pack()

    win.bind("<Return>", lambda e: win.destroy())
    win.grab_set()
    win.wait_window()


def load_words(language):
    """
    Loads the word list for the specified language.

    Parameters:
    - language: Language name as a string.

    Returns:
    - List of words in uppercase.
    """
    file_path = lang_files[language]
    words = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            words.append(line.strip().upper())
    return words


def get_todays_word(words):
    """
    Selects today's word deterministically based on the current date.

    Parameters:
    - words: List of possible words.

    Returns:
    - The selected word as a string.
    """
    today = datetime.date.today()
    seed = int(today.strftime("%Y%m%d"))
    random.seed(seed)
    return random.choice(words)


def create_grid(parent):
    """
    Creates the grid of tiles for the word game.

    Parameters:
    - parent: The parent tkinter widget where the grid will be placed.
    """
    for r in range(ROWS):
        row_tiles = []
        for c in range(COLS):
            # horizontal padding
            if c == 0:
                pad_x = (10, 5)  # left edge
            elif c == COLS - 1:
                pad_x = (5, 10)  # right edge
            else:
                pad_x = (5, 5)  # middle tiles

            # vertical padding
            if r == 0:
                pad_y = (10, 5)  # top edge
            elif r == ROWS - 1:
                pad_y = (5, 10)  # bottom edge
            else:
                pad_y = (5, 5)  # middle tiles

            tile = ctk.CTkLabel(parent, text="", width=60, height=60, corner_radius=5, fg_color=COLOR_BOARD_TILE,
                                font=FONT_30_BOLD, justify="center")
            tile.grid(row=r, column=c, padx=pad_x, pady=pad_y)

            row_tiles.append(tile)
        tiles.append(row_tiles)


def create_letter_key(parent, ch):
    """
    Creates a letter key button on the on-screen keyboard.

    Parameters:
    - parent: The parent tkinter widget where the key will be placed.
    - ch: The character for the key as a string.
    """
    key = ctk.CTkButton(parent, text=ch, width=34, height=36, text_color=get_text_color(None), fg_color=COLOR_KEY,
                        hover_color=COLOR_HOVER_KEY, corner_radius=5, font=FONT_18_BOLD,
                        command=lambda c=ch: type_letter(c))
    key.pack(side="left", padx=2)
    keyboard_buttons[ch] = key


def open_keyboard():
    """
    Opens the on-screen keyboard in a new window.
    """
    global keyboard_window
    keyboard_buttons.clear()

    if keyboard_window is not None and keyboard_window.winfo_exists():
        keyboard_window.lift()
        return

    lang = lang_box.get()

    layouts = {
        "English": (["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"], 420),
        "Norwegian": (["QWERTYUIOPÅ", "ASDFGHJKLØÆ", "ZXCVBNM"], 458),
        "Ukrainian": (["ЙЦУКЕНГШЩЗХЇ", "ФІВАПРОЛДЖЄ", "ЯЧСМИТЬБЮ"], 496),
    }

    rows, window_width = layouts.get(lang, layouts["English"])

    keyboard_window = ctk.CTkToplevel()
    keyboard_window.title("Keyboard")
    keyboard_window.geometry(f"{window_width}x140")
    keyboard_window.resizable(False, False)
    keyboard_window.configure(fg_color=COLOR_APP_BG)

    container = ctk.CTkFrame(keyboard_window, fg_color=COLOR_APP_BG)
    container.pack(expand=True)

    keyboard_frames.clear()
    keyboard_frames.extend([keyboard_window, container])

    row1 = ctk.CTkFrame(container, fg_color=COLOR_APP_BG)
    row1.pack(pady=2)
    for ch in rows[0]:
        create_letter_key(row1, ch)

    row2 = ctk.CTkFrame(container, fg_color=COLOR_APP_BG)
    row2.pack(pady=2)
    for ch in rows[1]:
        create_letter_key(row2, ch)

    row3 = ctk.CTkFrame(container, fg_color=COLOR_APP_BG)
    row3.pack(pady=2)

    # ENTER
    enter_btn = ctk.CTkButton(row3, text="⏎", width=53, height=36, text_color=COLOR_TEXT, fg_color=COLOR_GREEN,
                              hover_color=COLOR_GREEN_HOVER, corner_radius=5, font=FONT_16_BOLD,
                              command=submit_word)
    enter_btn.pack(side="left", padx=3)
    keyboard_buttons["⏎"] = enter_btn

    for ch in rows[2]:
        create_letter_key(row3, ch)

    # DELETE
    delete_btn = ctk.CTkButton(row3, text="⌫", width=53, height=36, text_color=COLOR_TEXT, fg_color=COLOR_RED,
                               hover_color=COLOR_RED_HOVER, corner_radius=5, font=FONT_16_BOLD,
                               command=delete_letter)
    delete_btn.pack(side="left", padx=3)
    keyboard_buttons["⌫"] = delete_btn

    keyboard_frames.extend([row1, row2, row3])

    # Refresh colors according to current theme
    refresh_keyboard_colors()


def refresh_keyboard_colors():
    """
    Refreshes the colors of the keyboard buttons.
    """
    for w in keyboard_frames:
        if w and w.winfo_exists():
            w.configure(fg_color=COLOR_APP_BG)

    for letter, btn in keyboard_buttons.items():
        if btn and btn.winfo_exists():
            state = keyboard_state.get(letter)
            if letter == "⏎":  # Enter key
                btn.configure(fg_color=COLOR_GREEN, hover_color=COLOR_GREEN_HOVER, text_color=COLOR_TEXT)
            elif letter == "⌫":  # Delete key
                btn.configure(fg_color=COLOR_RED, hover_color=COLOR_RED_HOVER, text_color=COLOR_TEXT)
            else:
                btn.configure(fg_color=get_key_fg_color(state), text_color=get_text_color(state))


def type_letter(letter):
    """
    Types a letter into the current tile.
    If the current row is full or the game is over, does nothing.

    Parameters:
    - letter: The letter to type as a string.
    """
    global current_row, current_col, game_over
    if game_over or current_row >= ROWS:
        return

    if current_col < COLS:
        tiles[current_row][current_col].configure(text=letter.upper(), text_color=get_text_color(None))
        current_col += 1


def delete_letter():
    """
    Deletes the last typed letter in the current row.
    If there are no letters to delete or the game is over, does nothing.
    """
    global current_row, current_col, game_over
    if game_over:
        return

    if current_col > 0:
        current_col -= 1
        tiles[current_row][current_col].configure(text="", text_color=get_text_color(None))


def submit_word():
    """
    Submits the current word guess for evaluation.
    If the word is incomplete, invalid, or the game is over, shows appropriate messages.
    """
    global current_row, current_col, game_over
    if game_over:
        return

    if current_col < COLS:
        show_message("Not Enough Letters", "Please complete the word before submitting.", message_type="warning")
        return

    guess = "".join(tile.cget("text") for tile in tiles[current_row])

    # Validate letters belong to selected language
    allowed = language_alphabets[current_language]

    word_letters = set(guess)

    if not word_letters.issubset(allowed):
        show_message("Invalid Letters", f"The word contains letters not in the {current_language} alphabet.",
                     message_type="warning")
        return

    # Check if word exists in dictionary
    if guess not in valid_words:
        show_message("Invalid Word", f'{guess} is not in the word list.', message_type="warning")
        return

    # Check if word was already guessed
    if guess in previous_guesses:
        show_message("Already Guessed", f'You have already submitted the word {guess}.\n'
                                        f'Please try a different word.', message_type="warning")
        return

    previous_guesses.add(guess)

    evaluate_guess(guess)

    if guess == secret_word.upper():
        num_guesses = len(previous_guesses)
        # Depending on number of guesses, show different messages
        if num_guesses == 1:
            msg = "Splendid! You got it on the first try!"
        elif num_guesses <= 3:
            msg = "Amazing! You solved it quickly!"
        elif num_guesses <= 6:
            msg = "Great job! You guessed the word!"

        show_message("Congratulations!", msg, message_type="success")
        disable_game()
        return

    current_row += 1
    current_col = 0

    # If player used all rows
    if current_row >= ROWS:
        show_message("Game Over", f'The word was {secret_word}.\nGreat effort! Try again tomorrow!',
                     message_type="info")
        disable_game()


def disable_game():
    """
    Disables further input to the game after it has ended.
    """
    global game_over
    game_over = True

    # Unbind keyboard input
    app.unbind("<Key>")


def get_state_color(state):
    """
    Maps a semantic state to its color.
    Returns None if the state is not evaluated yet.
    """
    if state == "correct":
        return COLOR_CORRECT
    elif state == "misplaced":
        return COLOR_MISPLACED
    elif state == "wrong":
        return COLOR_WRONG
    return None


def get_tile_fg_color(state):
    """
    Returns the background color for a board tile.
    """
    return get_state_color(state) or COLOR_BOARD_TILE


def get_key_fg_color(state):
    """
    Returns the background color for a keyboard key.
    """
    return get_state_color(state) or COLOR_KEY


def get_text_color(state):
    """
    Returns the text color based on the current theme and tile state.

    Parameters:
    - state: The state of the tile ("correct", "misplaced", "wrong") or None if not submitted.

    Returns:
    - The text color as a hex string.
    """
    theme_data = themes[current_theme]
    base = theme_data["BASE"]
    override = theme_data.get("TEXT_OVERRIDE", {})

    # typed but not submitted
    if state is None:
        typed_override = override.get("typed")
        if typed_override is None:
            return COLOR_TEXT
        return typed_override

    # submitted tiles
    submitted_override = override.get("submitted")
    if submitted_override:
        if isinstance(submitted_override, dict):  # per-state
            color = submitted_override.get(state)
            return COLOR_TEXT if color is None else color
        else:
            return COLOR_TEXT if submitted_override is None else submitted_override

    # default rules
    if base == "light":
        return "#FFFFFF"
    return COLOR_TEXT


def get_message_button_colors(kind):
    return themes[current_theme]["MESSAGE_BUTTONS"][kind]


def evaluate_guess(guess):
    """
    Evaluates the guessed word against the secret word and updates tile colors accordingly.

    Parameters:
    - guess: The guessed word as a string.
    """
    guess = guess.upper()
    secret = secret_word.upper()

    # 1 = wrong, 2 = misplaced, 3 = correct
    # correct positions
    result = [1] * COLS  # initially all wrong
    secret_list = list(secret)

    for i, ch in enumerate(guess):
        if ch == secret[i]:
            result[i] = 3  # correct
            secret_list[i] = None

    # misplaced positions
    for i, ch in enumerate(guess):
        if result[i] == 3:  # correct
            continue
        if ch in secret_list:
            result[i] = 2  # misplaced
            secret_list[secret_list.index(ch)] = None

    # update tile colors and keyboard
    for i, ch in enumerate(guess):
        if result[i] == 3:
            state = "correct"
        elif result[i] == 2:
            state = "misplaced"
        else:
            state = "wrong"

        tile_states[current_row][i] = state
        tiles[current_row][i].configure(fg_color=get_tile_fg_color(state), text_color=get_text_color(state))

        update_keyboard_key(ch, state)


def update_keyboard_key(letter, new_state):
    """
    Updates the color of a keyboard key based on the new state.

    Parameters:
    - letter: The letter on the keyboard key as a string.
    - new_state: The new state of the letter ("correct", "misplaced", "wrong").
    """
    old_state = keyboard_state.get(letter)

    if old_state and priority[old_state] >= priority[new_state]:
        return

    keyboard_state[letter] = new_state

    btn = keyboard_buttons.get(letter)
    if btn and btn.winfo_exists():
        btn.configure(fg_color=get_key_fg_color(new_state), text_color=get_text_color(new_state))


def on_key(event):
    """
    Handles key press events for typing letters, deleting, and submitting words.

    Parameters:
    - event: The key press event.
    """
    char = event.char.upper()

    if char == "ʼ":  # no words with apostrophes
        return

    if char.isalpha() and len(char) == 1:
        type_letter(char)

    elif event.keysym == "BackSpace":
        delete_letter()

    elif event.keysym == "Return":
        submit_word()


def reset_grid():
    """
    Resets the word grid to its initial empty state.
    """
    global current_row, current_col

    previous_guesses.clear()
    keyboard_state.clear()

    for r in range(ROWS):
        for c in range(COLS):
            tile_states[r][c] = None
            tiles[r][c].configure(text="", fg_color=COLOR_BOARD_TILE)

    for letter, btn in keyboard_buttons.items():
        if btn and btn.winfo_exists():
            btn.configure(fg_color=COLOR_KEY, text_color=get_text_color(None))

    current_row = 0
    current_col = 0


def on_language_change(choice):
    """
    Handles the event when the language selection is changed.
    Resets the game state and prompts the user if there are existing guesses.

    Parameters:
    - choice: The newly selected language as a string.
    """
    global current_language, valid_words, secret_word, current_row, current_col, game_over, keyboard_window

    if len(previous_guesses) >= 1 and game_over is False:
        word_text = "word" if len(previous_guesses) == 1 else "words"
        confirm = show_message("Change Language?",
                               f"You have already submitted {len(previous_guesses)} {word_text}. "
                               f"Changing the language will reset the game. Continue?",
                               message_type="confirm")
        if not confirm:
            lang_box.set(current_language)  # revert dropdown
            return

    # Reset game state
    game_over = False
    current_language = choice
    valid_words = load_words(current_language)
    secret_word = get_todays_word(valid_words)
    print("Today's word:", secret_word)

    reset_grid()

    # Re-enable keyboard buttons if they were disabled
    for btn in keyboard_buttons.values():
        if btn and btn.winfo_exists():
            btn.configure(state="normal")

    # Close the keyboard window if it's open, so it can be recreated with the new layout
    if keyboard_window is not None and keyboard_window.winfo_exists():
        keyboard_window.destroy()
        keyboard_window = None

    # Rebind key input
    app.bind("<Key>", on_key)


def on_theme_change(theme):
    """
    Handles the event when the theme selection is changed.

    Parameters:
    - theme: The newly selected theme as a string.
    """
    global current_theme, info_window
    global COLOR_APP_BG, COLOR_BOARD_BG, COLOR_BOARD_TILE, COLOR_TEXT, COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_DROPDOWN
    global COLOR_WRONG, COLOR_MISPLACED, COLOR_CORRECT, COLOR_KEY, COLOR_HOVER_KEY
    global COLOR_GREEN, COLOR_GREEN_HOVER, COLOR_RED, COLOR_RED_HOVER

    current_theme = theme

    COLOR_APP_BG = themes[current_theme]["APP_BG"]
    COLOR_BOARD_BG = themes[current_theme]["BOARD_BG"]
    COLOR_BOARD_TILE = themes[current_theme]["BOARD_TILE"]
    COLOR_TEXT = themes[current_theme]["TEXT"]
    COLOR_BUTTON = themes[current_theme]["BUTTON"]
    COLOR_BUTTON_HOVER = themes[current_theme]["BUTTON_HOVER"]
    COLOR_DROPDOWN = themes[current_theme]["DROPDOWN"]
    COLOR_WRONG = themes[current_theme]["WRONG"]
    COLOR_MISPLACED = themes[current_theme]["MISPLACED"]
    COLOR_CORRECT = themes[current_theme]["CORRECT"]

    COLOR_KEY = themes[current_theme]["KEY"]
    COLOR_HOVER_KEY = themes[current_theme]["HOVER_KEY"]

    COLOR_GREEN = themes[current_theme]["GREEN"]
    COLOR_GREEN_HOVER = themes[current_theme]["GREEN_HOVER"]
    COLOR_RED = themes[current_theme]["RED"]
    COLOR_RED_HOVER = themes[current_theme]["RED_HOVER"]

    app.configure(fg_color=themes[current_theme]["APP_BG"])
    frame.configure(fg_color=themes[current_theme]["BOARD_BG"])
    top.configure(fg_color=themes[current_theme]["APP_BG"])
    bottom.configure(fg_color=themes[current_theme]["APP_BG"])
    lang_label.configure(text_color=COLOR_TEXT)
    theme_label.configure(text_color=COLOR_TEXT)
    lang_box.configure(fg_color=COLOR_DROPDOWN, border_color=COLOR_BUTTON, button_color=COLOR_BUTTON,
                       text_color=COLOR_TEXT)
    theme_box.configure(fg_color=COLOR_DROPDOWN, border_color=COLOR_BUTTON, button_color=COLOR_BUTTON,
                        text_color=COLOR_TEXT)
    info_btn.configure(fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER, text_color=COLOR_TEXT)
    keyboard_btn.configure(fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER, text_color=COLOR_TEXT)

    for r in range(ROWS):
        for c in range(COLS):
            state = tile_states[r][c]
            tiles[r][c].configure(fg_color=get_tile_fg_color(state), text_color=get_text_color(state))

    refresh_keyboard_colors()

    # # ENTER
    # btn = keyboard_buttons.get("⏎")
    # if btn and btn.winfo_exists():
    #     btn.configure(fg_color=COLOR_GREEN, hover_color=COLOR_GREEN_HOVER)
    #
    # # DELETE
    # btn = keyboard_buttons.get("⌫")
    # if btn and btn.winfo_exists():
    #     btn.configure(fg_color=COLOR_RED, hover_color=COLOR_RED_HOVER)

    if info_window is not None and info_window.winfo_exists():
        info_window.destroy()
        info_window = None


def on_close():
    """
    Handles the event when the main window is closed.
    Prompts the user for confirmation before quitting.
    """
    confirm = show_message("Quit Game?", "Are you sure you want to quit?", message_type="confirm")
    if confirm:
        app.destroy()


def open_info():
    """
    Opens the information popup window.
    """
    global info_framesm, info_window
    info_frames.clear()

    info_window = ctk.CTkToplevel()
    info_window.title("About Wordle")
    info_window.geometry("360x277")
    info_window.resizable(False, False)
    info_window.configure(fg_color=COLOR_APP_BG)

    ctk.CTkLabel(info_window, text="Wordle is a word game where you have 6 attempts to guess a valid 5-letter word.",
                 font=FONT_15, text_color=COLOR_TEXT, justify="left", wraplength=300, bg_color=COLOR_APP_BG).pack(
        padx=(30, 0), pady=(30, 0), anchor="w")

    ctk.CTkLabel(info_window,
                 text="After each guess, the colour of the tiles changes to show how close your guess was:",
                 font=FONT_15, text_color=COLOR_TEXT, justify="left", wraplength=300).pack(pady=(5, 10), padx=30,
                                                                                           anchor="w")

    # Color explanations
    for letter, state, color, state_desc in [
        ("A", "correct", COLOR_CORRECT, "A is in the word and in the correct spot"),
        ("B", "misplaced", COLOR_MISPLACED, "B is in the word but in the wrong spot"),
        ("C", "wrong", COLOR_WRONG, "C is not in the word in any spot"),
    ]:
        frame = ctk.CTkFrame(info_window, fg_color=COLOR_APP_BG, width=300, height=40)
        frame.pack(pady=(0, 5), padx=30)
        info_frames.append(frame)

        ctk.CTkLabel(frame, text=letter, font=FONT_20_BOLD,
                     text_color=get_text_color(state), fg_color=color,
                     width=40, height=40, corner_radius=5).place(x=0, y=0)

        ctk.CTkLabel(frame, text="= " + state_desc,
                     font=FONT_13, text_color=COLOR_TEXT,
                     wraplength=255, justify="left").place(x=45, rely=0.5, anchor="w")


top = ctk.CTkFrame(app, width=360, height=30, fg_color=COLOR_APP_BG)
top.pack(pady=(30, 0), padx=30)

info_btn = ctk.CTkButton(top, text="?", width=60, height=30, fg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                         font=FONT_20_BOLD, text_color=COLOR_TEXT, corner_radius=5, command=open_info)
info_btn.place(x=290, y=0)

# Word grid
frame = ctk.CTkFrame(app, fg_color=COLOR_BOARD_BG)
frame.pack(padx=30, pady=(10, 5))
create_grid(frame)

bottom = ctk.CTkFrame(app, width=360, fg_color=COLOR_APP_BG)
bottom.pack()

# Language label
lang_label = ctk.CTkLabel(bottom, text="Language:", font=FONT_15, text_color=COLOR_TEXT)
lang_label.grid(row=0, column=0, sticky="w", padx=5)

# Language dropdown
lang_box = ctk.CTkComboBox(bottom, fg_color=COLOR_DROPDOWN, border_color=COLOR_BUTTON, button_color=COLOR_BUTTON,
                           text_color=COLOR_TEXT, values=["English", "Norwegian", "Ukrainian"], width=130, font=FONT_15,
                           corner_radius=5)
lang_box.set("English")
lang_box.configure(state="readonly")
lang_box.grid(row=1, column=0, padx=(0, 10))
lang_box.configure(command=on_language_change)

current_language = lang_box.get()
valid_words = load_words(current_language)
secret_word = get_todays_word(valid_words)
print("Today's word:", secret_word)

# Theme Label
theme_label = ctk.CTkLabel(bottom, text="Theme:", font=FONT_15, text_color=COLOR_TEXT)
theme_label.grid(row=0, column=1, sticky="w", padx=5)

# Theme Dropdown
theme_box = ctk.CTkComboBox(bottom, fg_color=COLOR_DROPDOWN, border_color=COLOR_BUTTON, button_color=COLOR_BUTTON,
                            text_color=COLOR_TEXT,
                            values=["Classic Dark", "Classic Light", "High Contrast Dark", "High Contrast Light",
                                    "Midnight Blue & Rose", "Blush & Teal"], width=130, height=30, font=FONT_15,
                            corner_radius=5)
theme_box.set("Classic Dark")
theme_box.configure(state="readonly")
theme_box.grid(row=1, column=1)
theme_box.configure(command=lambda t: on_theme_change(t))

# On-screen keyboard button
keyboard_btn = ctk.CTkButton(bottom, text="⌨️", width=60, height=30, command=open_keyboard, fg_color=COLOR_BUTTON,
                             hover_color=COLOR_BUTTON_HOVER, font=FONT_20_BOLD, corner_radius=5)
keyboard_btn.grid(row=1, column=2, padx=(10, 0))

app.protocol("WM_DELETE_WINDOW", on_close)
app.bind("<Key>", on_key)
app.mainloop()
