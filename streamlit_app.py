import streamlit as st
import random

# --- إعدادات الصفحة ---
st.set_page_config(page_title="تحدي الالعاب: Hangman Pro", page_icon="🎮")

# --- البيانات مع التلميحات (Dictionary) ---
# أضفت لك تصنيفاً بسيطاً لكل كلمة لتظهر كمساعدة
MLBB_DATA = {
    "Miya": "Marksman", "Balmond": "Fighter", "Saber": "Assassin", "Alice": "Mage",
    "Nana": "Mage/Support", "Tigreal": "Tank", "Alucard": "Fighter/Assassin", "Gusion": "Assassin/Mage",
    "Layla": "Marksman", "Franco": "Tank", "Zilong": "Fighter/Assassin", "Fanny": "Assassin"
} # يمكنك إضافة المزيد بنفس النمط

CR_DATA = {
    "Knight": "Common Troop", "P.E.K.K.A": "Epic Troop", "The Log": "Legendary Spell",
    "Princess": "Legendary Troop", "Giant": "Rare Troop", "Sparky": "Legendary Troop",
    "Miner": "Legendary Troop", "Fireball": "Rare Spell", "Arrows": "Common Spell"
}

# --- تهيئة حالة اللعبة ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'score' not in st.session_state:
    st.session_state.score = 0

def start_game(category, attempts):
    data_source = MLBB_DATA if category == "MLBB Characters" else CR_DATA
    word, hint = random.choice(list(data_source.items()))
    st.session_state.word = word.upper()
    st.session_state.hint = hint
    st.session_state.guessed_letters = []
    st.session_state.attempts = attempts
    st.session_state.max_attempts = attempts
    st.session_state.game_started = True

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ الإعدادات")
    st.write(f"🏆 النقاط: {st.session_state.score}")
    if st.button("🔄 العودة للرئيسية"):
        st.session_state.game_started = False
        st.rerun()

# --- واجهة الإعدادات ---
if not st.session_state.game_started:
    st.title("🎯 إعدادات اللعبة")
    category = st.selectbox("اختر القائمة:", ["MLBB Characters", "CR Cards"])
    attempts = st.slider("عدد المحاولات:", 3, 15, 7)
    
    if st.button("🚀 ابدأ اللعب", use_container_width=True):
        start_game(category, attempts)
        st.rerun()

# --- واجهة اللعب ---
else:
    st.title("🎮 خمن الكلمة")
    
    # 💡 إضافة نص المساعدة (التعديل الجديد)
    with st.expander("💡 هل تحتاج لمساعدة؟ (تلميح)"):
        st.write(f"هذه الشخصية/البطاقة تصنف كـ: **{st.session_state.hint}**")

    # عرض الكلمة
    display_word = "".join([char + " " if char in st.session_state.guessed_letters or not char.isalpha() else "_ " for char in st.session_state.word])
    st.header(f"`{display_word}`")

    # عرض المحاولات
    st.progress(st.session_state.attempts / st.session_state.max_attempts, 
                text=f"❤️ المحاولات المتبقية: {st.session_state.attempts}")

    # إدخال الحروف
    letter = st.text_input("أدخل حرفاً:", max_chars=1).upper()
    if st.button("تأكيد"):
        if letter and letter.isalpha() and letter not in st.session_state.guessed_letters:
            st.session_state.guessed_letters.append(letter)
            if letter not in st.session_state.word:
                st.session_state.attempts -= 1
        st.rerun()

    # نهاية اللعبة
    if all(c in st.session_state.guessed_letters or not c.isalpha() for c in st.session_state.word):
        st.balloons()
        st.success(f"🎊 أحسنت! الإجابة هي: {st.session_state.word}")
        if st.button("جولة جديدة"):
            st.session_state.score += 20
            start_game("MLBB Characters" if "Mage" in st.session_state.hint else "CR Cards", st.session_state.max_attempts)
            st.rerun()
    elif st.session_state.attempts <= 0:
        st.error(f"💀 للأسف! الكلمة كانت: {st.session_state.word}")
        if st.button("حاول مرة أخرى"):
            st.session_state.game_started = False
            st.rerun()
