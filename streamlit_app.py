import streamlit as st
import random

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Hangman: Ultimate Edition", page_icon="🎮")

# --- قاعدة البيانات المطورة ---
# الهيكل: "الاسم": ["لون الندرة", "النوع/الضرر", "وصف إضافي"]
MLBB_DATA = {
    "Gusion": ["بنفسجي", "ضرر سحري (Magic Damage)", "Assassin/Mage"],
    "Alucard": ["أزرق", "ضرر جسدي (Physical Damage)", "Fighter/Assassin"],
    "Karrie": ["بنفسجي", "ضرر حقيقي (True Damage)", "Marksman - Tank Killer"],
    "Tigreal": ["أزرق", "ضرر جسدي (Physical Damage)", "Tank - Crowd Control"],
    "Alice": ["بنفسجي", "ضرر سحري (Magic Damage)", "Mage/Tank - Lifesteal"],
    "Thamuz": ["بنفسجي", "ضرر حقيقي (True Damage)", "Fighter - Lava Lord"]
}

CR_DATA = {
    "P.E.K.K.A": ["بنفسجي", "بطاقة هجومية (Offensive)", "Epic Troop"],
    "Tesla": ["برتقالي", "مبنى دفاعي (Defensive Building)", "Common Structure"],
    "Fireball": ["برتقالي", "تعويذة (Spell)", "Rare Damage Spell"],
    "The Log": ["ملون/خرافي", "تعويذة (Spell)", "Legendary Ground Spell"],
    "Giant": ["برتقالي", "بطاقة هجومية (Offensive)", "Rare Tank"],
    "Inferno Tower": ["برتقالي", "مبنى دفاعي (Defensive Building)", "Rare Structure"]
}

# --- تهيئة حالة اللعبة ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.score = 100

def start_game(category, attempts):
    data_source = MLBB_DATA if category == "MLBB Characters" else CR_DATA
    word, info = random.choice(list(data_source.items()))
    st.session_state.word = word.upper()
    st.session_state.color = info[0]
    st.session_state.type_info = info[1]
    st.session_state.guessed_letters = []
    st.session_state.attempts = attempts
    st.session_state.max_attempts = attempts
    st.session_state.game_started = True
    st.session_state.show_type = False
    st.session_state.show_first_letter = False

# --- الواجهة الرئيسية ---
with st.sidebar:
    st.title(f"💰 رصيدك: {st.session_state.score}")
    if st.button("🔄 العودة للقائمة"):
        st.session_state.game_started = False
        st.rerun()

if not st.session_state.game_started:
    st.title("🏹 متجر التحدي: هانغ مان")
    category = st.selectbox("اختر القائمة:", ["MLBB Characters", "CR Cards"])
    attempts = st.slider("عدد المحاولات:", 3, 10, 7)
    if st.button("🚀 ابدأ اللعب", use_container_width=True):
        start_game(category, attempts)
        st.rerun()
else:
    st.title("🎮 خمن الكلمة")
    
    # --- نظام المساعدة المطور ---
    st.write(f"🎨 **لون الندرة:** {st.session_state.color}")
    
    col1, col2 = st.columns(2)
    with col1:
        if not st.session_state.show_type:
            if st.button("🔍 كشف النوع (-10 نقاط)"):
                if st.session_state.score >= 10:
                    st.session_state.score -= 10
                    st.session_state.show_type = True
                    st.rerun()
        else:
            st.info(f"⚡ النوع: {st.session_state.type_info}")

    with col2:
        if not st.session_state.show_first_letter:
            if st.button("🔡 أول حرف (-20 نقطة)"):
                if st.session_state.score >= 20:
                    st.session_state.score -= 20
                    st.session_state.show_first_letter = True
                    st.rerun()
        else:
            st.warning(f"🅰️ يبدأ بحرف: {st.session_state.word[0]}")

    # عرض الكلمة والمحاولات
    display_word = "".join([c + " " if c in st.session_state.guessed_letters or not c.isalpha() else "_ " for c in st.session_state.word])
    st.header(f"`{display_word}`")
    st.progress(st.session_state.attempts / st.session_state.max_attempts, text=f"❤️ المحاولات: {st.session_state.attempts}")

    letter = st.text_input("أدخل حرفاً:").upper()
    if st.button("تأكيد"):
        if letter and letter not in st.session_state.guessed_letters:
            st.session_state.guessed_letters.append(letter)
            if letter not in st.session_state.word:
                st.session_state.attempts -= 1
        st.rerun()

    # النتائج
    if all(c in st.session_state.guessed_letters or not c.isalpha() for c in st.session_state.word):
        st.balloons()
        st.success(f"🏆 فوز! الكلمة: {st.session_state.word}")
        if st.button("جولة جديدة (+30 نقطة)"):
            st.session_state.score += 30
            st.session_state.game_started = False
            st.rerun()
    elif st.session_state.attempts <= 0:
        st.error(f"💀 خسرت! الكلمة: {st.session_state.word}")
        if st.button("إعادة المحاولة"):
            st.session_state.game_started = False
            st.rerun()
