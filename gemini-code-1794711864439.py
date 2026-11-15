import json
import random
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Voca 3,000", page_icon="📚", layout="centered")

CSV_FILE = Path("Voca_3000.csv")
BATCH_SIZE = 20
LEVEL_NAMES = {"Elementary": "초급", "MidHigh": "중급", "Extended": "고급"}

@st.cache_data
def load_data():
    if not CSV_FILE.exists():
        return []
    df = pd.read_csv(CSV_FILE)
    out = []
    for _, r in df.iterrows():
        w = str(r["Word"]).strip()
        m = str(r["Korean meaning (뜻)"]).strip()
        lvl = str(r["Level"]).strip()
        no = int(r["No."])
        out.append({
            "no": no,
            "word": w,
            "meaning": m,
            "level": lvl,
            "sentence": f"Please use {w} in a clear English sentence.",
            "blank": "Please use _____ in a clear English sentence.",
            "ko": f"이 문장에서 {m}의 쓰임을 확인하세요.",
        })
    return out

words = load_data()
if not words:
    st.error("Voca_3000.csv 파일이 없습니다.")
    st.stop()

st.title("📚 Voca 3,000 학습 및 퀴즈")

lvl = st.selectbox("레벨", ["Elementary", "MidHigh", "Extended"], format_func=lambda x: LEVEL_NAMES[x])
lvl_words = [w for w in words if w["level"] == lvl]
total_sets = max(1, (len(lvl_words) + BATCH_SIZE - 1) // BATCH_SIZE)
set_i = st.selectbox("세트 (20단어)", list(range(total_sets)), format_func=lambda i: f"Set {i + 1}")
batch = lvl_words[set_i * BATCH_SIZE : (set_i + 1) * BATCH_SIZE]

tab = st.radio("단계 선택", ["플래시카드", "철자/뜻 퀴즈", "예문 빈칸 퀴즈"], horizontal=True)

if tab == "플래시카드":
    idx = st.number_input("카드 번호", 1, len(batch), 1) - 1
    item = batch[idx]
    st.subheader(f"#{item['no']} {item['word']}")
    if st.toggle("뜻과 예문 보기"):
        st.info(f"{item['meaning']} | {item['sentence']} ({item['ko']})")

elif tab == "철자/뜻 퀴즈":
    key = f"q2_{lvl}_{set_i}"
    if key not in st.session_state:
        t = random.choice(batch)
        ask_spell = random.choice([True, False])
        if ask_spell:
            pool = [w["word"] for w in lvl_words if w["word"] != t["word"]]
            opts = random.sample(pool, min(3, len(pool))) + [t["word"]]
            q_text = "뜻: " + t["meaning"] + " -> 알맞은 단어는?"
            ans = t["word"]
        else:
            pool = list({w["meaning"] for w in lvl_words if w["meaning"] != t["meaning"]})
            opts = random.sample(pool, min(3, len(pool))) + [t["meaning"]]
            q_text = "단어: " + t["word"] + " -> 뜻은?"
            ans = t["meaning"]
        random.shuffle(opts)
        st.session_state[key] = {"q": q_text, "ans": ans, "opts": opts}
    q = st.session_state[key]
    st.write(q["q"])
    pick = st.radio("선택", q["opts"], key=f"pick_{key}")
    if st.button("확인", key=f"chk_{key}"):
        st.success("정답!") if pick == q["ans"] else st.error("오답! 정답: " + q["ans"])
    if st.button("새 문제", key=f"nxt_{key}"):
        del st.session_state[key]
        st.rerun()

else:
    key3 = f"q3_{lvl}_{set_i}"
    if key3 not in st.session_state:
        t = random.choice(batch)
        pool = [w["word"] for w in lvl_words if w["word"] != t["word"]]
        opts = random.sample(pool, min(3, len(pool))) + [t["word"]]
        random.shuffle(opts)
        st.session_state[key3] = {"item": t, "opts": opts}
    q3 = st.session_state[key3]
    st.write(q3["item"]["blank"])
    st.caption(q3["item"]["ko"])
    pick3 = st.radio("빈칸 단어 선택", q3["opts"], key=f"pick3_{key3}")
    if st.button("정답 확인", key=f"chk3_{key3}"):
        ans3 = q3["item"]["word"]
        st.success("정답!") if pick3 == ans3 else st.error("오답! 정답: " + ans3)
    if st.button("다음 빈칸 문제", key=f"nxt3_{key3}"):
        del st.session_state[key3]
        st.rerun()
