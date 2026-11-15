import json
import random
import re
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Voca 3,000 스마트 학습장", page_icon="📚", layout="centered")

CSV_FILE = Path("Voca_3000.csv")
PROGRESS_FILE = Path("progress_3000.json")
BATCH_SIZE = 20

LEVEL_LABELS = {
    "Elementary": "초급 (Elementary)",
    "MidHigh": "중급 (MidHigh)",
    "Extended": "고급 (Extended)",
}

# 핵심 기능어·대명사 전용 자연 예문 사전
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
    "about": ("We talked about our plans for the summer vacation.", "우리는 여름방학 계획에 관하여 이야기했다."),
    "above": ("A bright star shone directly above the quiet hill.", "밝은 별 하나가 조용한 언덕 바로 위에 빛났다."),
    "across": ("They built a new bridge across the wide river.", "그들은 넓은 강을 가로질러 새 다리를 건설했다."),
    "after": ("Let us take a short walk after dinner.", "저녁 식사 후에 잠깐 산책을 합시다."),
    "against": ("The umbrella protected us against the sudden rain.", "우산이 갑작스러운 비로부터 우리를 막아 주었다."),
    "along": ("Many trees grow along both sides of the road.", "도로 양쪽을 따라 많은 나무가 자라고 있다."),
    "among": ("She felt comfortable among her close friends.", "그녀는 친한 친구들 중에서 편안함을 느꼈다."),
    "around": ("People gathered around the stage to watch the show.", "사람들이 공연을 보기 위해 무대 주위에 모였다."),
    "as": ("He works as a software engineer in Seoul.", "그는 서울에서 소프트웨어 엔지니어로서 일한다."),
    "at": ("We agreed to meet at the main entrance at noon.", "우리는 정오에 정문에서 만나기로 약속했다."),
    "be": ("Everyone wants to be happy and healthy.", "모든 사람은 행복하고 건강하기를 원한다."),
    "because": ("We stayed indoors because the wind was too strong.", "바람이 너무 강했기 때문에 우리는 실내에 머물렀다."),
    "before": ("Wash your hands carefully before eating a meal.", "식사를 하기 전에 손을 깨끗이 씻으세요."),
    "behind": ("The parking lot is located behind the main building.", "주차장은 본관 뒤에 위치해 있다."),
    "below": ("The temperature dropped below zero last night.", "어젯밤 기온이 영하 아래로 떨어졌다."),
    "between": ("The small cafe is right between the bank and the post office.", "그 작은 카페는 은행과 우체국 바로 사이에 있다."),
    "but": ("I wanted to go outside, but it started raining heavily.", "나는 밖에 나가고 싶었지만 비가 심하게 내리기 시작했다."),
    "by": ("The novel was written by a famous Korean author.", "그 소설은 유명한 한국 작가에 의해 쓰였다."),
    "can": ("She can speak three languages fluently.", "그녀는 세 가지 언어를 유창하게 말할 수 있다."),
    "could": ("We could see the whole city from the tower.", "우리는 탑에서 도시 전체를 볼 수 있었다."),
    "despite": ("Despite the heavy traffic, we arrived on schedule.", "심한 교통 체증에도 불구하고 우리는 예정대로 도착했다."),
    "do": ("Always do your best in everything you try.", "시도하는 모든 일에서 항상 최선을 다하세요."),
    "during": ("Many tourists visit the island during the spring season.", "봄철 동안 많은 관광객이 그 섬을 방문한다."),
    "for": ("This gift is specially prepared for your birthday.", "이 선물은 너의 생일을 위해 특별히 준비되었다."),
    "from": ("I received a postcard from my friend in London.", "나는 런던에 있는 친구로부터 엽서 한 장을 받았다."),
    "go": ("Let us go to the library together after class.", "수업이 끝난 후 함께 도서관에 갑시다."),
    "if": ("If it rains tomorrow, the outdoor game will be canceled.", "만약 내일 비가 오면 야외 경기는 취소될 것이다."),
    "in": ("The keys are inside the small box in the drawer.", "열쇠들은 서랍 안의 작은 상자 속에 있다."),
    "into": ("She poured cold water into the tall glass.", "그녀는 긴 유리잔 안으로 찬물을 부었다."),
    "may": ("It may snow in the northern region tonight.", "오늘 밤 북부 지역에 눈이 올지도 모른다."),
    "might": ("He might join us for dinner if he finishes early.", "그가 일찍 끝내면 저녁 식사에 우리와 함께할지도 모른다."),
    "must": ("Drivers must stop when the traffic light turns red.", "신호등이 빨간불로 바뀌면 운전자는 반드시 멈춰야 한다."),
    "no": ("There is no reason to worry about the result.", "결과에 대해 걱정할 이유가 전혀 없다."),
    "not": ("Do not forget to lock the front door.", "현관문을 잠그는 것을 잊지 마세요."),
    "of": ("A cup of warm tea helps me relax at night.", "따뜻한 차 한 잔은 밤에 내가 긴장을 푸는 데 도움이 된다."),
    "on": ("There is a cup of coffee on the wooden desk.", "나무 책상 위에 커피 한 잔이 있다."),
    "or": ("Would you like hot coffee or iced tea?", "따뜻한 커피와 아이스티 중 어느 것을 드시겠어요?"),
    "over": ("A flock of birds flew high over the lake.", "새 떼가 호수 너머로 높이 날아갔다."),
    "per": ("The speed limit on this road is sixty kilometers per hour.", "이 도로의 제한 속도는 시간당 60킬로미터이다."),
    "shall": ("Shall we review the vocabulary list together?", "우리가 함께 단어 목록을 복습할까요?"),
    "should": ("You should get enough sleep before the big exam.", "중요한 시험 전에는 충분한 수면을 취해야 한다."),
    "since": ("I have lived in this neighborhood since last year.", "나는 작년부터 이 동네에 살고 있다."),
    "so": ("It was getting dark, so we hurried back home.", "어두워지고 있어서 우리는 서둘러 집으로 돌아왔다."),
    "through": ("Sunlight streamed through the tall glass windows.", "햇빛이 높은 유리창을 통해 쏟아져 들어왔다."),
    "to": ("We walked to the park to enjoy the fresh air.", "우리는 신선한 공기를 즐기러 공원까지 걸어갔다."),
    "under": ("The cat was sleeping peacefully under the warm blanket.", "고양이가 따뜻한 담요 아래에서 평화롭게 자고 있었다."),
    "until": ("The library stays open until nine in the evening.", "도서관은 저녁 9시까지 문을 연다."),
    "up": ("We climbed up the stairs to reach the rooftop garden.", "우리는 옥상 정원에 닿기 위해 계단 위로 올라갔다."),
    "while": ("Please keep quiet while others are taking the test.", "다른 사람들이 시험을 보는 동안 조용히 해 주세요."),
    "with": ("She solved the difficult puzzle with her classmates.", "그녀는 반 친구들과 함께 어려운 퍼즐을 풀었다."),
    "without": ("He left the house without taking his wallet.", "그는 지갑을 챙기지 않고 집을 나섰다."),
    "yes": ("Yes, I would love to join your weekend trip.", "예, 주말 여행에 기꺼이 함께하고 싶습니다."),
    "yet": ("Have you finished reading that article yet?", "그 기사를 아직 다 읽지 못했나요?"),
}

VERB_TRANSITIVE_TPL = [
    ("The team worked hard to {w} the new system.", "팀은 새로운 시스템을 '{m}' 위해 열심히 일했다."),
    ("Experts advise people to {w} important details carefully.", "전문가들은 사람들에게 중요한 세부 사항을 신중하게 '{m}'(이)라고 조언한다."),
    ("We need a clear strategy to {w} this challenge.", "우리는 이 과제를 '{m}' 위한 명확한 전략이 필요하다."),
    ("Students learned how to {w} the task during the workshop.", "학생들은 워크숍 동안 그 과제를 '{m}' 방법을 배웠다."),
]

VERB_INTRANSITIVE_TPL = [
    ("Things began to {w} rapidly after the announcement.", "발표 이후 상황들이 빠르게 '{m}' 시작했다."),
    ("Everyone watched closely as the situation started to {w}.", "상황이 '{m}' 시작하자 모두가 유심히 지켜보았다."),
    ("People often {w} when they face unexpected news.", "사람들은 예상치 못한 소식을 접할 때 종종 '{m}'."),
]

ADJ_TPL = [
    ("The instructor gave a very {w} explanation to the class.", "강사는 수업에서 매우 {m} 설명을 해 주었다."),
    ("Everyone noticed the {w} atmosphere in the meeting room.", "모두가 회의실의 {m} 분위기를 알아챘다."),
    ("It is important to maintain a {w} attitude toward learning.", "배움에 대해 {m} 태도를 유지하는 것이 중요하다."),
    ("The report highlighted several {w} factors in the results.", "그 보고서는 결과에서 몇 가지 {m} 요인들을 강조했다."),
]

ADV_TPL = [
    ("She explained the whole procedure {w} to the new staff.", "그녀는 신입 직원들에게 전체 절차를 {m} 설명했다."),
    ("The plan progressed {w} despite several early obstacles.", "초기의 몇 가지 장애물에도 불구하고 계획은 {m} 진행되었다."),
    ("He checked every detail {w} before submitting the report.", "그는 보고서를 제출하기 전에 모든 세부 사항을 {m} 확인했다."),
]

NOUN_TPL = [
    ("The article discusses the role of {w} in modern society.", "그 기사는 현대 사회에서 {m}의 역할을 다룬다."),
    ("Understanding {w} is essential for solving this problem.", "'{m}'을(를) 이해하는 것은 이 문제를 해결하는 데 필수적이다."),
    ("They organized a special seminar focused on {w}.", "그들은 '{m}'에 초점을 맞춘 특별 세미나를 열었다."),
    ("The teacher used a clear example to illustrate {w}.", "선생님은 '{m}'을(를) 설명하기 위해 명확한 예시를 사용했다."),
]


def build_sentence_for_word(word: str, meaning: str, idx: int) -> tuple[str, str, str]:
    wl = word.lower().strip()
    m_clean = meaning.strip()

    if wl in EXACT_SENTENCES:
        en, ko = EXACT_SENTENCES[wl]
    elif (
        wl.endswith("ly")
        and len(wl) > 4
        and wl not in {"family", "reply", "supply", "apply", "fly", "rely", "friendly", "lovely", "lonely", "daily", "early", "likely", "only"}
    ) or m_clean.endswith(("하게", "히", "으로")):
        tpl_en, tpl_ko = ADV_TPL[idx % len(ADV_TPL)]
        en, ko = tpl_en.format(w=word), tpl_ko.format(m=m_clean)
    elif m_clean.endswith("다") and m_clean not in {"바다", "사다", "마다", "보다"}:
        if any(k in m_clean for k in ["되다", "오다", "가다", "서다", "앉다", "자라다", "변하다", "일어나다", "나타나다", "사라지다", "존재하다", "머무르다", "도착하다", "출발하다", "웃다", "울다", "자다", "살다", "아프다", "빛나다", "흐르다", "떨어지다", "오르다"]):
            tpl_en, tpl_ko = VERB_INTRANSITIVE_TPL[idx % len(VERB_INTRANSITIVE_TPL)]
        else:
            tpl_en, tpl_ko = VERB_TRANSITIVE_TPL[idx % len(VERB_TRANSITIVE_TPL)]
        en, ko = tpl_en.format(w=word), tpl_ko.format(m=m_clean)
    elif m_clean.endswith(("한", "인", "운", "은", "는", "적", "의")) and m_clean not in {
        "은", "주인", "군인", "시인", "범인", "증인", "노인", "성인", "개인", "타인", "거인",
        "의자", "회의", "주의", "의미", "정의", "동의", "항의", "목적", "기적", "성적", "흔적", "규칙", "지식", "면적", "국적", "적",
    }:
        tpl_en, tpl_ko = ADJ_TPL[idx % len(ADJ_TPL)]
        en, ko = tpl_en.format(w=word), tpl_ko.format(m=m_clean)
    else:
        tpl_en, tpl_ko = NOUN_TPL[idx % len(NOUN_TPL)]
        en, ko = tpl_en.format(w=word), tpl_ko.format(m=m_clean)

    pattern = re.compile(rf"(?<![A-Za-z]){re.escape(word)}(?![A-Za-z])", re.IGNORECASE)
    if not pattern.search(en):
        en = f"Please study the exact usage of {word} in this context."
        ko = f"이 문맥에서 '{m_clean}'의 정확한 쓰임을 학습해 보세요."
    blank_en = pattern.sub("_____", en, count=1)
    return en, blank_en, ko


@st.cache_data
def load_all_3000_words() -> list[dict]:
    if not CSV_FILE.exists():
        st.error(f"`{CSV_FILE}` 파일을 찾을 수 없습니다. `app.py`와 같은 폴더에 `Voca_3000.csv`를 두세요.")
        st.stop()

    df = pd.read_csv(CSV_FILE)
    words = []
    for idx, row in df.iterrows():
        w = str(row["Word"]).strip()
        m = str(row["Korean meaning (뜻)"]).strip()
        lvl = str(row["Level"]).strip()
        var = "" if pd.isna(row.get("Variation")) else str(row["Variation"]).strip()
        en, blank_en, ko = build_sentence_for_word(w, m, idx)
        words.append(
            {
                "id": int(row["No."]),
                "word": w,
                "meaning": m,
                "level": lvl,
                "variation": var,
                "sentence": en,
                "blank_sentence": blank_en,
                "sentence_ko": ko,
            }
        )
    return words


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    "mastered_ids": list(dict.fromkeys(data.get("mastered_ids", []))),
                    "wrong_ids": list(dict.fromkeys(data.get("wrong_ids", []))),
                }
        except Exception:
            pass
    return {"mastered_ids": [], "wrong_ids": []}


def save_progress(progress: dict) -> None:
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def speak_english(text: str, trigger_key: str) -> None:
    """브라우저 Web Speech API를 사용해 영어 발음을 재생합니다."""
    safe_text = json.dumps(text)
    components.html(
        f"""
        <script>
        (function() {{
            const synth = window.parent.speechSynthesis || window.speechSynthesis;
            if (!synth) return;
            synth.cancel();
            const utter = new SpeechSynthesisUtterance({safe_text});
            utter.lang = 'en-US';
            utter.rate = 0.92;
            synth.speak(utter);
        }})();
        </script>
        <div style="display:none">{trigger_key}</div>
        """,
        height=0,
    )


def get_batch_words(all_words: list[dict], level: str, set_idx: int) -> list[dict]:
    level_words = [w for w in all_words if w["level"] == level]
    start = set_idx * BATCH_SIZE
    return level_words[start : start + BATCH_SIZE]


def init_stage_state(batch: list[dict], level: str, set_idx: int, all_words: list[dict]) -> None:
    st.session_state.current_level = level
    st.session_state.current_set_idx = set_idx
    st.session_state.batch = batch

    # Stage 1: Flashcard
    st.session_state.stage = "flashcard"
    st.session_state.fc_idx = 0
    st.session_state.fc_flipped = False
    st.session_state.tts_seq = 0

    # Stage 2: Random Spelling & Meaning Quiz
    q2_list = []
    pool_words = [w["word"] for w in all_words if w["level"] == level]
    pool_meanings = list({w["meaning"] for w in all_words if w["level"] == level})

    for item in batch:
        qtype = random.choice(["spelling", "meaning"])
        if qtype == "spelling":
            distractors = random.sample([w for w in pool_words if w != item["word"]], 3)
            options = distractors + [item["word"]]
            random.shuffle(options)
            q2_list.append(
                {
                    "type": "spelling",
                    "item": item,
                    "prompt": f"다음 뜻에 해당하는 올바른 영어 철자는? → **{item['meaning']}**",
                    "answer": item["word"],
                    "options": options,
                }
            )
        else:
            distractors = random.sample([m for m in pool_meanings if m != item["meaning"]], 3)
            options = distractors + [item["meaning"]]
            random.shuffle(options)
            q2_list.append(
                {
                    "type": "meaning",
                    "item": item,
                    "prompt": f"다음 영어 단어의 뜻은? → **{item['word']}**",
                    "answer": item["meaning"],
                    "options": options,
                }
            )
    random.shuffle(q2_list)
    st.session_state.q2_list = q2_list
    st.session_state.q2_idx = 0
    st.session_state.q2_wrong_tries = []
    st.session_state.q2_feedback = ""

    # Stage 3: Example Sentence Blank Quiz (문맥 속 빈칸 뜻/단어 학습)
    q3_list = []
    for item in batch:
        mode = random.choice(["blank_meaning", "blank_word"])
        if mode == "blank_meaning":
            distractors = random.sample([m for m in pool_meanings if m != item["meaning"]], 3)
            options = distractors + [item["meaning"]]
            random.shuffle(options)
            q3_list.append(
                {
                    "mode": "blank_meaning",
                    "item": item,
                    "answer": item["meaning"],
                    "options": options,
                }
            )
        else:
            distractors = random.sample([w for w in pool_words if w != item["word"]], 3)
            options = distractors + [item["word"]]
            random.shuffle(options)
            q3_list.append(
                {
                    "mode": "blank_word",
                    "item": item,
                    "answer": item["word"],
                    "options": options,
                }
            )
    random.shuffle(q3_list)
    st.session_state.q3_list = q3_list
    st.session_state.q3_idx = 0
    st.session_state.q3_wrong_tries = []
    st.session_state.q3_feedback = ""


# --- 앱 시작 ---
all_words = load_all_3000_words()
if "progress" not in st.session_state:
    st.session_state.progress = load_progress()
if "audio_enabled" not in st.session_state:
    st.session_state.audio_enabled = True

with st.sidebar:
    st.header("🎯 레벨 및 20개 세트 선택")
    selected_level = st.selectbox(
        "학습 레벨",
        options=["Elementary", "MidHigh", "Extended"],
        format_func=lambda x: LEVEL_LABELS[x],
    )
    level_words = [w for w in all_words if w["level"] == selected_level]
    total_sets = (len(level_words) + BATCH_SIZE - 1) // BATCH_SIZE

    selected_set_idx = st.selectbox(
        f"20단어 세트 (총 {len(level_words)}단어 / {total_sets}세트)",
        options=list(range(total_sets)),
        format_func=lambda i: f"Set {i + 1} ({i * BATCH_SIZE + 1} ~ {min((i + 1) * BATCH_SIZE, len(level_words))}번)",
    )

    st.divider()
    st.header("🔊 발음 설정")
    st.session_state.audio_enabled = st.toggle(
        "Flashcard 발음 듣기 ON/OFF",
        value=st.session_state.audio_enabled,
        help="ON 상태에서는 카드를 넘길 때마다 영어 발음을 자동으로 읽어줍니다.",
    )

    st.divider()
    st.header("📊 전체 3,000단어 진도")
    mastered_cnt = len(st.session_state.progress["mastered_ids"])
    wrong_cnt = len(st.session_state.progress["wrong_ids"])
    st.progress(mastered_cnt / len(all_words), text=f"완전 학습: {mastered_cnt} / {len(all_words)}개")
    st.caption(f"오답 기록 단어: {wrong_cnt}개")
    if st.button("진도 초기화", use_container_width=True):
        st.session_state.progress = {"mastered_ids": [], "wrong_ids": []}
        save_progress(st.session_state.progress)
        st.rerun()

# 레벨 또는 세트가 바뀌면 새 20개 세트 초기화
if (
    "current_level" not in st.session_state
    or st.session_state.current_level != selected_level
    or st.session_state.current_set_idx != selected_set_idx
):
    batch = get_batch_words(all_words, selected_level, selected_set_idx)
    init_stage_state(batch, selected_level, selected_set_idx, all_words)

st.title("📚 Voca 3,000 단계별 마스터")
st.caption(
    f"**{LEVEL_LABELS[selected_level]}** · **Set {selected_set_idx + 1}** (20단어) | "
    "① Flashcard → ② Spelling & 뜻 랜덤 Quiz → ③ 예문 빈칸 Quiz"
)

# 상단 단계 표시 탭 버튼
s1, s2, s3 = st.columns(3)
with s1:
    if st.button(
        "1️⃣ Flashcard (20개)",
        use_container_width=True,
        type="primary" if st.session_state.stage == "flashcard" else "secondary",
    ):
        st.session_state.stage = "flashcard"
        st.rerun()
with s2:
    if st.button(
        "2️⃣ Spelling & 뜻 Quiz",
        use_container_width=True,
        type="primary" if st.session_state.stage == "quiz_mixed" else "secondary",
    ):
        st.session_state.stage = "quiz_mixed"
        st.rerun()
with s3:
    if st.button(
        "3️⃣ 예문 빈칸 Quiz",
        use_container_width=True,
        type="primary" if st.session_state.stage == "quiz_blank" else "secondary",
    ):
        st.session_state.stage = "quiz_blank"
        st.rerun()

st.divider()

# ==============================================================================
# STAGE 1: 20개 Flashcard 학습 (발음 ON/OFF + 스피커 버튼)
# ==============================================================================
if st.session_state.stage == "flashcard":
    batch = st.session_state.batch
    idx = st.session_state.fc_idx
    item = batch[idx]

    top_l, top_r = st.columns([3, 1])
    with top_l:
        st.subheader(f"카드 {idx + 1} / {len(batch)}  (No. #{item['id']})")
    with top_r:
        if st.button("🔊 발음 듣기", key=f"spk_{idx}", use_container_width=True):
            st.session_state.tts_seq += 1
            speak_english(item["word"], f"manual_{idx}_{st.session_state.tts_seq}")

    # 발음 ON 상태이고 새 카드에 진입했을 때 자동 재생
    auto_key = f"auto_{selected_level}_{selected_set_idx}_{idx}"
    if st.session_state.audio_enabled and st.session_state.get("last_auto_spoken") != auto_key:
        st.session_state.last_auto_spoken = auto_key
        speak_english(item["word"], auto_key)

    with st.container(border=True):
        st.markdown(f"<h1 style='text-align:center; margin: 16px 0;'>{item['word']}</h1>", unsafe_allow_html=True)
        if item["variation"]:
            st.markdown(
                f"<p style='text-align:center; color:gray;'>변형/관련어: {item['variation']}</p>",
                unsafe_allow_html=True,
            )

        if st.session_state.fc_flipped:
            st.divider()
            st.markdown(f"<h3 style='text-align:center; color:#1f77b4;'>{item['meaning']}</h3>", unsafe_allow_html=True)
            st.info(f"**예문:** {item['sentence']}\n\n**해석:** {item['sentence_ko']}")
        else:
            if st.button("👀 뜻 & 예문 뒤집어 보기", use_container_width=True):
                st.session_state.fc_flipped = True
                st.rerun()

    nav1, nav2, nav3 = st.columns([1, 1, 1.4])
    with nav1:
        if st.button("⬅️ 이전 카드", disabled=(idx == 0), use_container_width=True):
            st.session_state.fc_idx -= 1
            st.session_state.fc_flipped = False
            st.rerun()
    with nav2:
        if st.button("다음 카드 ➡️", disabled=(idx >= len(batch) - 1), use_container_width=True):
            st.session_state.fc_idx += 1
            st.session_state.fc_flipped = False
            st.rerun()
    with nav3:
        if idx == len(batch) - 1:
            if st.button("2단계: Spelling & 뜻 Quiz 시작 🚀", type="primary", use_container_width=True):
                st.session_state.stage = "quiz_mixed"
                st.rerun()
        else:
            if st.button("바로 2단계 Quiz로 건너뛰기", use_container_width=True):
                st.session_state.stage = "quiz_mixed"
                st.rerun()

# ==============================================================================
# STAGE 2: Spelling & 뜻 랜덤 Quiz (선택 즉시 채점, 첫 오답부터 힌트, 재도전 가능)
# ==============================================================================
elif st.session_state.stage == "quiz_mixed":
    q_list = st.session_state.q2_list
    q_idx = st.session_state.q2_idx

    if q_idx >= len(q_list):
        st.success("🎉 2단계 [Spelling & 뜻 랜덤 Quiz] 20문제를 모두 통과했습니다!")
        if st.button("3단계: 예문 빈칸 Quiz 시작하기 ➡️", type="primary", use_container_width=True):
            st.session_state.stage = "quiz_blank"
            st.rerun()
        st.stop()

    q = q_list[q_idx]
    item = q["item"]
    wrong_tries = st.session_state.q2_wrong_tries

    st.subheader(f"문제 {q_idx + 1} / {len(q_list)}  ({'철자 맞히기' if q['type'] == 'spelling' else '뜻 맞히기'})")
    with st.container(border=True):
        st.markdown(f"### {q['prompt']}")
        if q["type"] == "meaning":
            if st.button("🔊 단어 발음 듣기", key=f"q2_spk_{q_idx}"):
                st.session_state.tts_seq += 1
                speak_english(item["word"], f"q2_{q_idx}_{st.session_state.tts_seq}")

    # 첫 번째 오답부터 즉시 힌트 표시
    if wrong_tries:
        st.error(st.session_state.q2_feedback)
        if q["type"] == "spelling":
            w = item["word"]
            st.warning(f"💡 **힌트:** 첫 글자는 **`{w[0]}`**, 전체 글자 수는 **{len(w)}글자**입니다. (예문: *{item['blank_sentence']}*)")
        else:
            st.warning(f"💡 **힌트:** 예문 속 쓰임을 참고해 보세요 → *{item['sentence']}*")

    # 선택지 버튼: 누르는 순간 즉시 채점 (정답 확인 버튼 없음)
    cols = st.columns(2)
    for i, opt in enumerate(q["options"]):
        already_wrong = opt in wrong_tries
        label = f"❌ {opt}" if already_wrong else opt
        with cols[i % 2]:
            if st.button(
                label,
                key=f"q2_opt_{q_idx}_{i}",
                disabled=already_wrong,
                use_container_width=True,
            ):
                if opt == q["answer"]:
                    # 정답 선택 시 즉시 다음 문제로 이동
                    st.session_state.q2_idx += 1
                    st.session_state.q2_wrong_tries = []
                    st.session_state.q2_feedback = ""
                    st.rerun()
                else:
                    # 첫 번째 오답부터 오답 기록 + 힌트 활성화 + 재도전 허용
                    if item["id"] not in st.session_state.progress["wrong_ids"]:
                        st.session_state.progress["wrong_ids"].append(item["id"])
                        save_progress(st.session_state.progress)
                    st.session_state.q2_wrong_tries.append(opt)
                    st.session_state.q2_feedback = f"오답입니다! ('{opt}'은(는) 정답이 아닙니다. 아래 힌트를 보고 다시 선택해 보세요.)"
                    st.rerun()

# ==============================================================================
# STAGE 3: 예문 빈칸 Quiz (직접 만든 문장의 빈칸 뜻/단어 학습, 선택 즉시 채점)
# ==============================================================================
elif st.session_state.stage == "quiz_blank":
    q_list = st.session_state.q3_list
    q_idx = st.session_state.q3_idx

    if q_idx >= len(q_list):
        # 20단어 세트 완전 학습 처리
        for w in st.session_state.batch:
            if w["id"] not in st.session_state.progress["mastered_ids"]:
                st.session_state.progress["mastered_ids"].append(w["id"])
        save_progress(st.session_state.progress)

        st.balloons()
        st.success(f"🏆 **{LEVEL_LABELS[selected_level]} - Set {selected_set_idx + 1}** (20단어) 전 과정을 완료했습니다!")
        if selected_set_idx + 1 < total_sets:
            st.info(f"사이드바에서 **Set {selected_set_idx + 2}**를 선택해 다음 20단어를 이어서 학습하세요!")
        st.stop()

    q = q_list[q_idx]
    item = q["item"]
    wrong_tries = st.session_state.q3_wrong_tries

    st.subheader(f"예문 빈칸 문제 {q_idx + 1} / {len(q_list)}")
    with st.container(border=True):
        st.markdown(f"### `{item['blank_sentence']}`")
        if q["mode"] == "blank_meaning":
            st.caption("위 문장의 빈칸(_____)에 들어갈 단어의 **알맞은 뜻**을 고르세요.")
        else:
            st.caption(f"해석: **{item['sentence_ko']}** — 빈칸(_____)에 들어갈 **알맞은 영어 단어**를 고르세요.")

    # 첫 번째 오답부터 힌트 표시
    if wrong_tries:
        st.error(st.session_state.q3_feedback)
        w = item["word"]
        if q["mode"] == "blank_meaning":
            st.warning(f"💡 **힌트:** 빈칸에 들어갈 영어 단어는 **`{w}`**이며, 해석은 *'{item['sentence_ko']}'*입니다.")
        else:
            st.warning(f"💡 **힌트:** 빈칸 단어의 뜻은 **'{item['meaning']}'**, 첫 글자는 **`{w[0]}`** ({len(w)}글자)입니다.")

    cols = st.columns(2)
    for i, opt in enumerate(q["options"]):
        already_wrong = opt in wrong_tries
        label = f"❌ {opt}" if already_wrong else opt
        with cols[i % 2]:
            if st.button(
                label,
                key=f"q3_opt_{q_idx}_{i}",
                disabled=already_wrong,
                use_container_width=True,
            ):
                if opt == q["answer"]:
                    st.session_state.q3_idx += 1
                    st.session_state.q3_wrong_tries = []
                    st.session_state.q3_feedback = ""
                    st.rerun()
                else:
                    if item["id"] not in st.session_state.progress["wrong_ids"]:
                        st.session_state.progress["wrong_ids"].append(item["id"])
                        save_progress(st.session_state.progress)
                    st.session_state.q3_wrong_tries.append(opt)
                    st.session_state.q3_feedback = f"오답입니다! ('{opt}'은(는) 정답이 아닙니다. 힌트를 확인하고 다시 골라보세요.)"
                    st.rerun()