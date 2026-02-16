import streamlit as st
import random

# --- إعدادات الصفحة ---
st.set_page_config(page_title="تحدي الالعاب المطوّر", page_icon="🎮")

# --- البيانات (الكلمات) ---
MLBB_HEROES = ["Miya", "Balmond", "Saber", "Alice", "Nana", "Tigreal", "Alucard", "Akai", "Franco", "Bane", "Bruno", "Clint", "Rafaela", "Eudora", "Zilong", "Fanny", "Layla", "Minotaur", "Lolita", "Hayabusa", "Freya", "Gord", "Natalia", "Kagura", "Chou", "Sun", "Alpha", "Ruby", "Yi Sun-shin", "Moskov", "Johnson", "Cyclops", "Estes", "Hilda", "Aurora", "Lapu-Lapu", "Vexana", "Roger", "Karrie", "Grock", "Irithel", "Harley", "Odette", "Lancelot", "Diggie", "Hylos", "Zhask", "Helcurt", "Pharsa", "Lesley", "Jawhead", "Angela", "Gusion", "Valir", "Martis", "Uranus", "Hanabi", "Chang'e", "Selina", "Aldous", "Claude", "Vale", "Leomord", "Lunox", "Hanzo", "Belerick", "Kimmy", "Thamuz", "Harith", "Kadita", "Faramis", "Badang", "Khufra", "Granger", "Guinevere", "Esmeralda", "Terizla", "X.Borg", "Lylia", "Baxia", "Masha", "Wanwan", "Silvanna", "Cecilion", "Carmilla", "Atlas", "Popol and Kupa", "Yu Zhong", "Khaleed", "Barats", "Brody", "Benedetta", "Mathilda", "Paquito", "Gloo", "Beatrix", "Phoveus", "Natan", "Aulus", "Floryn", "Valentina", "Edith", "Yin", "Melissa", "Xavier", "Julian", "Fredrinn", "Joy", "Arlott", "Novaria", "Ixia", "Nolan", "Cici"]
CR_CARDS = ["Knight", "Archers", "Goblins", "Giant", "P.E.K.K.A", "Mini P.E.K.K.A", "Balloon", "Witch", "Skeleton Army", "Baby Dragon", "Prince", "Wizard", "Ice Wizard", "Princess", "Miner", "Sparky", "Log", "Lumberjack", "Inferno Dragon", "Electro Wizard", "Night Witch", "Bandit", "Royal Ghost", "Magic Archer", "Ram Rider", "Mega Knight", "Graveyard", "Freeze", "Mirror", "Lightning", "Fireball", "Arrows", "Rocket", "Zap", "Tornado", "Poison", "Fisherman", "Phoenix", "Monk", "Little Prince"]

# --- تهيئة حالة اللعبة ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'score' not in st.session_state:
    st.session_state.score = 0

def start_game(category, attempts):
    words = MLBB_HEROES if category == "MLBB Characters" else CR_CARDS
    st.session_state.word = random.choice(words).upper()
    st.session_state.guessed_letters = []
    st.session_state.attempts = attempts
    st.session_state.max_attempts = attempts
    st.session_state.game_started = True

# --- القائمة الجانبية للإدارة ---
with st.sidebar:
    st.header("⚙️ الإعدادات")
    st.write(f"🏆 النقاط: {st.session_state.score}")
    if st.button("🔄 إعادة اللعبة بالكامل"):
        st.session_state.game_started = False
        st.rerun()

# --- واجهة البداية ---
if not st.session_state.game_started:
    st.title("🎯 إعدادات تحدي هانغ مان")
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("1. اختر القائمة:", ["MLBB Characters", "CR Cards"])
    with col2:
        attempts = st.slider("2. عدد المحاولات:", min_value=3, max_value=15, value=7)
    
    st.info(f"ستلعب الآن بكلمات من {category} ومعك {attempts} محاولات.")
    
    if st.button("🚀 ابدأ اللعب الآن", use_container_width=True):
        start_game(category, attempts)
        st.rerun()

# --- مرحلة اللعب ---
else:
    st.title("🎮 خمن الكلمة!")
    
    # عرض الكلمة المخفية
    display_word = "".join([char + " " if char in st.session_state.guessed_letters or not char.isalpha() else "_ " for char in st.session_state.word])
    st.header(f"`{display_word}`")

    # شريط المحاولات
    progress = st.session_state.attempts / st.session_state.max_attempts
    st.progress(progress, text=f"❤️ المحاولات المتبقية: {st.session_state.attempts}")

    # إدخال الحروف
    letter = st.text_input("أدخل حرفاً:", max_chars=1).upper()
    if st.button("تأكيد الحرف"):
        if letter and letter.isalpha():
            if letter not in st.session_state.guessed_letters:
                st.session_state.guessed_letters.append(letter)
                if letter not in st.session_state.word:
                    st.session_state.attempts -= 1
            st.rerun()

    # فحص الفوز أو الخسارة
    if all(c in st.session_state.guessed_letters or not c.isalpha() for c in st.session_state.word):
        st.balloons()
        st.success(f"🎊 فوز رائع! الكلمة هي: {st.session_state.word}")
        if st.button("جولة جديدة بنفس الإعدادات"):
            st.session_state.score += 20
            start_game(category if 'category' in locals() else "MLBB Characters", st.session_state.max_attempts)
            st.rerun()

    elif st.session_state.attempts <= 0:
        st.error(f"💀 خسرت! الكلمة كانت: {st.session_state.word}")
        if st.button("محاولة أخرى"):
            st.session_state.score = max(0, st.session_state.score - 10)
            st.session_state.game_started = False
            st.rerun()
