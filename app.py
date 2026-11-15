import json
import random
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SkyTrip Voca | 단어 여행", page_icon="🧭", layout="wide")

# -------------------- 데이터 --------------------
@st.cache_data
def load_words():
    with open(Path(__file__).with_name("words.json"), encoding="utf-8") as f:
        return json.load(f)

WORDS = load_words()
LEVELS = ["초급", "중급", "고급"]

# -------------------- 스타일 --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap');
.stApp {background: linear-gradient(135deg,#dff5ff,#f5fcff 55%,#d8f0ff); color:#23485d;}
html, body, [class*="css"] {font-family:'Noto Sans KR',sans-serif;}
.block-container {max-width:1120px; padding-top:1.5rem; padding-bottom:3rem;}
.brand {font-size:1.55rem;font-weight:900;color:#145879;margin-bottom:0;}
.brand-sub {font-size:.82rem;color:#7894a3;margin-top:-5px;}
.hero {background:linear-gradient(115deg,#80cff2,#c3edff);padding:25px 29px;border-radius:23px;margin:20px 0;color:#205d7b;box-shadow:0 12px 35px #2a83a91c;}
.hero h2 {color:#104e70;margin:0 0 7px;font-size:1.8rem;}
.panel {background:#ffffffdf;border:1px solid #d6edf7;border-radius:19px;padding:18px;box-shadow:0 10px 28px #2a83a912;}
.flashcard {background:linear-gradient(145deg,#fff,#f1fbff);border:1px solid #cceaf8;border-radius:22px;padding:35px 18px;text-align:center;box-shadow:0 12px 30px #207ca51b;margin:12px 0;}
.word {font-size:clamp(2.5rem,6vw,3.5rem);font-weight:900;color:#155a7c;margin:8px 0;}
.meaning {font-size:1.45rem;font-weight:800;color:#217b9e;margin:8px 0;}
.example {background:#edf8fd;border-radius:12px;padding:13px;color:#315f75;line-height:1.7;margin-top:14px;}
.question {font-size:1.35rem;font-weight:850;color:#174f6d;line-height:1.5;margin:10px 0;}
.feedback {padding:12px 14px;border-radius:11px;background:#f1f8fb;color:#5c7b8d;margin:12px 0;}
.good {background:#e7f8f0;color:#177552;}.bad {background:#fff0f2;color:#ad4051;}
.hint {color:#a96b22;font-weight:750;margin-top:6px;}
div.stButton > button {border-radius:11px;font-weight:750;border:1px solid #cde8f4;}
[data-testid="stProgressBar"] > div > div {background:linear-gradient(90deg,#54b7e5,#6ed2b1);}
.small-muted {font-size:.85rem;color:#7894a3;}
</style>
""", unsafe_allow_html=True)

# -------------------- 세션 상태 --------------------
def init_state():
    defaults = {
        "level": "초급", "set_index": 0, "stage": "flash", "card_index": 0,
        "revealed": False, "quiz_items": [], "quiz_index": 0,
        "cloze_items": [], "cloze_index": 0, "correct": 0, "total": 0,
        "answered": False, "speech": True, "quiz_choices": [], "cloze_choices": [],
        "quiz_wrong": [], "cloze_wrong": [], "last_feedback": "", "last_feedback_type": ""
    }
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v

def level_words():
    return [w for w in WORDS if w["level"] == st.session_state.level]

def current_words():
    all_words = level_words()
    batch = all_words[st.session_state.set_index*20:st.session_state.set_index*20+20]
    return batch or all_words[:20]

def make_quiz_items(batch):
    items = []
    for w in batch:
        items.extend([{"type":"meaning","word":w},{"type":"spelling","word":w}])
    random.shuffle(items)
    return items

def start_set():
    batch = current_words()
    st.session_state.card_index = 0
    st.session_state.revealed = False
    st.session_state.correct = 0
    st.session_state.total = 0
    st.session_state.quiz_index = 0
    st.session_state.cloze_index = 0
    st.session_state.quiz_items = make_quiz_items(batch)
    st.session_state.cloze_items = random.sample(batch, len(batch))
    st.session_state.quiz_choices = []
    st.session_state.cloze_choices = []
    st.session_state.quiz_wrong = []
    st.session_state.cloze_wrong = []
    st.session_state.answered = False
    st.session_state.last_feedback = ""
    st.session_state.stage = "flash"

def make_choices(target, batch):
    pool = [w for w in batch if w["word"] != target["word"]]
    distractors = random.sample(pool, min(3, len(pool)))
    choices = [target] + distractors
    random.shuffle(choices)
    return choices

init_state()
if not st.session_state.quiz_items:
    start_set()

# -------------------- 상단 --------------------
st.markdown('<div class="brand">🧭 SkyTrip Voca</div><div class="brand-sub">오늘의 단어 여행을 시작해요</div>', unsafe_allow_html=True)
st.markdown("""<div class="hero"><h2>단어를 모아 떠나는 영어 여행 ✈</h2>
초급부터 고급까지, 20개 단어씩 차근차근! 플래시카드로 익히고 철자·뜻 퀴즈와 문장 속 빈칸으로 내 것으로 만들어 보세요.<br><b>SEOUL ───── ✈ ───── WORLD OF WORDS</b></div>""", unsafe_allow_html=True)

# -------------------- 레벨 / 진도 --------------------
left, right = st.columns([1, 3], gap="medium")
with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### 🗺️ 학습 레벨 선택")
    selected_level = st.radio("레벨", LEVELS, index=LEVELS.index(st.session_state.level), horizontal=False, label_visibility="collapsed")
    if selected_level != st.session_state.level:
        st.session_state.level = selected_level
        st.session_state.set_index = 0
        start_set()
        st.rerun()
    all_count = len(level_words())
    done = min(st.session_state.set_index * 20, all_count)
    pct = done / all_count if all_count else 0
    st.markdown("---")
    st.caption("현재 레벨 학습 진도")
    st.progress(pct, text=f"{round(pct*100)}% · {done:,}/{all_count:,}개")
    st.caption("각 레벨은 20개 단어 단위로 진행돼요. 플래시카드 → 랜덤 퀴즈 → 문장 빈칸 순서로 학습합니다.")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    batch = current_words()
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    stage_names = {"flash":"1 카드", "quiz":"2 퀴즈", "cloze":"3 문장", "complete":"완료"}
    stage = st.session_state.stage
    st.markdown(f"#### {stage_names[stage]} · {st.session_state.level} 레벨")
    chosen_stage = st.radio("학습 단계", ["flash","quiz","cloze"], index=["flash","quiz","cloze"].index(stage) if stage in ["flash","quiz","cloze"] else 0, format_func=lambda x: {"flash":"1 카드","quiz":"2 퀴즈","cloze":"3 문장"}[x], horizontal=True, label_visibility="collapsed")
    if chosen_stage != stage and stage != "complete":
        st.session_state.stage = chosen_stage
        st.rerun()
    speech_col, restart_col = st.columns([2,1])
    with speech_col:
        st.session_state.speech = st.toggle("🔊 발음 듣기", value=st.session_state.speech)
    with restart_col:
        if st.button("↻ 세트 다시 시작", use_container_width=True):
            start_set(); st.rerun()

    # Flashcards
    if st.session_state.stage == "flash":
        w = batch[st.session_state.card_index]
        st.markdown('<div class="flashcard">', unsafe_allow_html=True)
        st.markdown(f'<div class="small-muted">WORD {st.session_state.card_index+1} / {len(batch)}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="word">{w["word"]}</div>', unsafe_allow_html=True)
        if st.session_state.revealed:
            st.markdown(f'<div class="meaning">{w["meaning"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="meaning" style="color:#9bb8c7">뜻을 확인해 보세요</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="example"><b>EXAMPLE</b><br>{w.get("example", "")}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.session_state.speech = st.checkbox("발음 듣기 사용", value=st.session_state.speech)
        if st.session_state.speech and st.button("🔊 현재 단어 발음 듣기"):
            js_word = json.dumps(w["word"])
            components.html(f"""<script>
            const utterance = new SpeechSynthesisUtterance({js_word});
            utterance.lang = 'en-US'; utterance.rate = 0.88;
            window.speechSynthesis.cancel(); window.speechSynthesis.speak(utterance);
            </script>""", height=0)
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("뜻 보기 / 숨기기", use_container_width=True):
                st.session_state.revealed = not st.session_state.revealed; st.rerun()
        with c2:
            if st.button("← 이전", disabled=st.session_state.card_index==0, use_container_width=True):
                st.session_state.card_index -= 1; st.session_state.revealed=False; st.rerun()
        with c3:
            if st.button("다음 단어 →", use_container_width=True):
                if st.session_state.card_index < len(batch)-1:
                    st.session_state.card_index += 1; st.session_state.revealed=False
                else:
                    st.session_state.stage="quiz"
                st.rerun()
        st.progress((st.session_state.card_index+1)/len(batch), text=f"{st.session_state.card_index} / {len(batch)} 학습 완료")
        if st.button("플래시카드 완료 · 퀴즈 시작 →", type="primary", use_container_width=True):
            st.session_state.stage="quiz"; st.session_state.quiz_index=0; st.rerun()

    # Multiple-choice quiz
    elif st.session_state.stage == "quiz":
        if st.session_state.quiz_index >= len(st.session_state.quiz_items):
            st.session_state.stage="cloze"; st.session_state.cloze_index=0; st.rerun()
        item = st.session_state.quiz_items[st.session_state.quiz_index]
        target = item["word"]
        if not st.session_state.quiz_choices:
            st.session_state.quiz_choices = make_choices(target,batch)
        st.caption("SPELLING QUIZ" if item["type"]=="spelling" else "MEANING QUIZ")
        q = f'‘{target["meaning"]}’에 해당하는 영어 단어는?' if item["type"]=="spelling" else f'‘{target["word"]}’의 뜻은 무엇일까요?'
        st.markdown(f'<div class="question">{q}</div>', unsafe_allow_html=True)
        st.caption("올바른 철자를 선택하세요. 첫 오답부터 힌트가 나타납니다." if item["type"]=="spelling" else "가장 알맞은 한국어 뜻을 선택하세요.")
        for i, choice in enumerate(st.session_state.quiz_choices):
            label = choice["word"] if item["type"]=="spelling" else choice["meaning"]
            if st.button(label, key=f"quiz_{st.session_state.quiz_index}_{i}", use_container_width=True, disabled=(st.session_state.answered or str(i) in st.session_state.quiz_wrong)):
                st.session_state.total += 1
                if choice["word"] == target["word"]:
                    st.session_state.correct += 1
                    st.session_state.answered = True
                    st.session_state.last_feedback = f'정답이에요! {target["word"]} — {target["meaning"]}'
                    st.session_state.last_feedback_type = "good"
                else:
                    st.session_state.quiz_wrong.append(str(i))
                    hint = f'힌트: 첫 글자는 {target["word"][0].upper()}, 글자 수는 {len(target["word"])}개입니다.' if item["type"]=="spelling" else "다른 선택지를 다시 골라보세요."
                    st.session_state.last_feedback = "아쉬워요. 다시 골라보세요. " + hint
                    st.session_state.last_feedback_type = "bad"
                st.rerun()
        if st.session_state.last_feedback:
            cls = "good" if st.session_state.last_feedback_type=="good" else "bad"
            st.markdown(f'<div class="feedback {cls}">{st.session_state.last_feedback}</div>', unsafe_allow_html=True)
        st.caption(f'{st.session_state.quiz_index+1} / {len(st.session_state.quiz_items)} 문제')
        if st.session_state.answered and st.button("다음 문제 →", type="primary"):
            st.session_state.quiz_index += 1
            st.session_state.answered=False; st.session_state.quiz_choices=[]; st.session_state.quiz_wrong=[]; st.session_state.last_feedback=""; st.rerun()

    # Sentence cloze
    elif st.session_state.stage == "cloze":
        if st.session_state.cloze_index >= len(st.session_state.cloze_items):
            st.session_state.stage="complete"; st.rerun()
        target = st.session_state.cloze_items[st.session_state.cloze_index]
        if not st.session_state.cloze_choices:
            st.session_state.cloze_choices = make_choices(target,batch)
        sentence = target.get("example") or f'We learned about {target["word"]} during our trip.'
        pattern = re.compile(rf'\b{re.escape(target["word"])}\b', re.IGNORECASE)
        sentence_blank = pattern.sub("______", sentence, count=1)
        st.caption("SENTENCE CLOZE")
        st.markdown('<div class="question">문장 속 빈칸에 알맞은 단어를 골라보세요.</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="flashcard" style="font-size:1.1rem;line-height:1.8">{sentence_blank}</div>', unsafe_allow_html=True)
        for i, choice in enumerate(st.session_state.cloze_choices):
            if st.button(choice["word"], key=f"cloze_{st.session_state.cloze_index}_{i}", use_container_width=True, disabled=(st.session_state.answered or str(i) in st.session_state.cloze_wrong)):
                st.session_state.total += 1
                if choice["word"] == target["word"]:
                    st.session_state.correct += 1
                    st.session_state.answered = True
                    st.session_state.last_feedback = f'정답! {target["word"]}의 뜻은 ‘{target["meaning"]}’입니다.'
                    st.session_state.last_feedback_type = "good"
                else:
                    st.session_state.cloze_wrong.append(str(i))
                    st.session_state.last_feedback = f'다시 골라보세요. 힌트: {target["meaning"]}와 관련된 단어를 찾아보세요.'
                    st.session_state.last_feedback_type = "bad"
                st.rerun()
        if st.session_state.last_feedback:
            cls = "good" if st.session_state.last_feedback_type=="good" else "bad"
            st.markdown(f'<div class="feedback {cls}">{st.session_state.last_feedback}</div>', unsafe_allow_html=True)
        st.caption(f'{st.session_state.cloze_index+1} / {len(st.session_state.cloze_items)} 문장')
        if st.session_state.answered and st.button("다음 문장 →", type="primary"):
            st.session_state.cloze_index += 1
            st.session_state.answered=False; st.session_state.cloze_choices=[]; st.session_state.cloze_wrong=[]; st.session_state.last_feedback=""; st.rerun()

    # Completion
    elif st.session_state.stage == "complete":
        rate = round(st.session_state.correct/st.session_state.total*100) if st.session_state.total else 0
        st.markdown("## 🏝️ 이번 여행 코스를 완료했어요!")
        st.write("20개 단어 학습을 마쳤습니다. 다음 세트로 이동하거나 같은 세트를 다시 학습해보세요.")
        a,b,c = st.columns(3)
        a.metric("정답", st.session_state.correct)
        b.metric("응답", st.session_state.total)
        c.metric("정답률", f"{rate}%")
        if st.button("다음 20개 단어 여행하기 →", type="primary", use_container_width=True):
            st.session_state.set_index += 1
            if st.session_state.set_index*20 >= len(level_words()): st.session_state.set_index=0
            start_set(); st.rerun()
        if st.button("이 세트 다시 학습", use_container_width=True):
            start_set(); st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

st.caption("SkyTrip Voca · 작은 단어가 모여 큰 여행이 됩니다.")
