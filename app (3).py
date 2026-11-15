"""SkyTrip Voca - Streamlit 버전
Voca_3000.csv 를 읽어 플래시카드 → 뜻/철자 퀴즈 → 문장 빈칸 순서로 20개씩 학습합니다.

실행:  streamlit run app.py
"""
import html
import json
import random
import re
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

BASE = Path(__file__).parent
CSV_PATH = BASE / "Voca_3000.csv"
EXAMPLES_PATH = BASE / "examples.json"  # {"1": "예문", ...}  (No. 기준, 없어도 동작)
SET_SIZE = 20
LEVEL_MAP = {"Elementary": "초급", "MidHigh": "중급", "Extended": "고급"}
LEVELS = list(LEVEL_MAP.values())

st.set_page_config(page_title="SkyTrip Voca | 단어 여행", page_icon="🧭", layout="wide")

# ───────────────────────── 스타일 ─────────────────────────
st.markdown(
    """
<style>
.stApp{background:linear-gradient(135deg,#dff5ff,#f5fcff 55%,#d8f0ff)}
.block-container{max-width:1000px;padding-top:1.6rem}
.hero{background:linear-gradient(115deg,#80cff2,#c3edff);padding:22px 28px;border-radius:22px;
      box-shadow:0 12px 35px #2a83a91c;margin-bottom:18px}
.hero h2{margin:0 0 6px;color:#104e70;font-size:28px}
.hero p{margin:0;color:#205d7b;line-height:1.6}
.flashcard{min-height:240px;padding:28px;border-radius:22px;border:1px solid #cceaf8;
      background:linear-gradient(145deg,#fff,#f1fbff);box-shadow:0 12px 30px #207ca51b;
      text-align:center;margin:10px 0}
.flashcard .meta{font-size:12px;color:#8aa4b2}
.flashcard .word{font-size:52px;font-weight:900;color:#155a7c;margin:12px 0 6px;letter-spacing:-1px}
.flashcard .meaning{font-size:25px;font-weight:800;color:#217b9e;margin:6px 0}
.flashcard .hidden-meaning{font-size:15px;color:#9ab5c3;margin:14px 0}
.flashcard .example{margin:12px auto 0;max-width:640px;padding:12px 15px;border-radius:12px;
      background:#edf8fd;color:#315f75;font-size:14px;line-height:1.6}
.q-label{font-size:11px;font-weight:900;letter-spacing:1px;color:#4a9bc0}
.question{font-size:26px;font-weight:900;color:#174f6d;line-height:1.45;margin:8px 0}
.cloze{font-size:22px;line-height:1.7;color:#174f6d;background:#f5fbff;border:1px solid #d8edf7;
      border-radius:14px;padding:16px 18px;margin:10px 0 16px}
.cloze b.blank{color:#2696c9;letter-spacing:2px}
.stat-row{display:flex;gap:14px;justify-content:center;margin:18px 0}
.stat{background:#fff;border:1px solid #d6edf7;border-radius:14px;padding:14px 26px;text-align:center;color:#6b8a9a}
.stat b{display:block;font-size:28px;color:#145879}
</style>
""",
    unsafe_allow_html=True,
)


# ───────────────────────── 데이터 ─────────────────────────
@st.cache_data
def load_words():
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig", keep_default_na=False)
    df = df.rename(
        columns={
            "No.": "no",
            "Word": "word",
            "Level": "level",
            "Korean meaning (뜻)": "meaning",
            "Variation": "variation",
            "Star mark": "star",
        }
    )
    df["level"] = df["level"].map(LEVEL_MAP)
    for col in ("variation", "star"):
        df[col] = df[col].replace({"NA": "", "None": ""})
    examples = {}
    if EXAMPLES_PATH.exists():
        examples = json.loads(EXAMPLES_PATH.read_text(encoding="utf-8"))
    df["example"] = df["no"].astype(str).map(examples).fillna("")
    return df[["no", "word", "level", "meaning", "variation", "star", "example"]].to_dict("records")


WORDS = load_words()


def level_words(level):
    return [w for w in WORDS if w["level"] == level]


def esc(s):
    return html.escape(str(s))


# ───────────────────────── 상태 관리 ─────────────────────────
ss = st.session_state


def start_set():
    all_w = level_words(ss.level)
    words = all_w[ss.set_idx * SET_SIZE : ss.set_idx * SET_SIZE + SET_SIZE]
    if not words:
        ss.set_idx = 0
        words = all_w[:SET_SIZE]
    ss.words = words
    ss.stage = "flash"
    ss.card_idx = 0
    ss.revealed = False
    ss.correct = 0
    ss.total = 0
    ss.quiz_items = random.sample(
        [{"type": t, "word": w} for w in words for t in ("meaning", "spelling")],
        k=len(words) * 2,
    )
    ss.quiz_idx = 0
    ss.cloze_items = random.sample(words, k=len(words))
    ss.cloze_idx = 0
    ss.answered = False
    ss.choice_key = None
    ss.wrong_opts = set()


if "level" not in ss:
    ss.level = LEVELS[0]
    ss.set_idx = 0
    ss.speech = True
    start_set()


def select_level(level):
    ss.level = level
    ss.set_idx = 0
    start_set()


def go_stage(stage):
    if stage == "quiz" and ss.quiz_idx >= len(ss.quiz_items):
        ss.quiz_idx = 0
    if stage == "cloze" and ss.cloze_idx >= len(ss.cloze_items):
        ss.cloze_idx = 0
    ss.stage = stage
    ss.choice_key = None  # 선택지/오답 표시 초기화
    ss.answered = False


def next_card():
    if ss.card_idx < len(ss.words) - 1:
        ss.card_idx += 1
        ss.revealed = False
    else:
        begin_quiz()


def prev_card():
    if ss.card_idx > 0:
        ss.card_idx -= 1
        ss.revealed = False


def toggle_reveal():
    ss.revealed = not ss.revealed


def begin_quiz():
    ss.quiz_idx = 0
    go_stage("quiz")


def next_question():
    ss.quiz_idx += 1
    ss.choice_key = None
    ss.answered = False
    if ss.quiz_idx >= len(ss.quiz_items):
        ss.cloze_idx = 0
        go_stage("cloze")


def next_cloze():
    ss.cloze_idx += 1
    ss.choice_key = None
    ss.answered = False
    if ss.cloze_idx >= len(ss.cloze_items):
        go_stage("complete")


def next_set():
    ss.set_idx += 1
    if ss.set_idx * SET_SIZE >= len(level_words(ss.level)):
        ss.set_idx = 0
    start_set()


def answer(picked_word, target_word):
    if ss.answered:
        return
    ss.total += 1
    if picked_word == target_word:
        ss.answered = True
        ss.correct += 1
    else:
        ss.wrong_opts.add(picked_word)


def get_choices(key, target):
    """문제마다 한 번만 보기 4개를 만들어 rerun 사이에 유지한다."""
    if ss.choice_key != key:
        pool = random.sample([w for w in ss.words if w["word"] != target["word"]], k=min(3, len(ss.words) - 1))
        choices = pool + [target]
        random.shuffle(choices)
        ss.choices = choices
        ss.choice_key = key
        ss.wrong_opts = set()
        ss.answered = False
    return ss.choices


def render_options(kind, idx, target, label_of):
    choices = get_choices((kind, idx), target)
    cols = st.columns(2)
    for i, c in enumerate(choices):
        label = label_of(c)
        disabled = ss.answered or c["word"] in ss.wrong_opts
        if ss.answered and c["word"] == target["word"]:
            label = "✅ " + label
        elif c["word"] in ss.wrong_opts:
            label = "❌ " + label
        cols[i % 2].button(
            label,
            key=f"{kind}_{idx}_{i}",
            disabled=disabled,
            use_container_width=True,
            on_click=answer,
            args=(c["word"], target["word"]),
        )


def speak_widget(word, auto=False):
    """브라우저 내장 음성합성(Web Speech API)으로 발음 재생."""
    auto_js = "setTimeout(say,150);" if auto else ""
    components.html(
        f"""
<button id="b" style="padding:8px 14px;border-radius:10px;border:1px solid #cbe6f3;background:#e9f7fd;
  color:#197ca9;font-size:14px;font-weight:700;cursor:pointer">🔊 발음 듣기</button>
<script>
const w={json.dumps(word)};
function say(){{ if(!('speechSynthesis' in window)) return; speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(w); u.lang='en-US'; u.rate=.88; speechSynthesis.speak(u); }}
document.getElementById('b').onclick=say; {auto_js}
</script>""",
        height=50,
    )


def cloze_sentence(w, reveal=False):
    source = w["example"] or f"We learned about {w['word']} during our trip."
    pattern = re.compile(rf"\b{re.escape(w['word'])}\b", re.IGNORECASE)
    rep = f"<b style='color:#16845f'>{esc(w['word'])}</b>" if reveal else "<b class='blank'>______</b>"
    return pattern.sub(rep, esc(source), count=1)


# ───────────────────────── 사이드바 ─────────────────────────
with st.sidebar:
    st.subheader("🗺️ 학습 레벨 선택")
    for lv in LEVELS:
        st.button(
            f"{lv}  ·  {len(level_words(lv)):,}개",
            key=f"lv_{lv}",
            type="primary" if lv == ss.level else "secondary",
            use_container_width=True,
            on_click=select_level,
            args=(lv,),
        )
    total_lv = len(level_words(ss.level))
    done = min(ss.set_idx * SET_SIZE, total_lv)
    st.caption(f"현재 레벨 학습 진도 · {round(done / total_lv * 100) if total_lv else 0}%")
    st.progress(done / total_lv if total_lv else 0)
    st.checkbox("발음 자동 재생", key="speech")
    st.button("↻ 세트 다시 시작", on_click=start_set, use_container_width=True)
    st.caption("각 레벨은 20개 단어 단위로 진행돼요. 카드 → 퀴즈 → 문장 빈칸 순서로 학습합니다.")

# ───────────────────────── 본문 ─────────────────────────
st.markdown(
    """<div class="hero"><h2>🧭 SkyTrip Voca · 단어 여행</h2>
<p>초급부터 고급까지, 20개 단어씩 차근차근! 플래시카드로 익히고 뜻·철자 퀴즈와 문장 빈칸으로 내 것으로 만들어 보세요.</p></div>""",
    unsafe_allow_html=True,
)

tab_cols = st.columns(3)
for col, (stage, label) in zip(tab_cols, [("flash", "1 카드"), ("quiz", "2 퀴즈"), ("cloze", "3 문장")]):
    col.button(
        label,
        key=f"tab_{stage}",
        type="primary" if ss.stage == stage else "secondary",
        use_container_width=True,
        on_click=go_stage,
        args=(stage,),
    )

# ── 1) 플래시카드 ──
if ss.stage == "flash":
    w = ss.words[ss.card_idx]
    if ss.revealed:
        body = f"<div class='meaning'>{esc(w['meaning'])}</div>"
        if w["variation"]:
            body += f"<div class='meta'>변형: {esc(w['variation'])}</div>"
        if w["example"]:
            body += f"<div class='example'>{esc(w['example'])}</div>"
    else:
        body = "<div class='hidden-meaning'>‘뜻 보기’ 버튼을 눌러 뜻을 확인하세요</div>"
    st.markdown(
        f"""<div class="flashcard"><div class="meta">WORD {ss.card_idx + 1} / {len(ss.words)}</div>
<div class="word">{esc(w['word'])}</div>{body}</div>""",
        unsafe_allow_html=True,
    )
    speak_widget(w["word"], auto=ss.speech)
    c1, c2, c3 = st.columns(3)
    c1.button("뜻 보기" if not ss.revealed else "뜻 가리기", on_click=toggle_reveal, use_container_width=True)
    c2.button("← 이전", on_click=prev_card, disabled=ss.card_idx == 0, use_container_width=True)
    c3.button("다음 단어 →", on_click=next_card, type="primary", use_container_width=True)
    st.progress((ss.card_idx + 1) / len(ss.words))
    st.button("플래시카드 완료 · 퀴즈 시작 →", on_click=begin_quiz)

# ── 2) 뜻 / 철자 퀴즈 ──
elif ss.stage == "quiz":
    item = ss.quiz_items[ss.quiz_idx]
    w, spelling = item["word"], item["type"] == "spelling"
    st.markdown(
        f"""<div class="q-label">{'SPELLING QUIZ' if spelling else 'MEANING QUIZ'}</div>
<div class="question">{'‘' + esc(w['meaning']) + '’에 해당하는 영어 단어는?' if spelling else '‘' + esc(w['word']) + '’의 뜻은 무엇일까요?'}</div>""",
        unsafe_allow_html=True,
    )
    render_options("quiz", ss.quiz_idx, w, (lambda c: c["word"]) if spelling else (lambda c: c["meaning"]))
    if ss.answered:
        st.success(f"정답이에요! **{w['word']}** — {w['meaning']}")
        st.button("다음 문제 →", on_click=next_question, type="primary")
    elif ss.wrong_opts:
        hint = f"  \n힌트: 첫 글자는 **{w['word'][0].upper()}**, 글자 수는 **{len(w['word'])}개**" if spelling else ""
        st.error("아쉬워요. 다른 선택지를 다시 골라보세요." + hint)
    else:
        st.info("선택지를 누르면 바로 채점됩니다.")
    st.caption(f"{ss.quiz_idx + 1} / {len(ss.quiz_items)} 문제")

# ── 3) 문장 빈칸 ──
elif ss.stage == "cloze":
    w = ss.cloze_items[ss.cloze_idx]
    st.markdown(
        """<div class="q-label">SENTENCE CLOZE</div>
<div class="question">문장 속 빈칸에 알맞은 단어를 골라보세요.</div>""",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div class='cloze'>{cloze_sentence(w, reveal=ss.answered)}</div>", unsafe_allow_html=True)
    render_options("cloze", ss.cloze_idx, w, lambda c: c["word"])
    if ss.answered:
        st.success(f"정답! **{w['word']}** 의 뜻은 ‘{w['meaning']}’ 입니다.")
        st.button("다음 문장 →", on_click=next_cloze, type="primary")
    elif ss.wrong_opts:
        st.error(f"다시 골라보세요.  \n힌트: ‘{w['meaning']}’ 와 관련된 단어를 찾아보세요.")
    else:
        st.info("정답을 선택하면 뜻도 함께 확인할 수 있어요.")
    st.caption(f"{ss.cloze_idx + 1} / {len(ss.cloze_items)} 문장")

# ── 완료 ──
else:
    rate = round(ss.correct / ss.total * 100) if ss.total else 0
    st.markdown(
        f"""<div style="text-align:center;padding:20px 0"><div style="font-size:56px">🏝️</div>
<h2 style="color:#145879">이번 여행 코스를 완료했어요!</h2>
<p style="color:#6b8a9a">{len(ss.words)}개 단어 학습을 마쳤습니다.</p>
<div class="stat-row"><div class="stat"><b>{ss.correct}</b>정답</div>
<div class="stat"><b>{ss.total}</b>시도</div><div class="stat"><b>{rate}%</b>정답률</div></div></div>""",
        unsafe_allow_html=True,
    )
    more = (ss.set_idx + 1) * SET_SIZE < len(level_words(ss.level))
    c1, c2 = st.columns(2)
    c1.button(
        "다음 20개 단어 여행하기 →" if more else "레벨 처음부터 다시 여행하기 ↻",
        on_click=next_set,
        type="primary",
        use_container_width=True,
    )
    c2.button("이 세트 다시 학습", on_click=start_set, use_container_width=True)

st.caption("SkyTrip Voca · 작은 단어가 모여 큰 여행이 됩니다.")
