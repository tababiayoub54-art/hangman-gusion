import streamlit as st
import random

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Hangman: MLBB & CR Full Edition", page_icon="🎮", layout="centered")

# --- قاعدة بيانات MLBB الشاملة (الاسم: [الضرر، الدور]) ---
MLBB_DATA = {
    "Miya": ["جسدي", "Marksman"], "Balmond": ["جسدي", "Fighter"], "Saber": ["جسدي", "Assassin"],
    "Alice": ["سحري", "Mage/Tank"], "Nana": ["سحري", "Mage/Support"], "Tigreal": ["جسدي", "Tank"],
    "Alucard": ["جسدي", "Fighter/Assassin"], "Akai": ["جسدي", "Tank"], "Franco": ["جسدي", "Tank"],
    "Bane": ["جسدي", "Fighter/Mage"], "Bruno": ["جسدي", "Marksman"], "Clint": ["جسدي", "Marksman"],
    "Rafaela": ["سحري", "Support"], "Eudora": ["سحري", "Mage"], "Zilong": ["جسدي", "Fighter/Assassin"],
    "Fanny": ["جسدي", "Assassin"], "Layla": ["جسدي", "Marksman"], "Minotaur": ["جسدي", "Tank/Support"],
    "Lolita": ["جسدي", "Tank/Support"], "Hayabusa": ["جسدي", "Assassin"], "Freya": ["جسدي", "Fighter"],
    "Gord": ["سحري", "Mage"], "Natalia": ["جسدي", "Assassin"], "Kagura": ["سحري", "Mage"],
    "Chou": ["جسدي", "Fighter"], "Sun": ["جسدي", "Fighter"], "Alpha": ["جسدي", "Fighter"],
    "Ruby": ["جسدي", "Fighter/Tank"], "Yi Sun-shin": ["جسدي", "Marksman/Assassin"], "Moskov": ["جسدي", "Marksman"],
    "Johnson": ["سحري", "Tank"], "Cyclops": ["سحري", "Mage"], "Estes": ["سحري", "Support"],
    "Hilda": ["جسدي", "Fighter/Tank"], "Aurora": ["سحري", "Mage"], "Lapu-Lapu": ["جسدي", "Fighter"],
    "Vexana": ["سحري", "Mage"], "Roger": ["جسدي", "Fighter/Marksman"], "Karrie": ["حقيقي (True)", "Marksman"],
    "Grock": ["جسدي", "Tank"], "Irithel": ["جسدي", "Marksman"], "Harley": ["سحري", "Mage/Assassin"],
    "Odette": ["سحري", "Mage"], "Lancelot": ["جسدي", "Assassin"], "Diggie": ["سحري", "Support"],
    "Hylos": ["سحري", "Tank"], "Zhask": ["سحري", "Mage"], "Helcurt": ["جسدي", "Assassin"],
    "Pharsa": ["سحري", "Mage"], "Lesley": ["جسدي", "Marksman/Assassin"], "Jawhead": ["جسدي", "Fighter"],
    "Angela": ["سحري", "Support"], "Gusion": ["سحري", "Assassin/Mage"], "Valir": ["سحري", "Mage"],
    "Martis": ["جسدي", "Fighter"], "Uranus": ["سحري", "Tank"], "Hanabi": ["جسدي", "Marksman"],
    "Chang'e": ["سحري", "Mage"], "Selena": ["سحري", "Assassin/Mage"], "Aldous": ["جسدي", "Fighter"],
    "Claude": ["جسدي", "Marksman"], "Vale": ["سحري", "Mage"], "Leomord": ["جسدي", "Fighter"],
    "Lunox": ["سحري", "Mage"], "Hanzo": ["جسدي", "Assassin"], "Belerick": ["سحري", "Tank"],
    "Kimmy": ["جسدي/سحري", "Marksman/Mage"], "Thamuz": ["حقيقي (True)", "Fighter"], "Harith": ["سحري", "Mage"],
    "Kadita": ["سحري", "Mage/Assassin"], "Badang": ["جسدي", "Fighter"], "Khufra": ["جسدي", "Tank"],
    "Granger": ["جسدي", "Marksman"], "Guinevere": ["سحري", "Fighter/Mage"], "Esmeralda": ["سحري/جسدي", "Mage/Tank"],
    "Terizla": ["جسدي", "Fighter"], "X Borg": ["حقيقي (True)", "Fighter"], "Lylia": ["سحري", "Mage"],
    "Baxia": ["سحري", "Tank"], "Masha": ["جسدي", "Fighter/Tank"], "Wanwan": ["جسدي", "Marksman"],
    "Silvanna": ["سحري", "Fighter/Mage"], "Cecilion": ["سحري", "Mage"], "Atlas": ["سحري", "Tank"],
    "Popol and Kupa": ["جسدي", "Marksman"], "Yu Zhong": ["جسدي", "Fighter"], "Khaleed": ["جسدي", "Fighter"],
    "Barats": ["جسدي/سحري", "Tank/Fighter"], "Brody": ["جسدي", "Marksman"], "Benedetta": ["جسدي", "Assassin/Fighter"],
    "Paquito": ["جسدي", "Fighter"], "Gloo": ["سحري", "Tank"], "Beatrix": ["جسدي", "Marksman"],
    "Phoveus": ["سحري", "Fighter/Mage"], "Natan": ["سحري", "Marksman"], "Aulus": ["جسدي", "Fighter"],
    "Valentina": ["سحري", "Mage"], "Edith": ["سحري/جسدي", "Tank/Marksman"], "Yin": ["جسدي", "Fighter/Assassin"],
    "Melissa": ["جسدي", "Marksman"], "Xavier": ["سحري", "Mage"], "Julian": ["سحري", "Fighter/Mage"],
    "Fredrinn": ["جسدي", "Tank/Fighter"], "Joy": ["سحري", "Assassin/Mage"], "Arlott": ["جسدي", "Fighter/Assassin"],
    "Novaria": ["سحري", "Mage"], "Ixia": ["جسدي", "Marksman"], "Nolan": ["جسدي", "Assassin"], "Cici": ["جسدي", "Fighter"]
}

# --- قاعدة بيانات Clash Royale الشاملة (الاسم: [اللون، النوع]) ---
CR_DATA = {
    "Knight": ["أزرق (Common)", "Troop"], "Archers": ["أزرق (Common)", "Troop"],
    "Goblins": ["أزرق (Common)", "Troop"], "Giant": ["برتقالي (Rare)", "Tank"],
    "PEKKA": ["بنفسجي (Epic)", "Troop"], "Mini PEKKA": ["برتقالي (Rare)", "Troop"],
    "Balloon": ["بنفسجي (Epic)", "Troop"], "Witch": ["بنفسجي (Epic)", "Troop"],
    "Skeleton Army": ["بنفسجي (Epic)", "Troop"], "Baby Dragon": ["بنفسجي (Epic)", "Troop"],
    "Prince": ["بنفسجي (Epic)", "Troop"], "Wizard": ["برتقالي (Rare)", "Troop"],
    "Ice Wizard": ["ملون (Legendary)", "Troop"], "Princess": ["ملون (Legendary)", "Troop"],
    "Miner": ["ملون (Legendary)", "Troop"], "Sparky": ["ملون (Legendary)", "Troop"],
    "The Log": ["ملون (Legendary)", "Spell"], "Lumberjack": ["ملون (Legendary)", "Troop"],
    "Inferno Dragon": ["ملون (Legendary)", "Troop"], "Electro Wizard": ["ملون (Legendary)", "Troop"],
    "Night Witch": ["ملون (Legendary)", "Troop"], "Bandit": ["ملون (Legendary)", "Troop"],
    "Mega Knight": ["ملون (Legendary)", "Troop"], "Graveyard": ["ملون (Legendary)", "Spell"],
    "Freeze": ["بنفسجي (Epic)", "Spell"], "Lightning": ["بنفسجي (Epic)", "Spell"],
    "Fireball": ["برتقالي (Rare)", "Spell"], "Arrows": ["أزرق (Common)", "Spell"],
    "Rocket": ["برتقالي (Rare)", "Spell"], "Zap": ["أزرق (Common)", "Spell"],
    "Tornado": ["بنفسجي (Epic)", "Spell"], "Poison": ["بنفسجي (Epic)", "Spell"],
    "Fisherman": ["ملون (Legendary)", "Troop"], "Phoenix": ["ملون (Legendary)", "Troop"],
    "Monk": ["ذهبي (Champion)", "Troop"], "Little Prince": ["ذهبي (Champion)", "Troop"],
    "Tesla": ["أزرق (Common)", "Building"], "Inferno Tower": ["برتقالي (Rare)", "Building"],
    "X Bow": ["بنفسجي (Epic)", "Building"], "Mortar": ["أزرق (Common)", "Building"],
    "Hog Rider": ["برتقالي (Rare)", "Troop"], "Ram Rider": ["ملون (Legendary)", "Troop"]
}

# --- نظام اللعبة ---
if 'playing' not in st.session_state:
    st.session_state.playing, st.session_state.score = False, 100

def start_game(cat, att):
    data = MLBB_DATA if cat == "MLBB Characters" else CR_DATA
    word, info = random.choice(list(data.items()))
    st.session_state.word, st.session_state.hint = word.upper(), info[0]
    st.session_state.cat_type, st.session_state.category = info[1], cat
    st.session_state.guessed, st.session_state.wrong = [], []
    st.session_state.attempts, st.session_state.max_att = att, att
    st.session_state.playing, st.session_state.show_first = True, False

# --- الواجهة الجانبية ---
with st.sidebar:
    st.title(f"💰 الرصيد: {st.session_state.score}")
    if st.button("🔄 القائمة الرئيسية"):
        st.session_state.playing = False
        st.rerun()

# --- الشاشة الرئيسية ---
if not st.session_state.playing:
    st.title("🏹 Hangman: المجموعات الكاملة")
    c = st.selectbox("اختر القائمة:", ["MLBB Characters", "CR Cards"])
    a = st.slider("المحاولات:", 3, 15, 7)
    if st.button("🚀 ابدأ الآن", use_container_width=True):
        start_game(c, a)
        st.rerun()
else:
    # التلميح التلقائي بناءً على طلبك
    hint_label = "⚡ نوع الضرر" if st.session_state.category == "MLBB Characters" else "🎨 لون الندرة"
    st.info(f"**{hint_label}:** {st.session_state.hint}")

    if not st.session_state.show_first:
        if st.button("🔡 أول حرف (-20💰)"):
            if st.session_state.score >= 20:
                st.session_state.score -= 20
                st.session_state.show_first = True
                st.rerun()
    else: st.warning(f"🅰️ يبدأ بحرف: {st.session_state.word[0]}")

    display = "".join([l + " " if l in st.session_state.guessed or not l.isalpha() else "_ " for l in st.session_state.word])
    st.markdown(f"<h1 style='text-align: center; font-size: 55px;'>{display}</h1>", unsafe_allow_html=True)

    if st.session_state.wrong:
        st.write(f"❌ **أخطاء:** {', '.join(st.session_state.wrong)}")

    st.progress(st.session_state.attempts / st.session_state.max_att, text=f"❤️ محاولات: {st.session_state.attempts}")

    # الإدخال مع التركيز ومسح تلقائي
    with st.form(key='input_form', clear_on_submit=True):
        letter = st.text_input("اكتب الحرف هنا ثم اضغط Enter:", max_chars=1).upper()
        if st.form_submit_button("تأكيد"):
            if letter.isalpha() and letter not in st.session_state.guessed and letter not in st.session_state.wrong:
                if letter in st.session_state.word: st.session_state.guessed.append(letter)
                else:
                    st.session_state.wrong.append(letter)
                    st.session_state.attempts -= 1
            st.rerun()

    if all(l in st.session_state.guessed or not l.isalpha() for l in st.session_state.word):
        st.balloons()
        st.success(f"🏆 الإجابة: {st.session_state.word}")
        if st.button("جولة جديدة (+30💰)"):
            st.session_state.score += 30
            st.session_state.playing = False
            st.rerun()
    elif st.session_state.attempts <= 0:
        st.error(f"💀 خسرت! كانت: {st.session_state.word}")
        if st.button("حاول مجدداً"):
            st.session_state.playing = False
            st.rerun()
