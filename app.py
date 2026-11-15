import json
import random
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="3,000단어 랜덤 학습장", page_icon="📚", layout="centered")

PROGRESS_FILE = Path("progress.json")
BATCH_SIZE = 20

# 내장 단어 데이터 (이 리스트에 3,000여 개 단어를 모두 넣어 하나의 파일로 실행할 수 있습니다)
BUILTIN_WORDS = [
    {"id": 1, "word": "abundant", "meaning": "풍부한, 많은"},
    {"id": 2, "word": "benevolent", "meaning": "자애로운, 인정 많은"},
    {"id": 3, "word": "candid", "meaning": "솔직한, 숨김없는"},
    {"id": 4, "word": "diligent", "meaning": "근면한, 성실한"},
    {"id": 5, "word": "eloquent", "meaning": "웅변의, 달변인"},
    {"id": 6, "word": "frugal", "meaning": "검소한, 절약하는"},
    {"id": 7, "word": "gregarious", "meaning": "사교적인"},
    {"id": 8, "word": "hinder", "meaning": "방해하다, 지연시키다"},
    {"id": 9, "word": "impartial", "meaning": "공정한, 치우치지 않는"},
    {"id": 10, "word": "jeopardy", "meaning": "위험, 위태로움"},
    {"id": 11, "word": "keen", "meaning": "예리한, 열망하는"},
    {"id": 12, "word": "lucid", "meaning": "명쾌한, 투명한"},
    {"id": 13, "word": "meticulous", "meaning": "꼼꼼한, 세심한"},
    {"id": 14, "word": "novel", "meaning": "새로운, 참신한"},
    {"id": 15, "word": "obscure", "meaning": "모호한, 무명의"},
    {"id": 16, "word": "pragmatic", "meaning": "실용적인, 현실적인"},
    {"id": 17, "word": "quaint", "meaning": "고풍스러운, 진기한"},
    {"id": 18, "word": "resilient", "meaning": "회복력이 있는, 탄력 있는"},
    {"id": 19, "word": "scrutinize", "meaning": "면밀히 조사하다"},
    {"id": 20, "word": "tenacious", "meaning": "집요한, 완강한"},
]


def load_words(uploaded_json=None) -> list[dict]:
    """업로드된 JSON 파일이 있으면 사용하고, 없으면 내장 단어 목록(BUILTIN_WORDS)을 사용합니다."""
    if uploaded_json is not None:
        raw = json.load(uploaded_json)
        words = []
        for idx, item in enumerate(raw, start=1):
            word = str(item.get("word", "")).strip()
            meaning = str(item.get("meaning", "")).strip()
            if word and meaning:
                words.append({
                    "id": int(item.get("id", idx)),
                    "word": word,
                    "meaning": meaning,
                })
        if words:
            return words

    return BUILTIN_WORDS


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                "learned_ids": list(dict.fromkeys(data.get("learned_ids", []))),
                "wrong_ids": list(dict.fromkeys(data.get("wrong_ids", []))),
            }
    return {"learned_ids": [], "wrong_ids": []}


def save_progress(progress: dict) -> None:
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def start_batch(mode: str) -> None:
    """mode='all'이면 미학습 단어 위주로 20개, mode='wrong'이면 틀린 단어 중 20개를 랜덤 선택합니다."""
    words = st.session_state.words
    id_map = {w["id"]: w for w in words}
    learned_set = set(st.session_state.progress["learned_ids"])
    wrong_set = set(st.session_state.progress["wrong_ids"])

    if mode == "wrong":
        pool = [id_map[wid] for wid in wrong_set if wid in id_map]
    else:
        unlearned = [w for w in words if w["id"] not in learned_set]
        if len(unlearned) >= BATCH_SIZE:
            pool = unlearned
        else:
            pool = unlearned + [w for w in words if w["id"] in learned_set]

    random.shuffle(pool)
    st.session_state.mode = mode
    st.session_state.batch = pool[:BATCH_SIZE]
    st.session_state.index = 0
    st.session_state.reveal = False


with st.sidebar:
    st.header("📂 단어 데이터")
    uploaded_file = st.file_uploader(
        "JSON 단어장 불러오기 (선택)",
        type=["json"],
        help="별도 JSON 파일이 없으면 코드 내 BUILTIN_WORDS 데이터를 바로 사용합니다.",
    )

current_words = load_words(uploaded_file)

if "words" not in st.session_state or len(st.session_state.words) != len(current_words):
    st.session_state.words = current_words
    if "progress" not in st.session_state:
        st.session_state.progress = load_progress()
    start_batch("all")

if "progress" not in st.session_state:
    st.session_state.progress = load_progress()
if "batch" not in st.session_state:
    start_batch("all")

valid_ids = {w["id"] for w in st.session_state.words}
learned_set = set(st.session_state.progress["learned_ids"]) & valid_ids
wrong_set = set(st.session_state.progress["wrong_ids"]) & valid_ids
total_words = len(st.session_state.words)

with st.sidebar:
    st.divider()
    st.header("📊 전체 학습 진도")
    ratio = (len(learned_set) / total_words) if total_words else 0.0
    st.progress(ratio, text=f"학습 완료: {len(learned_set)} / {total_words} ({ratio * 100:.1f}%)")
    st.write(f"- 남은 미학습 단어: **{max(0, total_words - len(learned_set))}개**")
    st.write(f"- 틀린 단어(복습 대상): **{len(wrong_set)}개**")

    st.divider()
    st.download_button(
        label="💾 학습 진도 JSON 백업",
        data=json.dumps(st.session_state.progress, ensure_ascii=False, indent=2),
        file_name="progress.json",
        mime="application/json",
        use_container_width=True,
    )
    if st.button("🔄 전체 진도 초기화", use_container_width=True):
        st.session_state.progress = {"learned_ids": [], "wrong_ids": []}
        save_progress(st.session_state.progress)
        start_batch(st.session_state.mode)
        st.rerun()

st.title("📖 20단어 랜덤 학습 & 오답 복습")

c1, c2 = st.columns(2)
with c1:
    if st.button(
        "🎲 20단어 랜덤 시작",
        use_container_width=True,
        type="primary" if st.session_state.mode == "all" else "secondary",
    ):
        start_batch("all")
        st.rerun()
with c2:
    if st.button(
        f"❌ 틀린 단어 복습 ({len(wrong_set)}개)",
        use_container_width=True,
        disabled=(len(wrong_set) == 0),
    ):
        start_batch("wrong")
        st.rerun()

batch = st.session_state.batch
idx = st.session_state.index

if not batch:
    st.info("현재 선택된 모드에 학습할 단어가 없습니다.")
    st.stop()

if idx >= len(batch):
    st.success(f"🎉 {len(batch)}단어 세트를 마쳤습니다!")
    if st.button("다음 20단어 뽑기", use_container_width=True, type="primary"):
        start_batch(st.session_state.mode)
        st.rerun()
    st.stop()

item = batch[idx]
wid = item["id"]

st.caption(
    f"세트 진행: {idx + 1} / {len(batch)}  |  "
    f"모드: {'일반 20단어' if st.session_state.mode == 'all' else '틀린 단어 복습'}"
)

with st.container(border=True):
    st.markdown(f"## {item['word']}")
    if st.session_state.reveal:
        st.divider()
        st.markdown(f"### {item['meaning']}")
    else:
        if st.button("뜻 보기", use_container_width=True):
            st.session_state.reveal = True
            st.rerun()

col_bad, col_good = st.columns(2)
with col_bad:
    if st.button("😵 틀렸어요 (복습 추가)", use_container_width=True):
        if wid not in st.session_state.progress["wrong_ids"]:
            st.session_state.progress["wrong_ids"].append(wid)
        save_progress(st.session_state.progress)
        st.session_state.index += 1
        st.session_state.reveal = False
        st.rerun()

with col_good:
    if st.button("✅ 맞았어요 (완료)", use_container_width=True, type="primary"):
        if wid not in st.session_state.progress["learned_ids"]:
            st.session_state.progress["learned_ids"].append(wid)
        if wid in st.session_state.progress["wrong_ids"]:
            st.session_state.progress["wrong_ids"].remove(wid)
        save_progress(st.session_state.progress)
        st.session_state.index += 1
        st.session_state.reveal = False
        st.rerun()
