import json
import random
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Voca 3,000 학습장", page_icon="📚", layout="centered")

CSV_PATH = Path("Voca_3000.csv")
BATCH_SIZE = 20
LEVEL_MAP = {
    "Elementary": "초급 (Elementary)",
    "MidHigh": "중급 (MidHigh)",
    "Extended": "고급 (Extended)",
}


@st.cache_data
def load_words():
    if not CSV_PATH.exists():
        return []
    df = pd.read_csv(CSV_PATH)
    rows = []
    for _, r in df.iterrows():
        var_val = r.get("Variation", "")
        var_str = "" if pd.isna(var_val) else str(var_val).strip()
        rows.append({
            "id": int(r["No."]),
            "word": str(r["Word"]).strip(),
            "level": str(r["Level"]).strip(),
            "meaning": str(r["Korean meaning (뜻)"]).strip(),
            "variation": var_str,
        })
    return rows


words = load_words()
if not words:
    st.error("`Voca_3000.csv` 파일을 찾을 수 없습니다. 앱 파일과 같은 위치에 올려주세요.")
    st.stop()

st.title("📚 Voca 3,000 단어장 & 퀴즈")

with st.sidebar:
    level = st.selectbox(
        "레벨 선택",
        options=["Elementary", "MidHigh", "Extended"],
        format_func=lambda x: LEVEL_MAP[x],
    )
    level_words = [w for w in words if w["level"] == level]
    total_sets = max(1, (len(level_words) + BATCH_SIZE - 1) // BATCH_SIZE)
    set_idx = st.selectbox(
        f"세트 선택 (총 {len(level_words)}단어 / {total_sets}세트)",
        options=list(range(total_sets)),
        format_func=lambda i: f"Set {i + 1} ({i * BATCH_SIZE + 1} ~ {min((i + 1) * BATCH_SIZE, len(level_words))}번)",
    )

batch = level_words[set_idx * BATCH_SIZE : (set_idx + 1) * BATCH_SIZE]
mode = st.radio("학습 모드", ["플래시카드", "뜻/철자 퀴즈"], horizontal=True)

if mode == "플래시카드":
    idx = st.number_input("카드 번호", min_value=1, max_value=len(batch), value=1, step=1) - 1
    item = batch[idx]
    st.subheader(f"#{item['id']} · {item['word']}")
    if item["variation"]:
        st.caption(f"변형/관련어: {item['variation']}")
    if st.toggle("뜻 보기"):
        st.success(item["meaning"])
else:
    q_key = f"q_{level}_{set_idx}"
    if q_key not in st.session_state:
        target = random.choice(batch)
        ask_word = random.choice([True, False])
        pool_w = [w["word"] for w in level_words if w["word"] != target["word"]]
        pool_m = list({w["meaning"] for w in level_words if w["meaning"] != target["meaning"]})
        if ask_word:
            opts = random.sample(pool_w, min(3, len(pool_w))) + [target["word"]]
            prompt = f"뜻 **'{target['meaning']}'** 에 알맞은 영어 단어는?"
            ans = target["word"]
        else:
            opts = random.sample(pool_m, min(3, len(pool_m))) + [target["meaning"]]
            prompt = f"단어 **'{target['word']}'** 의 뜻은?"
            ans = target["meaning"]
        random.shuffle(opts)
        st.session_state[q_key] = {"prompt": prompt, "ans": ans, "opts": opts}

    q = st.session_state[q_key]
    st.markdown(f"### {q['prompt']}")
    choice = st.radio("보기 선택", q["opts"], key=f"choice_{q_key}")
    if st.button("정답 확인"):
        if choice == q["ans"]:
            st.success("정답입니다!")
        else:
            st.error(f"오답입니다. 정답은 **{q['ans']}** 입니다.")
    if st.button("다음 문제"):
        del st.session_state[q_key]
        st.rerun()
