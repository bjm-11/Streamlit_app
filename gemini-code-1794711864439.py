import json
import random
import re
from pathlib import Path
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Voca 3,000", page_icon="📚", layout="centered")

CSV_FILE = Path("Voca_3000.csv")
PROGRESS_FILE = Path("progress_3000.json")
BATCH_SIZE = 20
LEVEL_NAMES = {"Elementary": "초급", "MidHigh": "중급", "Extended": "고급"}

EXACT_SENTENCES = {
    "a": ("She bought a new notebook for her English class.", "그녀는 영어 수업을 위해 새 공책 하나를 샀다."),
    "an": ("He ate an apple after finishing his lunch.", "그는 점심을 다 먹은 후 사과 하나를 먹었다."),
    "the": ("Please close the window before you leave.", "나가기 전에 그 창문을 닫아 주세요."),
    "i": ("I always check my schedule every morning.", "나는 매일 아침 내 일정을 확인한다."),
    "you": ("You can ask me whenever you need help.", "도움이 필요할 때 언제든 나에게 물어볼 수 있다."),
    "he": ("He arrived at the station ten minutes early.", "그는 역에 10분 일찍 도착했다."),
    "she": ("She finished her report before the deadline.", "그녀는 마감 기한 전에 보고서를 끝냈다."),
    "it": ("It looks like a great plan for our team.", "그것은 우리 팀에 아주 좋은 계획처럼 보인다."),
    "we": ("We decided to start the project next Monday.", "우리는 다음 주 월요일에 프로젝트를 시작하기로 결정했다."),
    "they": ("They shared their ideas during the meeting.", "그들은 회의 중에 각자의 아이디어를 공유했다."),
}

VERB_TPL = [("The team worked hard to {w} the new system.", "팀은 새로운 시스템을 '{m}' 위해 열심히 일했다.")]
ADJ_TPL = [("The instructor gave a very {w} explanation to the class.", "강사는 수업에서 매우 {m} 설명을 해 주었다.")]
ADV_TPL = [("She explained the whole procedure {w} to the new staff.", "그녀는 신입 직원들에게 전체 절차를 {m} 설명했다.")]
NOUN_TPL = [("The article discusses the role of {w} in modern society.", "그 기사는 현대 사회에서 {m}의 역할을 다룬다.")]


def make_sentence(word, meaning, idx):
    wl = word.lower().strip()
    m = meaning.strip()
    if wl in EXACT_SENTENCES:
        en, ko = EXACT_SENTENCES[wl]
    elif wl.endswith("ly") and len(wl) > 4:
        t_en, t_ko = ADV_TPL[0]
        en, ko = t_en.format(w=word), t_ko.format(m=m)
    elif m.endswith("다") and m not in {"바다", "사다", "마다", "보다"}:
        t_en, t_ko = VERB_TPL[0]
        en, ko = t_en.format(w=word), t_ko.format(m=m)
    elif m.endswith(("한", "인", "운", "은", "는", "적", "의")):
        t_en, t_ko = ADJ_TPL[0]
        en, ko = t_en.format(w=word), t_ko.format(m=m)
    else:
        t_en, t_ko = NOUN_TPL[0]
        en, ko = t_en.format(w=word), t_ko.format(m=m)
    pat = re.compile(rf"(?<![A-Za-z-]){re.escape(word)}(?![A-Za-z-])", re.IGNORECASE)
    if not pat.search(en):
        en = "Please study the exact usage of " + word + " in this context."
        ko = "이 문맥에서 " + m + "의 정확한 쓰임을 학습해 보세요."
    blank = pat.sub("_____", en, count=1)
    return en, blank, ko


@st.cache_data
def load_words():
    if not CSV_FILE.exists():
        return []
    df = pd.read_csv(CSV_FILE)
    items = []
    for idx, r in df.iterrows():
        w = str(r["Word"]).strip()
        m = str(r["Korean meaning (뜻)"]).strip()
        lvl = str(r["Level"]).strip()
        no = int(r["No."])
        en, blank, ko = make_sentence(w, m, idx)
        items.append({
            "id": no,
            "word": w,
            "meaning": m,
            "level": lvl,
            "sentence": en,
            "blank": blank,
            "ko": ko,
        })
    return items


def speak(text, key_tag):
    safe = json.dumps(text)
    h = "<script>(function(){var s=window.parent.speechSynthesis||window.speechSynthesis;if(!s)return;s.cancel();var u=new SpeechSynthesisUtterance(" + safe + ");u.lang='en-US';u.rate=0.92;s.speak(u);})();</script><div style='display:none'>" + key_tag + "</div>"
    components.html(h, height=0)


def load_prog():
    if PROGRESS_FILE.exists():
        try:
            data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
            return {"mastered": list(dict.fromkeys(data.get("mastered", []))), "wrong": list(dict.fromkeys(data.get("wrong", [])))}
        except Exception:
            pass
    return {"mastered": [], "wrong": []}


def save_prog(prog):
    try:
        PROGRESS_FILE.write_text(json.dumps(prog, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


words = load_words()
if not words:
    st.error("Voca_3000.csv 파일을 찾을 수 없습니다.")
    st.stop()

if "prog" not in st.session_state:
    st.session_state.prog = load_prog()
if "audio_on" not in st.session_state:
    st.session_state.audio_on = True

with st.sidebar:
    st.header("학습 설정")
    lvl = st.selectbox("레벨", ["Elementary", "MidHigh", "Extended"], format_func=lambda x: LEVEL_NAMES[x])
    lvl_words = [w for w in words if w["level"] == lvl]
    total_sets = max(1, (len(lvl_words) + BATCH_SIZE - 1) // BATCH_SIZE)
    set_i = st.selectbox("20단어 세트", list(range(total_sets)), format_func=lambda i: "Set " + str(i + 1))
    st.session_state.audio_on = st.toggle("Flashcard 발음 듣기 ON/OFF", value=st.session_state.audio_on)
    st.divider()
    st.caption("완전 학습: " + str(len(st.session_state.prog["mastered"])) + " / " + str(len(words)))
    st.caption("오답 기록: " + str(len(st.session_state.prog["wrong"])))

batch = lvl_words[set_i * BATCH_SIZE : (set_i + 1) * BATCH_SIZE]
state_key = lvl + "_" + str(set_i)
if st.session_state.get("cur_key") != state_key:
    st.session_state.cur_key = state_key
    st.session_state.stage = "flashcard"
    st.session_state.fc_i = 0
    st.session_state.fc_show = False
    st.session_state.tts_n = 0
    pool_w = [w["word"] for w in lvl_words]
    pool_m = list({w["meaning"] for w in lvl_words})
    q2 = []
    for it in batch:
        if random.choice(["spell", "mean"]) == "spell":
            d = random.sample([x for x in pool_w if x != it["word"]], min(3, len(pool_w) - 1))
            opts = d + [it["word"]]
            random.shuffle(opts)
            q2.append({"kind": "spell", "item": it, "prompt": "다음 뜻에 해당하는 올바른 영어 철자는? → **" + it["meaning"] + "**", "ans": it["word"], "opts": opts})
        else:
            d = random.sample([x for x in pool_m if x != it["meaning"]], min(3, len(pool_m) - 1))
            opts = d + [it["meaning"]]
            random.shuffle(opts)
            q2.append({"kind": "mean", "item": it, "prompt": "다음 영어 단어의 뜻은? → **" + it["word"] + "**", "ans": it["meaning"], "opts": opts})
    random.shuffle(q2)
    st.session_state.q2 = q2
    st.session_state.q2_i = 0
    st.session_state.q2_bad = []
    q3 = []
    for it in batch:
        d = random.sample([x for x in pool_w if x != it["word"]], min(3, len(pool_w) - 1))
        opts = d + [it["word"]]
        random.shuffle(opts)
        q3.append({"item": it, "ans": it["word"], "opts": opts})
    random.shuffle(q3)
    st.session_state.q3 = q3
    st.session_state.q3_i = 0
    st.session_state.q3_bad = []

st.title("📚 Voca 3,000 학습장")
st.caption(LEVEL_NAMES[lvl] + " · Set " + str(set_i + 1) + " (20단어)")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("1. Flashcard", use_container_width=True, type=("primary" if st.session_state.stage == "flashcard" else "secondary")):
        st.session_state.stage = "flashcard"
        st.rerun()
with c2:
    if st.button("2. Spelling & 뜻 Quiz", use_container_width=True, type=("primary" if st.session_state.stage == "q2" else "secondary")):
        st.session_state.stage = "q2"
        st.rerun()
with c3:
    if st.button("3. 예문 빈칸 Quiz", use_container_width=True, type=("primary" if st.session_state.stage == "q3" else "secondary")):
        st.session_state.stage = "q3"
        st.rerun()

st.divider()

if st.session_state.stage == "flashcard":
    i = st.session_state.fc_i
    it = batch[i]
    top1, top2 = st.columns([3, 1])
    with top1:
        st.subheader("카드 " + str(i + 1) + " / " + str(len(batch)) + " (#" + str(it["id"]) + ")")
    with top2:
        if st.button("🔊 발음 듣기", key="spk_" + state_key + "_" + str(i), use_container_width=True):
            st.session_state.tts_n += 1
            speak(it["word"], "m_" + str(i) + "_" + str(st.session_state.tts_n))
    auto_id = "a_" + state_key + "_" + str(i)
    if st.session_state.audio_on and st.session_state.get("last_a") != auto_id:
        st.session_state.last_a = auto_id
        speak(it["word"], auto_id)
    with st.container(border=True):
        st.markdown("## " + it["word"])
        if st.session_state.fc_show:
            st.divider()
            st.markdown("### " + it["meaning"])
            st.info("예문: " + it["sentence"] + "\n\n해석: " + it["ko"])
        else:
            if st.button("뜻 & 예문 보기", key="show_" + state_key + "_" + str(i), use_container_width=True):
                st.session_state.fc_show = True
                st.rerun()
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("⬅️ 이전", disabled=(i == 0), key="prev_" + state_key + "_" + str(i), use_container_width=True):
            st.session_state.fc_i -= 1
            st.session_state.fc_show = False
            st.rerun()
    with b2:
        if st.button("다음 ➡️", disabled=(i >= len(batch) - 1), key="next_" + state_key + "_" + str(i), use_container_width=True):
            st.session_state.fc_i += 1
            st.session_state.fc_show = False
            st.rerun()
    with b3:
        if st.button("2단계 퀴즈로 ➡️", type="primary", key="go2_" + state_key + "_" + str(i), use_container_width=True):
            st.session_state.stage = "q2"
            st.rerun()

elif st.session_state.stage == "q2":
    qlist = st.session_state.q2
    qi = st.session_state.q2_i
    if qi >= len(qlist):
        st.success("2단계 퀴즈를 모두 마쳤습니다!")
        if st.button("3단계 예문 빈칸 Quiz로 ➡️", type="primary", key="to3_" + state_key, use_container_width=True):
            st.session_state.stage = "q3"
            st.rerun()
    else:
        q = qlist[qi]
        it = q["item"]
        bad = st.session_state.q2_bad
        st.subheader("문제 " + str(qi + 1) + " / " + str(len(qlist)))
        with st.container(border=True):
            st.markdown("### " + q["prompt"])
            if q["kind"] == "mean":
                if st.button("🔊 발음 듣기", key="q2s_" + state_key + "_" + str(qi)):
                    st.session_state.tts_n += 1
                    speak(it["word"], "q2_" + str(qi) + "_" + str(st.session_state.tts_n))
        if bad:
            st.error("오답입니다! 힌트를 보고 다시 선택해 보세요.")
            if q["kind"] == "spell":
                w = it["word"]
                st.warning("힌트: 첫 글자는 '" + w[0] + "', 글자 수는 " + str(len(w)) + "글자입니다.")
            else:
                st.warning("힌트: 예문 → " + it["sentence"])
        cols = st.columns(2)
        for idx_o, opt in enumerate(q["opts"]):
            is_bad = opt in bad
            lbl = ("❌ " + opt) if is_bad else opt
            with cols[idx_o % 2]:
                if st.button(lbl, disabled=is_bad, key="q2o_" + state_key + "_" + str(qi) + "_" + str(idx_o), use_container_width=True):
                    if opt == q["ans"]:
                        st.session_state.q2_i += 1
                        st.session_state.q2_bad = []
                        st.rerun()
                    else:
                        if it["id"] not in st.session_state.prog["wrong
