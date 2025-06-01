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


st.title('タミル文字 読み方練習')

# --- セッション状態管理 ---
if 'remaining_characters' not in st.session_state:
    st.session_state.remaining_characters = TAMIL_CHARACTERS.copy()
    random.shuffle(st.session_state.remaining_characters)
    st.session_state.used_characters = []

if 'current_char_data' not in st.session_state:
    if not st.session_state.remaining_characters: # 全ての文字を使い切った場合
        st.session_state.remaining_characters = st.session_state.used_characters.copy()
        random.shuffle(st.session_state.remaining_characters)
        st.session_state.used_characters = []
        if not st.session_state.remaining_characters: # 初期リストも空だった場合（念のため）
            st.session_state.remaining_characters = TAMIL_CHARACTERS.copy()
            random.shuffle(st.session_state.remaining_characters)

    next_char_tuple = st.session_state.remaining_characters.pop(0)
    st.session_state.used_characters.append(next_char_tuple)
    st.session_state.current_char_data = next_char_tuple
    st.session_state.show_answer = False

character, pronunciation = st.session_state.current_char_data

st.divider()

# 1. タミル文字を表示 (CSSクラスを適用)
st.markdown(f"<div class='tamil-char-display'>{character}</div>", unsafe_allow_html=True)


# --- ボタンと回答表示 ---
col1, col2 = st.columns(2)
with col1:
    if st.button('回答を見る', key=f'show_{character}'):
        st.session_state.show_answer = True
with col2:
    if st.button('次へ', key=f'next_{character}'):
        if not st.session_state.remaining_characters: # 全ての文字を使い切った場合
            st.session_state.remaining_characters = st.session_state.used_characters.copy()
            random.shuffle(st.session_state.remaining_characters)
            st.session_state.used_characters = []
            if not st.session_state.remaining_characters: # 初期リストも空だった場合（念のため）
                 # この状況は通常発生しないはずだが、安全策としてTAMIL_CHARACTERSから再初期化
                st.session_state.remaining_characters = TAMIL_CHARACTERS.copy()
                random.shuffle(st.session_state.remaining_characters)

        if st.session_state.remaining_characters: # まだ残りがある場合
            next_char_tuple = st.session_state.remaining_characters.pop(0)
            st.session_state.used_characters.append(next_char_tuple)
            st.session_state.current_char_data = next_char_tuple
        else: # 本当にリストが空で、再初期化もできなかった場合（エラーケース）
            st.error("文字リストを読み込めませんでした。ページを再読み込みしてください。")
            # current_char_data は変更しない
            pass

        st.session_state.show_answer = False
        st.rerun()

if st.session_state.show_answer:
    # 回答のフォントもNoto Sans Tamilになるようにする（全体適用していれば不要かも）
    st.success(f'読み: **{pronunciation}**')

st.divider()