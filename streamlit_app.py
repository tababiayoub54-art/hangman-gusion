import streamlit as st
import random

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Hangman: Pro Edition", page_icon="🎮")

# --- قاعدة البيانات ---
MLBB_DATA = {
    "Gusion": ["ضرر سحري (Magic)", "Assassin/Mage"],
    "Alucard": ["ضرر جسدي (Physical)", "Fighter/Assassin"],
    "Karrie": ["ضرر حقيقي (True Damage)", "Marksman"],
    "Tigreal": ["ضرر جسدي (Physical)", "Tank"],
    "Alice": ["ضرر سحري (Magic)", "Mage/Tank"],
    "Thamuz": ["ضرر حقيقي (True Damage)", "Fighter"],
    "Nana": ["ضرر سحري (Magic)", "Mage/Support"],
    "Layla": ["ضرر جسدي (Physical)", "Marksman"],
    "Fanny": ["ضرر جسدي (Physical)", "Assassin"]
}

CR_DATA = {
    "P.E.K.K.A": ["بنفسجي (Epic)", "Troop"],
    "Tesla": ["أزرق (Common)", "Building"],
    "Fireball": ["برتقالي (Rare)", "Spell"],
    "The Log": ["ملون (Legendary)", "Spell"],
    "Giant": ["برتقالي (Rare)", "Tank"],
    "Inferno Tower": ["برتقالي (Rare)", "Building"],
    "Mega Knight": ["ملون (Legendary)", "Troop"]
}

# --- دالة البدء ---
def start_game(category, attempts):
    st.session_state.category = category
    data_source = MLBB_DATA if category == "MLBB Characters" else CR_DATA
    word, info = random.choice(list(data_source.items()))
    st.session_state.word = word.upper()
    st.session_state.main_hint = info[0] # اللون للكروت والنوع للشخصيات
    st.session_state.guessed_letters = []
    st.session_state.wrong_letters = []
    st.session_state.attempts = attempts
    st.session_state.max_attempts = attempts
    st.session_state.game_started = True
    st.session_state.show_first_letter = False

# --- تهيئة الحالة ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.score = 100

# --- الواجهة الجانبية ---
with st.sidebar:
    st.title(f"💰 الرصيد: {st.session_state.score}")
    if st.button("🔄 العودة للقائمة الرئيسية"):
        st.session_state.game_started = False
        st.rerun()

# --- واجهة الإعدادات ---
if not st.session_state.game_started:
    st.title("🏹 تحدي هانغ مان الذكي")
    cat = st.selectbox("اختر عالمك:", ["MLBB Characters", "CR Cards"])
    att = st.slider("عدد المحاولات:", 3, 12, 7)
    if st.button("🚀 ابدأ اللعب", use_container_width=True):
        start_game(cat, att)
        st.rerun()

# --- واجهة اللعب ---
else:
    st.title("🎮 خمن الآن")
    
    # ميزة التلميح التلقائي حسب النوع
    if st.session_state.category == "MLBB Characters":
        st.info(f"⚡ **نوع الضرر:** {st.session_state.main_hint}")
    else:
        st.info(f"🎨 **لون الندرة:** {st.session_state.main_hint}")

    # زر شراء الحرف الأول
    if not st.session_state.show_first_letter:
        if st.button("🔡 شراء أول حرف (-20💰)"):
            if st.session_state.score >= 20:
                st.session_state.score -= 20
                st.session_state.show_first_letter = True
                st.rerun()
    else:
        st.warning(f"🅰️ أول حرف هو: {st.session_state.word[0]}")

    # عرض الكلمة
    display_word = "".join([c + " " if c in st.session_state.guessed_letters or not c.isalpha() else "_ " for c in st.session_state.word])
    st.markdown(f"<h1 style='text-align: center; font-size: 50px;'>{display_word}</h1>", unsafe_allow_html=True)

    # عرض الحروف الخاطئة
    if st.session_state.wrong_letters:
        st.write(f"❌ **حروف خاطئة جربتها:** {', '.join(st.session_state.wrong_letters)}")

    st.progress(st.session_state.attempts / st.session_state.max_attempts, text=f"❤️ المحاولات المتبقية: {st.session_state.attempts}")

    # إدخال الحرف مع المسح التلقائي
    with st.form(key='input_form', clear_on_submit=True):
        letter = st.text_input("أدخل حرفاً واحداً:").upper()
        submit = st.form_submit_button("تأكيد الحرف ✅")

    if submit and letter:
        if letter.isalpha() and letter not in st.session_state.guessed_letters and letter not in st.session_state.wrong_letters:
            if letter in st.session_state.word:
                st.session_state.guessed_letters.append(letter)
            else:
                st.session_state.wrong_letters.append(letter)
                st.session_state.attempts -= 1
        st.rerun()

    # التحقق من النهاية
    if all(c in st.session_state.guessed_letters or not c.isalpha() for c in st.session_state.word):
        st.balloons()
        st.success(f"🏆 مذهل! الكلمة هي: {st.session_state.word}")
        if st.button("جولة جديدة (+30💰)"):
            st.session_state.score += 30
            st.session_state.game_started = False
            st.rerun()
    elif st.session_state.attempts <= 0:
        st.error(f"💀 حظاً أوفر! الكلمة كانت: {st.session_state.word}")
        if st.button("حاول مرة أخرى"):
            st.session_state.game_started = False
            st.rerun()
