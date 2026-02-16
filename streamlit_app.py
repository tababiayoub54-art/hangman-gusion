import streamlit as st
import random

# --- إعدادات الصفحة ---
st.set_page_config(page_title="تحدي الالعاب: Hangman", page_icon="🎮", layout="centered")

# --- البيانات (الكلمات) ---
MLBB_HEROES = [
    "Miya", "Balmond", "Saber", "Alice", "Nana", "Tigreal", "Alucard", "Akai", "Franco", "Bane", "Bruno", "Clint", "Rafaela", "Eudora", "Zilong", "Fanny", "Layla", "Minotaur", "Lolita", "Hayabusa", "Freya", "Gord", "Natalia", "Kagura", "Chou", "Sun", "Alpha", "Ruby", "Yi Sun-shin", "Moskov", "Johnson", "Cyclops", "Estes", "Hilda", "Aurora", "Lapu-Lapu", "Vexana", "Roger", "Karrie", "Grock", "Irithel", "Harley", "Odette", "Lancelot", "Diggie", "Hylos", "Zhask", "Helcurt", "Pharsa", "Lesley", "Jawhead", "Angela", "Gusion", "Valir", "Martis", "Uranus", "Hanabi", "Chang'e", "Selina", "Aldous", "Claude", "Vale", "Leomord", "Lunox", "Hanzo", "Belerick", "Kimmy", "Thamuz", "Harith", "Kadita", "Faramis", "Badang", "Khufra", "Granger", "Guinevere", "Esmeralda", "Terizla", "X.Borg", "Lylia", "Baxia", "Masha", "Wanwan", "Silvanna", "Cecilion", "Carmilla", "Atlas", "Popol and Kupa", "Yu Zhong", "Khaleed", "Barats", "Brody", "Benedetta", "Mathilda", "Paquito", "Gloo", "Beatrix", "Phoveus", "Natan", "Aulus", "Floryn", "Valentina", "Edith", "Yin", "Melissa", "Xavier", "Julian", "Fredrinn", "Joy", "Arlott", "Novaria", "Ixia", "Nolan", "Cici"
]

CR_CARDS = [
    "Knight", "Archers", "Goblins", "Giant", "P.E.K.K.A", "Mini P.E.K.K.A", "Balloon", "Witch", "Skeleton Army", "Baby Dragon", "Prince", "Wizard", "Ice Wizard", "Princess", "Miner", "Sparky", "Log", "Lumberjack", "Inferno Dragon", "Electro Wizard", "Night Witch", "Bandit", "Royal Ghost", "Magic Archer", "Ram Rider", "Mega Knight", "Graveyard", "Freeze", "Mirror", "Lightning", "Fireball", "Arrows", "Rocket", "Zap", "Tornado", "Poison", "Bat Cave", "Wall Breakers", "Fisherman", "Electro Spirit", "Phoenix", "Monk", "Little Prince", "Electro Giant", "Golden Knight", "Skeleton King", "Archer Queen", "Mighty Miner"
]

# --- تهيئة حالة اللعبة ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_wins' not in st.session_state:
    st.session_state.total_wins = 0

def reset_game(category):
    if category == "MLBB Characters":
        st.session_state.word = random.choice(MLBB_HEROES).upper()
    else:
        st.session_state.word = random.choice(CR_CARDS).upper()
    st.session_state.guessed_letters = []
    st.session_state.attempts = 7

# --- الواجهة الرئيسية ---
st.title("🎮 تحدي تخمين الأسماء")
st.sidebar.header("📊 إحصائياتك")
st.sidebar.write(f"النقاط: {st.session_state.score}")
st.sidebar.write(f"الفوز المتتالي: {st.session_state.total_wins}")

if not st.session_state.game_started:
    st.markdown("""
    ### مرحباً بك في اللعبة! 
    لقد تم تجهيز قوائم خاصة بـ **Mobile Legends** و **Clash Royale**. 
    هل تستطيع تخمين كل الشخصيات؟
    """)
    if st.button("🚀 ابدأ التحدي الآن", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

else:
    # اختيار القائمة
    category = st.selectbox("اختر عالمك المفضل:", ["MLBB Characters", "CR Cards"])
    
    if 'word' not in st.session_state:
        reset_game(category)

    # عرض حالة المحاولات برسم مبسط
    progress = st.session_state.attempts / 7
    st.progress(progress, text=f"المحاولات المتبقية: {st.session_state.attempts}")

    # عرض الكلمة المخفية
    display_word = ""
    for char in st.session_state.word:
        if char == " ":
            display_word += "  "
        elif char in st.session_state.guessed_letters or not char.isalpha():
            display_word += char + " "
        else:
            display_word += "_ "
    
    st.markdown(f"<h1 style='text-align: center; letter-spacing: 5px;'>{display_word}</h1>", unsafe_allow_html=True)

    # إدخال الحروف
    col1, col2 = st.columns([3, 1])
    with col1:
        letter = st.text_input("خمن حرفاً:", max_chars=1, key="input").upper()
    with col2:
        submit = st.button("تأكيد ✅")

    if submit:
        if letter and letter.isalpha():
            if letter not in st.session_state.guessed_letters:
                st.session_state.guessed_letters.append(letter)
                if letter not in st.session_state.word:
                    st.session_state.attempts -= 1
                    st.toast("خطأ! حاول مجدداً", icon="❌")
                else:
                    st.toast("حرف صحيح!", icon="✅")
            else:
                st.warning("لقد جربت هذا الحرف من قبل!")
        st.rerun()

    # التحقق من الفوز أو الخسارة
    clean_word = st.session_state.word.replace(" ", "")
    if all(c in st.session_state.guessed_letters or not c.isalpha() for c in clean_word):
        st.balloons()
        st.success(f"🏆 فوز مذهل! الكلمة هي: {st.session_state.word}")
        if st.button("الكلمة التالية ➡️"):
            st.session_state.score += 20
            st.session_state.total_wins += 1
            reset_game(category)
            st.rerun()

    elif st.session_state.attempts <= 0:
        st.error(f"💀 حظاً أوفر! الكلمة كانت: {st.session_state.word}")
        if st.button("حاول مرة أخرى 🔄"):
            st.session_state.score = max(0, st.session_state.score - 10)
            st.session_state.total_wins = 0
            reset_game(category)
            st.rerun()

    if st.button("العودة للقائمة الرئيسية"):
        st.session_state.game_started = False
        if 'word' in st.session_state: del st.session_state.word
        st.rerun()
