import streamlit as st
import random

# --- (前のコードの文字生成部分) ---
# 基本母音 (Uyir)
vowels = {
    'அ': 'a', 'ஆ': 'aa', 'இ': 'i', 'ஈ': 'ii', 'உ': 'u',
    'ஊ': 'uu', 'எ': 'e', 'ஏ': 'ee', 'ஐ': 'ai', 'ஒ': 'o',
    'ஓ': 'oo', 'ஔ': 'au'
}
# 基本子音 (Mei - プッリ(点)なしの形) とその基本音
consonants_base = {
    'க': 'k', 'ங': 'ng', 'ச': 's', 'ஞ': 'ny', 'ட': 'ṭ', # ச は 'ch' の場合もある
    'ண': 'ṇ', 'த': 'th', 'ந': 'n', 'ப': 'p', 'ம': 'm',
    'ய': 'y', 'ர': 'r', 'ல': 'l', 'வ': 'v', 'ழ': 'ḻ',
    'ள': 'ḷ', 'ற': 'ṟ', 'ன': 'ṉ'
}
# グランタ文字 (オプション)
grantha_consonants = {
    'ஜ': 'j', 'ஷ': 'ṣ', 'ஸ': 's', 'ஹ': 'h'
}
all_consonants = {**consonants_base, **grantha_consonants}
# 母音記号 (Diacritics) - ア(a)は記号なし
vowel_diacritics = {
    'aa': 'ா', 'i': 'ி', 'ii': 'ீ', 'u': 'ு', 'uu': 'ூ',
    'e': 'ெ', 'ee': 'ே', 'ai': 'ை', 'o': 'ொ', 'oo': 'ோ', 'au': 'ௌ'
}
# 特殊記号
aytham = {'ஃ': 'ak'}
TAMIL_CHARACTERS = []
# 1. 母音を追加
for char, pron in vowels.items():
    TAMIL_CHARACTERS.append((char, pron))
# 2. アイクタムを追加
TAMIL_CHARACTERS.append((aytham.popitem()))
# 3. 純粋な子音 (Mei - 点付き) を追加
pulli = '\u0BCD' # プッリ(点)のUnicode
for base_char, base_pron in all_consonants.items():
    mei_char = base_char + pulli
    TAMIL_CHARACTERS.append((mei_char, base_pron))
# 4. 子音 + 母音 の結合文字 (Uyirmei) を生成
for base_char, base_pron in all_consonants.items():
    uyirmei_char_a = base_char
    uyirmei_pron_a = base_pron + 'a'
    TAMIL_CHARACTERS.append((uyirmei_char_a, uyirmei_pron_a))
    for vowel_sound, diacritic in vowel_diacritics.items():
        uyirmei_char = base_char + diacritic
        uyirmei_pron = base_pron + vowel_sound
        TAMIL_CHARACTERS.append((uyirmei_char, uyirmei_pron))
TAMIL_CHARACTERS.append(('ஸ்ரீ', 'sri'))
# --- ここまで文字生成 ---

TAMIL_WORDS = [
    ('வணக்கம்', 'vaṇakkam'),  # Hello
    ('நன்றி', 'naṉṟi'),      # Thank you
    ('தமிழ்', 'tamiḻ'),      # Tamil
    ('காலை', 'kālai'),      # Morning
    ('மாலை', 'mālai'),      # Evening
    ('பழம்', 'paḻam'),       # Fruit
    ('தண்ணீர்', 'taṇṇīr'),   # Water
    ('சோறு', 'sōṟu'),        # Rice (cooked)
    ('பூ', 'pū'),           # Flower
    ('வீடு', 'vīṭu')         # House
]

# --- Helper function to get next item ---
def _get_next_item(session_state, all_chars):
    if not session_state.remaining_characters:
        if session_state.used_characters:
            # Repopulate from used_characters
            session_state.remaining_characters = session_state.used_characters.copy()
            random.shuffle(session_state.remaining_characters)
            session_state.used_characters = []
        elif all_chars: # used_characters is empty, but all_chars is available
            session_state.remaining_characters = all_chars.copy()
            random.shuffle(session_state.remaining_characters)
            session_state.used_characters = []
        else:
            # No characters in used_characters and no all_chars provided (or all_chars is empty)
            return None

    if not session_state.remaining_characters:
        # If still empty after trying to repopulate (e.g. all_chars was empty initially)
        return None

    next_char_tuple = session_state.remaining_characters.pop(0)
    session_state.used_characters.append(next_char_tuple)
    return next_char_tuple


# --- Streamlit アプリケーション ---

# --- Webフォント (Noto Sans Tamil) を読み込む ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;700&display=swap');

/* アプリ全体、または特定の要素にフォントを適用 */
html, body, [class*="st-"] {
    font-family: 'Noto Sans Tamil', sans-serif;
}
/* 特に文字を表示する部分に強く適用する場合 */
.tamil-char-display {
    font-family: 'Noto Sans Tamil', sans-serif;
    font-size: 5em; /* サイズもここで調整可能 */
    text-align: center;
}
</style>
""", unsafe_allow_html=True)
# --- フォント読み込みここまで ---

# --- Initialize quiz_mode before setting title ---
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = "文字" # Default to Characters

# --- Set title based on quiz_mode ---
if st.session_state.quiz_mode == "文字":
    st.title('タミル文字 読み方練習')
else: # "単語"
    st.title('タミル単語 読み方練習')

# --- Mode selection ---
# Note: The radio button will now correctly reflect the initialized quiz_mode
st.session_state.quiz_mode = st.radio(
    "練習モードを選択:",
    ("文字", "単語"),
    index=0 if st.session_state.quiz_mode == "文字" else 1, # Set default selection
    key='quiz_mode_radio' # Add a key for stability if needed elsewhere
)

# --- セッション状態管理 ---
# Function to initialize or reset lists based on quiz_mode
def initialize_lists():
    if st.session_state.quiz_mode == "文字":
        source_list = TAMIL_CHARACTERS
    else: # "単語"
        source_list = TAMIL_WORDS

    st.session_state.remaining_characters = source_list.copy()
    random.shuffle(st.session_state.remaining_characters)
    st.session_state.used_characters = []

    next_item = _get_next_item(st.session_state, source_list)
    if next_item:
        st.session_state.current_char_data = next_item
        st.session_state.show_answer = False
    else:
        st.error(f"{st.session_state.quiz_mode}のリストが空です。")
        st.session_state.current_char_data = (None, "エラー")
        st.session_state.show_answer = False

# Check if quiz_mode has changed or if it's the first run for list initialization
if 'previous_quiz_mode' not in st.session_state:
    st.session_state.previous_quiz_mode = st.session_state.quiz_mode # Initialize on first run
    initialize_lists()
elif st.session_state.previous_quiz_mode != st.session_state.quiz_mode:
    st.session_state.previous_quiz_mode = st.session_state.quiz_mode # Update mode
    initialize_lists() # Re-initialize lists and fetch new item
elif 'current_char_data' not in st.session_state: # Ensure current_char_data is always initialized
    initialize_lists()


item_text, item_pronunciation = st.session_state.current_char_data if st.session_state.current_char_data else (" ", " ")

st.divider()

# 1. タミル文字/単語を表示 (CSSクラスを適用)
# Ensure item_text is not None before trying to display it
if item_text:
    st.markdown(f"<div class='tamil-char-display'>{item_text}</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='tamil-char-display'> </div>", unsafe_allow_html=True) # Show empty space
    st.warning(f"表示する{st.session_state.quiz_mode}がありません。")


# --- ボタンと回答表示 ---
col1, col2 = st.columns(2)
with col1:
    if st.button('回答を見る', key=f'show_{st.session_state.quiz_mode}_{item_text if item_text else "no_item_show"}'):
        st.session_state.show_answer = True
with col2:
    if st.button('次へ', key=f'next_{st.session_state.quiz_mode}_{item_text if item_text else "no_item_next"}'):
        current_list = TAMIL_CHARACTERS if st.session_state.quiz_mode == "文字" else TAMIL_WORDS
        next_item = _get_next_item(st.session_state, current_list)
        if next_item:
            st.session_state.current_char_data = next_item
            st.session_state.show_answer = False
        else:
            st.error(f"次の{st.session_state.quiz_mode}を取得できませんでした。リストの終端か、リストが空の可能性があります。")
            # Keep current_char_data or set to an error/empty state
        st.rerun()

if st.session_state.show_answer:
    if item_text: # Only show pronunciation if there's an item
        st.success(f'読み: **{item_pronunciation}**')

st.divider()