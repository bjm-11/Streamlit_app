import json
import random
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Voca 3,000 랜덤 학습장", page_icon="📚", layout="centered")

PROGRESS_FILE = Path("progress.json")
BATCH_SIZE = 20

# Voca_3000.csv 전체 3000개 단어가 내장된 데이터입니다.
BUILTIN_WORDS = [
  {
    "id": 1,
    "word": "a",
    "meaning": "하나의",
    "level": "Elementary",
    "variation": "an"
  },
  {
    "id": 2,
    "word": "abandon",
    "meaning": "버리다",
    "level": "Extended"
  },
  {
    "id": 3,
    "word": "able",
    "meaning": "할 수 있는",
    "level": "MidHigh",
    "variation": "disabled"
  },
  {
    "id": 4,
    "word": "aboard",
    "meaning": "탑승하여",
    "level": "Extended"
  },
  {
    "id": 5,
    "word": "abort",
    "meaning": "중단하다",
    "level": "Extended",
    "variation": "abortion"
  },
  {
    "id": 6,
    "word": "abound",
    "meaning": "풍부하다",
    "level": "Extended",
    "variation": "abundant"
  },
  {
    "id": 7,
    "word": "about",
    "meaning": "~에 관하여",
    "level": "Elementary"
  },
  {
    "id": 8,
    "word": "above",
    "meaning": "위에",
    "level": "Elementary"
  },
  {
    "id": 9,
    "word": "abroad",
    "meaning": "해외에",
    "level": "Extended"
  },
  {
    "id": 10,
    "word": "absent",
    "meaning": "결석한",
    "level": "Extended"
  },
  {
    "id": 11,
    "word": "absolute",
    "meaning": "절대적인",
    "level": "MidHigh"
  },
  {
    "id": 12,
    "word": "absorb",
    "meaning": "흡수하다",
    "level": "Extended"
  },
  {
    "id": 13,
    "word": "abstract",
    "meaning": "추상적인",
    "level": "Extended"
  },
  {
    "id": 14,
    "word": "absurd",
    "meaning": "터무니없는",
    "level": "Extended"
  },
  {
    "id": 15,
    "word": "abuse",
    "meaning": "남용하다",
    "level": "Extended"
  },
  {
    "id": 16,
    "word": "academy",
    "meaning": "학원",
    "level": "Extended"
  },
  {
    "id": 17,
    "word": "accelerate",
    "meaning": "가속하다",
    "level": "Extended"
  },
  {
    "id": 18,
    "word": "accent",
    "meaning": "억양",
    "level": "MidHigh"
  },
  {
    "id": 19,
    "word": "accept",
    "meaning": "받아들이다",
    "level": "MidHigh"
  },
  {
    "id": 20,
    "word": "access",
    "meaning": "접근",
    "level": "MidHigh"
  },
  {
    "id": 21,
    "word": "accident",
    "meaning": "사고",
    "level": "MidHigh"
  },
  {
    "id": 22,
    "word": "accommodate",
    "meaning": "수용하다",
    "level": "Extended"
  },
  {
    "id": 23,
    "word": "accompany",
    "meaning": "동행하다",
    "level": "Extended"
  },
  {
    "id": 24,
    "word": "accomplish",
    "meaning": "성취하다",
    "level": "Extended"
  },
  {
    "id": 25,
    "word": "accord",
    "meaning": "일치하다",
    "level": "Extended"
  },
  {
    "id": 26,
    "word": "account",
    "meaning": "계정",
    "level": "MidHigh"
  },
  {
    "id": 27,
    "word": "accumulate",
    "meaning": "축적하다",
    "level": "Extended"
  },
  {
    "id": 28,
    "word": "accurate",
    "meaning": "정확한",
    "level": "Extended"
  },
  {
    "id": 29,
    "word": "accuse",
    "meaning": "비난하다",
    "level": "MidHigh"
  },
  {
    "id": 30,
    "word": "ache",
    "meaning": "아프다",
    "level": "Extended",
    "variation": "headache"
  },
  {
    "id": 31,
    "word": "achieve",
    "meaning": "달성하다",
    "level": "MidHigh"
  },
  {
    "id": 32,
    "word": "acid",
    "meaning": "산",
    "level": "Extended"
  },
  {
    "id": 33,
    "word": "acknowledge",
    "meaning": "인정하다",
    "level": "Extended"
  },
  {
    "id": 34,
    "word": "acquire",
    "meaning": "얻다",
    "level": "Extended"
  },
  {
    "id": 35,
    "word": "acquisition",
    "meaning": "습득",
    "level": "Extended"
  },
  {
    "id": 36,
    "word": "across",
    "meaning": "가로질러",
    "level": "Elementary"
  },
  {
    "id": 37,
    "word": "act",
    "meaning": "행동하다",
    "level": "Elementary",
    "variation": "actual, interact"
  },
  {
    "id": 38,
    "word": "adapt",
    "meaning": "적응하다",
    "level": "MidHigh"
  },
  {
    "id": 39,
    "word": "add",
    "meaning": "더하다",
    "level": "Elementary"
  },
  {
    "id": 40,
    "word": "addict",
    "meaning": "중독자",
    "level": "Extended"
  },
  {
    "id": 41,
    "word": "address",
    "meaning": "주소",
    "level": "Elementary"
  },
  {
    "id": 42,
    "word": "adequate",
    "meaning": "적절한",
    "level": "Extended"
  },
  {
    "id": 43,
    "word": "adjust",
    "meaning": "조정하다",
    "level": "Extended"
  },
  {
    "id": 44,
    "word": "administer",
    "meaning": "관리하다",
    "level": "Extended",
    "variation": "administration"
  },
  {
    "id": 45,
    "word": "admire",
    "meaning": "존경하다",
    "level": "MidHigh"
  },
  {
    "id": 46,
    "word": "admit",
    "meaning": "인정하다",
    "level": "MidHigh",
    "variation": "admission"
  },
  {
    "id": 47,
    "word": "adolescent",
    "meaning": "청소년",
    "level": "Extended"
  },
  {
    "id": 48,
    "word": "adopt",
    "meaning": "입양하다",
    "level": "MidHigh"
  },
  {
    "id": 49,
    "word": "adult",
    "meaning": "성인",
    "level": "Elementary"
  },
  {
    "id": 50,
    "word": "advance",
    "meaning": "진보",
    "level": "MidHigh"
  },
  {
    "id": 51,
    "word": "advantage",
    "meaning": "이점",
    "level": "MidHigh",
    "variation": "disadvantage"
  },
  {
    "id": 52,
    "word": "adventure",
    "meaning": "모험",
    "level": "MidHigh"
  },
  {
    "id": 53,
    "word": "adverse",
    "meaning": "불리한",
    "level": "Extended"
  },
  {
    "id": 54,
    "word": "advertize",
    "meaning": "광고하다",
    "level": "MidHigh",
    "variation": "advertise"
  },
  {
    "id": 55,
    "word": "advice",
    "meaning": "조언",
    "level": "MidHigh"
  },
  {
    "id": 56,
    "word": "advise",
    "meaning": "조언하다",
    "level": "MidHigh"
  },
  {
    "id": 57,
    "word": "advocate",
    "meaning": "옹호하다",
    "level": "Extended"
  },
  {
    "id": 58,
    "word": "aesthetic",
    "meaning": "미학적인",
    "level": "Extended"
  },
  {
    "id": 59,
    "word": "affair",
    "meaning": "일",
    "level": "MidHigh"
  },
  {
    "id": 60,
    "word": "affect",
    "meaning": "영향을 미치다",
    "level": "MidHigh",
    "variation": "affection"
  },
  {
    "id": 61,
    "word": "afford",
    "meaning": "여유가 있다",
    "level": "MidHigh"
  },
  {
    "id": 62,
    "word": "afraid",
    "meaning": "두려워하는",
    "level": "Elementary"
  },
  {
    "id": 63,
    "word": "after",
    "meaning": "뒤에",
    "level": "Elementary"
  },
  {
    "id": 64,
    "word": "afternoon",
    "meaning": "오후",
    "level": "Elementary"
  },
  {
    "id": 65,
    "word": "again",
    "meaning": "다시",
    "level": "Elementary"
  },
  {
    "id": 66,
    "word": "against",
    "meaning": "반대하여",
    "level": "Elementary"
  },
  {
    "id": 67,
    "word": "age",
    "meaning": "나이",
    "level": "Elementary"
  },
  {
    "id": 68,
    "word": "agency",
    "meaning": "대행사",
    "level": "Extended"
  },
  {
    "id": 69,
    "word": "agenda",
    "meaning": "의제",
    "level": "Extended"
  },
  {
    "id": 70,
    "word": "agent",
    "meaning": "대리인",
    "level": "MidHigh"
  },
  {
    "id": 71,
    "word": "aggress",
    "meaning": "공격하다",
    "level": "Extended",
    "variation": "aggressive"
  },
  {
    "id": 72,
    "word": "ago",
    "meaning": "전에",
    "level": "Elementary"
  },
  {
    "id": 73,
    "word": "agree",
    "meaning": "동의하다",
    "level": "Elementary",
    "variation": "disagree"
  },
  {
    "id": 74,
    "word": "agriculture",
    "meaning": "농업",
    "level": "Extended"
  },
  {
    "id": 75,
    "word": "ahead",
    "meaning": "앞에",
    "level": "Elementary"
  },
  {
    "id": 76,
    "word": "aid",
    "meaning": "도움",
    "level": "MidHigh"
  },
  {
    "id": 77,
    "word": "aim",
    "meaning": "목표",
    "level": "MidHigh"
  },
  {
    "id": 78,
    "word": "air",
    "meaning": "공기",
    "level": "Elementary"
  },
  {
    "id": 79,
    "word": "airline",
    "meaning": "항공사",
    "level": "MidHigh"
  },
  {
    "id": 80,
    "word": "airplane",
    "meaning": "비행기",
    "level": "Elementary",
    "variation": "aeroplane"
  },
  {
    "id": 81,
    "word": "airport",
    "meaning": "공항",
    "level": "MidHigh"
  },
  {
    "id": 82,
    "word": "alarm",
    "meaning": "경보",
    "level": "MidHigh"
  },
  {
    "id": 83,
    "word": "album",
    "meaning": "앨범",
    "level": "Elementary"
  },
  {
    "id": 84,
    "word": "alcohol",
    "meaning": "알코올",
    "level": "MidHigh"
  },
  {
    "id": 85,
    "word": "alert",
    "meaning": "경계하는",
    "level": "Extended"
  },
  {
    "id": 86,
    "word": "alien",
    "meaning": "외국인",
    "level": "Extended"
  },
  {
    "id": 87,
    "word": "alike",
    "meaning": "비슷한",
    "level": "Extended"
  },
  {
    "id": 88,
    "word": "alive",
    "meaning": "살아 있는",
    "level": "MidHigh"
  },
  {
    "id": 89,
    "word": "all",
    "meaning": "모든",
    "level": "Elementary"
  },
  {
    "id": 90,
    "word": "allocate",
    "meaning": "할당하다",
    "level": "Extended"
  },
  {
    "id": 91,
    "word": "allow",
    "meaning": "허락하다",
    "level": "MidHigh"
  },
  {
    "id": 92,
    "word": "ally",
    "meaning": "동맹",
    "level": "Extended"
  },
  {
    "id": 93,
    "word": "almost",
    "meaning": "거의",
    "level": "Elementary"
  },
  {
    "id": 94,
    "word": "alone",
    "meaning": "혼자",
    "level": "Elementary"
  },
  {
    "id": 95,
    "word": "along",
    "meaning": "따라서",
    "level": "Elementary"
  },
  {
    "id": 96,
    "word": "alongside",
    "meaning": "나란히",
    "level": "Extended"
  },
  {
    "id": 97,
    "word": "aloud",
    "meaning": "소리 내어",
    "level": "MidHigh"
  },
  {
    "id": 98,
    "word": "already",
    "meaning": "이미",
    "level": "Elementary"
  },
  {
    "id": 99,
    "word": "alright",
    "meaning": "괜찮은",
    "level": "Elementary"
  },
  {
    "id": 100,
    "word": "also",
    "meaning": "또한",
    "level": "Elementary"
  },
  {
    "id": 101,
    "word": "alter",
    "meaning": "바꾸다",
    "level": "MidHigh"
  },
  {
    "id": 102,
    "word": "alternate",
    "meaning": "번갈아 하다",
    "level": "Extended",
    "variation": "alternative"
  },
  {
    "id": 103,
    "word": "although",
    "meaning": "비록",
    "level": "MidHigh"
  },
  {
    "id": 104,
    "word": "altogether",
    "meaning": "완전히",
    "level": "MidHigh"
  },
  {
    "id": 105,
    "word": "always",
    "meaning": "항상",
    "level": "Elementary"
  },
  {
    "id": 106,
    "word": "amaze",
    "meaning": "놀라게 하다",
    "level": "MidHigh"
  },
  {
    "id": 107,
    "word": "ambassador",
    "meaning": "대사",
    "level": "Extended"
  },
  {
    "id": 108,
    "word": "ambition",
    "meaning": "야망",
    "level": "Extended",
    "variation": "ambitious"
  },
  {
    "id": 109,
    "word": "ambulance",
    "meaning": "구급차",
    "level": "MidHigh"
  },
  {
    "id": 110,
    "word": "among",
    "meaning": "~중에",
    "level": "MidHigh"
  },
  {
    "id": 111,
    "word": "amount",
    "meaning": "양",
    "level": "MidHigh"
  },
  {
    "id": 112,
    "word": "amuse",
    "meaning": "즐겁게 하다",
    "level": "MidHigh"
  },
  {
    "id": 113,
    "word": "analysis",
    "meaning": "분석",
    "level": "MidHigh"
  },
  {
    "id": 114,
    "word": "analyze",
    "meaning": "분석하다",
    "level": "Extended",
    "variation": "analyse"
  },
  {
    "id": 115,
    "word": "anchor",
    "meaning": "닻",
    "level": "Extended"
  },
  {
    "id": 116,
    "word": "ancient",
    "meaning": "고대의",
    "level": "Extended"
  },
  {
    "id": 117,
    "word": "and",
    "meaning": "그리고",
    "level": "Elementary"
  },
  {
    "id": 118,
    "word": "angel",
    "meaning": "천사",
    "level": "MidHigh"
  },
  {
    "id": 119,
    "word": "anger",
    "meaning": "분노",
    "level": "MidHigh"
  },
  {
    "id": 120,
    "word": "angle",
    "meaning": "각도",
    "level": "Extended"
  },
  {
    "id": 121,
    "word": "animal",
    "meaning": "동물",
    "level": "Elementary"
  },
  {
    "id": 122,
    "word": "anniversary",
    "meaning": "기념일",
    "level": "Extended"
  },
  {
    "id": 123,
    "word": "announce",
    "meaning": "발표하다",
    "level": "MidHigh"
  },
  {
    "id": 124,
    "word": "annoy",
    "meaning": "짜증 나게 하다",
    "level": "MidHigh"
  },
  {
    "id": 125,
    "word": "annual",
    "meaning": "매년의",
    "level": "MidHigh"
  },
  {
    "id": 126,
    "word": "another",
    "meaning": "또 다른",
    "level": "Elementary"
  },
  {
    "id": 127,
    "word": "answer",
    "meaning": "대답",
    "level": "Elementary"
  },
  {
    "id": 128,
    "word": "ant",
    "meaning": "개미",
    "level": "MidHigh"
  },
  {
    "id": 129,
    "word": "anticipate",
    "meaning": "예상하다",
    "level": "Extended"
  },
  {
    "id": 130,
    "word": "anxiety",
    "meaning": "불안",
    "level": "Extended"
  },
  {
    "id": 131,
    "word": "anxious",
    "meaning": "불안한",
    "level": "MidHigh"
  },
  {
    "id": 132,
    "word": "any",
    "meaning": "어떤",
    "level": "Elementary"
  },
  {
    "id": 133,
    "word": "apart",
    "meaning": "떨어져",
    "level": "MidHigh"
  },
  {
    "id": 134,
    "word": "apartment",
    "meaning": "아파트",
    "level": "Elementary"
  },
  {
    "id": 135,
    "word": "apology",
    "meaning": "사과",
    "level": "Extended"
  },
  {
    "id": 136,
    "word": "apparent",
    "meaning": "명백한",
    "level": "Extended"
  },
  {
    "id": 137,
    "word": "appeal",
    "meaning": "호소하다",
    "level": "MidHigh"
  },
  {
    "id": 138,
    "word": "appear",
    "meaning": "나타나다",
    "level": "MidHigh",
    "variation": "disappear"
  },
  {
    "id": 139,
    "word": "apple",
    "meaning": "사과",
    "level": "Elementary"
  },
  {
    "id": 140,
    "word": "apply",
    "meaning": "신청하다",
    "level": "MidHigh",
    "variation": "applicant"
  },
  {
    "id": 141,
    "word": "appoint",
    "meaning": "임명하다",
    "level": "MidHigh"
  },
  {
    "id": 142,
    "word": "appreciate",
    "meaning": "감사하다",
    "level": "MidHigh"
  },
  {
    "id": 143,
    "word": "approach",
    "meaning": "접근하다",
    "level": "MidHigh"
  },
  {
    "id": 144,
    "word": "appropriate",
    "meaning": "적절한",
    "level": "MidHigh"
  },
  {
    "id": 145,
    "word": "approve",
    "meaning": "승인하다",
    "level": "Extended"
  },
  {
    "id": 146,
    "word": "approximate",
    "meaning": "대략적인",
    "level": "Extended"
  },
  {
    "id": 147,
    "word": "architect",
    "meaning": "건축가",
    "level": "Extended",
    "variation": "architecture"
  },
  {
    "id": 148,
    "word": "area",
    "meaning": "지역",
    "level": "Elementary"
  },
  {
    "id": 149,
    "word": "argue",
    "meaning": "논쟁하다",
    "level": "MidHigh"
  },
  {
    "id": 150,
    "word": "arise",
    "meaning": "발생하다",
    "level": "Extended"
  },
  {
    "id": 151,
    "word": "arm",
    "meaning": "팔",
    "level": "Elementary"
  },
  {
    "id": 152,
    "word": "army",
    "meaning": "군대",
    "level": "MidHigh"
  },
  {
    "id": 153,
    "word": "around",
    "meaning": "주위에",
    "level": "Elementary"
  },
  {
    "id": 154,
    "word": "arrange",
    "meaning": "정리하다",
    "level": "MidHigh"
  },
  {
    "id": 155,
    "word": "arrest",
    "meaning": "체포하다",
    "level": "MidHigh"
  },
  {
    "id": 156,
    "word": "arrive",
    "meaning": "도착하다",
    "level": "Elementary"
  },
  {
    "id": 157,
    "word": "arrow",
    "meaning": "화살",
    "level": "Extended"
  },
  {
    "id": 158,
    "word": "art",
    "meaning": "예술",
    "level": "Elementary"
  },
  {
    "id": 159,
    "word": "article",
    "meaning": "기사",
    "level": "MidHigh"
  },
  {
    "id": 160,
    "word": "artifice",
    "meaning": "기교",
    "level": "Extended",
    "variation": "artificial"
  },
  {
    "id": 161,
    "word": "as",
    "meaning": "~로서",
    "level": "Elementary"
  },
  {
    "id": 162,
    "word": "aside",
    "meaning": "한쪽으로",
    "level": "MidHigh"
  },
  {
    "id": 163,
    "word": "ask",
    "meaning": "묻다",
    "level": "Elementary"
  },
  {
    "id": 164,
    "word": "asleep",
    "meaning": "잠든",
    "level": "MidHigh"
  },
  {
    "id": 165,
    "word": "aspect",
    "meaning": "측면",
    "level": "Extended"
  },
  {
    "id": 166,
    "word": "aspire",
    "meaning": "열망하다",
    "level": "Extended"
  },
  {
    "id": 167,
    "word": "assault",
    "meaning": "폭행",
    "level": "Extended"
  },
  {
    "id": 168,
    "word": "assemble",
    "meaning": "조립하다",
    "level": "Extended"
  },
  {
    "id": 169,
    "word": "assert",
    "meaning": "주장하다",
    "level": "Extended"
  },
  {
    "id": 170,
    "word": "assess",
    "meaning": "평가하다",
    "level": "MidHigh"
  },
  {
    "id": 171,
    "word": "asset",
    "meaning": "자산",
    "level": "Extended"
  },
  {
    "id": 172,
    "word": "assign",
    "meaning": "할당하다",
    "level": "MidHigh",
    "variation": "assignment"
  },
  {
    "id": 173,
    "word": "assist",
    "meaning": "돕다",
    "level": "MidHigh",
    "variation": "assistant"
  },
  {
    "id": 174,
    "word": "associate",
    "meaning": "연관시키다",
    "level": "MidHigh"
  },
  {
    "id": 175,
    "word": "assume",
    "meaning": "가정하다",
    "level": "MidHigh"
  },
  {
    "id": 176,
    "word": "assure",
    "meaning": "확신시키다",
    "level": "Extended"
  },
  {
    "id": 177,
    "word": "astonish",
    "meaning": "깜짝 놀라게 하다",
    "level": "Extended"
  },
  {
    "id": 178,
    "word": "at",
    "meaning": "~에",
    "level": "Elementary"
  },
  {
    "id": 179,
    "word": "athlete",
    "meaning": "운동선수",
    "level": "Extended"
  },
  {
    "id": 180,
    "word": "atmosphere",
    "meaning": "대기",
    "level": "MidHigh"
  },
  {
    "id": 181,
    "word": "atom",
    "meaning": "원자",
    "level": "Extended"
  },
  {
    "id": 182,
    "word": "attach",
    "meaning": "붙이다",
    "level": "MidHigh"
  },
  {
    "id": 183,
    "word": "attack",
    "meaning": "공격하다",
    "level": "MidHigh"
  },
  {
    "id": 184,
    "word": "attempt",
    "meaning": "시도하다",
    "level": "MidHigh"
  },
  {
    "id": 185,
    "word": "attend",
    "meaning": "참석하다",
    "level": "MidHigh"
  },
  {
    "id": 186,
    "word": "attention",
    "meaning": "주의",
    "level": "MidHigh"
  },
  {
    "id": 187,
    "word": "attitude",
    "meaning": "태도",
    "level": "MidHigh"
  },
  {
    "id": 188,
    "word": "attract",
    "meaning": "끌어당기다",
    "level": "MidHigh"
  },
  {
    "id": 189,
    "word": "attribute",
    "meaning": "속성",
    "level": "Extended"
  },
  {
    "id": 190,
    "word": "auction",
    "meaning": "경매",
    "level": "Extended"
  },
  {
    "id": 191,
    "word": "audience",
    "meaning": "청중",
    "level": "MidHigh"
  },
  {
    "id": 192,
    "word": "aunt",
    "meaning": "이모",
    "level": "Elementary"
  },
  {
    "id": 193,
    "word": "authentic",
    "meaning": "진짜의",
    "level": "Extended"
  },
  {
    "id": 194,
    "word": "author",
    "meaning": "작가",
    "level": "Extended"
  },
  {
    "id": 195,
    "word": "automatic",
    "meaning": "자동적인",
    "level": "MidHigh"
  },
  {
    "id": 196,
    "word": "autumn",
    "meaning": "가을",
    "level": "Elementary"
  },
  {
    "id": 197,
    "word": "avail",
    "meaning": "이용하다",
    "level": "Extended",
    "variation": "available"
  },
  {
    "id": 198,
    "word": "average",
    "meaning": "평균",
    "level": "MidHigh"
  },
  {
    "id": 199,
    "word": "avoid",
    "meaning": "피하다",
    "level": "MidHigh"
  },
  {
    "id": 200,
    "word": "await",
    "meaning": "기다리다",
    "level": "Extended"
  },
  {
    "id": 201,
    "word": "awake",
    "meaning": "깨어 있는",
    "level": "MidHigh"
  },
  {
    "id": 202,
    "word": "award",
    "meaning": "상",
    "level": "MidHigh"
  },
  {
    "id": 203,
    "word": "aware",
    "meaning": "알고 있는",
    "level": "MidHigh",
    "variation": "unaware"
  },
  {
    "id": 204,
    "word": "away",
    "meaning": "떨어져",
    "level": "Elementary"
  },
  {
    "id": 205,
    "word": "awe",
    "meaning": "경외심",
    "level": "Extended",
    "variation": "awful"
  },
  {
    "id": 206,
    "word": "awkward",
    "meaning": "어색한",
    "level": "MidHigh"
  },
  {
    "id": 207,
    "word": "baby",
    "meaning": "아기",
    "level": "Elementary"
  },
  {
    "id": 208,
    "word": "back",
    "meaning": "뒤",
    "level": "Elementary"
  },
  {
    "id": 209,
    "word": "background",
    "meaning": "배경",
    "level": "MidHigh"
  },
  {
    "id": 210,
    "word": "bacon",
    "meaning": "베이컨",
    "level": "MidHigh"
  },
  {
    "id": 211,
    "word": "bad",
    "meaning": "나쁜",
    "level": "Elementary"
  },
  {
    "id": 212,
    "word": "badminton",
    "meaning": "배드민턴",
    "level": "Elementary"
  },
  {
    "id": 213,
    "word": "bag",
    "meaning": "가방",
    "level": "Elementary"
  },
  {
    "id": 214,
    "word": "bake",
    "meaning": "굽다",
    "level": "Elementary"
  },
  {
    "id": 215,
    "word": "balance",
    "meaning": "균형",
    "level": "MidHigh"
  },
  {
    "id": 216,
    "word": "ball",
    "meaning": "공",
    "level": "Elementary"
  },
  {
    "id": 217,
    "word": "balloon",
    "meaning": "풍선",
    "level": "MidHigh"
  },
  {
    "id": 218,
    "word": "ban",
    "meaning": "금지하다",
    "level": "Extended"
  },
  {
    "id": 219,
    "word": "banana",
    "meaning": "바나나",
    "level": "Elementary"
  },
  {
    "id": 220,
    "word": "band",
    "meaning": "악단",
    "level": "MidHigh"
  },
  {
    "id": 221,
    "word": "bang",
    "meaning": "쾅 하는 소리",
    "level": "MidHigh"
  },
  {
    "id": 222,
    "word": "bank",
    "meaning": "은행",
    "level": "Elementary"
  },
  {
    "id": 223,
    "word": "bankrupt",
    "meaning": "파산한",
    "level": "Extended"
  },
  {
    "id": 224,
    "word": "bar",
    "meaning": "막대",
    "level": "MidHigh"
  },
  {
    "id": 225,
    "word": "bare",
    "meaning": "벌거벗은",
    "level": "MidHigh"
  },
  {
    "id": 226,
    "word": "bargain",
    "meaning": "흥정",
    "level": "Extended"
  },
  {
    "id": 227,
    "word": "bark",
    "meaning": "짖다",
    "level": "MidHigh"
  },
  {
    "id": 228,
    "word": "barrier",
    "meaning": "장벽",
    "level": "Extended"
  },
  {
    "id": 229,
    "word": "base",
    "meaning": "기초",
    "level": "Elementary"
  },
  {
    "id": 230,
    "word": "baseball",
    "meaning": "야구",
    "level": "Elementary"
  },
  {
    "id": 231,
    "word": "basis",
    "meaning": "기초",
    "level": "MidHigh"
  },
  {
    "id": 232,
    "word": "basket",
    "meaning": "바구니",
    "level": "Elementary"
  },
  {
    "id": 233,
    "word": "basketball",
    "meaning": "농구",
    "level": "Elementary"
  },
  {
    "id": 234,
    "word": "bat",
    "meaning": "박쥐",
    "level": "Elementary"
  },
  {
    "id": 235,
    "word": "bath",
    "meaning": "목욕",
    "level": "Elementary"
  },
  {
    "id": 236,
    "word": "battery",
    "meaning": "배터리",
    "level": "MidHigh"
  },
  {
    "id": 237,
    "word": "battle",
    "meaning": "전투",
    "level": "MidHigh"
  },
  {
    "id": 238,
    "word": "bay",
    "meaning": "만",
    "level": "MidHigh"
  },
  {
    "id": 239,
    "word": "be",
    "meaning": "~이다",
    "level": "Elementary"
  },
  {
    "id": 240,
    "word": "beach",
    "meaning": "해변",
    "level": "Elementary"
  },
  {
    "id": 241,
    "word": "beam",
    "meaning": "광선",
    "level": "Extended"
  },
  {
    "id": 242,
    "word": "bean",
    "meaning": "콩",
    "level": "MidHigh"
  },
  {
    "id": 243,
    "word": "bear",
    "meaning": "곰",
    "level": "Elementary"
  },
  {
    "id": 244,
    "word": "beard",
    "meaning": "수염",
    "level": "Extended"
  },
  {
    "id": 245,
    "word": "beast",
    "meaning": "짐승",
    "level": "Extended"
  },
  {
    "id": 246,
    "word": "beat",
    "meaning": "때리다",
    "level": "MidHigh"
  },
  {
    "id": 247,
    "word": "beauty",
    "meaning": "아름다움",
    "level": "Elementary"
  },
  {
    "id": 248,
    "word": "because",
    "meaning": "왜냐하면",
    "level": "Elementary"
  },
  {
    "id": 249,
    "word": "become",
    "meaning": "되다",
    "level": "Elementary"
  },
  {
    "id": 250,
    "word": "bed",
    "meaning": "침대",
    "level": "Elementary"
  },
  {
    "id": 251,
    "word": "bee",
    "meaning": "벌",
    "level": "Elementary"
  },
  {
    "id": 252,
    "word": "beef",
    "meaning": "쇠고기",
    "level": "Elementary"
  },
  {
    "id": 253,
    "word": "beer",
    "meaning": "맥주",
    "level": "MidHigh"
  },
  {
    "id": 254,
    "word": "before",
    "meaning": "전에",
    "level": "Elementary"
  },
  {
    "id": 255,
    "word": "beg",
    "meaning": "구걸하다",
    "level": "MidHigh"
  },
  {
    "id": 256,
    "word": "begin",
    "meaning": "시작하다",
    "level": "Elementary"
  },
  {
    "id": 257,
    "word": "behalf",
    "meaning": "~을 대신하여",
    "level": "Extended"
  },
  {
    "id": 258,
    "word": "behave",
    "meaning": "행동하다",
    "level": "Extended",
    "variation": "behavior, behaviour"
  },
  {
    "id": 259,
    "word": "behind",
    "meaning": "뒤에",
    "level": "Elementary"
  },
  {
    "id": 260,
    "word": "belief",
    "meaning": "믿음",
    "level": "MidHigh"
  },
  {
    "id": 261,
    "word": "believe",
    "meaning": "믿다",
    "level": "Elementary"
  },
  {
    "id": 262,
    "word": "bell",
    "meaning": "종",
    "level": "Elementary"
  },
  {
    "id": 263,
    "word": "belong",
    "meaning": "속하다",
    "level": "MidHigh"
  },
  {
    "id": 264,
    "word": "below",
    "meaning": "아래에",
    "level": "Elementary"
  },
  {
    "id": 265,
    "word": "belt",
    "meaning": "허리띠",
    "level": "Elementary"
  },
  {
    "id": 266,
    "word": "bench",
    "meaning": "긴 의자",
    "level": "MidHigh"
  },
  {
    "id": 267,
    "word": "bend",
    "meaning": "구부리다",
    "level": "MidHigh"
  },
  {
    "id": 268,
    "word": "beneath",
    "meaning": "아래에",
    "level": "MidHigh"
  },
  {
    "id": 269,
    "word": "benefit",
    "meaning": "이익",
    "level": "MidHigh"
  },
  {
    "id": 270,
    "word": "beside",
    "meaning": "옆에",
    "level": "Elementary"
  },
  {
    "id": 271,
    "word": "bet",
    "meaning": "내기하다",
    "level": "MidHigh"
  },
  {
    "id": 272,
    "word": "betray",
    "meaning": "배신하다",
    "level": "Extended"
  },
  {
    "id": 273,
    "word": "between",
    "meaning": "사이에",
    "level": "Elementary"
  },
  {
    "id": 274,
    "word": "beyond",
    "meaning": "넘어서",
    "level": "MidHigh"
  },
  {
    "id": 275,
    "word": "bias",
    "meaning": "편견",
    "level": "Extended"
  },
  {
    "id": 276,
    "word": "big",
    "meaning": "큰",
    "level": "Elementary"
  },
  {
    "id": 277,
    "word": "bike",
    "meaning": "자전거",
    "level": "Elementary"
  },
  {
    "id": 278,
    "word": "bill",
    "meaning": "청구서",
    "level": "Elementary"
  },
  {
    "id": 279,
    "word": "billion",
    "meaning": "십억",
    "level": "MidHigh"
  },
  {
    "id": 280,
    "word": "bin",
    "meaning": "쓰레기통",
    "level": "MidHigh"
  },
  {
    "id": 281,
    "word": "bind",
    "meaning": "묶다",
    "level": "MidHigh"
  },
  {
    "id": 282,
    "word": "biography",
    "meaning": "전기",
    "level": "Extended"
  },
  {
    "id": 283,
    "word": "biology",
    "meaning": "생물학",
    "level": "Extended"
  },
  {
    "id": 284,
    "word": "bird",
    "meaning": "새",
    "level": "Elementary"
  },
  {
    "id": 285,
    "word": "birth",
    "meaning": "출생",
    "level": "Elementary"
  },
  {
    "id": 286,
    "word": "biscuit",
    "meaning": "비스킷",
    "level": "Elementary"
  },
  {
    "id": 287,
    "word": "bit",
    "meaning": "조금",
    "level": "MidHigh"
  },
  {
    "id": 288,
    "word": "bite",
    "meaning": "물다",
    "level": "MidHigh"
  },
  {
    "id": 289,
    "word": "bitter",
    "meaning": "쓴",
    "level": "MidHigh"
  },
  {
    "id": 290,
    "word": "black",
    "meaning": "검은색",
    "level": "Elementary"
  },
  {
    "id": 291,
    "word": "blame",
    "meaning": "비난하다",
    "level": "MidHigh"
  },
  {
    "id": 292,
    "word": "blank",
    "meaning": "빈",
    "level": "MidHigh"
  },
  {
    "id": 293,
    "word": "blanket",
    "meaning": "담요",
    "level": "MidHigh"
  },
  {
    "id": 294,
    "word": "blast",
    "meaning": "폭발",
    "level": "Extended"
  },
  {
    "id": 295,
    "word": "blend",
    "meaning": "섞다",
    "level": "Extended"
  },
  {
    "id": 296,
    "word": "bless",
    "meaning": "축복하다",
    "level": "MidHigh"
  },
  {
    "id": 297,
    "word": "blind",
    "meaning": "눈먼",
    "level": "MidHigh"
  },
  {
    "id": 298,
    "word": "blink",
    "meaning": "눈을 깜박이다",
    "level": "Extended"
  },
  {
    "id": 299,
    "word": "block",
    "meaning": "막다",
    "level": "MidHigh"
  },
  {
    "id": 300,
    "word": "blonde",
    "meaning": "금발의",
    "level": "MidHigh"
  },
  {
    "id": 301,
    "word": "blood",
    "meaning": "피",
    "level": "Elementary"
  },
  {
    "id": 302,
    "word": "bloom",
    "meaning": "꽃이 피다",
    "level": "MidHigh"
  },
  {
    "id": 303,
    "word": "blossom",
    "meaning": "꽃",
    "level": "Extended"
  },
  {
    "id": 304,
    "word": "blow",
    "meaning": "불다",
    "level": "MidHigh"
  },
  {
    "id": 305,
    "word": "blue",
    "meaning": "파란색",
    "level": "Elementary"
  },
  {
    "id": 306,
    "word": "board",
    "meaning": "판",
    "level": "Elementary"
  },
  {
    "id": 307,
    "word": "boat",
    "meaning": "배",
    "level": "Elementary"
  },
  {
    "id": 308,
    "word": "body",
    "meaning": "몸",
    "level": "Elementary",
    "variation": "embody"
  },
  {
    "id": 309,
    "word": "boil",
    "meaning": "끓다",
    "level": "MidHigh"
  },
  {
    "id": 310,
    "word": "bold",
    "meaning": "대담한",
    "level": "Extended"
  },
  {
    "id": 311,
    "word": "bomb",
    "meaning": "폭탄",
    "level": "MidHigh"
  },
  {
    "id": 312,
    "word": "bond",
    "meaning": "유대",
    "level": "MidHigh"
  },
  {
    "id": 313,
    "word": "bone",
    "meaning": "뼈",
    "level": "Elementary"
  },
  {
    "id": 314,
    "word": "book",
    "meaning": "책",
    "level": "Elementary"
  },
  {
    "id": 315,
    "word": "boom",
    "meaning": "급증",
    "level": "MidHigh"
  },
  {
    "id": 316,
    "word": "boost",
    "meaning": "촉진하다",
    "level": "Extended"
  },
  {
    "id": 317,
    "word": "boot",
    "meaning": "장화",
    "level": "MidHigh"
  },
  {
    "id": 318,
    "word": "border",
    "meaning": "국경",
    "level": "Extended"
  },
  {
    "id": 319,
    "word": "bore",
    "meaning": "지루하게 하다",
    "level": "MidHigh"
  },
  {
    "id": 320,
    "word": "borrow",
    "meaning": "빌리다",
    "level": "Elementary"
  },
  {
    "id": 321,
    "word": "boss",
    "meaning": "상사",
    "level": "MidHigh"
  },
  {
    "id": 322,
    "word": "both",
    "meaning": "둘 다",
    "level": "Elementary"
  },
  {
    "id": 323,
    "word": "bother",
    "meaning": "괴롭히다",
    "level": "MidHigh"
  },
  {
    "id": 324,
    "word": "bottle",
    "meaning": "병",
    "level": "Elementary"
  },
  {
    "id": 325,
    "word": "bottom",
    "meaning": "바닥",
    "level": "Elementary"
  },
  {
    "id": 326,
    "word": "bounce",
    "meaning": "튀어 오르다",
    "level": "MidHigh"
  },
  {
    "id": 327,
    "word": "boundary",
    "meaning": "경계",
    "level": "Extended"
  },
  {
    "id": 328,
    "word": "bow",
    "meaning": "절하다",
    "level": "MidHigh"
  },
  {
    "id": 329,
    "word": "bowl",
    "meaning": "그릇",
    "level": "MidHigh"
  },
  {
    "id": 330,
    "word": "box",
    "meaning": "상자",
    "level": "Elementary"
  },
  {
    "id": 331,
    "word": "boy",
    "meaning": "소년",
    "level": "Elementary"
  },
  {
    "id": 332,
    "word": "brain",
    "meaning": "뇌",
    "level": "MidHigh"
  },
  {
    "id": 333,
    "word": "brake",
    "meaning": "브레이크",
    "level": "MidHigh"
  },
  {
    "id": 334,
    "word": "branch",
    "meaning": "나뭇가지",
    "level": "MidHigh"
  },
  {
    "id": 335,
    "word": "brand",
    "meaning": "상표",
    "level": "MidHigh"
  },
  {
    "id": 336,
    "word": "brave",
    "meaning": "용감한",
    "level": "Elementary"
  },
  {
    "id": 337,
    "word": "bread",
    "meaning": "빵",
    "level": "Elementary"
  },
  {
    "id": 338,
    "word": "break",
    "meaning": "깨다",
    "level": "Elementary"
  },
  {
    "id": 339,
    "word": "breakfast",
    "meaning": "아침 식사",
    "level": "Elementary"
  },
  {
    "id": 340,
    "word": "breast",
    "meaning": "가슴",
    "level": "MidHigh"
  },
  {
    "id": 341,
    "word": "breath",
    "meaning": "숨",
    "level": "MidHigh"
  },
  {
    "id": 342,
    "word": "breathe",
    "meaning": "호흡하다",
    "level": "MidHigh"
  },
  {
    "id": 343,
    "word": "breed",
    "meaning": "번식하다",
    "level": "Extended"
  },
  {
    "id": 344,
    "word": "breeze",
    "meaning": "산들바람",
    "level": "Extended"
  },
  {
    "id": 345,
    "word": "brick",
    "meaning": "벽돌",
    "level": "MidHigh"
  },
  {
    "id": 346,
    "word": "bridge",
    "meaning": "다리",
    "level": "Elementary"
  },
  {
    "id": 347,
    "word": "brief",
    "meaning": "간략한",
    "level": "MidHigh"
  },
  {
    "id": 348,
    "word": "bright",
    "meaning": "밝은",
    "level": "Elementary"
  },
  {
    "id": 349,
    "word": "brilliant",
    "meaning": "훌륭한",
    "level": "MidHigh"
  },
  {
    "id": 350,
    "word": "bring",
    "meaning": "가져오다",
    "level": "Elementary"
  },
  {
    "id": 351,
    "word": "broad",
    "meaning": "넓은",
    "level": "MidHigh"
  },
  {
    "id": 352,
    "word": "broadcast",
    "meaning": "방송하다",
    "level": "Extended"
  },
  {
    "id": 353,
    "word": "brother",
    "meaning": "형제",
    "level": "Elementary"
  },
  {
    "id": 354,
    "word": "brown",
    "meaning": "갈색",
    "level": "Elementary"
  },
  {
    "id": 355,
    "word": "brush",
    "meaning": "솔",
    "level": "Elementary"
  },
  {
    "id": 356,
    "word": "brute",
    "meaning": "야만인",
    "level": "Extended",
    "variation": "brutal"
  },
  {
    "id": 357,
    "word": "bubble",
    "meaning": "거품",
    "level": "MidHigh"
  },
  {
    "id": 358,
    "word": "budget",
    "meaning": "예산",
    "level": "MidHigh"
  },
  {
    "id": 359,
    "word": "bug",
    "meaning": "벌레",
    "level": "MidHigh"
  },
  {
    "id": 360,
    "word": "build",
    "meaning": "짓다",
    "level": "Elementary"
  },
  {
    "id": 361,
    "word": "bulk",
    "meaning": "대량",
    "level": "Extended"
  },
  {
    "id": 362,
    "word": "bull",
    "meaning": "황소",
    "level": "Extended"
  },
  {
    "id": 363,
    "word": "bully",
    "meaning": "괴롭히다",
    "level": "Extended"
  },
  {
    "id": 364,
    "word": "bump",
    "meaning": "부딪치다",
    "level": "MidHigh"
  },
  {
    "id": 365,
    "word": "bunch",
    "meaning": "다발",
    "level": "MidHigh"
  },
  {
    "id": 366,
    "word": "bundle",
    "meaning": "묶음",
    "level": "Extended"
  },
  {
    "id": 367,
    "word": "burden",
    "meaning": "부담",
    "level": "Extended"
  },
  {
    "id": 368,
    "word": "burn",
    "meaning": "타다",
    "level": "Elementary"
  },
  {
    "id": 369,
    "word": "burst",
    "meaning": "터지다",
    "level": "MidHigh"
  },
  {
    "id": 370,
    "word": "bury",
    "meaning": "묻다",
    "level": "MidHigh"
  },
  {
    "id": 371,
    "word": "bus",
    "meaning": "버스",
    "level": "Elementary"
  },
  {
    "id": 372,
    "word": "bush",
    "meaning": "덤불",
    "level": "MidHigh"
  },
  {
    "id": 373,
    "word": "business",
    "meaning": "사업",
    "level": "Elementary"
  },
  {
    "id": 374,
    "word": "busy",
    "meaning": "바쁜",
    "level": "Elementary"
  },
  {
    "id": 375,
    "word": "but",
    "meaning": "그러나",
    "level": "Elementary"
  },
  {
    "id": 376,
    "word": "butcher",
    "meaning": "정육점 주인",
    "level": "Extended"
  },
  {
    "id": 377,
    "word": "butter",
    "meaning": "버터",
    "level": "Elementary"
  },
  {
    "id": 378,
    "word": "button",
    "meaning": "단추",
    "level": "Elementary"
  },
  {
    "id": 379,
    "word": "buy",
    "meaning": "사다",
    "level": "Elementary"
  },
  {
    "id": 380,
    "word": "buzz",
    "meaning": "윙윙거리다",
    "level": "Extended"
  },
  {
    "id": 381,
    "word": "by",
    "meaning": "~에 의하여",
    "level": "Elementary"
  },
  {
    "id": 382,
    "word": "cable",
    "meaning": "케이블",
    "level": "MidHigh"
  },
  {
    "id": 383,
    "word": "cage",
    "meaning": "우리",
    "level": "MidHigh"
  },
  {
    "id": 384,
    "word": "cake",
    "meaning": "케이크",
    "level": "Elementary"
  },
  {
    "id": 385,
    "word": "calculate",
    "meaning": "계산하다",
    "level": "MidHigh",
    "variation": "calculator"
  },
  {
    "id": 386,
    "word": "calendar",
    "meaning": "달력",
    "level": "MidHigh"
  },
  {
    "id": 387,
    "word": "call",
    "meaning": "부르다",
    "level": "Elementary"
  },
  {
    "id": 388,
    "word": "calm",
    "meaning": "차분한",
    "level": "MidHigh"
  },
  {
    "id": 389,
    "word": "camera",
    "meaning": "카메라",
    "level": "Elementary"
  },
  {
    "id": 390,
    "word": "camp",
    "meaning": "야영지",
    "level": "Elementary"
  },
  {
    "id": 391,
    "word": "campaign",
    "meaning": "운동",
    "level": "Elementary"
  },
  {
    "id": 392,
    "word": "can",
    "meaning": "할 수 있다",
    "level": "Elementary"
  },
  {
    "id": 393,
    "word": "cancel",
    "meaning": "취소하다",
    "level": "Extended"
  },
  {
    "id": 394,
    "word": "cancer",
    "meaning": "암",
    "level": "Extended"
  },
  {
    "id": 395,
    "word": "candidate",
    "meaning": "후보자",
    "level": "Extended"
  },
  {
    "id": 396,
    "word": "candy",
    "meaning": "사탕",
    "level": "Elementary"
  },
  {
    "id": 397,
    "word": "canvas",
    "meaning": "화폭",
    "level": "Extended"
  },
  {
    "id": 398,
    "word": "cap",
    "meaning": "모자",
    "level": "Elementary"
  },
  {
    "id": 399,
    "word": "capable",
    "meaning": "유능한",
    "level": "MidHigh"
  },
  {
    "id": 400,
    "word": "cape",
    "meaning": "망토",
    "level": "MidHigh"
  },
  {
    "id": 401,
    "word": "capital",
    "meaning": "수도",
    "level": "MidHigh"
  },
  {
    "id": 402,
    "word": "captain",
    "meaning": "선장",
    "level": "MidHigh"
  },
  {
    "id": 403,
    "word": "capture",
    "meaning": "붙잡다",
    "level": "Extended"
  },
  {
    "id": 404,
    "word": "car",
    "meaning": "자동차",
    "level": "Elementary"
  },
  {
    "id": 405,
    "word": "card",
    "meaning": "카드",
    "level": "Elementary"
  },
  {
    "id": 406,
    "word": "care",
    "meaning": "돌보다",
    "level": "Elementary"
  },
  {
    "id": 407,
    "word": "career",
    "meaning": "직업",
    "level": "MidHigh"
  },
  {
    "id": 408,
    "word": "carpet",
    "meaning": "양탄자",
    "level": "MidHigh"
  },
  {
    "id": 409,
    "word": "carrot",
    "meaning": "당근",
    "level": "Elementary"
  },
  {
    "id": 410,
    "word": "carry",
    "meaning": "나르다",
    "level": "Elementary"
  },
  {
    "id": 411,
    "word": "cart",
    "meaning": "수레",
    "level": "MidHigh"
  },
  {
    "id": 412,
    "word": "carve",
    "meaning": "새기다",
    "level": "Extended"
  },
  {
    "id": 413,
    "word": "case",
    "meaning": "경우",
    "level": "Elementary",
    "variation": "casual"
  },
  {
    "id": 414,
    "word": "cash",
    "meaning": "현금",
    "level": "Elementary"
  },
  {
    "id": 415,
    "word": "cast",
    "meaning": "던지다",
    "level": "MidHigh"
  },
  {
    "id": 416,
    "word": "castle",
    "meaning": "성",
    "level": "MidHigh"
  },
  {
    "id": 417,
    "word": "cat",
    "meaning": "고양이",
    "level": "Elementary"
  },
  {
    "id": 418,
    "word": "catalogue",
    "meaning": "목록",
    "level": "MidHigh",
    "variation": "catalog"
  },
  {
    "id": 419,
    "word": "catch",
    "meaning": "잡다",
    "level": "Elementary"
  },
  {
    "id": 420,
    "word": "category",
    "meaning": "범주",
    "level": "MidHigh"
  },
  {
    "id": 421,
    "word": "cater",
    "meaning": "음식을 제공하다",
    "level": "Extended"
  },
  {
    "id": 422,
    "word": "cattle",
    "meaning": "소",
    "level": "Extended"
  },
  {
    "id": 423,
    "word": "cause",
    "meaning": "원인",
    "level": "MidHigh",
    "variation": "causal"
  },
  {
    "id": 424,
    "word": "caution",
    "meaning": "주의",
    "level": "Extended"
  },
  {
    "id": 425,
    "word": "cave",
    "meaning": "동굴",
    "level": "Extended"
  },
  {
    "id": 426,
    "word": "cease",
    "meaning": "중지하다",
    "level": "Extended"
  },
  {
    "id": 427,
    "word": "ceiling",
    "meaning": "천장",
    "level": "MidHigh"
  },
  {
    "id": 428,
    "word": "celebrate",
    "meaning": "축하하다",
    "level": "Extended"
  },
  {
    "id": 429,
    "word": "celebrity",
    "meaning": "유명인",
    "level": "Extended"
  },
  {
    "id": 430,
    "word": "cell",
    "meaning": "세포",
    "level": "MidHigh"
  },
  {
    "id": 431,
    "word": "censor",
    "meaning": "검열하다",
    "level": "Extended"
  },
  {
    "id": 432,
    "word": "center",
    "meaning": "중심",
    "level": "Elementary"
  },
  {
    "id": 433,
    "word": "century",
    "meaning": "세기",
    "level": "MidHigh"
  },
  {
    "id": 434,
    "word": "certain",
    "meaning": "확실한",
    "level": "Elementary"
  },
  {
    "id": 435,
    "word": "certificate",
    "meaning": "증명서",
    "level": "Extended"
  },
  {
    "id": 436,
    "word": "chain",
    "meaning": "사슬",
    "level": "MidHigh"
  },
  {
    "id": 437,
    "word": "chair",
    "meaning": "의자",
    "level": "Elementary"
  },
  {
    "id": 438,
    "word": "chairman",
    "meaning": "의장",
    "level": "MidHigh"
  },
  {
    "id": 439,
    "word": "challenge",
    "meaning": "도전",
    "level": "MidHigh"
  },
  {
    "id": 440,
    "word": "chamber",
    "meaning": "방",
    "level": "Extended"
  },
  {
    "id": 441,
    "word": "champion",
    "meaning": "우승자",
    "level": "MidHigh"
  },
  {
    "id": 442,
    "word": "chance",
    "meaning": "기회",
    "level": "Elementary"
  },
  {
    "id": 443,
    "word": "change",
    "meaning": "변화",
    "level": "Elementary"
  },
  {
    "id": 444,
    "word": "channel",
    "meaning": "채널",
    "level": "MidHigh"
  },
  {
    "id": 445,
    "word": "chaos",
    "meaning": "혼돈",
    "level": "Extended"
  },
  {
    "id": 446,
    "word": "character",
    "meaning": "성격",
    "level": "MidHigh"
  },
  {
    "id": 447,
    "word": "characteristic",
    "meaning": "특징적인",
    "level": "MidHigh"
  },
  {
    "id": 448,
    "word": "charge",
    "meaning": "요금",
    "level": "MidHigh",
    "variation": "discharge"
  },
  {
    "id": 449,
    "word": "charity",
    "meaning": "자선",
    "level": "Extended"
  },
  {
    "id": 450,
    "word": "charm",
    "meaning": "매력",
    "level": "MidHigh"
  },
  {
    "id": 451,
    "word": "chart",
    "meaning": "도표",
    "level": "MidHigh"
  },
  {
    "id": 452,
    "word": "chase",
    "meaning": "쫓다",
    "level": "MidHigh"
  },
  {
    "id": 453,
    "word": "chat",
    "meaning": "대화하다",
    "level": "MidHigh"
  },
  {
    "id": 454,
    "word": "cheap",
    "meaning": "싼",
    "level": "Elementary"
  },
  {
    "id": 455,
    "word": "check",
    "meaning": "확인하다",
    "level": "Elementary",
    "variation": "cheque"
  },
  {
    "id": 456,
    "word": "cheek",
    "meaning": "뺨",
    "level": "MidHigh"
  },
  {
    "id": 457,
    "word": "cheer",
    "meaning": "응원하다",
    "level": "MidHigh"
  },
  {
    "id": 458,
    "word": "cheese",
    "meaning": "치즈",
    "level": "Elementary"
  },
  {
    "id": 459,
    "word": "chef",
    "meaning": "요리사",
    "level": "Extended"
  },
  {
    "id": 460,
    "word": "chemical",
    "meaning": "화학적인",
    "level": "Extended"
  },
  {
    "id": 461,
    "word": "chest",
    "meaning": "가슴",
    "level": "MidHigh"
  },
  {
    "id": 462,
    "word": "chew",
    "meaning": "씹다",
    "level": "MidHigh"
  },
  {
    "id": 463,
    "word": "chicken",
    "meaning": "닭",
    "level": "Elementary"
  },
  {
    "id": 464,
    "word": "chief",
    "meaning": "주요한",
    "level": "MidHigh"
  },
  {
    "id": 465,
    "word": "child",
    "meaning": "아이",
    "level": "Elementary"
  },
  {
    "id": 466,
    "word": "chill",
    "meaning": "한기",
    "level": "Extended"
  },
  {
    "id": 467,
    "word": "chin",
    "meaning": "턱",
    "level": "Extended"
  },
  {
    "id": 468,
    "word": "chip",
    "meaning": "조각",
    "level": "MidHigh"
  },
  {
    "id": 469,
    "word": "chocolate",
    "meaning": "초콜릿",
    "level": "Elementary"
  },
  {
    "id": 470,
    "word": "choice",
    "meaning": "선택",
    "level": "MidHigh"
  },
  {
    "id": 471,
    "word": "choir",
    "meaning": "합창단",
    "level": "Extended"
  },
  {
    "id": 472,
    "word": "choose",
    "meaning": "고르다",
    "level": "Elementary"
  },
  {
    "id": 473,
    "word": "chop",
    "meaning": "자르다",
    "level": "MidHigh"
  },
  {
    "id": 474,
    "word": "chorus",
    "meaning": "후렴",
    "level": "Extended"
  },
  {
    "id": 475,
    "word": "chronic",
    "meaning": "만성적인",
    "level": "Extended"
  },
  {
    "id": 476,
    "word": "church",
    "meaning": "교회",
    "level": "Elementary"
  },
  {
    "id": 477,
    "word": "cigarette",
    "meaning": "담배",
    "level": "MidHigh"
  },
  {
    "id": 478,
    "word": "cinema",
    "meaning": "영화관",
    "level": "MidHigh"
  },
  {
    "id": 479,
    "word": "circle",
    "meaning": "원",
    "level": "Elementary"
  },
  {
    "id": 480,
    "word": "circulate",
    "meaning": "순환하다",
    "level": "Extended"
  },
  {
    "id": 481,
    "word": "circumstance",
    "meaning": "상황",
    "level": "MidHigh"
  },
  {
    "id": 482,
    "word": "cite",
    "meaning": "인용하다",
    "level": "Extended"
  },
  {
    "id": 483,
    "word": "citizen",
    "meaning": "시민",
    "level": "MidHigh"
  },
  {
    "id": 484,
    "word": "city",
    "meaning": "도시",
    "level": "Elementary"
  },
  {
    "id": 485,
    "word": "civil",
    "meaning": "시민의",
    "level": "MidHigh"
  },
  {
    "id": 486,
    "word": "claim",
    "meaning": "주장하다",
    "level": "MidHigh"
  },
  {
    "id": 487,
    "word": "clap",
    "meaning": "박수 치다",
    "level": "Extended"
  },
  {
    "id": 488,
    "word": "clash",
    "meaning": "충돌",
    "level": "Extended"
  },
  {
    "id": 489,
    "word": "class",
    "meaning": "수업",
    "level": "Elementary",
    "variation": "classic, classify"
  },
  {
    "id": 490,
    "word": "clause",
    "meaning": "절",
    "level": "Extended"
  },
  {
    "id": 491,
    "word": "clay",
    "meaning": "진흙",
    "level": "Extended"
  },
  {
    "id": 492,
    "word": "clean",
    "meaning": "깨끗한",
    "level": "Elementary"
  },
  {
    "id": 493,
    "word": "clear",
    "meaning": "분명한",
    "level": "Elementary",
    "variation": "clarify"
  },
  {
    "id": 494,
    "word": "clerk",
    "meaning": "사무원",
    "level": "MidHigh"
  },
  {
    "id": 495,
    "word": "clever",
    "meaning": "영리한",
    "level": "Elementary"
  },
  {
    "id": 496,
    "word": "click",
    "meaning": "딸깍 소리",
    "level": "MidHigh"
  },
  {
    "id": 497,
    "word": "client",
    "meaning": "고객",
    "level": "MidHigh"
  },
  {
    "id": 498,
    "word": "cliff",
    "meaning": "절벽",
    "level": "MidHigh"
  },
  {
    "id": 499,
    "word": "climate",
    "meaning": "기후",
    "level": "MidHigh"
  },
  {
    "id": 500,
    "word": "climb",
    "meaning": "오르다",
    "level": "Elementary"
  },
  {
    "id": 501,
    "word": "cling",
    "meaning": "달라붙다",
    "level": "Extended"
  },
  {
    "id": 502,
    "word": "clinic",
    "meaning": "진료소",
    "level": "Extended"
  },
  {
    "id": 503,
    "word": "clip",
    "meaning": "클립",
    "level": "MidHigh"
  },
  {
    "id": 504,
    "word": "clock",
    "meaning": "시계",
    "level": "Elementary"
  },
  {
    "id": 505,
    "word": "close",
    "meaning": "닫다",
    "level": "Elementary",
    "variation": "disclose, enclose"
  },
  {
    "id": 506,
    "word": "clothes",
    "meaning": "옷",
    "level": "Elementary"
  },
  {
    "id": 507,
    "word": "cloud",
    "meaning": "구름",
    "level": "Elementary"
  },
  {
    "id": 508,
    "word": "club",
    "meaning": "동아리",
    "level": "Elementary"
  },
  {
    "id": 509,
    "word": "clue",
    "meaning": "단서",
    "level": "MidHigh"
  },
  {
    "id": 510,
    "word": "cluster",
    "meaning": "무리",
    "level": "Extended"
  },
  {
    "id": 511,
    "word": "coach",
    "meaning": "코치",
    "level": "MidHigh"
  },
  {
    "id": 512,
    "word": "coal",
    "meaning": "석탄",
    "level": "MidHigh"
  },
  {
    "id": 513,
    "word": "coast",
    "meaning": "해안",
    "level": "MidHigh"
  },
  {
    "id": 514,
    "word": "coat",
    "meaning": "외투",
    "level": "Elementary"
  },
  {
    "id": 515,
    "word": "code",
    "meaning": "암호",
    "level": "MidHigh"
  },
  {
    "id": 516,
    "word": "coffee",
    "meaning": "커피",
    "level": "Elementary"
  },
  {
    "id": 517,
    "word": "coin",
    "meaning": "동전",
    "level": "MidHigh"
  },
  {
    "id": 518,
    "word": "coincide",
    "meaning": "동시에 일어나다",
    "level": "Extended"
  },
  {
    "id": 519,
    "word": "cold",
    "meaning": "추운",
    "level": "Elementary"
  },
  {
    "id": 520,
    "word": "collaborate",
    "meaning": "협업하다",
    "level": "Extended"
  },
  {
    "id": 521,
    "word": "collapse",
    "meaning": "붕괴하다",
    "level": "Extended"
  },
  {
    "id": 522,
    "word": "collar",
    "meaning": "옷깃",
    "level": "Extended"
  },
  {
    "id": 523,
    "word": "colleague",
    "meaning": "동료",
    "level": "Extended"
  },
  {
    "id": 524,
    "word": "collect",
    "meaning": "모으다",
    "level": "Elementary"
  },
  {
    "id": 525,
    "word": "college",
    "meaning": "대학",
    "level": "Elementary"
  },
  {
    "id": 526,
    "word": "colony",
    "meaning": "식민지",
    "level": "Extended"
  },
  {
    "id": 527,
    "word": "color",
    "meaning": "색깔",
    "level": "Elementary",
    "variation": "colour"
  },
  {
    "id": 528,
    "word": "column",
    "meaning": "기둥",
    "level": "Extended"
  },
  {
    "id": 529,
    "word": "combat",
    "meaning": "전투",
    "level": "Extended"
  },
  {
    "id": 530,
    "word": "combine",
    "meaning": "결합하다",
    "level": "MidHigh"
  },
  {
    "id": 531,
    "word": "come",
    "meaning": "오다",
    "level": "Elementary"
  },
  {
    "id": 532,
    "word": "comedy",
    "meaning": "희극",
    "level": "MidHigh"
  },
  {
    "id": 533,
    "word": "comfort",
    "meaning": "편안함",
    "level": "MidHigh",
    "variation": "comfortable"
  },
  {
    "id": 534,
    "word": "comic",
    "meaning": "만화",
    "level": "Elementary"
  },
  {
    "id": 535,
    "word": "command",
    "meaning": "명령",
    "level": "MidHigh"
  },
  {
    "id": 536,
    "word": "comment",
    "meaning": "논평",
    "level": "MidHigh"
  },
  {
    "id": 537,
    "word": "commerce",
    "meaning": "상업",
    "level": "MidHigh"
  },
  {
    "id": 538,
    "word": "commit",
    "meaning": "전념하다",
    "level": "Extended",
    "variation": "commission"
  },
  {
    "id": 539,
    "word": "committee",
    "meaning": "위원회",
    "level": "MidHigh"
  },
  {
    "id": 540,
    "word": "commodity",
    "meaning": "상품",
    "level": "Extended"
  },
  {
    "id": 541,
    "word": "common",
    "meaning": "공통의",
    "level": "MidHigh"
  },
  {
    "id": 542,
    "word": "communicate",
    "meaning": "의사소통하다",
    "level": "MidHigh",
    "variation": "communication"
  },
  {
    "id": 543,
    "word": "communist",
    "meaning": "공산주의자",
    "level": "Extended"
  },
  {
    "id": 544,
    "word": "community",
    "meaning": "공동체",
    "level": "MidHigh"
  },
  {
    "id": 545,
    "word": "companion",
    "meaning": "동반자",
    "level": "Extended"
  },
  {
    "id": 546,
    "word": "company",
    "meaning": "회사",
    "level": "Elementary"
  },
  {
    "id": 547,
    "word": "compare",
    "meaning": "비교하다",
    "level": "MidHigh"
  },
  {
    "id": 548,
    "word": "compatible",
    "meaning": "양립할 수 있는",
    "level": "Extended"
  },
  {
    "id": 549,
    "word": "compel",
    "meaning": "강요하다",
    "level": "Extended"
  },
  {
    "id": 550,
    "word": "compensate",
    "meaning": "보상하다",
    "level": "Extended"
  },
  {
    "id": 551,
    "word": "compete",
    "meaning": "경쟁하다",
    "level": "Extended",
    "variation": "competent"
  },
  {
    "id": 552,
    "word": "compile",
    "meaning": "편집하다",
    "level": "Extended"
  },
  {
    "id": 553,
    "word": "complain",
    "meaning": "불평하다",
    "level": "MidHigh"
  },
  {
    "id": 554,
    "word": "complement",
    "meaning": "보완하다",
    "level": "Extended"
  },
  {
    "id": 555,
    "word": "complete",
    "meaning": "완성하다",
    "level": "MidHigh"
  },
  {
    "id": 556,
    "word": "complex",
    "meaning": "복잡한",
    "level": "MidHigh",
    "variation": "complexity"
  },
  {
    "id": 557,
    "word": "complicate",
    "meaning": "복잡하게 하다",
    "level": "MidHigh"
  },
  {
    "id": 558,
    "word": "component",
    "meaning": "구성 요소",
    "level": "Extended"
  },
  {
    "id": 559,
    "word": "compose",
    "meaning": "구성하다",
    "level": "Extended"
  },
  {
    "id": 560,
    "word": "compound",
    "meaning": "화합물",
    "level": "Extended"
  },
  {
    "id": 561,
    "word": "comprehend",
    "meaning": "이해하다",
    "level": "Extended",
    "variation": "comprehensive"
  },
  {
    "id": 562,
    "word": "comprise",
    "meaning": "포함하다",
    "level": "Extended"
  },
  {
    "id": 563,
    "word": "compromise",
    "meaning": "타협하다",
    "level": "Extended"
  },
  {
    "id": 564,
    "word": "compute",
    "meaning": "계산하다",
    "level": "Elementary",
    "variation": "computer"
  },
  {
    "id": 565,
    "word": "conceal",
    "meaning": "숨기다",
    "level": "Extended"
  },
  {
    "id": 566,
    "word": "conceive",
    "meaning": "생각해 내다",
    "level": "Extended"
  },
  {
    "id": 567,
    "word": "concentrate",
    "meaning": "집중하다",
    "level": "MidHigh"
  },
  {
    "id": 568,
    "word": "concept",
    "meaning": "개념",
    "level": "MidHigh"
  },
  {
    "id": 569,
    "word": "concern",
    "meaning": "우려",
    "level": "MidHigh"
  },
  {
    "id": 570,
    "word": "concert",
    "meaning": "연주회",
    "level": "MidHigh"
  },
  {
    "id": 571,
    "word": "conclude",
    "meaning": "결론짓다",
    "level": "Extended"
  },
  {
    "id": 572,
    "word": "concrete",
    "meaning": "콘크리트",
    "level": "Extended"
  },
  {
    "id": 573,
    "word": "condemn",
    "meaning": "비난하다",
    "level": "Extended"
  },
  {
    "id": 574,
    "word": "condition",
    "meaning": "상태",
    "level": "Elementary"
  },
  {
    "id": 575,
    "word": "conduct",
    "meaning": "수행하다",
    "level": "Extended"
  },
  {
    "id": 576,
    "word": "confer",
    "meaning": "협의하다",
    "level": "Extended"
  },
  {
    "id": 577,
    "word": "confess",
    "meaning": "고백하다",
    "level": "Extended"
  },
  {
    "id": 578,
    "word": "confide",
    "meaning": "털어놓다",
    "level": "Extended",
    "variation": "confident"
  },
  {
    "id": 579,
    "word": "confine",
    "meaning": "가두다",
    "level": "Extended"
  },
  {
    "id": 580,
    "word": "confirm",
    "meaning": "확인하다",
    "level": "MidHigh"
  },
  {
    "id": 581,
    "word": "conflict",
    "meaning": "갈등",
    "level": "MidHigh"
  },
  {
    "id": 582,
    "word": "conform",
    "meaning": "따르다",
    "level": "Extended"
  },
  {
    "id": 583,
    "word": "confront",
    "meaning": "맞서다",
    "level": "Extended"
  },
  {
    "id": 584,
    "word": "confuse",
    "meaning": "혼란스럽게 하다",
    "level": "MidHigh"
  },
  {
    "id": 585,
    "word": "congratulate",
    "meaning": "축하하다",
    "level": "Elementary"
  },
  {
    "id": 586,
    "word": "congress",
    "meaning": "의회",
    "level": "Extended"
  },
  {
    "id": 587,
    "word": "connect",
    "meaning": "연결하다",
    "level": "MidHigh"
  },
  {
    "id": 588,
    "word": "conscience",
    "meaning": "양심",
    "level": "Extended"
  },
  {
    "id": 589,
    "word": "conscious",
    "meaning": "의식하는",
    "level": "MidHigh"
  },
  {
    "id": 590,
    "word": "consent",
    "meaning": "동의",
    "level": "Extended"
  },
  {
    "id": 591,
    "word": "conserve",
    "meaning": "보존하다",
    "level": "Extended"
  },
  {
    "id": 592,
    "word": "consider",
    "meaning": "고려하다",
    "level": "MidHigh"
  },
  {
    "id": 593,
    "word": "consist",
    "meaning": "구성되다",
    "level": "Extended",
    "variation": "consistent"
  },
  {
    "id": 594,
    "word": "constant",
    "meaning": "일정한",
    "level": "MidHigh"
  },
  {
    "id": 595,
    "word": "constitute",
    "meaning": "구성하다",
    "level": "Extended",
    "variation": "constitution"
  },
  {
    "id": 596,
    "word": "constrain",
    "meaning": "제한하다",
    "level": "Extended"
  },
  {
    "id": 597,
    "word": "construct",
    "meaning": "건설하다",
    "level": "Extended",
    "variation": "construction"
  },
  {
    "id": 598,
    "word": "consult",
    "meaning": "상담하다",
    "level": "Extended"
  },
  {
    "id": 599,
    "word": "consume",
    "meaning": "소비하다",
    "level": "MidHigh",
    "variation": "consumer, consumption"
  },
  {
    "id": 600,
    "word": "contact",
    "meaning": "연락",
    "level": "MidHigh"
  },
  {
    "id": 601,
    "word": "contain",
    "meaning": "포함하다",
    "level": "MidHigh"
  },
  {
    "id": 602,
    "word": "contemporary",
    "meaning": "현대의",
    "level": "Extended"
  },
  {
    "id": 603,
    "word": "contend",
    "meaning": "다투다",
    "level": "Extended"
  },
  {
    "id": 604,
    "word": "content",
    "meaning": "내용",
    "level": "MidHigh"
  },
  {
    "id": 605,
    "word": "contest",
    "meaning": "대회",
    "level": "MidHigh"
  },
  {
    "id": 606,
    "word": "context",
    "meaning": "맥락",
    "level": "MidHigh"
  },
  {
    "id": 607,
    "word": "continent",
    "meaning": "대륙",
    "level": "Extended"
  },
  {
    "id": 608,
    "word": "continue",
    "meaning": "계속하다",
    "level": "MidHigh"
  },
  {
    "id": 609,
    "word": "contract",
    "meaning": "계약",
    "level": "MidHigh"
  },
  {
    "id": 610,
    "word": "contradict",
    "meaning": "모순되다",
    "level": "Extended"
  },
  {
    "id": 611,
    "word": "contrary",
    "meaning": "반대의",
    "level": "Extended"
  },
  {
    "id": 612,
    "word": "contrast",
    "meaning": "대조",
    "level": "Extended"
  },
  {
    "id": 613,
    "word": "contribute",
    "meaning": "기여하다",
    "level": "MidHigh"
  },
  {
    "id": 614,
    "word": "control",
    "meaning": "통제하다",
    "level": "Elementary"
  },
  {
    "id": 615,
    "word": "controversy",
    "meaning": "논란",
    "level": "Extended"
  },
  {
    "id": 616,
    "word": "convene",
    "meaning": "소집하다",
    "level": "Extended",
    "variation": "convenient, convention"
  },
  {
    "id": 617,
    "word": "converse",
    "meaning": "대화하다",
    "level": "MidHigh",
    "variation": "conversation"
  },
  {
    "id": 618,
    "word": "convert",
    "meaning": "전환하다",
    "level": "Extended"
  },
  {
    "id": 619,
    "word": "convey",
    "meaning": "전달하다",
    "level": "Extended"
  },
  {
    "id": 620,
    "word": "convict",
    "meaning": "유죄를 선고하다",
    "level": "Extended"
  },
  {
    "id": 621,
    "word": "convince",
    "meaning": "설득하다",
    "level": "MidHigh"
  },
  {
    "id": 622,
    "word": "cook",
    "meaning": "요리하다",
    "level": "Elementary"
  },
  {
    "id": 623,
    "word": "cookie",
    "meaning": "과자",
    "level": "Elementary",
    "variation": "cooky"
  },
  {
    "id": 624,
    "word": "cool",
    "meaning": "시원한",
    "level": "Elementary"
  },
  {
    "id": 625,
    "word": "cooperate",
    "meaning": "협력하다",
    "level": "Extended"
  },
  {
    "id": 626,
    "word": "coordinate",
    "meaning": "조정하다",
    "level": "Extended"
  },
  {
    "id": 627,
    "word": "cop",
    "meaning": "경찰관",
    "level": "MidHigh"
  },
  {
    "id": 628,
    "word": "cope",
    "meaning": "대처하다",
    "level": "MidHigh"
  },
  {
    "id": 629,
    "word": "copy",
    "meaning": "복사하다",
    "level": "MidHigh"
  },
  {
    "id": 630,
    "word": "copyright",
    "meaning": "저작권",
    "level": "Extended"
  },
  {
    "id": 631,
    "word": "cord",
    "meaning": "끈",
    "level": "Extended"
  },
  {
    "id": 632,
    "word": "core",
    "meaning": "핵심",
    "level": "Extended"
  },
  {
    "id": 633,
    "word": "corn",
    "meaning": "옥수수",
    "level": "Extended"
  },
  {
    "id": 634,
    "word": "corner",
    "meaning": "모퉁이",
    "level": "Elementary"
  },
  {
    "id": 635,
    "word": "corporate",
    "meaning": "기업의",
    "level": "Extended",
    "variation": "corporation"
  },
  {
    "id": 636,
    "word": "correct",
    "meaning": "올바른",
    "level": "MidHigh"
  },
  {
    "id": 637,
    "word": "correspond",
    "meaning": "일치하다",
    "level": "Extended"
  },
  {
    "id": 638,
    "word": "corridor",
    "meaning": "복도",
    "level": "Extended"
  },
  {
    "id": 639,
    "word": "corrupt",
    "meaning": "부패한",
    "level": "Extended"
  },
  {
    "id": 640,
    "word": "cost",
    "meaning": "비용",
    "level": "Elementary"
  },
  {
    "id": 641,
    "word": "costume",
    "meaning": "의상",
    "level": "Extended"
  },
  {
    "id": 642,
    "word": "cottage",
    "meaning": "시골집",
    "level": "MidHigh"
  },
  {
    "id": 643,
    "word": "cotton",
    "meaning": "면화",
    "level": "MidHigh"
  },
  {
    "id": 644,
    "word": "cough",
    "meaning": "기침하다",
    "level": "MidHigh"
  },
  {
    "id": 645,
    "word": "could",
    "meaning": "~할 수 있었다",
    "level": "Elementary"
  },
  {
    "id": 646,
    "word": "council",
    "meaning": "의회",
    "level": "MidHigh"
  },
  {
    "id": 647,
    "word": "counsel",
    "meaning": "상담",
    "level": "Extended"
  },
  {
    "id": 648,
    "word": "count",
    "meaning": "세다",
    "level": "MidHigh",
    "variation": "discount, counter"
  },
  {
    "id": 649,
    "word": "counterpart",
    "meaning": "대응물",
    "level": "Extended"
  },
  {
    "id": 650,
    "word": "country",
    "meaning": "나라",
    "level": "Elementary"
  },
  {
    "id": 651,
    "word": "countryside",
    "meaning": "시골",
    "level": "MidHigh"
  },
  {
    "id": 652,
    "word": "county",
    "meaning": "군",
    "level": "MidHigh"
  },
  {
    "id": 653,
    "word": "couple",
    "meaning": "한 쌍",
    "level": "Elementary"
  },
  {
    "id": 654,
    "word": "coupon",
    "meaning": "쿠폰",
    "level": "Extended"
  },
  {
    "id": 655,
    "word": "courage",
    "meaning": "용기",
    "level": "Extended",
    "variation": "discourage, encourage"
  },
  {
    "id": 656,
    "word": "course",
    "meaning": "과정",
    "level": "Elementary"
  },
  {
    "id": 657,
    "word": "court",
    "meaning": "법정",
    "level": "Elementary"
  },
  {
    "id": 658,
    "word": "cousin",
    "meaning": "사촌",
    "level": "Elementary"
  },
  {
    "id": 659,
    "word": "cover",
    "meaning": "덮다",
    "level": "Elementary",
    "variation": "discover"
  },
  {
    "id": 660,
    "word": "cow",
    "meaning": "암소",
    "level": "Elementary"
  },
  {
    "id": 661,
    "word": "crack",
    "meaning": "금",
    "level": "MidHigh"
  },
  {
    "id": 662,
    "word": "craft",
    "meaning": "공예",
    "level": "Extended"
  },
  {
    "id": 663,
    "word": "crash",
    "meaning": "충돌하다",
    "level": "MidHigh"
  },
  {
    "id": 664,
    "word": "crawl",
    "meaning": "기어가다",
    "level": "MidHigh"
  },
  {
    "id": 665,
    "word": "crayon",
    "meaning": "크레용",
    "level": "Elementary"
  },
  {
    "id": 666,
    "word": "craze",
    "meaning": "열광",
    "level": "Extended",
    "variation": "crazy"
  },
  {
    "id": 667,
    "word": "cream",
    "meaning": "크림",
    "level": "Elementary"
  },
  {
    "id": 668,
    "word": "create",
    "meaning": "창조하다",
    "level": "MidHigh",
    "variation": "creature"
  },
  {
    "id": 669,
    "word": "credible",
    "meaning": "믿을 수 있는",
    "level": "Extended",
    "variation": "incredible"
  },
  {
    "id": 670,
    "word": "credit",
    "meaning": "신용",
    "level": "MidHigh"
  },
  {
    "id": 671,
    "word": "creep",
    "meaning": "살금살금 움직이다",
    "level": "Extended"
  },
  {
    "id": 672,
    "word": "crew",
    "meaning": "승무원",
    "level": "Extended"
  },
  {
    "id": 673,
    "word": "crime",
    "meaning": "범죄",
    "level": "MidHigh",
    "variation": "criminal"
  },
  {
    "id": 674,
    "word": "crisis",
    "meaning": "위기",
    "level": "MidHigh"
  },
  {
    "id": 675,
    "word": "crisp",
    "meaning": "바삭바삭한",
    "level": "MidHigh"
  },
  {
    "id": 676,
    "word": "criterion",
    "meaning": "기준",
    "level": "Extended"
  },
  {
    "id": 677,
    "word": "critic",
    "meaning": "비평가",
    "level": "Extended",
    "variation": "criticize, criticise, criticism"
  },
  {
    "id": 678,
    "word": "crop",
    "meaning": "농작물",
    "level": "Extended"
  },
  {
    "id": 679,
    "word": "cross",
    "meaning": "가로지르다",
    "level": "Elementary"
  },
  {
    "id": 680,
    "word": "crowd",
    "meaning": "군중",
    "level": "MidHigh"
  },
  {
    "id": 681,
    "word": "crown",
    "meaning": "왕관",
    "level": "MidHigh"
  },
  {
    "id": 682,
    "word": "crucial",
    "meaning": "중요한",
    "level": "Extended"
  },
  {
    "id": 683,
    "word": "cruel",
    "meaning": "잔인한",
    "level": "MidHigh"
  },
  {
    "id": 684,
    "word": "cruise",
    "meaning": "유람",
    "level": "Extended"
  },
  {
    "id": 685,
    "word": "crush",
    "meaning": "짓누르다",
    "level": "Extended"
  },
  {
    "id": 686,
    "word": "cry",
    "meaning": "울다",
    "level": "Elementary"
  },
  {
    "id": 687,
    "word": "crystal",
    "meaning": "수정",
    "level": "Extended"
  },
  {
    "id": 688,
    "word": "cultivate",
    "meaning": "경작하다",
    "level": "Extended"
  },
  {
    "id": 689,
    "word": "culture",
    "meaning": "문화",
    "level": "Elementary"
  },
  {
    "id": 690,
    "word": "cup",
    "meaning": "컵",
    "level": "Elementary"
  },
  {
    "id": 691,
    "word": "cure",
    "meaning": "치료하다",
    "level": "MidHigh"
  },
  {
    "id": 692,
    "word": "curious",
    "meaning": "호기심 많은",
    "level": "MidHigh",
    "variation": "curiosity"
  },
  {
    "id": 693,
    "word": "curl",
    "meaning": "곱슬거리다",
    "level": "MidHigh"
  },
  {
    "id": 694,
    "word": "currency",
    "meaning": "통화",
    "level": "Extended"
  },
  {
    "id": 695,
    "word": "current",
    "meaning": "현재의",
    "level": "MidHigh"
  },
  {
    "id": 696,
    "word": "curriculum",
    "meaning": "교육과정",
    "level": "Extended"
  },
  {
    "id": 697,
    "word": "curry",
    "meaning": "카레",
    "level": "Extended"
  },
  {
    "id": 698,
    "word": "curse",
    "meaning": "저주",
    "level": "Extended"
  },
  {
    "id": 699,
    "word": "curtain",
    "meaning": "커튼",
    "level": "Elementary"
  },
  {
    "id": 700,
    "word": "curve",
    "meaning": "곡선",
    "level": "Extended"
  },
  {
    "id": 701,
    "word": "custody",
    "meaning": "보호 관리",
    "level": "Extended"
  },
  {
    "id": 702,
    "word": "custom",
    "meaning": "관습",
    "level": "Extended"
  },
  {
    "id": 703,
    "word": "customer",
    "meaning": "고객",
    "level": "Elementary"
  },
  {
    "id": 704,
    "word": "cut",
    "meaning": "자르다",
    "level": "Elementary"
  },
  {
    "id": 705,
    "word": "cute",
    "meaning": "귀여운",
    "level": "MidHigh"
  },
  {
    "id": 706,
    "word": "cycle",
    "meaning": "순환",
    "level": "MidHigh",
    "variation": "recycle, cyclist"
  },
  {
    "id": 707,
    "word": "cynical",
    "meaning": "냉소적인",
    "level": "Extended"
  },
  {
    "id": 708,
    "word": "dairy",
    "meaning": "유제품",
    "level": "Extended"
  },
  {
    "id": 709,
    "word": "damage",
    "meaning": "손상",
    "level": "MidHigh"
  },
  {
    "id": 710,
    "word": "damp",
    "meaning": "축축한",
    "level": "Extended"
  },
  {
    "id": 711,
    "word": "dance",
    "meaning": "춤추다",
    "level": "Elementary"
  },
  {
    "id": 712,
    "word": "danger",
    "meaning": "위험",
    "level": "Elementary"
  },
  {
    "id": 713,
    "word": "dare",
    "meaning": "감히 하다",
    "level": "MidHigh"
  },
  {
    "id": 714,
    "word": "dark",
    "meaning": "어두운",
    "level": "Elementary"
  },
  {
    "id": 715,
    "word": "darling",
    "meaning": "사랑하는 사람",
    "level": "MidHigh"
  },
  {
    "id": 716,
    "word": "dash",
    "meaning": "돌진",
    "level": "Extended"
  },
  {
    "id": 717,
    "word": "database",
    "meaning": "데이터베이스",
    "level": "Extended"
  },
  {
    "id": 718,
    "word": "date",
    "meaning": "날짜",
    "level": "Elementary"
  },
  {
    "id": 719,
    "word": "datum",
    "meaning": "자료",
    "level": "Extended",
    "variation": "data"
  },
  {
    "id": 720,
    "word": "daughter",
    "meaning": "딸",
    "level": "Elementary"
  },
  {
    "id": 721,
    "word": "dawn",
    "meaning": "새벽",
    "level": "MidHigh"
  },
  {
    "id": 722,
    "word": "day",
    "meaning": "날",
    "level": "Elementary"
  },
  {
    "id": 723,
    "word": "dead",
    "meaning": "죽은",
    "level": "Elementary"
  },
  {
    "id": 724,
    "word": "deal",
    "meaning": "거래",
    "level": "MidHigh"
  },
  {
    "id": 725,
    "word": "death",
    "meaning": "죽음",
    "level": "Elementary"
  },
  {
    "id": 726,
    "word": "debate",
    "meaning": "토론",
    "level": "MidHigh"
  },
  {
    "id": 727,
    "word": "debt",
    "meaning": "빚",
    "level": "MidHigh"
  },
  {
    "id": 728,
    "word": "decade",
    "meaning": "십 년",
    "level": "Extended"
  },
  {
    "id": 729,
    "word": "decay",
    "meaning": "부패하다",
    "level": "Extended"
  },
  {
    "id": 730,
    "word": "decent",
    "meaning": "괜찮은",
    "level": "Extended"
  },
  {
    "id": 731,
    "word": "decide",
    "meaning": "결정하다",
    "level": "Elementary",
    "variation": "decision"
  },
  {
    "id": 732,
    "word": "deck",
    "meaning": "갑판",
    "level": "MidHigh"
  },
  {
    "id": 733,
    "word": "declare",
    "meaning": "선언하다",
    "level": "Extended"
  },
  {
    "id": 734,
    "word": "decline",
    "meaning": "감소하다",
    "level": "Extended",
    "variation": "declension"
  },
  {
    "id": 735,
    "word": "decorate",
    "meaning": "장식하다",
    "level": "MidHigh"
  },
  {
    "id": 736,
    "word": "decrease",
    "meaning": "줄어들다",
    "level": "Extended"
  },
  {
    "id": 737,
    "word": "dedicate",
    "meaning": "바치다",
    "level": "Extended"
  },
  {
    "id": 738,
    "word": "deep",
    "meaning": "깊은",
    "level": "Elementary"
  },
  {
    "id": 739,
    "word": "defeat",
    "meaning": "패배시키다",
    "level": "Extended"
  },
  {
    "id": 740,
    "word": "defend",
    "meaning": "방어하다",
    "level": "Extended",
    "variation": "defendant"
  },
  {
    "id": 741,
    "word": "defense",
    "meaning": "방어",
    "level": "MidHigh",
    "variation": "defence"
  },
  {
    "id": 742,
    "word": "deficiency",
    "meaning": "결핍",
    "level": "Extended"
  },
  {
    "id": 743,
    "word": "deficit",
    "meaning": "적자",
    "level": "Extended"
  },
  {
    "id": 744,
    "word": "define",
    "meaning": "정의하다",
    "level": "MidHigh"
  },
  {
    "id": 745,
    "word": "definite",
    "meaning": "확실한",
    "level": "MidHigh"
  },
  {
    "id": 746,
    "word": "degree",
    "meaning": "정도",
    "level": "MidHigh"
  },
  {
    "id": 747,
    "word": "delay",
    "meaning": "지연",
    "level": "MidHigh"
  },
  {
    "id": 748,
    "word": "delegate",
    "meaning": "대표자",
    "level": "Extended"
  },
  {
    "id": 749,
    "word": "delete",
    "meaning": "삭제하다",
    "level": "Extended"
  },
  {
    "id": 750,
    "word": "deliberate",
    "meaning": "신중한",
    "level": "Extended"
  },
  {
    "id": 751,
    "word": "delicate",
    "meaning": "섬세한",
    "level": "Extended"
  },
  {
    "id": 752,
    "word": "delicious",
    "meaning": "맛있는",
    "level": "Elementary"
  },
  {
    "id": 753,
    "word": "delight",
    "meaning": "기쁨",
    "level": "MidHigh"
  },
  {
    "id": 754,
    "word": "deliver",
    "meaning": "배달하다",
    "level": "MidHigh"
  },
  {
    "id": 755,
    "word": "demand",
    "meaning": "요구하다",
    "level": "MidHigh"
  },
  {
    "id": 756,
    "word": "democracy",
    "meaning": "민주주의",
    "level": "Extended"
  },
  {
    "id": 757,
    "word": "democrat",
    "meaning": "민주당원",
    "level": "Extended"
  },
  {
    "id": 758,
    "word": "demon",
    "meaning": "악마",
    "level": "Extended"
  },
  {
    "id": 759,
    "word": "demonstrate",
    "meaning": "입증하다",
    "level": "MidHigh"
  },
  {
    "id": 760,
    "word": "dense",
    "meaning": "빽빽한",
    "level": "Extended"
  },
  {
    "id": 761,
    "word": "dentist",
    "meaning": "치과의사",
    "level": "MidHigh"
  },
  {
    "id": 762,
    "word": "deny",
    "meaning": "부인하다",
    "level": "MidHigh"
  },
  {
    "id": 763,
    "word": "depart",
    "meaning": "출발하다",
    "level": "Extended",
    "variation": "department, departure"
  },
  {
    "id": 764,
    "word": "depend",
    "meaning": "의존하다",
    "level": "MidHigh",
    "variation": "dependence, independent"
  },
  {
    "id": 765,
    "word": "depict",
    "meaning": "묘사하다",
    "level": "Extended"
  },
  {
    "id": 766,
    "word": "deposit",
    "meaning": "예금",
    "level": "Extended"
  },
  {
    "id": 767,
    "word": "depress",
    "meaning": "우울하게 하다",
    "level": "MidHigh"
  },
  {
    "id": 768,
    "word": "deprive",
    "meaning": "빼앗다",
    "level": "Extended"
  },
  {
    "id": 769,
    "word": "derive",
    "meaning": "유래하다",
    "level": "Extended"
  },
  {
    "id": 770,
    "word": "descend",
    "meaning": "내려가다",
    "level": "Extended"
  },
  {
    "id": 771,
    "word": "describe",
    "meaning": "묘사하다",
    "level": "MidHigh",
    "variation": "description"
  },
  {
    "id": 772,
    "word": "desert",
    "meaning": "사막",
    "level": "MidHigh"
  },
  {
    "id": 773,
    "word": "deserve",
    "meaning": "~할 가치가 있다",
    "level": "MidHigh"
  },
  {
    "id": 774,
    "word": "design",
    "meaning": "설계",
    "level": "Elementary"
  },
  {
    "id": 775,
    "word": "designate",
    "meaning": "지정하다",
    "level": "Extended"
  },
  {
    "id": 776,
    "word": "desire",
    "meaning": "욕망",
    "level": "MidHigh"
  },
  {
    "id": 777,
    "word": "desk",
    "meaning": "책상",
    "level": "Elementary"
  },
  {
    "id": 778,
    "word": "despair",
    "meaning": "절망",
    "level": "Extended"
  },
  {
    "id": 779,
    "word": "desperate",
    "meaning": "필사적인",
    "level": "MidHigh"
  },
  {
    "id": 780,
    "word": "despite",
    "meaning": "~에도 불구하고",
    "level": "MidHigh"
  },
  {
    "id": 781,
    "word": "destine",
    "meaning": "운명 짓다",
    "level": "Extended",
    "variation": "destination"
  },
  {
    "id": 782,
    "word": "destiny",
    "meaning": "운명",
    "level": "Extended"
  },
  {
    "id": 783,
    "word": "destroy",
    "meaning": "파괴하다",
    "level": "MidHigh"
  },
  {
    "id": 784,
    "word": "destruct",
    "meaning": "파괴하다",
    "level": "Extended",
    "variation": "destruction"
  },
  {
    "id": 785,
    "word": "detach",
    "meaning": "떼어 내다",
    "level": "Extended"
  },
  {
    "id": 786,
    "word": "detail",
    "meaning": "세부 사항",
    "level": "MidHigh"
  },
  {
    "id": 787,
    "word": "detect",
    "meaning": "발견하다",
    "level": "MidHigh"
  },
  {
    "id": 788,
    "word": "determine",
    "meaning": "결정하다",
    "level": "MidHigh"
  },
  {
    "id": 789,
    "word": "develop",
    "meaning": "발전시키다",
    "level": "MidHigh"
  },
  {
    "id": 790,
    "word": "device",
    "meaning": "장치",
    "level": "Extended"
  },
  {
    "id": 791,
    "word": "devil",
    "meaning": "악마",
    "level": "Extended"
  },
  {
    "id": 792,
    "word": "devise",
    "meaning": "고안하다",
    "level": "Extended"
  },
  {
    "id": 793,
    "word": "devote",
    "meaning": "바치다",
    "level": "Extended"
  },
  {
    "id": 794,
    "word": "diabetes",
    "meaning": "당뇨병",
    "level": "Extended"
  },
  {
    "id": 795,
    "word": "dialogue",
    "meaning": "대화",
    "level": "Elementary",
    "variation": "dialog"
  },
  {
    "id": 796,
    "word": "diary",
    "meaning": "일기",
    "level": "MidHigh"
  },
  {
    "id": 797,
    "word": "dictate",
    "meaning": "받아쓰게 하다",
    "level": "Extended"
  },
  {
    "id": 798,
    "word": "dictionary",
    "meaning": "사전",
    "level": "MidHigh"
  },
  {
    "id": 799,
    "word": "die",
    "meaning": "죽다",
    "level": "Elementary"
  },
  {
    "id": 800,
    "word": "diet",
    "meaning": "식단",
    "level": "MidHigh"
  },
  {
    "id": 801,
    "word": "differ",
    "meaning": "다르다",
    "level": "Extended",
    "variation": "different"
  },
  {
    "id": 802,
    "word": "difficult",
    "meaning": "어려운",
    "level": "Elementary"
  },
  {
    "id": 803,
    "word": "dig",
    "meaning": "파다",
    "level": "MidHigh"
  },
  {
    "id": 804,
    "word": "dignity",
    "meaning": "존엄",
    "level": "Extended"
  },
  {
    "id": 805,
    "word": "dimension",
    "meaning": "차원",
    "level": "Extended"
  },
  {
    "id": 806,
    "word": "diminish",
    "meaning": "줄이다",
    "level": "Extended"
  },
  {
    "id": 807,
    "word": "dine",
    "meaning": "식사하다",
    "level": "Extended"
  },
  {
    "id": 808,
    "word": "dinner",
    "meaning": "저녁 식사",
    "level": "Elementary"
  },
  {
    "id": 809,
    "word": "dip",
    "meaning": "담그다",
    "level": "Extended"
  },
  {
    "id": 810,
    "word": "diplomat",
    "meaning": "외교관",
    "level": "Extended"
  },
  {
    "id": 811,
    "word": "direct",
    "meaning": "직접적인",
    "level": "MidHigh"
  },
  {
    "id": 812,
    "word": "dirt",
    "meaning": "흙",
    "level": "MidHigh",
    "variation": "dirty"
  },
  {
    "id": 813,
    "word": "disappoint",
    "meaning": "실망시키다",
    "level": "MidHigh"
  },
  {
    "id": 814,
    "word": "disaster",
    "meaning": "재난",
    "level": "Extended"
  },
  {
    "id": 815,
    "word": "disc",
    "meaning": "원반",
    "level": "MidHigh",
    "variation": "disk"
  },
  {
    "id": 816,
    "word": "discipline",
    "meaning": "규율",
    "level": "MidHigh"
  },
  {
    "id": 817,
    "word": "discourse",
    "meaning": "담화",
    "level": "Extended"
  },
  {
    "id": 818,
    "word": "discriminate",
    "meaning": "차별하다",
    "level": "Extended"
  },
  {
    "id": 819,
    "word": "discuss",
    "meaning": "논의하다",
    "level": "Elementary"
  },
  {
    "id": 820,
    "word": "disgust",
    "meaning": "혐오",
    "level": "MidHigh"
  },
  {
    "id": 821,
    "word": "dish",
    "meaning": "접시",
    "level": "MidHigh"
  },
  {
    "id": 822,
    "word": "dismiss",
    "meaning": "해고하다",
    "level": "Extended"
  },
  {
    "id": 823,
    "word": "display",
    "meaning": "전시하다",
    "level": "MidHigh"
  },
  {
    "id": 824,
    "word": "dispute",
    "meaning": "논쟁",
    "level": "Extended"
  },
  {
    "id": 825,
    "word": "disrupt",
    "meaning": "방해하다",
    "level": "Extended"
  },
  {
    "id": 826,
    "word": "distance",
    "meaning": "거리",
    "level": "MidHigh"
  },
  {
    "id": 827,
    "word": "distinct",
    "meaning": "뚜렷한",
    "level": "Extended"
  },
  {
    "id": 828,
    "word": "distinguish",
    "meaning": "구별하다",
    "level": "Extended"
  },
  {
    "id": 829,
    "word": "distort",
    "meaning": "왜곡하다",
    "level": "Extended"
  },
  {
    "id": 830,
    "word": "distract",
    "meaning": "주의를 흩뜨리다",
    "level": "Extended"
  },
  {
    "id": 831,
    "word": "distribute",
    "meaning": "분배하다",
    "level": "Extended"
  },
  {
    "id": 832,
    "word": "district",
    "meaning": "구역",
    "level": "MidHigh"
  },
  {
    "id": 833,
    "word": "disturb",
    "meaning": "방해하다",
    "level": "MidHigh"
  },
  {
    "id": 834,
    "word": "dive",
    "meaning": "잠수하다",
    "level": "MidHigh"
  },
  {
    "id": 835,
    "word": "diverse",
    "meaning": "다양한",
    "level": "Extended"
  },
  {
    "id": 836,
    "word": "divide",
    "meaning": "나누다",
    "level": "MidHigh"
  },
  {
    "id": 837,
    "word": "divine",
    "meaning": "신성한",
    "level": "Extended"
  },
  {
    "id": 838,
    "word": "divorce",
    "meaning": "이혼하다",
    "level": "MidHigh"
  },
  {
    "id": 839,
    "word": "do",
    "meaning": "하다",
    "level": "Elementary"
  },
  {
    "id": 840,
    "word": "doctor",
    "meaning": "의사",
    "level": "Elementary"
  },
  {
    "id": 841,
    "word": "document",
    "meaning": "문서",
    "level": "MidHigh"
  },
  {
    "id": 842,
    "word": "dog",
    "meaning": "개",
    "level": "Elementary"
  },
  {
    "id": 843,
    "word": "doll",
    "meaning": "인형",
    "level": "Elementary"
  },
  {
    "id": 844,
    "word": "dolphin",
    "meaning": "돌고래",
    "level": "MidHigh"
  },
  {
    "id": 845,
    "word": "domain",
    "meaning": "영역",
    "level": "Extended"
  },
  {
    "id": 846,
    "word": "domestic",
    "meaning": "국내의",
    "level": "MidHigh"
  },
  {
    "id": 847,
    "word": "dominate",
    "meaning": "지배하다",
    "level": "Extended",
    "variation": "dominant"
  },
  {
    "id": 848,
    "word": "donate",
    "meaning": "기부하다",
    "level": "MidHigh"
  },
  {
    "id": 849,
    "word": "door",
    "meaning": "문",
    "level": "Elementary"
  },
  {
    "id": 850,
    "word": "dose",
    "meaning": "복용량",
    "level": "Extended"
  },
  {
    "id": 851,
    "word": "dot",
    "meaning": "점",
    "level": "Extended"
  },
  {
    "id": 852,
    "word": "double",
    "meaning": "두 배",
    "level": "Elementary"
  },
  {
    "id": 853,
    "word": "doubt",
    "meaning": "의심하다",
    "level": "MidHigh"
  },
  {
    "id": 854,
    "word": "doughnut",
    "meaning": "도넛",
    "level": "Elementary"
  },
  {
    "id": 855,
    "word": "down",
    "meaning": "아래로",
    "level": "Elementary"
  },
  {
    "id": 856,
    "word": "dozen",
    "meaning": "열두 개",
    "level": "MidHigh"
  },
  {
    "id": 857,
    "word": "draft",
    "meaning": "초안",
    "level": "Extended"
  },
  {
    "id": 858,
    "word": "drag",
    "meaning": "끌다",
    "level": "MidHigh"
  },
  {
    "id": 859,
    "word": "drain",
    "meaning": "배수하다",
    "level": "Extended"
  },
  {
    "id": 860,
    "word": "drama",
    "meaning": "극",
    "level": "MidHigh"
  },
  {
    "id": 861,
    "word": "draw",
    "meaning": "그리다",
    "level": "Elementary",
    "variation": "drawer"
  },
  {
    "id": 862,
    "word": "dread",
    "meaning": "두려워하다",
    "level": "Extended"
  },
  {
    "id": 863,
    "word": "dream",
    "meaning": "꿈",
    "level": "Elementary"
  },
  {
    "id": 864,
    "word": "dress",
    "meaning": "옷을 입다",
    "level": "Elementary"
  },
  {
    "id": 865,
    "word": "drill",
    "meaning": "훈련",
    "level": "Extended"
  },
  {
    "id": 866,
    "word": "drink",
    "meaning": "마시다",
    "level": "Elementary"
  },
  {
    "id": 867,
    "word": "drive",
    "meaning": "운전하다",
    "level": "Elementary"
  },
  {
    "id": 868,
    "word": "drop",
    "meaning": "떨어뜨리다",
    "level": "Elementary"
  },
  {
    "id": 869,
    "word": "drown",
    "meaning": "익사하다",
    "level": "Extended"
  },
  {
    "id": 870,
    "word": "drug",
    "meaning": "약물",
    "level": "MidHigh"
  },
  {
    "id": 871,
    "word": "drum",
    "meaning": "북",
    "level": "Elementary"
  },
  {
    "id": 872,
    "word": "dry",
    "meaning": "마른",
    "level": "Elementary"
  },
  {
    "id": 873,
    "word": "dual",
    "meaning": "이중의",
    "level": "Extended"
  },
  {
    "id": 874,
    "word": "duck",
    "meaning": "오리",
    "level": "Elementary"
  },
  {
    "id": 875,
    "word": "due",
    "meaning": "~할 예정인",
    "level": "MidHigh"
  },
  {
    "id": 876,
    "word": "dull",
    "meaning": "따분한",
    "level": "Extended"
  },
  {
    "id": 877,
    "word": "dump",
    "meaning": "버리다",
    "level": "MidHigh"
  },
  {
    "id": 878,
    "word": "during",
    "meaning": "~동안",
    "level": "Elementary"
  },
  {
    "id": 879,
    "word": "dust",
    "meaning": "먼지",
    "level": "MidHigh"
  },
  {
    "id": 880,
    "word": "duty",
    "meaning": "의무",
    "level": "MidHigh"
  },
  {
    "id": 881,
    "word": "dwell",
    "meaning": "거주하다",
    "level": "Extended"
  },
  {
    "id": 882,
    "word": "dynamic",
    "meaning": "역동적인",
    "level": "Extended"
  },
  {
    "id": 883,
    "word": "each",
    "meaning": "각각의",
    "level": "MidHigh"
  },
  {
    "id": 884,
    "word": "eager",
    "meaning": "열망하는",
    "level": "Extended"
  },
  {
    "id": 885,
    "word": "ear",
    "meaning": "귀",
    "level": "Elementary"
  },
  {
    "id": 886,
    "word": "early",
    "meaning": "이른",
    "level": "Elementary"
  },
  {
    "id": 887,
    "word": "earn",
    "meaning": "벌다",
    "level": "MidHigh"
  },
  {
    "id": 888,
    "word": "earth",
    "meaning": "지구",
    "level": "Elementary"
  },
  {
    "id": 889,
    "word": "ease",
    "meaning": "쉬움",
    "level": "MidHigh",
    "variation": "disease, easy"
  },
  {
    "id": 890,
    "word": "east",
    "meaning": "동쪽",
    "level": "Elementary"
  },
  {
    "id": 891,
    "word": "eat",
    "meaning": "먹다",
    "level": "Elementary"
  },
  {
    "id": 892,
    "word": "economy",
    "meaning": "경제",
    "level": "MidHigh"
  },
  {
    "id": 893,
    "word": "edge",
    "meaning": "가장자리",
    "level": "MidHigh"
  },
  {
    "id": 894,
    "word": "edit",
    "meaning": "편집하다",
    "level": "MidHigh"
  },
  {
    "id": 895,
    "word": "educate",
    "meaning": "교육하다",
    "level": "MidHigh"
  },
  {
    "id": 896,
    "word": "effect",
    "meaning": "효과",
    "level": "MidHigh",
    "variation": "effective"
  },
  {
    "id": 897,
    "word": "efficient",
    "meaning": "효율적인",
    "level": "Extended"
  },
  {
    "id": 898,
    "word": "effort",
    "meaning": "노력",
    "level": "MidHigh"
  },
  {
    "id": 899,
    "word": "egg",
    "meaning": "달걀",
    "level": "Elementary"
  },
  {
    "id": 900,
    "word": "eight",
    "meaning": "여덟",
    "level": "Elementary"
  },
  {
    "id": 901,
    "word": "either",
    "meaning": "둘 중 하나",
    "level": "MidHigh"
  },
  {
    "id": 902,
    "word": "elaborate",
    "meaning": "정교한",
    "level": "Extended"
  },
  {
    "id": 903,
    "word": "elect",
    "meaning": "선출하다",
    "level": "MidHigh"
  },
  {
    "id": 904,
    "word": "electric",
    "meaning": "전기의",
    "level": "MidHigh"
  },
  {
    "id": 905,
    "word": "electronic",
    "meaning": "전자의",
    "level": "Extended"
  },
  {
    "id": 906,
    "word": "elegant",
    "meaning": "우아한",
    "level": "Extended"
  },
  {
    "id": 907,
    "word": "element",
    "meaning": "요소",
    "level": "MidHigh",
    "variation": "elementary"
  },
  {
    "id": 908,
    "word": "elephant",
    "meaning": "코끼리",
    "level": "Elementary"
  },
  {
    "id": 909,
    "word": "elevate",
    "meaning": "높이다",
    "level": "Extended",
    "variation": "elevator"
  },
  {
    "id": 910,
    "word": "eleven",
    "meaning": "열하나",
    "level": "Elementary"
  },
  {
    "id": 911,
    "word": "eliminate",
    "meaning": "제거하다",
    "level": "Extended"
  },
  {
    "id": 912,
    "word": "elite",
    "meaning": "엘리트",
    "level": "Extended"
  },
  {
    "id": 913,
    "word": "else",
    "meaning": "그 밖의",
    "level": "MidHigh"
  },
  {
    "id": 914,
    "word": "embarrass",
    "meaning": "당황하게 하다",
    "level": "MidHigh"
  },
  {
    "id": 915,
    "word": "embassy",
    "meaning": "대사관",
    "level": "Extended"
  },
  {
    "id": 916,
    "word": "embrace",
    "meaning": "껴안다",
    "level": "Extended"
  },
  {
    "id": 917,
    "word": "emerge",
    "meaning": "나타나다",
    "level": "Extended",
    "variation": "emergence"
  },
  {
    "id": 918,
    "word": "emergency",
    "meaning": "긴급 상황",
    "level": "Extended"
  },
  {
    "id": 919,
    "word": "emit",
    "meaning": "방출하다",
    "level": "Extended",
    "variation": "emission"
  },
  {
    "id": 920,
    "word": "emotion",
    "meaning": "감정",
    "level": "MidHigh"
  },
  {
    "id": 921,
    "word": "emphasis",
    "meaning": "강조",
    "level": "Extended"
  },
  {
    "id": 922,
    "word": "emphasize",
    "meaning": "강조하다",
    "level": "MidHigh"
  },
  {
    "id": 923,
    "word": "empire",
    "meaning": "제국",
    "level": "MidHigh"
  },
  {
    "id": 924,
    "word": "employ",
    "meaning": "고용하다",
    "level": "MidHigh"
  },
  {
    "id": 925,
    "word": "empty",
    "meaning": "빈",
    "level": "MidHigh"
  },
  {
    "id": 926,
    "word": "encounter",
    "meaning": "마주치다",
    "level": "Extended"
  },
  {
    "id": 927,
    "word": "end",
    "meaning": "끝",
    "level": "Elementary"
  },
  {
    "id": 928,
    "word": "endure",
    "meaning": "견디다",
    "level": "Extended"
  },
  {
    "id": 929,
    "word": "enemy",
    "meaning": "적",
    "level": "MidHigh"
  },
  {
    "id": 930,
    "word": "energy",
    "meaning": "에너지",
    "level": "Elementary"
  },
  {
    "id": 931,
    "word": "engage",
    "meaning": "참여하다",
    "level": "MidHigh"
  },
  {
    "id": 932,
    "word": "engine",
    "meaning": "엔진",
    "level": "MidHigh"
  },
  {
    "id": 933,
    "word": "engineer",
    "meaning": "기술자",
    "level": "MidHigh"
  },
  {
    "id": 934,
    "word": "enhance",
    "meaning": "향상시키다",
    "level": "Extended"
  },
  {
    "id": 935,
    "word": "enormous",
    "meaning": "거대한",
    "level": "MidHigh"
  },
  {
    "id": 936,
    "word": "enough",
    "meaning": "충분한",
    "level": "Elementary"
  },
  {
    "id": 937,
    "word": "enter",
    "meaning": "들어가다",
    "level": "Elementary"
  },
  {
    "id": 938,
    "word": "enterprise",
    "meaning": "기업",
    "level": "Extended"
  },
  {
    "id": 939,
    "word": "entertain",
    "meaning": "즐겁게 하다",
    "level": "MidHigh"
  },
  {
    "id": 940,
    "word": "enthusiastic",
    "meaning": "열정적인",
    "level": "Extended"
  },
  {
    "id": 941,
    "word": "entire",
    "meaning": "전체의",
    "level": "MidHigh"
  },
  {
    "id": 942,
    "word": "entry",
    "meaning": "입장",
    "level": "Extended"
  },
  {
    "id": 943,
    "word": "envelope",
    "meaning": "봉투",
    "level": "MidHigh"
  },
  {
    "id": 944,
    "word": "environ",
    "meaning": "환경",
    "level": "Extended",
    "variation": "environment"
  },
  {
    "id": 945,
    "word": "envy",
    "meaning": "부러워하다",
    "level": "Extended"
  },
  {
    "id": 946,
    "word": "equal",
    "meaning": "같은",
    "level": "MidHigh"
  },
  {
    "id": 947,
    "word": "equip",
    "meaning": "갖추다",
    "level": "Extended",
    "variation": "equipment"
  },
  {
    "id": 948,
    "word": "era",
    "meaning": "시대",
    "level": "Extended"
  },
  {
    "id": 949,
    "word": "erase",
    "meaning": "지우다",
    "level": "Extended",
    "variation": "eraser"
  },
  {
    "id": 950,
    "word": "erect",
    "meaning": "세우다",
    "level": "Extended"
  },
  {
    "id": 951,
    "word": "err",
    "meaning": "실수하다",
    "level": "Extended",
    "variation": "error"
  },
  {
    "id": 952,
    "word": "escape",
    "meaning": "탈출하다",
    "level": "MidHigh"
  },
  {
    "id": 953,
    "word": "especial",
    "meaning": "특별한",
    "level": "MidHigh",
    "variation": "especially"
  },
  {
    "id": 954,
    "word": "essay",
    "meaning": "수필",
    "level": "MidHigh"
  },
  {
    "id": 955,
    "word": "essence",
    "meaning": "본질",
    "level": "Extended",
    "variation": "essential"
  },
  {
    "id": 956,
    "word": "establish",
    "meaning": "설립하다",
    "level": "MidHigh"
  },
  {
    "id": 957,
    "word": "estate",
    "meaning": "재산",
    "level": "Extended"
  },
  {
    "id": 958,
    "word": "estimate",
    "meaning": "추정하다",
    "level": "MidHigh"
  },
  {
    "id": 959,
    "word": "ethic",
    "meaning": "윤리",
    "level": "Extended",
    "variation": "ethical"
  },
  {
    "id": 960,
    "word": "ethnic",
    "meaning": "민족의",
    "level": "Extended"
  },
  {
    "id": 961,
    "word": "evacuate",
    "meaning": "대피시키다",
    "level": "Extended"
  },
  {
    "id": 962,
    "word": "evaluate",
    "meaning": "평가하다",
    "level": "Extended"
  },
  {
    "id": 963,
    "word": "even",
    "meaning": "심지어",
    "level": "MidHigh"
  },
  {
    "id": 964,
    "word": "evening",
    "meaning": "저녁",
    "level": "Elementary"
  },
  {
    "id": 965,
    "word": "event",
    "meaning": "사건",
    "level": "MidHigh",
    "variation": "eventually"
  },
  {
    "id": 966,
    "word": "ever",
    "meaning": "언제나",
    "level": "MidHigh"
  },
  {
    "id": 967,
    "word": "every",
    "meaning": "모든",
    "level": "Elementary"
  },
  {
    "id": 968,
    "word": "evidence",
    "meaning": "증거",
    "level": "MidHigh"
  },
  {
    "id": 969,
    "word": "evil",
    "meaning": "악",
    "level": "MidHigh"
  },
  {
    "id": 970,
    "word": "evitable",
    "meaning": "피할 수 있는",
    "level": "Extended",
    "variation": "inevitable"
  },
  {
    "id": 971,
    "word": "evolution",
    "meaning": "진화",
    "level": "Extended"
  },
  {
    "id": 972,
    "word": "evolve",
    "meaning": "발전하다",
    "level": "Extended"
  },
  {
    "id": 973,
    "word": "exact",
    "meaning": "정확한",
    "level": "MidHigh"
  },
  {
    "id": 974,
    "word": "exaggerate",
    "meaning": "과장하다",
    "level": "Extended"
  },
  {
    "id": 975,
    "word": "examine",
    "meaning": "조사하다",
    "level": "MidHigh",
    "variation": "examination, exam"
  },
  {
    "id": 976,
    "word": "example",
    "meaning": "예시",
    "level": "Elementary"
  },
  {
    "id": 977,
    "word": "exceed",
    "meaning": "초과하다",
    "level": "Extended"
  },
  {
    "id": 978,
    "word": "excel",
    "meaning": "뛰어나다",
    "level": "Extended",
    "variation": "excellent"
  },
  {
    "id": 979,
    "word": "except",
    "meaning": "제외하고",
    "level": "MidHigh"
  },
  {
    "id": 980,
    "word": "excess",
    "meaning": "초과",
    "level": "Extended"
  },
  {
    "id": 981,
    "word": "exchange",
    "meaning": "교환",
    "level": "MidHigh"
  },
  {
    "id": 982,
    "word": "excite",
    "meaning": "흥분시키다",
    "level": "MidHigh"
  },
  {
    "id": 983,
    "word": "exclude",
    "meaning": "배제하다",
    "level": "Extended",
    "variation": "exclusive"
  },
  {
    "id": 984,
    "word": "excuse",
    "meaning": "변명",
    "level": "MidHigh"
  },
  {
    "id": 985,
    "word": "executive",
    "meaning": "경영진",
    "level": "Extended"
  },
  {
    "id": 986,
    "word": "exercise",
    "meaning": "운동",
    "level": "Elementary"
  },
  {
    "id": 987,
    "word": "exhaust",
    "meaning": "소진시키다",
    "level": "MidHigh"
  },
  {
    "id": 988,
    "word": "exhibit",
    "meaning": "전시하다",
    "level": "Extended"
  },
  {
    "id": 989,
    "word": "exist",
    "meaning": "존재하다",
    "level": "MidHigh"
  },
  {
    "id": 990,
    "word": "exit",
    "meaning": "출구",
    "level": "MidHigh"
  },
  {
    "id": 991,
    "word": "exotic",
    "meaning": "이국적인",
    "level": "Extended"
  },
  {
    "id": 992,
    "word": "expand",
    "meaning": "확장하다",
    "level": "MidHigh"
  },
  {
    "id": 993,
    "word": "expect",
    "meaning": "기대하다",
    "level": "MidHigh"
  },
  {
    "id": 994,
    "word": "expense",
    "meaning": "비용",
    "level": "MidHigh",
    "variation": "expensive"
  },
  {
    "id": 995,
    "word": "experience",
    "meaning": "경험",
    "level": "MidHigh"
  },
  {
    "id": 996,
    "word": "experiment",
    "meaning": "실험",
    "level": "MidHigh"
  },
  {
    "id": 997,
    "word": "expert",
    "meaning": "전문가",
    "level": "MidHigh"
  },
  {
    "id": 998,
    "word": "expertise",
    "meaning": "전문 지식",
    "level": "Extended"
  },
  {
    "id": 999,
    "word": "explain",
    "meaning": "설명하다",
    "level": "MidHigh"
  },
  {
    "id": 1000,
    "word": "explicit",
    "meaning": "명시적인",
    "level": "Extended"
  },
  {
    "id": 1001,
    "word": "explode",
    "meaning": "폭발하다",
    "level": "Extended"
  },
  {
    "id": 1002,
    "word": "explore",
    "meaning": "탐구하다",
    "level": "Extended"
  },
  {
    "id": 1003,
    "word": "export",
    "meaning": "수출하다",
    "level": "Extended"
  },
  {
    "id": 1004,
    "word": "expose",
    "meaning": "노출하다",
    "level": "MidHigh"
  },
  {
    "id": 1005,
    "word": "express",
    "meaning": "표현하다",
    "level": "MidHigh"
  },
  {
    "id": 1006,
    "word": "extend",
    "meaning": "연장하다",
    "level": "MidHigh"
  },
  {
    "id": 1007,
    "word": "extent",
    "meaning": "범위",
    "level": "Extended"
  },
  {
    "id": 1008,
    "word": "external",
    "meaning": "외부의",
    "level": "Extended"
  },
  {
    "id": 1009,
    "word": "extinct",
    "meaning": "멸종한",
    "level": "Extended"
  },
  {
    "id": 1010,
    "word": "extra",
    "meaning": "추가의",
    "level": "MidHigh"
  },
  {
    "id": 1011,
    "word": "extract",
    "meaning": "추출하다",
    "level": "Extended"
  },
  {
    "id": 1012,
    "word": "extraordinary",
    "meaning": "비범한",
    "level": "Extended"
  },
  {
    "id": 1013,
    "word": "extreme",
    "meaning": "극단적인",
    "level": "MidHigh"
  },
  {
    "id": 1014,
    "word": "eye",
    "meaning": "눈",
    "level": "Elementary"
  },
  {
    "id": 1015,
    "word": "eyebrow",
    "meaning": "눈썹",
    "level": "Extended"
  },
  {
    "id": 1016,
    "word": "fabric",
    "meaning": "직물",
    "level": "Extended"
  },
  {
    "id": 1017,
    "word": "face",
    "meaning": "얼굴",
    "level": "Elementary"
  },
  {
    "id": 1018,
    "word": "facilitate",
    "meaning": "촉진하다",
    "level": "Extended"
  },
  {
    "id": 1019,
    "word": "facility",
    "meaning": "시설",
    "level": "Extended"
  },
  {
    "id": 1020,
    "word": "fact",
    "meaning": "사실",
    "level": "Elementary",
    "variation": "factual"
  },
  {
    "id": 1021,
    "word": "factor",
    "meaning": "요인",
    "level": "MidHigh"
  },
  {
    "id": 1022,
    "word": "factory",
    "meaning": "공장",
    "level": "MidHigh"
  },
  {
    "id": 1023,
    "word": "faculty",
    "meaning": "교수진",
    "level": "Extended"
  },
  {
    "id": 1024,
    "word": "fade",
    "meaning": "희미해지다",
    "level": "Extended"
  },
  {
    "id": 1025,
    "word": "fail",
    "meaning": "실패하다",
    "level": "Elementary"
  },
  {
    "id": 1026,
    "word": "faint",
    "meaning": "희미한",
    "level": "MidHigh"
  },
  {
    "id": 1027,
    "word": "fair",
    "meaning": "공정한",
    "level": "MidHigh"
  },
  {
    "id": 1028,
    "word": "faith",
    "meaning": "신앙",
    "level": "MidHigh"
  },
  {
    "id": 1029,
    "word": "fall",
    "meaning": "떨어지다",
    "level": "Elementary"
  },
  {
    "id": 1030,
    "word": "false",
    "meaning": "거짓의",
    "level": "Extended"
  },
  {
    "id": 1031,
    "word": "fame",
    "meaning": "명성",
    "level": "Extended",
    "variation": "famous"
  },
  {
    "id": 1032,
    "word": "familiar",
    "meaning": "익숙한",
    "level": "MidHigh"
  },
  {
    "id": 1033,
    "word": "family",
    "meaning": "가족",
    "level": "Elementary"
  },
  {
    "id": 1034,
    "word": "fan",
    "meaning": "팬",
    "level": "Elementary"
  },
  {
    "id": 1035,
    "word": "fancy",
    "meaning": "화려한",
    "level": "MidHigh"
  },
  {
    "id": 1036,
    "word": "fantastic",
    "meaning": "환상적인",
    "level": "MidHigh"
  },
  {
    "id": 1037,
    "word": "far",
    "meaning": "먼",
    "level": "Elementary"
  },
  {
    "id": 1038,
    "word": "fare",
    "meaning": "요금",
    "level": "Extended"
  },
  {
    "id": 1039,
    "word": "farm",
    "meaning": "농장",
    "level": "Elementary"
  },
  {
    "id": 1040,
    "word": "fascinate",
    "meaning": "매혹하다",
    "level": "MidHigh"
  },
  {
    "id": 1041,
    "word": "fashion",
    "meaning": "유행",
    "level": "MidHigh"
  },
  {
    "id": 1042,
    "word": "fast",
    "meaning": "빠른",
    "level": "Elementary"
  },
  {
    "id": 1043,
    "word": "fasten",
    "meaning": "묶다",
    "level": "Extended"
  },
  {
    "id": 1044,
    "word": "fat",
    "meaning": "살찐",
    "level": "Elementary"
  },
  {
    "id": 1045,
    "word": "fate",
    "meaning": "운명",
    "level": "Extended",
    "variation": "fatal"
  },
  {
    "id": 1046,
    "word": "father",
    "meaning": "아버지",
    "level": "Elementary",
    "variation": "dad, daddy"
  },
  {
    "id": 1047,
    "word": "fault",
    "meaning": "잘못",
    "level": "MidHigh"
  },
  {
    "id": 1048,
    "word": "favor",
    "meaning": "호의",
    "level": "MidHigh",
    "variation": "favour"
  },
  {
    "id": 1049,
    "word": "favorite",
    "meaning": "가장 좋아하는",
    "level": "Elementary",
    "variation": "favourite"
  },
  {
    "id": 1050,
    "word": "fear",
    "meaning": "두려움",
    "level": "MidHigh"
  },
  {
    "id": 1051,
    "word": "feature",
    "meaning": "특징",
    "level": "MidHigh"
  },
  {
    "id": 1052,
    "word": "federal",
    "meaning": "연방의",
    "level": "Extended"
  },
  {
    "id": 1053,
    "word": "fee",
    "meaning": "요금",
    "level": "MidHigh"
  },
  {
    "id": 1054,
    "word": "feed",
    "meaning": "먹이를 주다",
    "level": "MidHigh"
  },
  {
    "id": 1055,
    "word": "feel",
    "meaning": "느끼다",
    "level": "Elementary"
  },
  {
    "id": 1056,
    "word": "fellow",
    "meaning": "동료",
    "level": "MidHigh"
  },
  {
    "id": 1057,
    "word": "female",
    "meaning": "여성",
    "level": "MidHigh"
  },
  {
    "id": 1058,
    "word": "fence",
    "meaning": "울타리",
    "level": "MidHigh"
  },
  {
    "id": 1059,
    "word": "ferry",
    "meaning": "여객선",
    "level": "Extended"
  },
  {
    "id": 1060,
    "word": "fertile",
    "meaning": "비옥한",
    "level": "Extended"
  },
  {
    "id": 1061,
    "word": "festival",
    "meaning": "축제",
    "level": "Elementary"
  },
  {
    "id": 1062,
    "word": "fever",
    "meaning": "열",
    "level": "MidHigh"
  },
  {
    "id": 1063,
    "word": "few",
    "meaning": "소수의",
    "level": "MidHigh"
  },
  {
    "id": 1064,
    "word": "fiber",
    "meaning": "섬유",
    "level": "Extended",
    "variation": "fibre"
  },
  {
    "id": 1065,
    "word": "fiction",
    "meaning": "소설",
    "level": "Extended"
  },
  {
    "id": 1066,
    "word": "field",
    "meaning": "들판",
    "level": "Elementary"
  },
  {
    "id": 1067,
    "word": "fierce",
    "meaning": "사나운",
    "level": "Extended"
  },
  {
    "id": 1068,
    "word": "fight",
    "meaning": "싸우다",
    "level": "Elementary"
  },
  {
    "id": 1069,
    "word": "figure",
    "meaning": "숫자",
    "level": "MidHigh"
  },
  {
    "id": 1070,
    "word": "file",
    "meaning": "파일",
    "level": "Elementary"
  },
  {
    "id": 1071,
    "word": "fill",
    "meaning": "채우다",
    "level": "Elementary"
  },
  {
    "id": 1072,
    "word": "film",
    "meaning": "영화",
    "level": "Elementary"
  },
  {
    "id": 1073,
    "word": "filter",
    "meaning": "거르다",
    "level": "Extended"
  },
  {
    "id": 1074,
    "word": "final",
    "meaning": "마지막의",
    "level": "MidHigh"
  },
  {
    "id": 1075,
    "word": "finance",
    "meaning": "재정",
    "level": "MidHigh"
  },
  {
    "id": 1076,
    "word": "find",
    "meaning": "찾다",
    "level": "Elementary"
  },
  {
    "id": 1077,
    "word": "fine",
    "meaning": "괜찮은",
    "level": "Elementary"
  },
  {
    "id": 1078,
    "word": "finger",
    "meaning": "손가락",
    "level": "Elementary"
  },
  {
    "id": 1079,
    "word": "finish",
    "meaning": "끝내다",
    "level": "Elementary"
  },
  {
    "id": 1080,
    "word": "finite",
    "meaning": "유한한",
    "level": "Extended"
  },
  {
    "id": 1081,
    "word": "fire",
    "meaning": "불",
    "level": "Elementary"
  },
  {
    "id": 1082,
    "word": "firm",
    "meaning": "회사",
    "level": "MidHigh"
  },
  {
    "id": 1083,
    "word": "first",
    "meaning": "첫 번째",
    "level": "Elementary"
  },
  {
    "id": 1084,
    "word": "fish",
    "meaning": "물고기",
    "level": "Elementary"
  },
  {
    "id": 1085,
    "word": "fit",
    "meaning": "적합한",
    "level": "MidHigh"
  },
  {
    "id": 1086,
    "word": "five",
    "meaning": "다섯",
    "level": "Elementary"
  },
  {
    "id": 1087,
    "word": "fix",
    "meaning": "고치다",
    "level": "Elementary"
  },
  {
    "id": 1088,
    "word": "flag",
    "meaning": "깃발",
    "level": "MidHigh"
  },
  {
    "id": 1089,
    "word": "flame",
    "meaning": "불꽃",
    "level": "MidHigh"
  },
  {
    "id": 1090,
    "word": "flash",
    "meaning": "번쩍이다",
    "level": "MidHigh"
  },
  {
    "id": 1091,
    "word": "flat",
    "meaning": "평평한",
    "level": "MidHigh"
  },
  {
    "id": 1092,
    "word": "flavor",
    "meaning": "맛",
    "level": "Extended",
    "variation": "flavour"
  },
  {
    "id": 1093,
    "word": "flaw",
    "meaning": "결함",
    "level": "Extended"
  },
  {
    "id": 1094,
    "word": "flee",
    "meaning": "달아나다",
    "level": "Extended"
  },
  {
    "id": 1095,
    "word": "flesh",
    "meaning": "살",
    "level": "Extended"
  },
  {
    "id": 1096,
    "word": "flexible",
    "meaning": "유연한",
    "level": "Extended"
  },
  {
    "id": 1097,
    "word": "flight",
    "meaning": "비행",
    "level": "MidHigh"
  },
  {
    "id": 1098,
    "word": "flip",
    "meaning": "뒤집다",
    "level": "Extended"
  },
  {
    "id": 1099,
    "word": "float",
    "meaning": "뜨다",
    "level": "MidHigh"
  },
  {
    "id": 1100,
    "word": "flock",
    "meaning": "무리",
    "level": "Extended"
  },
  {
    "id": 1101,
    "word": "flood",
    "meaning": "홍수",
    "level": "MidHigh"
  },
  {
    "id": 1102,
    "word": "floor",
    "meaning": "바닥",
    "level": "Elementary"
  },
  {
    "id": 1103,
    "word": "flourish",
    "meaning": "번창하다",
    "level": "Extended"
  },
  {
    "id": 1104,
    "word": "flow",
    "meaning": "흐르다",
    "level": "MidHigh"
  },
  {
    "id": 1105,
    "word": "flower",
    "meaning": "꽃",
    "level": "Elementary"
  },
  {
    "id": 1106,
    "word": "flush",
    "meaning": "얼굴이 붉어지다",
    "level": "Extended"
  },
  {
    "id": 1107,
    "word": "fly",
    "meaning": "날다",
    "level": "Elementary"
  },
  {
    "id": 1108,
    "word": "focus",
    "meaning": "초점",
    "level": "Elementary"
  },
  {
    "id": 1109,
    "word": "fog",
    "meaning": "안개",
    "level": "MidHigh"
  },
  {
    "id": 1110,
    "word": "fold",
    "meaning": "접다",
    "level": "MidHigh"
  },
  {
    "id": 1111,
    "word": "folk",
    "meaning": "사람들",
    "level": "MidHigh"
  },
  {
    "id": 1112,
    "word": "follow",
    "meaning": "따르다",
    "level": "MidHigh"
  },
  {
    "id": 1113,
    "word": "fond",
    "meaning": "좋아하는",
    "level": "Extended"
  },
  {
    "id": 1114,
    "word": "food",
    "meaning": "음식",
    "level": "Elementary"
  },
  {
    "id": 1115,
    "word": "fool",
    "meaning": "바보",
    "level": "Elementary"
  },
  {
    "id": 1116,
    "word": "foot",
    "meaning": "발",
    "level": "Elementary"
  },
  {
    "id": 1117,
    "word": "football",
    "meaning": "축구",
    "level": "Elementary"
  },
  {
    "id": 1118,
    "word": "for",
    "meaning": "~을 위하여",
    "level": "Elementary"
  },
  {
    "id": 1119,
    "word": "forbid",
    "meaning": "금지하다",
    "level": "Extended"
  },
  {
    "id": 1120,
    "word": "force",
    "meaning": "힘",
    "level": "MidHigh",
    "variation": "enforce"
  },
  {
    "id": 1121,
    "word": "forecast",
    "meaning": "예보",
    "level": "Extended"
  },
  {
    "id": 1122,
    "word": "forehead",
    "meaning": "이마",
    "level": "Extended"
  },
  {
    "id": 1123,
    "word": "foreign",
    "meaning": "외국의",
    "level": "MidHigh"
  },
  {
    "id": 1124,
    "word": "forest",
    "meaning": "숲",
    "level": "Elementary"
  },
  {
    "id": 1125,
    "word": "forever",
    "meaning": "영원히",
    "level": "MidHigh"
  },
  {
    "id": 1126,
    "word": "forget",
    "meaning": "잊다",
    "level": "Elementary"
  },
  {
    "id": 1127,
    "word": "forgive",
    "meaning": "용서하다",
    "level": "MidHigh"
  },
  {
    "id": 1128,
    "word": "fork",
    "meaning": "포크",
    "level": "Elementary"
  },
  {
    "id": 1129,
    "word": "form",
    "meaning": "형태",
    "level": "Elementary",
    "variation": "formal, formation, informal"
  },
  {
    "id": 1130,
    "word": "format",
    "meaning": "형식",
    "level": "Extended"
  },
  {
    "id": 1131,
    "word": "former",
    "meaning": "이전의",
    "level": "Extended"
  },
  {
    "id": 1132,
    "word": "formula",
    "meaning": "공식",
    "level": "Extended"
  },
  {
    "id": 1133,
    "word": "forth",
    "meaning": "앞으로",
    "level": "MidHigh"
  },
  {
    "id": 1134,
    "word": "fortunate",
    "meaning": "운이 좋은",
    "level": "MidHigh"
  },
  {
    "id": 1135,
    "word": "fortune",
    "meaning": "행운",
    "level": "MidHigh"
  },
  {
    "id": 1136,
    "word": "forward",
    "meaning": "앞쪽으로",
    "level": "MidHigh"
  },
  {
    "id": 1137,
    "word": "foster",
    "meaning": "육성하다",
    "level": "Extended"
  },
  {
    "id": 1138,
    "word": "found",
    "meaning": "설립하다",
    "level": "MidHigh",
    "variation": "foundation"
  },
  {
    "id": 1139,
    "word": "fountain",
    "meaning": "분수",
    "level": "Extended"
  },
  {
    "id": 1140,
    "word": "four",
    "meaning": "넷",
    "level": "Elementary"
  },
  {
    "id": 1141,
    "word": "fox",
    "meaning": "여우",
    "level": "Elementary"
  },
  {
    "id": 1142,
    "word": "fraction",
    "meaning": "분수",
    "level": "Extended"
  },
  {
    "id": 1143,
    "word": "frame",
    "meaning": "틀",
    "level": "MidHigh"
  },
  {
    "id": 1144,
    "word": "framework",
    "meaning": "체계",
    "level": "Extended"
  },
  {
    "id": 1145,
    "word": "frankly",
    "meaning": "솔직히",
    "level": "MidHigh"
  },
  {
    "id": 1146,
    "word": "free",
    "meaning": "자유로운",
    "level": "Elementary"
  },
  {
    "id": 1147,
    "word": "freeze",
    "meaning": "얼다",
    "level": "MidHigh"
  },
  {
    "id": 1148,
    "word": "frequent",
    "meaning": "빈번한",
    "level": "Extended"
  },
  {
    "id": 1149,
    "word": "fresh",
    "meaning": "신선한",
    "level": "Elementary"
  },
  {
    "id": 1150,
    "word": "friend",
    "meaning": "친구",
    "level": "Elementary",
    "variation": "friendship"
  },
  {
    "id": 1151,
    "word": "fright",
    "meaning": "공포",
    "level": "MidHigh"
  },
  {
    "id": 1152,
    "word": "frog",
    "meaning": "개구리",
    "level": "MidHigh"
  },
  {
    "id": 1153,
    "word": "from",
    "meaning": "~로부터",
    "level": "Elementary"
  },
  {
    "id": 1154,
    "word": "front",
    "meaning": "앞",
    "level": "Elementary"
  },
  {
    "id": 1155,
    "word": "frost",
    "meaning": "서리",
    "level": "Extended"
  },
  {
    "id": 1156,
    "word": "frown",
    "meaning": "눈살을 찌푸리다",
    "level": "Extended"
  },
  {
    "id": 1157,
    "word": "fruit",
    "meaning": "과일",
    "level": "Elementary"
  },
  {
    "id": 1158,
    "word": "frustrate",
    "meaning": "좌절시키다",
    "level": "MidHigh"
  },
  {
    "id": 1159,
    "word": "fry",
    "meaning": "튀기다",
    "level": "MidHigh"
  },
  {
    "id": 1160,
    "word": "fuel",
    "meaning": "연료",
    "level": "Extended"
  },
  {
    "id": 1161,
    "word": "fulfil",
    "meaning": "이행하다",
    "level": "Extended"
  },
  {
    "id": 1162,
    "word": "full",
    "meaning": "가득 찬",
    "level": "Elementary"
  },
  {
    "id": 1163,
    "word": "fun",
    "meaning": "재미",
    "level": "Elementary"
  },
  {
    "id": 1164,
    "word": "function",
    "meaning": "기능",
    "level": "MidHigh"
  },
  {
    "id": 1165,
    "word": "fund",
    "meaning": "기금",
    "level": "MidHigh"
  },
  {
    "id": 1166,
    "word": "fundamental",
    "meaning": "근본적인",
    "level": "Extended"
  },
  {
    "id": 1167,
    "word": "funeral",
    "meaning": "장례식",
    "level": "Extended"
  },
  {
    "id": 1168,
    "word": "fur",
    "meaning": "모피",
    "level": "MidHigh"
  },
  {
    "id": 1169,
    "word": "furnish",
    "meaning": "제공하다",
    "level": "Extended"
  },
  {
    "id": 1170,
    "word": "furniture",
    "meaning": "가구",
    "level": "MidHigh"
  },
  {
    "id": 1171,
    "word": "furthermore",
    "meaning": "게다가",
    "level": "Extended"
  },
  {
    "id": 1172,
    "word": "fury",
    "meaning": "격노",
    "level": "Extended",
    "variation": "furious"
  },
  {
    "id": 1173,
    "word": "fuse",
    "meaning": "퓨즈",
    "level": "Extended"
  },
  {
    "id": 1174,
    "word": "future",
    "meaning": "미래",
    "level": "Elementary"
  },
  {
    "id": 1175,
    "word": "gain",
    "meaning": "얻다",
    "level": "MidHigh"
  },
  {
    "id": 1176,
    "word": "gallery",
    "meaning": "미술관",
    "level": "Extended"
  },
  {
    "id": 1177,
    "word": "gamble",
    "meaning": "도박하다",
    "level": "Extended"
  },
  {
    "id": 1178,
    "word": "game",
    "meaning": "경기",
    "level": "Elementary"
  },
  {
    "id": 1179,
    "word": "gang",
    "meaning": "무리",
    "level": "Extended"
  },
  {
    "id": 1180,
    "word": "gap",
    "meaning": "틈",
    "level": "Extended"
  },
  {
    "id": 1181,
    "word": "garage",
    "meaning": "차고",
    "level": "MidHigh"
  },
  {
    "id": 1182,
    "word": "garden",
    "meaning": "정원",
    "level": "Elementary"
  },
  {
    "id": 1183,
    "word": "gas",
    "meaning": "기체",
    "level": "Elementary"
  },
  {
    "id": 1184,
    "word": "gasoline",
    "meaning": "휘발유",
    "level": "Extended",
    "variation": "petrol"
  },
  {
    "id": 1185,
    "word": "gate",
    "meaning": "문",
    "level": "MidHigh"
  },
  {
    "id": 1186,
    "word": "gather",
    "meaning": "모으다",
    "level": "MidHigh"
  },
  {
    "id": 1187,
    "word": "gaze",
    "meaning": "응시하다",
    "level": "Extended"
  },
  {
    "id": 1188,
    "word": "gear",
    "meaning": "장비",
    "level": "MidHigh"
  },
  {
    "id": 1189,
    "word": "gender",
    "meaning": "성별",
    "level": "Extended"
  },
  {
    "id": 1190,
    "word": "gene",
    "meaning": "유전자",
    "level": "Extended",
    "variation": "genetic"
  },
  {
    "id": 1191,
    "word": "general",
    "meaning": "일반적인",
    "level": "MidHigh"
  },
  {
    "id": 1192,
    "word": "generate",
    "meaning": "생성하다",
    "level": "Extended",
    "variation": "generation"
  },
  {
    "id": 1193,
    "word": "generous",
    "meaning": "관대한",
    "level": "Extended"
  },
  {
    "id": 1194,
    "word": "genius",
    "meaning": "천재",
    "level": "Extended"
  },
  {
    "id": 1195,
    "word": "gentle",
    "meaning": "온화한",
    "level": "MidHigh"
  },
  {
    "id": 1196,
    "word": "gentleman",
    "meaning": "신사",
    "level": "Elementary"
  },
  {
    "id": 1197,
    "word": "genuine",
    "meaning": "진짜의",
    "level": "Extended"
  },
  {
    "id": 1198,
    "word": "geography",
    "meaning": "지리학",
    "level": "Extended"
  },
  {
    "id": 1199,
    "word": "geology",
    "meaning": "지질학",
    "level": "Extended"
  },
  {
    "id": 1200,
    "word": "gesture",
    "meaning": "몸짓",
    "level": "MidHigh"
  },
  {
    "id": 1201,
    "word": "get",
    "meaning": "얻다",
    "level": "Elementary"
  },
  {
    "id": 1202,
    "word": "ghost",
    "meaning": "유령",
    "level": "MidHigh"
  },
  {
    "id": 1203,
    "word": "giant",
    "meaning": "거인",
    "level": "MidHigh"
  },
  {
    "id": 1204,
    "word": "gift",
    "meaning": "선물",
    "level": "MidHigh"
  },
  {
    "id": 1205,
    "word": "giraffe",
    "meaning": "기린",
    "level": "MidHigh"
  },
  {
    "id": 1206,
    "word": "girl",
    "meaning": "소녀",
    "level": "Elementary"
  },
  {
    "id": 1207,
    "word": "give",
    "meaning": "주다",
    "level": "Elementary"
  },
  {
    "id": 1208,
    "word": "glad",
    "meaning": "기쁜",
    "level": "Elementary"
  },
  {
    "id": 1209,
    "word": "glance",
    "meaning": "흘끗 보다",
    "level": "MidHigh"
  },
  {
    "id": 1210,
    "word": "glare",
    "meaning": "노려보다",
    "level": "Extended"
  },
  {
    "id": 1211,
    "word": "glass",
    "meaning": "유리",
    "level": "Elementary"
  },
  {
    "id": 1212,
    "word": "globe",
    "meaning": "지구본",
    "level": "Extended",
    "variation": "global"
  },
  {
    "id": 1213,
    "word": "glory",
    "meaning": "영광",
    "level": "MidHigh"
  },
  {
    "id": 1214,
    "word": "glove",
    "meaning": "장갑",
    "level": "MidHigh"
  },
  {
    "id": 1215,
    "word": "glow",
    "meaning": "빛나다",
    "level": "Extended"
  },
  {
    "id": 1216,
    "word": "glue",
    "meaning": "풀",
    "level": "MidHigh"
  },
  {
    "id": 1217,
    "word": "go",
    "meaning": "가다",
    "level": "Elementary"
  },
  {
    "id": 1218,
    "word": "goal",
    "meaning": "목표",
    "level": "Elementary"
  },
  {
    "id": 1219,
    "word": "goat",
    "meaning": "염소",
    "level": "Extended"
  },
  {
    "id": 1220,
    "word": "god",
    "meaning": "신",
    "level": "Elementary"
  },
  {
    "id": 1221,
    "word": "gold",
    "meaning": "금",
    "level": "Elementary"
  },
  {
    "id": 1222,
    "word": "golf",
    "meaning": "골프",
    "level": "MidHigh"
  },
  {
    "id": 1223,
    "word": "good",
    "meaning": "좋은",
    "level": "Elementary",
    "variation": "goods"
  },
  {
    "id": 1224,
    "word": "goodbye",
    "meaning": "안녕",
    "level": "Elementary",
    "variation": "bye"
  },
  {
    "id": 1225,
    "word": "gorgeous",
    "meaning": "멋진",
    "level": "MidHigh"
  },
  {
    "id": 1226,
    "word": "govern",
    "meaning": "통치하다",
    "level": "MidHigh",
    "variation": "government"
  },
  {
    "id": 1227,
    "word": "grab",
    "meaning": "붙잡다",
    "level": "MidHigh"
  },
  {
    "id": 1228,
    "word": "grace",
    "meaning": "우아함",
    "level": "MidHigh"
  },
  {
    "id": 1229,
    "word": "grade",
    "meaning": "등급",
    "level": "MidHigh",
    "variation": "gradual"
  },
  {
    "id": 1230,
    "word": "graduate",
    "meaning": "졸업하다",
    "level": "Extended"
  },
  {
    "id": 1231,
    "word": "grain",
    "meaning": "곡물",
    "level": "Extended"
  },
  {
    "id": 1232,
    "word": "grand",
    "meaning": "웅장한",
    "level": "MidHigh"
  },
  {
    "id": 1233,
    "word": "grandfather",
    "meaning": "할아버지",
    "level": "Elementary"
  },
  {
    "id": 1234,
    "word": "grant",
    "meaning": "수여하다",
    "level": "MidHigh"
  },
  {
    "id": 1235,
    "word": "grape",
    "meaning": "포도",
    "level": "Elementary"
  },
  {
    "id": 1236,
    "word": "graph",
    "meaning": "그래프",
    "level": "MidHigh",
    "variation": "graphic"
  },
  {
    "id": 1237,
    "word": "grasp",
    "meaning": "파악하다",
    "level": "Extended"
  },
  {
    "id": 1238,
    "word": "grass",
    "meaning": "풀",
    "level": "Elementary"
  },
  {
    "id": 1239,
    "word": "grateful",
    "meaning": "감사하는",
    "level": "Extended"
  },
  {
    "id": 1240,
    "word": "grave",
    "meaning": "무덤",
    "level": "Extended"
  },
  {
    "id": 1241,
    "word": "gray",
    "meaning": "회색",
    "level": "Elementary",
    "variation": "grey"
  },
  {
    "id": 1242,
    "word": "great",
    "meaning": "훌륭한",
    "level": "Elementary"
  },
  {
    "id": 1243,
    "word": "greed",
    "meaning": "탐욕",
    "level": "Extended"
  },
  {
    "id": 1244,
    "word": "green",
    "meaning": "초록색",
    "level": "Elementary"
  },
  {
    "id": 1245,
    "word": "greet",
    "meaning": "인사하다",
    "level": "MidHigh"
  },
  {
    "id": 1246,
    "word": "grief",
    "meaning": "슬픔",
    "level": "Extended"
  },
  {
    "id": 1247,
    "word": "grip",
    "meaning": "붙잡다",
    "level": "Extended"
  },
  {
    "id": 1248,
    "word": "grocery",
    "meaning": "식료품",
    "level": "MidHigh"
  },
  {
    "id": 1249,
    "word": "gross",
    "meaning": "총계",
    "level": "Extended"
  },
  {
    "id": 1250,
    "word": "ground",
    "meaning": "땅",
    "level": "Elementary"
  },
  {
    "id": 1251,
    "word": "group",
    "meaning": "집단",
    "level": "Elementary"
  },
  {
    "id": 1252,
    "word": "grow",
    "meaning": "자라다",
    "level": "Elementary"
  },
  {
    "id": 1253,
    "word": "guarantee",
    "meaning": "보증하다",
    "level": "MidHigh"
  },
  {
    "id": 1254,
    "word": "guard",
    "meaning": "지키다",
    "level": "MidHigh"
  },
  {
    "id": 1255,
    "word": "guardian",
    "meaning": "보호자",
    "level": "Extended"
  },
  {
    "id": 1256,
    "word": "guess",
    "meaning": "추측하다",
    "level": "Elementary"
  },
  {
    "id": 1257,
    "word": "guest",
    "meaning": "손님",
    "level": "MidHigh"
  },
  {
    "id": 1258,
    "word": "guide",
    "meaning": "안내하다",
    "level": "MidHigh"
  },
  {
    "id": 1259,
    "word": "guideline",
    "meaning": "지침",
    "level": "Extended"
  },
  {
    "id": 1260,
    "word": "guilt",
    "meaning": "죄책감",
    "level": "MidHigh",
    "variation": "guilty"
  },
  {
    "id": 1261,
    "word": "guitar",
    "meaning": "기타",
    "level": "Elementary"
  },
  {
    "id": 1262,
    "word": "gulf",
    "meaning": "만",
    "level": "Extended"
  },
  {
    "id": 1263,
    "word": "gum",
    "meaning": "껌",
    "level": "Elementary"
  },
  {
    "id": 1264,
    "word": "gun",
    "meaning": "총",
    "level": "MidHigh"
  },
  {
    "id": 1265,
    "word": "guy",
    "meaning": "남자",
    "level": "Elementary"
  },
  {
    "id": 1266,
    "word": "gymnasium",
    "meaning": "체육관",
    "level": "Extended",
    "variation": "gym"
  },
  {
    "id": 1267,
    "word": "habit",
    "meaning": "습관",
    "level": "Elementary"
  },
  {
    "id": 1268,
    "word": "habitat",
    "meaning": "서식지",
    "level": "Extended"
  },
  {
    "id": 1269,
    "word": "hair",
    "meaning": "머리카락",
    "level": "Elementary"
  },
  {
    "id": 1270,
    "word": "half",
    "meaning": "절반",
    "level": "MidHigh"
  },
  {
    "id": 1271,
    "word": "hall",
    "meaning": "홀",
    "level": "MidHigh"
  },
  {
    "id": 1272,
    "word": "halt",
    "meaning": "멈추다",
    "level": "Extended"
  },
  {
    "id": 1273,
    "word": "hamburger",
    "meaning": "햄버거",
    "level": "Elementary"
  },
  {
    "id": 1274,
    "word": "hammer",
    "meaning": "망치",
    "level": "Extended"
  },
  {
    "id": 1275,
    "word": "hand",
    "meaning": "손",
    "level": "Elementary"
  },
  {
    "id": 1276,
    "word": "handicap",
    "meaning": "장애",
    "level": "Extended"
  },
  {
    "id": 1277,
    "word": "handle",
    "meaning": "다루다",
    "level": "MidHigh"
  },
  {
    "id": 1278,
    "word": "handsome",
    "meaning": "잘생긴",
    "level": "MidHigh"
  },
  {
    "id": 1279,
    "word": "hang",
    "meaning": "걸다",
    "level": "Elementary"
  },
  {
    "id": 1280,
    "word": "happen",
    "meaning": "일어나다",
    "level": "MidHigh"
  },
  {
    "id": 1281,
    "word": "happy",
    "meaning": "행복한",
    "level": "Elementary"
  },
  {
    "id": 1282,
    "word": "harbor",
    "meaning": "항구",
    "level": "Extended",
    "variation": "harbour"
  },
  {
    "id": 1283,
    "word": "hard",
    "meaning": "어려운",
    "level": "Elementary",
    "variation": "hardly"
  },
  {
    "id": 1284,
    "word": "harm",
    "meaning": "해치다",
    "level": "MidHigh"
  },
  {
    "id": 1285,
    "word": "harmony",
    "meaning": "조화",
    "level": "Extended",
    "variation": "harmonious"
  },
  {
    "id": 1286,
    "word": "harsh",
    "meaning": "가혹한",
    "level": "Extended"
  },
  {
    "id": 1287,
    "word": "harvest",
    "meaning": "수확",
    "level": "Extended"
  },
  {
    "id": 1288,
    "word": "hat",
    "meaning": "모자",
    "level": "Elementary"
  },
  {
    "id": 1289,
    "word": "hate",
    "meaning": "미워하다",
    "level": "Elementary"
  },
  {
    "id": 1290,
    "word": "haunt",
    "meaning": "괴롭히다",
    "level": "Extended"
  },
  {
    "id": 1291,
    "word": "have",
    "meaning": "가지다",
    "level": "Elementary"
  },
  {
    "id": 1292,
    "word": "hazard",
    "meaning": "위험 요소",
    "level": "Extended"
  },
  {
    "id": 1293,
    "word": "he",
    "meaning": "그",
    "level": "Elementary"
  },
  {
    "id": 1294,
    "word": "head",
    "meaning": "머리",
    "level": "Elementary"
  },
  {
    "id": 1295,
    "word": "headquarters",
    "meaning": "본부",
    "level": "Extended"
  },
  {
    "id": 1296,
    "word": "heal",
    "meaning": "치유하다",
    "level": "Extended"
  },
  {
    "id": 1297,
    "word": "health",
    "meaning": "건강",
    "level": "MidHigh",
    "variation": "healthy"
  },
  {
    "id": 1298,
    "word": "hear",
    "meaning": "듣다",
    "level": "MidHigh"
  },
  {
    "id": 1299,
    "word": "heart",
    "meaning": "심장",
    "level": "Elementary"
  },
  {
    "id": 1300,
    "word": "heat",
    "meaning": "열",
    "level": "Elementary"
  },
  {
    "id": 1301,
    "word": "heaven",
    "meaning": "천국",
    "level": "MidHigh"
  },
  {
    "id": 1302,
    "word": "heavy",
    "meaning": "무거운",
    "level": "Elementary"
  },
  {
    "id": 1303,
    "word": "heel",
    "meaning": "발뒤꿈치",
    "level": "Extended"
  },
  {
    "id": 1304,
    "word": "height",
    "meaning": "높이",
    "level": "MidHigh"
  },
  {
    "id": 1305,
    "word": "heir",
    "meaning": "상속인",
    "level": "Extended"
  },
  {
    "id": 1306,
    "word": "helicopter",
    "meaning": "헬리콥터",
    "level": "MidHigh"
  },
  {
    "id": 1307,
    "word": "hell",
    "meaning": "지옥",
    "level": "MidHigh"
  },
  {
    "id": 1308,
    "word": "hello",
    "meaning": "안녕",
    "level": "Elementary",
    "variation": "hey, hi"
  },
  {
    "id": 1309,
    "word": "helmet",
    "meaning": "헬멧",
    "level": "Elementary"
  },
  {
    "id": 1310,
    "word": "help",
    "meaning": "돕다",
    "level": "Elementary"
  },
  {
    "id": 1311,
    "word": "hence",
    "meaning": "그러므로",
    "level": "Extended"
  },
  {
    "id": 1312,
    "word": "here",
    "meaning": "여기",
    "level": "Elementary"
  },
  {
    "id": 1313,
    "word": "heritage",
    "meaning": "유산",
    "level": "Extended"
  },
  {
    "id": 1314,
    "word": "hero",
    "meaning": "영웅",
    "level": "Elementary"
  },
  {
    "id": 1315,
    "word": "hesitate",
    "meaning": "망설이다",
    "level": "MidHigh"
  },
  {
    "id": 1316,
    "word": "hide",
    "meaning": "숨기다",
    "level": "MidHigh"
  },
  {
    "id": 1317,
    "word": "hierarchy",
    "meaning": "위계",
    "level": "Extended"
  },
  {
    "id": 1318,
    "word": "high",
    "meaning": "높은",
    "level": "Elementary"
  },
  {
    "id": 1319,
    "word": "highlight",
    "meaning": "강조하다",
    "level": "Extended"
  },
  {
    "id": 1320,
    "word": "highway",
    "meaning": "고속도로",
    "level": "MidHigh"
  },
  {
    "id": 1321,
    "word": "hike",
    "meaning": "도보 여행",
    "level": "Elementary"
  },
  {
    "id": 1322,
    "word": "hill",
    "meaning": "언덕",
    "level": "Elementary"
  },
  {
    "id": 1323,
    "word": "hint",
    "meaning": "힌트",
    "level": "MidHigh"
  },
  {
    "id": 1324,
    "word": "hire",
    "meaning": "고용하다",
    "level": "MidHigh"
  },
  {
    "id": 1325,
    "word": "history",
    "meaning": "역사",
    "level": "Elementary"
  },
  {
    "id": 1326,
    "word": "hit",
    "meaning": "치다",
    "level": "Elementary"
  },
  {
    "id": 1327,
    "word": "hobby",
    "meaning": "취미",
    "level": "Elementary"
  },
  {
    "id": 1328,
    "word": "hold",
    "meaning": "잡다",
    "level": "Elementary"
  },
  {
    "id": 1329,
    "word": "hole",
    "meaning": "구멍",
    "level": "MidHigh"
  },
  {
    "id": 1330,
    "word": "holiday",
    "meaning": "휴일",
    "level": "Elementary"
  },
  {
    "id": 1331,
    "word": "holy",
    "meaning": "성스러운",
    "level": "Extended"
  },
  {
    "id": 1332,
    "word": "home",
    "meaning": "집",
    "level": "Elementary"
  },
  {
    "id": 1333,
    "word": "homework",
    "meaning": "숙제",
    "level": "Elementary"
  },
  {
    "id": 1334,
    "word": "honest",
    "meaning": "정직한",
    "level": "Elementary"
  },
  {
    "id": 1335,
    "word": "honey",
    "meaning": "꿀",
    "level": "MidHigh"
  },
  {
    "id": 1336,
    "word": "honor",
    "meaning": "명예",
    "level": "MidHigh",
    "variation": "honour"
  },
  {
    "id": 1337,
    "word": "hook",
    "meaning": "갈고리",
    "level": "Extended"
  },
  {
    "id": 1338,
    "word": "hope",
    "meaning": "희망",
    "level": "Elementary"
  },
  {
    "id": 1339,
    "word": "horizon",
    "meaning": "지평선",
    "level": "Extended"
  },
  {
    "id": 1340,
    "word": "horror",
    "meaning": "공포",
    "level": "Extended"
  },
  {
    "id": 1341,
    "word": "horse",
    "meaning": "말",
    "level": "Elementary"
  },
  {
    "id": 1342,
    "word": "hospital",
    "meaning": "병원",
    "level": "Elementary"
  },
  {
    "id": 1343,
    "word": "host",
    "meaning": "주인",
    "level": "Extended"
  },
  {
    "id": 1344,
    "word": "hostile",
    "meaning": "적대적인",
    "level": "Extended"
  },
  {
    "id": 1345,
    "word": "hot",
    "meaning": "뜨거운",
    "level": "Elementary"
  },
  {
    "id": 1346,
    "word": "hotel",
    "meaning": "호텔",
    "level": "MidHigh"
  },
  {
    "id": 1347,
    "word": "hour",
    "meaning": "시간",
    "level": "Elementary"
  },
  {
    "id": 1348,
    "word": "house",
    "meaning": "집",
    "level": "Elementary"
  },
  {
    "id": 1349,
    "word": "household",
    "meaning": "가정",
    "level": "Extended"
  },
  {
    "id": 1350,
    "word": "how",
    "meaning": "어떻게",
    "level": "Elementary"
  },
  {
    "id": 1351,
    "word": "however",
    "meaning": "그러나",
    "level": "Elementary"
  },
  {
    "id": 1352,
    "word": "hug",
    "meaning": "껴안다",
    "level": "MidHigh"
  },
  {
    "id": 1353,
    "word": "huge",
    "meaning": "거대한",
    "level": "MidHigh"
  },
  {
    "id": 1354,
    "word": "human",
    "meaning": "인간",
    "level": "Elementary"
  },
  {
    "id": 1355,
    "word": "humor",
    "meaning": "유머",
    "level": "MidHigh",
    "variation": "humour"
  },
  {
    "id": 1356,
    "word": "hundred",
    "meaning": "백",
    "level": "Elementary"
  },
  {
    "id": 1357,
    "word": "hunger",
    "meaning": "배고픔",
    "level": "MidHigh",
    "variation": "hungry"
  },
  {
    "id": 1358,
    "word": "hunt",
    "meaning": "사냥하다",
    "level": "Elementary"
  },
  {
    "id": 1359,
    "word": "hurry",
    "meaning": "서두르다",
    "level": "Elementary"
  },
  {
    "id": 1360,
    "word": "hurt",
    "meaning": "다치게 하다",
    "level": "MidHigh"
  },
  {
    "id": 1361,
    "word": "husband",
    "meaning": "남편",
    "level": "Elementary"
  },
  {
    "id": 1362,
    "word": "hut",
    "meaning": "오두막",
    "level": "Extended"
  },
  {
    "id": 1363,
    "word": "hypothesis",
    "meaning": "가설",
    "level": "Extended"
  },
  {
    "id": 1364,
    "word": "I",
    "meaning": "나",
    "level": "Elementary"
  },
  {
    "id": 1365,
    "word": "ice",
    "meaning": "얼음",
    "level": "Elementary"
  },
  {
    "id": 1366,
    "word": "idea",
    "meaning": "생각",
    "level": "Elementary"
  },
  {
    "id": 1367,
    "word": "ideal",
    "meaning": "이상적인",
    "level": "Extended"
  },
  {
    "id": 1368,
    "word": "identical",
    "meaning": "똑같은",
    "level": "Extended"
  },
  {
    "id": 1369,
    "word": "identity",
    "meaning": "정체성",
    "level": "MidHigh",
    "variation": "identify"
  },
  {
    "id": 1370,
    "word": "ideology",
    "meaning": "이념",
    "level": "Extended"
  },
  {
    "id": 1371,
    "word": "if",
    "meaning": "만약",
    "level": "Elementary"
  },
  {
    "id": 1372,
    "word": "ignore",
    "meaning": "무시하다",
    "level": "MidHigh"
  },
  {
    "id": 1373,
    "word": "ill",
    "meaning": "아픈",
    "level": "MidHigh"
  },
  {
    "id": 1374,
    "word": "illude",
    "meaning": "속이다",
    "level": "Extended",
    "variation": "illusion"
  },
  {
    "id": 1375,
    "word": "illustrate",
    "meaning": "설명하다",
    "level": "MidHigh"
  },
  {
    "id": 1376,
    "word": "image",
    "meaning": "이미지",
    "level": "Elementary"
  },
  {
    "id": 1377,
    "word": "imagine",
    "meaning": "상상하다",
    "level": "MidHigh"
  },
  {
    "id": 1378,
    "word": "imitate",
    "meaning": "모방하다",
    "level": "Extended"
  },
  {
    "id": 1379,
    "word": "immediate",
    "meaning": "즉각적인",
    "level": "MidHigh"
  },
  {
    "id": 1380,
    "word": "immense",
    "meaning": "거대한",
    "level": "Extended"
  },
  {
    "id": 1381,
    "word": "immigrate",
    "meaning": "이민 오다",
    "level": "Extended"
  },
  {
    "id": 1382,
    "word": "immune",
    "meaning": "면역이 있는",
    "level": "Extended"
  },
  {
    "id": 1383,
    "word": "impact",
    "meaning": "영향",
    "level": "Extended"
  },
  {
    "id": 1384,
    "word": "imperial",
    "meaning": "제국의",
    "level": "Extended"
  },
  {
    "id": 1385,
    "word": "implement",
    "meaning": "실행하다",
    "level": "Extended"
  },
  {
    "id": 1386,
    "word": "imply",
    "meaning": "암시하다",
    "level": "Extended"
  },
  {
    "id": 1387,
    "word": "import",
    "meaning": "수입하다",
    "level": "Extended",
    "variation": "importance, important"
  },
  {
    "id": 1388,
    "word": "impose",
    "meaning": "부과하다",
    "level": "Extended"
  },
  {
    "id": 1389,
    "word": "impress",
    "meaning": "감명을 주다",
    "level": "MidHigh"
  },
  {
    "id": 1390,
    "word": "improve",
    "meaning": "개선하다",
    "level": "MidHigh"
  },
  {
    "id": 1391,
    "word": "in",
    "meaning": "~안에",
    "level": "Elementary"
  },
  {
    "id": 1392,
    "word": "incentive",
    "meaning": "유인책",
    "level": "Extended"
  },
  {
    "id": 1393,
    "word": "incident",
    "meaning": "사건",
    "level": "Extended"
  },
  {
    "id": 1394,
    "word": "incline",
    "meaning": "기울다",
    "level": "Extended"
  },
  {
    "id": 1395,
    "word": "include",
    "meaning": "포함하다",
    "level": "MidHigh"
  },
  {
    "id": 1396,
    "word": "income",
    "meaning": "소득",
    "level": "MidHigh"
  },
  {
    "id": 1397,
    "word": "incorporate",
    "meaning": "통합하다",
    "level": "Extended"
  },
  {
    "id": 1398,
    "word": "increase",
    "meaning": "증가하다",
    "level": "MidHigh"
  },
  {
    "id": 1399,
    "word": "indeed",
    "meaning": "실제로",
    "level": "MidHigh"
  },
  {
    "id": 1400,
    "word": "index",
    "meaning": "색인",
    "level": "Extended"
  },
  {
    "id": 1401,
    "word": "indicate",
    "meaning": "나타내다",
    "level": "MidHigh"
  },
  {
    "id": 1402,
    "word": "individual",
    "meaning": "개인의",
    "level": "MidHigh"
  },
  {
    "id": 1403,
    "word": "induce",
    "meaning": "유발하다",
    "level": "Extended"
  },
  {
    "id": 1404,
    "word": "industry",
    "meaning": "산업",
    "level": "MidHigh"
  },
  {
    "id": 1405,
    "word": "infant",
    "meaning": "유아",
    "level": "Extended"
  },
  {
    "id": 1406,
    "word": "infect",
    "meaning": "감염시키다",
    "level": "Extended"
  },
  {
    "id": 1407,
    "word": "infer",
    "meaning": "추론하다",
    "level": "Extended",
    "variation": "inference"
  },
  {
    "id": 1408,
    "word": "inflate",
    "meaning": "부풀리다",
    "level": "Extended"
  },
  {
    "id": 1409,
    "word": "influence",
    "meaning": "영향",
    "level": "MidHigh"
  },
  {
    "id": 1410,
    "word": "inform",
    "meaning": "알리다",
    "level": "MidHigh"
  },
  {
    "id": 1411,
    "word": "ingredient",
    "meaning": "재료",
    "level": "Extended"
  },
  {
    "id": 1412,
    "word": "inhabit",
    "meaning": "살다",
    "level": "Extended"
  },
  {
    "id": 1413,
    "word": "inherent",
    "meaning": "내재적인",
    "level": "Extended"
  },
  {
    "id": 1414,
    "word": "inhibit",
    "meaning": "억제하다",
    "level": "Extended"
  },
  {
    "id": 1415,
    "word": "initial",
    "meaning": "처음의",
    "level": "Extended"
  },
  {
    "id": 1416,
    "word": "inject",
    "meaning": "주입하다",
    "level": "Extended"
  },
  {
    "id": 1417,
    "word": "injure",
    "meaning": "다치게 하다",
    "level": "MidHigh"
  },
  {
    "id": 1418,
    "word": "inn",
    "meaning": "여관",
    "level": "Extended"
  },
  {
    "id": 1419,
    "word": "innocent",
    "meaning": "무고한",
    "level": "MidHigh"
  },
  {
    "id": 1420,
    "word": "innovate",
    "meaning": "혁신하다",
    "level": "Extended"
  },
  {
    "id": 1421,
    "word": "input",
    "meaning": "입력",
    "level": "Extended"
  },
  {
    "id": 1422,
    "word": "inquire",
    "meaning": "문의하다",
    "level": "Extended",
    "variation": "enquire"
  },
  {
    "id": 1423,
    "word": "insect",
    "meaning": "곤충",
    "level": "Extended"
  },
  {
    "id": 1424,
    "word": "insert",
    "meaning": "삽입하다",
    "level": "Extended"
  },
  {
    "id": 1425,
    "word": "inside",
    "meaning": "안쪽",
    "level": "Elementary"
  },
  {
    "id": 1426,
    "word": "insight",
    "meaning": "통찰력",
    "level": "Extended"
  },
  {
    "id": 1427,
    "word": "insist",
    "meaning": "주장하다",
    "level": "MidHigh"
  },
  {
    "id": 1428,
    "word": "inspect",
    "meaning": "검사하다",
    "level": "MidHigh"
  },
  {
    "id": 1429,
    "word": "inspire",
    "meaning": "영감을 주다",
    "level": "Extended"
  },
  {
    "id": 1430,
    "word": "install",
    "meaning": "설치하다",
    "level": "Extended"
  },
  {
    "id": 1431,
    "word": "instance",
    "meaning": "사례",
    "level": "MidHigh"
  },
  {
    "id": 1432,
    "word": "instant",
    "meaning": "즉각적인",
    "level": "MidHigh"
  },
  {
    "id": 1433,
    "word": "instead",
    "meaning": "대신에",
    "level": "MidHigh"
  },
  {
    "id": 1434,
    "word": "instinct",
    "meaning": "본능",
    "level": "Extended"
  },
  {
    "id": 1435,
    "word": "institute",
    "meaning": "기관",
    "level": "Extended",
    "variation": "institution"
  },
  {
    "id": 1436,
    "word": "instruct",
    "meaning": "지시하다",
    "level": "MidHigh"
  },
  {
    "id": 1437,
    "word": "instrument",
    "meaning": "도구",
    "level": "MidHigh"
  },
  {
    "id": 1438,
    "word": "insult",
    "meaning": "모욕하다",
    "level": "Extended"
  },
  {
    "id": 1439,
    "word": "insure",
    "meaning": "보험에 들다",
    "level": "MidHigh",
    "variation": "insurance"
  },
  {
    "id": 1440,
    "word": "integrate",
    "meaning": "통합하다",
    "level": "Extended"
  },
  {
    "id": 1441,
    "word": "intellect",
    "meaning": "지성",
    "level": "Extended",
    "variation": "intellectual"
  },
  {
    "id": 1442,
    "word": "intelligent",
    "meaning": "지적인",
    "level": "Extended"
  },
  {
    "id": 1443,
    "word": "intend",
    "meaning": "의도하다",
    "level": "MidHigh"
  },
  {
    "id": 1444,
    "word": "intense",
    "meaning": "강렬한",
    "level": "MidHigh"
  },
  {
    "id": 1445,
    "word": "intent",
    "meaning": "의도",
    "level": "MidHigh",
    "variation": "intention"
  },
  {
    "id": 1446,
    "word": "interest",
    "meaning": "관심",
    "level": "MidHigh"
  },
  {
    "id": 1447,
    "word": "interfere",
    "meaning": "방해하다",
    "level": "Extended"
  },
  {
    "id": 1448,
    "word": "interior",
    "meaning": "내부",
    "level": "Extended"
  },
  {
    "id": 1449,
    "word": "intermediate",
    "meaning": "중간의",
    "level": "Extended"
  },
  {
    "id": 1450,
    "word": "internal",
    "meaning": "내부의",
    "level": "MidHigh"
  },
  {
    "id": 1451,
    "word": "internet",
    "meaning": "인터넷",
    "level": "Elementary"
  },
  {
    "id": 1452,
    "word": "interpret",
    "meaning": "해석하다",
    "level": "Extended"
  },
  {
    "id": 1453,
    "word": "interrupt",
    "meaning": "중단시키다",
    "level": "MidHigh"
  },
  {
    "id": 1454,
    "word": "interval",
    "meaning": "간격",
    "level": "Extended"
  },
  {
    "id": 1455,
    "word": "intervene",
    "meaning": "개입하다",
    "level": "Extended"
  },
  {
    "id": 1456,
    "word": "intimate",
    "meaning": "친밀한",
    "level": "Extended"
  },
  {
    "id": 1457,
    "word": "into",
    "meaning": "~안으로",
    "level": "Elementary"
  },
  {
    "id": 1458,
    "word": "intrigue",
    "meaning": "흥미를 돋우다",
    "level": "Extended"
  },
  {
    "id": 1459,
    "word": "introduce",
    "meaning": "소개하다",
    "level": "Elementary"
  },
  {
    "id": 1460,
    "word": "invade",
    "meaning": "침입하다",
    "level": "Extended"
  },
  {
    "id": 1461,
    "word": "invent",
    "meaning": "발명하다",
    "level": "MidHigh",
    "variation": "inventor"
  },
  {
    "id": 1462,
    "word": "invest",
    "meaning": "투자하다",
    "level": "MidHigh"
  },
  {
    "id": 1463,
    "word": "investigate",
    "meaning": "조사하다",
    "level": "MidHigh"
  },
  {
    "id": 1464,
    "word": "invite",
    "meaning": "초대하다",
    "level": "Elementary"
  },
  {
    "id": 1465,
    "word": "involve",
    "meaning": "포함하다",
    "level": "MidHigh"
  },
  {
    "id": 1466,
    "word": "iron",
    "meaning": "철",
    "level": "MidHigh"
  },
  {
    "id": 1467,
    "word": "irony",
    "meaning": "반어",
    "level": "Extended"
  },
  {
    "id": 1468,
    "word": "irritate",
    "meaning": "짜증 나게 하다",
    "level": "Extended"
  },
  {
    "id": 1469,
    "word": "island",
    "meaning": "섬",
    "level": "MidHigh"
  },
  {
    "id": 1470,
    "word": "isolate",
    "meaning": "고립시키다",
    "level": "Extended"
  },
  {
    "id": 1471,
    "word": "issue",
    "meaning": "문제",
    "level": "Elementary"
  },
  {
    "id": 1472,
    "word": "it",
    "meaning": "그것",
    "level": "Elementary"
  },
  {
    "id": 1473,
    "word": "item",
    "meaning": "항목",
    "level": "MidHigh"
  },
  {
    "id": 1474,
    "word": "jacket",
    "meaning": "재킷",
    "level": "Elementary"
  },
  {
    "id": 1475,
    "word": "jail",
    "meaning": "감옥",
    "level": "Extended"
  },
  {
    "id": 1476,
    "word": "jam",
    "meaning": "잼",
    "level": "Elementary"
  },
  {
    "id": 1477,
    "word": "jar",
    "meaning": "항아리",
    "level": "Extended"
  },
  {
    "id": 1478,
    "word": "jaw",
    "meaning": "턱",
    "level": "MidHigh"
  },
  {
    "id": 1479,
    "word": "jeans",
    "meaning": "청바지",
    "level": "MidHigh"
  },
  {
    "id": 1480,
    "word": "job",
    "meaning": "일",
    "level": "Elementary"
  },
  {
    "id": 1481,
    "word": "jog",
    "meaning": "조깅하다",
    "level": "Extended"
  },
  {
    "id": 1482,
    "word": "join",
    "meaning": "가입하다",
    "level": "Elementary"
  },
  {
    "id": 1483,
    "word": "joint",
    "meaning": "관절",
    "level": "Extended"
  },
  {
    "id": 1484,
    "word": "joke",
    "meaning": "농담",
    "level": "MidHigh"
  },
  {
    "id": 1485,
    "word": "journal",
    "meaning": "학술지",
    "level": "Extended"
  },
  {
    "id": 1486,
    "word": "journey",
    "meaning": "여행",
    "level": "MidHigh"
  },
  {
    "id": 1487,
    "word": "joy",
    "meaning": "기쁨",
    "level": "MidHigh",
    "variation": "enjoy"
  },
  {
    "id": 1488,
    "word": "judge",
    "meaning": "판사",
    "level": "MidHigh"
  },
  {
    "id": 1489,
    "word": "juice",
    "meaning": "주스",
    "level": "Elementary"
  },
  {
    "id": 1490,
    "word": "jump",
    "meaning": "뛰다",
    "level": "Elementary"
  },
  {
    "id": 1491,
    "word": "junior",
    "meaning": "후배",
    "level": "MidHigh"
  },
  {
    "id": 1492,
    "word": "jury",
    "meaning": "배심원단",
    "level": "Extended"
  },
  {
    "id": 1493,
    "word": "just",
    "meaning": "단지",
    "level": "Elementary"
  },
  {
    "id": 1494,
    "word": "justice",
    "meaning": "정의",
    "level": "MidHigh"
  },
  {
    "id": 1495,
    "word": "keen",
    "meaning": "열심인",
    "level": "Extended"
  },
  {
    "id": 1496,
    "word": "keep",
    "meaning": "유지하다",
    "level": "Elementary"
  },
  {
    "id": 1497,
    "word": "key",
    "meaning": "열쇠",
    "level": "Elementary"
  },
  {
    "id": 1498,
    "word": "kick",
    "meaning": "차다",
    "level": "Elementary"
  },
  {
    "id": 1499,
    "word": "kid",
    "meaning": "아이",
    "level": "Elementary"
  },
  {
    "id": 1500,
    "word": "kill",
    "meaning": "죽이다",
    "level": "Elementary"
  },
  {
    "id": 1501,
    "word": "kind",
    "meaning": "친절한",
    "level": "Elementary"
  },
  {
    "id": 1502,
    "word": "king",
    "meaning": "왕",
    "level": "Elementary"
  },
  {
    "id": 1503,
    "word": "kiss",
    "meaning": "입맞춤",
    "level": "Elementary"
  },
  {
    "id": 1504,
    "word": "kit",
    "meaning": "도구 세트",
    "level": "Extended"
  },
  {
    "id": 1505,
    "word": "kitchen",
    "meaning": "부엌",
    "level": "Elementary"
  },
  {
    "id": 1506,
    "word": "knee",
    "meaning": "무릎",
    "level": "MidHigh"
  },
  {
    "id": 1507,
    "word": "knife",
    "meaning": "칼",
    "level": "Elementary"
  },
  {
    "id": 1508,
    "word": "knight",
    "meaning": "기사",
    "level": "Extended"
  },
  {
    "id": 1509,
    "word": "knock",
    "meaning": "두드리다",
    "level": "MidHigh"
  },
  {
    "id": 1510,
    "word": "knot",
    "meaning": "매듭",
    "level": "Extended"
  },
  {
    "id": 1511,
    "word": "know",
    "meaning": "알다",
    "level": "Elementary"
  },
  {
    "id": 1512,
    "word": "knowledge",
    "meaning": "지식",
    "level": "MidHigh"
  },
  {
    "id": 1513,
    "word": "label",
    "meaning": "상표",
    "level": "MidHigh"
  },
  {
    "id": 1514,
    "word": "labor",
    "meaning": "노동",
    "level": "MidHigh",
    "variation": "labour"
  },
  {
    "id": 1515,
    "word": "laboratory",
    "meaning": "실험실",
    "level": "MidHigh",
    "variation": "lab"
  },
  {
    "id": 1516,
    "word": "lack",
    "meaning": "부족",
    "level": "MidHigh"
  },
  {
    "id": 1517,
    "word": "ladder",
    "meaning": "사다리",
    "level": "Extended"
  },
  {
    "id": 1518,
    "word": "lady",
    "meaning": "숙녀",
    "level": "Elementary"
  },
  {
    "id": 1519,
    "word": "lake",
    "meaning": "호수",
    "level": "Elementary"
  },
  {
    "id": 1520,
    "word": "lamb",
    "meaning": "어린 양",
    "level": "MidHigh"
  },
  {
    "id": 1521,
    "word": "lamp",
    "meaning": "램프",
    "level": "MidHigh"
  },
  {
    "id": 1522,
    "word": "land",
    "meaning": "땅",
    "level": "Elementary"
  },
  {
    "id": 1523,
    "word": "landscape",
    "meaning": "풍경",
    "level": "Extended"
  },
  {
    "id": 1524,
    "word": "lane",
    "meaning": "차선",
    "level": "MidHigh"
  },
  {
    "id": 1525,
    "word": "language",
    "meaning": "언어",
    "level": "MidHigh"
  },
  {
    "id": 1526,
    "word": "lap",
    "meaning": "무릎",
    "level": "Extended"
  },
  {
    "id": 1527,
    "word": "large",
    "meaning": "큰",
    "level": "Elementary"
  },
  {
    "id": 1528,
    "word": "laser",
    "meaning": "레이저",
    "level": "Elementary"
  },
  {
    "id": 1529,
    "word": "last",
    "meaning": "마지막",
    "level": "Elementary"
  },
  {
    "id": 1530,
    "word": "late",
    "meaning": "늦은",
    "level": "Elementary"
  },
  {
    "id": 1531,
    "word": "latter",
    "meaning": "후자의",
    "level": "Extended"
  },
  {
    "id": 1532,
    "word": "laugh",
    "meaning": "웃다",
    "level": "MidHigh"
  },
  {
    "id": 1533,
    "word": "launch",
    "meaning": "발사하다",
    "level": "Extended"
  },
  {
    "id": 1534,
    "word": "laundry",
    "meaning": "세탁물",
    "level": "Extended"
  },
  {
    "id": 1535,
    "word": "law",
    "meaning": "법",
    "level": "MidHigh"
  },
  {
    "id": 1536,
    "word": "lawn",
    "meaning": "잔디",
    "level": "MidHigh"
  },
  {
    "id": 1537,
    "word": "lawyer",
    "meaning": "변호사",
    "level": "MidHigh"
  },
  {
    "id": 1538,
    "word": "lay",
    "meaning": "놓다",
    "level": "MidHigh",
    "variation": "layer"
  },
  {
    "id": 1539,
    "word": "lazy",
    "meaning": "게으른",
    "level": "Elementary"
  },
  {
    "id": 1540,
    "word": "lead",
    "meaning": "이끌다",
    "level": "MidHigh"
  },
  {
    "id": 1541,
    "word": "leaf",
    "meaning": "잎",
    "level": "MidHigh"
  },
  {
    "id": 1542,
    "word": "league",
    "meaning": "연맹",
    "level": "MidHigh"
  },
  {
    "id": 1543,
    "word": "leak",
    "meaning": "새다",
    "level": "Extended"
  },
  {
    "id": 1544,
    "word": "lean",
    "meaning": "기대다",
    "level": "MidHigh"
  },
  {
    "id": 1545,
    "word": "leap",
    "meaning": "도약하다",
    "level": "MidHigh"
  },
  {
    "id": 1546,
    "word": "learn",
    "meaning": "배우다",
    "level": "Elementary"
  },
  {
    "id": 1547,
    "word": "lease",
    "meaning": "임대차",
    "level": "Extended"
  },
  {
    "id": 1548,
    "word": "leather",
    "meaning": "가죽",
    "level": "Extended"
  },
  {
    "id": 1549,
    "word": "leave",
    "meaning": "떠나다",
    "level": "MidHigh"
  },
  {
    "id": 1550,
    "word": "lecture",
    "meaning": "강의",
    "level": "Extended"
  },
  {
    "id": 1551,
    "word": "left",
    "meaning": "왼쪽",
    "level": "Elementary"
  },
  {
    "id": 1552,
    "word": "leg",
    "meaning": "다리",
    "level": "Elementary"
  },
  {
    "id": 1553,
    "word": "legal",
    "meaning": "법적인",
    "level": "MidHigh"
  },
  {
    "id": 1554,
    "word": "legend",
    "meaning": "전설",
    "level": "Extended"
  },
  {
    "id": 1555,
    "word": "legislate",
    "meaning": "법률을 제정하다",
    "level": "Extended"
  },
  {
    "id": 1556,
    "word": "legitimate",
    "meaning": "합법적인",
    "level": "Extended"
  },
  {
    "id": 1557,
    "word": "leisure",
    "meaning": "여가",
    "level": "Extended"
  },
  {
    "id": 1558,
    "word": "lemon",
    "meaning": "레몬",
    "level": "MidHigh"
  },
  {
    "id": 1559,
    "word": "lend",
    "meaning": "빌려주다",
    "level": "MidHigh"
  },
  {
    "id": 1560,
    "word": "lesson",
    "meaning": "수업",
    "level": "Elementary"
  },
  {
    "id": 1561,
    "word": "let",
    "meaning": "허락하다",
    "level": "MidHigh"
  },
  {
    "id": 1562,
    "word": "letter",
    "meaning": "편지",
    "level": "Elementary",
    "variation": "literal"
  },
  {
    "id": 1563,
    "word": "level",
    "meaning": "수준",
    "level": "MidHigh"
  },
  {
    "id": 1564,
    "word": "liberal",
    "meaning": "자유주의의",
    "level": "Extended"
  },
  {
    "id": 1565,
    "word": "liberty",
    "meaning": "자유",
    "level": "Extended"
  },
  {
    "id": 1566,
    "word": "library",
    "meaning": "도서관",
    "level": "Elementary"
  },
  {
    "id": 1567,
    "word": "license",
    "meaning": "면허",
    "level": "MidHigh",
    "variation": "licence"
  },
  {
    "id": 1568,
    "word": "lid",
    "meaning": "뚜껑",
    "level": "MidHigh"
  },
  {
    "id": 1569,
    "word": "lie",
    "meaning": "거짓말하다",
    "level": "Elementary"
  },
  {
    "id": 1570,
    "word": "life",
    "meaning": "삶",
    "level": "Elementary"
  },
  {
    "id": 1571,
    "word": "lift",
    "meaning": "들어 올리다",
    "level": "MidHigh"
  },
  {
    "id": 1572,
    "word": "light",
    "meaning": "빛",
    "level": "Elementary"
  },
  {
    "id": 1573,
    "word": "like",
    "meaning": "좋아하다",
    "level": "Elementary",
    "variation": "likely"
  },
  {
    "id": 1574,
    "word": "likewise",
    "meaning": "마찬가지로",
    "level": "Extended"
  },
  {
    "id": 1575,
    "word": "limit",
    "meaning": "한계",
    "level": "MidHigh"
  },
  {
    "id": 1576,
    "word": "line",
    "meaning": "선",
    "level": "Elementary"
  },
  {
    "id": 1577,
    "word": "linguistic",
    "meaning": "언어학적인",
    "level": "Extended"
  },
  {
    "id": 1578,
    "word": "link",
    "meaning": "연결",
    "level": "MidHigh"
  },
  {
    "id": 1579,
    "word": "lion",
    "meaning": "사자",
    "level": "Elementary"
  },
  {
    "id": 1580,
    "word": "lip",
    "meaning": "입술",
    "level": "Elementary"
  },
  {
    "id": 1581,
    "word": "liquid",
    "meaning": "액체",
    "level": "Extended"
  },
  {
    "id": 1582,
    "word": "list",
    "meaning": "목록",
    "level": "MidHigh"
  },
  {
    "id": 1583,
    "word": "listen",
    "meaning": "듣다",
    "level": "Elementary"
  },
  {
    "id": 1584,
    "word": "literature",
    "meaning": "문학",
    "level": "Extended"
  },
  {
    "id": 1585,
    "word": "little",
    "meaning": "작은",
    "level": "Elementary"
  },
  {
    "id": 1586,
    "word": "live",
    "meaning": "살다",
    "level": "Elementary"
  },
  {
    "id": 1587,
    "word": "livingroom",
    "meaning": "거실",
    "level": "MidHigh"
  },
  {
    "id": 1588,
    "word": "load",
    "meaning": "짐",
    "level": "MidHigh"
  },
  {
    "id": 1589,
    "word": "loan",
    "meaning": "대출",
    "level": "MidHigh"
  },
  {
    "id": 1590,
    "word": "local",
    "meaning": "지역의",
    "level": "MidHigh"
  },
  {
    "id": 1591,
    "word": "locate",
    "meaning": "위치를 찾다",
    "level": "MidHigh"
  },
  {
    "id": 1592,
    "word": "lock",
    "meaning": "잠그다",
    "level": "MidHigh"
  },
  {
    "id": 1593,
    "word": "log",
    "meaning": "통나무",
    "level": "MidHigh"
  },
  {
    "id": 1594,
    "word": "logic",
    "meaning": "논리",
    "level": "Extended"
  },
  {
    "id": 1595,
    "word": "lone",
    "meaning": "홀로 있는",
    "level": "Extended"
  },
  {
    "id": 1596,
    "word": "long",
    "meaning": "긴",
    "level": "Elementary"
  },
  {
    "id": 1597,
    "word": "look",
    "meaning": "보다",
    "level": "Elementary"
  },
  {
    "id": 1598,
    "word": "loose",
    "meaning": "느슨한",
    "level": "MidHigh"
  },
  {
    "id": 1599,
    "word": "lose",
    "meaning": "잃다",
    "level": "MidHigh"
  },
  {
    "id": 1600,
    "word": "loss",
    "meaning": "손실",
    "level": "MidHigh"
  },
  {
    "id": 1601,
    "word": "lot",
    "meaning": "많음",
    "level": "MidHigh"
  },
  {
    "id": 1602,
    "word": "loud",
    "meaning": "시끄러운",
    "level": "MidHigh"
  },
  {
    "id": 1603,
    "word": "love",
    "meaning": "사랑",
    "level": "Elementary"
  },
  {
    "id": 1604,
    "word": "low",
    "meaning": "낮은",
    "level": "Elementary"
  },
  {
    "id": 1605,
    "word": "loyal",
    "meaning": "충성스러운",
    "level": "Extended"
  },
  {
    "id": 1606,
    "word": "luck",
    "meaning": "운",
    "level": "Elementary"
  },
  {
    "id": 1607,
    "word": "lump",
    "meaning": "덩어리",
    "level": "Extended"
  },
  {
    "id": 1608,
    "word": "lunch",
    "meaning": "점심",
    "level": "Elementary"
  },
  {
    "id": 1609,
    "word": "luxury",
    "meaning": "사치",
    "level": "Extended"
  },
  {
    "id": 1610,
    "word": "machine",
    "meaning": "기계",
    "level": "MidHigh"
  },
  {
    "id": 1611,
    "word": "mad",
    "meaning": "화난",
    "level": "Elementary"
  },
  {
    "id": 1612,
    "word": "magazine",
    "meaning": "잡지",
    "level": "MidHigh"
  },
  {
    "id": 1613,
    "word": "magic",
    "meaning": "마술",
    "level": "MidHigh"
  },
  {
    "id": 1614,
    "word": "magnet",
    "meaning": "자석",
    "level": "Extended"
  },
  {
    "id": 1615,
    "word": "magnificent",
    "meaning": "장엄한",
    "level": "Extended"
  },
  {
    "id": 1616,
    "word": "mail",
    "meaning": "우편",
    "level": "Elementary"
  },
  {
    "id": 1617,
    "word": "main",
    "meaning": "주요한",
    "level": "MidHigh"
  },
  {
    "id": 1618,
    "word": "maintain",
    "meaning": "유지하다",
    "level": "MidHigh"
  },
  {
    "id": 1619,
    "word": "major",
    "meaning": "주요한",
    "level": "MidHigh",
    "variation": "majority"
  },
  {
    "id": 1620,
    "word": "make",
    "meaning": "만들다",
    "level": "Elementary"
  },
  {
    "id": 1621,
    "word": "male",
    "meaning": "남성",
    "level": "MidHigh"
  },
  {
    "id": 1622,
    "word": "man",
    "meaning": "남자",
    "level": "Elementary"
  },
  {
    "id": 1623,
    "word": "manage",
    "meaning": "관리하다",
    "level": "MidHigh"
  },
  {
    "id": 1624,
    "word": "manifest",
    "meaning": "명백하게 나타내다",
    "level": "Extended"
  },
  {
    "id": 1625,
    "word": "manipulate",
    "meaning": "조작하다",
    "level": "Extended"
  },
  {
    "id": 1626,
    "word": "manner",
    "meaning": "방식",
    "level": "MidHigh"
  },
  {
    "id": 1627,
    "word": "manufacture",
    "meaning": "제조하다",
    "level": "MidHigh"
  },
  {
    "id": 1628,
    "word": "many",
    "meaning": "많은",
    "level": "Elementary"
  },
  {
    "id": 1629,
    "word": "map",
    "meaning": "지도",
    "level": "Elementary"
  },
  {
    "id": 1630,
    "word": "marathon",
    "meaning": "마라톤",
    "level": "Elementary"
  },
  {
    "id": 1631,
    "word": "margin",
    "meaning": "여백",
    "level": "Extended"
  },
  {
    "id": 1632,
    "word": "marine",
    "meaning": "해양의",
    "level": "Extended"
  },
  {
    "id": 1633,
    "word": "mark",
    "meaning": "표시",
    "level": "MidHigh"
  },
  {
    "id": 1634,
    "word": "market",
    "meaning": "시장",
    "level": "Elementary"
  },
  {
    "id": 1635,
    "word": "marry",
    "meaning": "결혼하다",
    "level": "Elementary"
  },
  {
    "id": 1636,
    "word": "marvel",
    "meaning": "경이",
    "level": "MidHigh"
  },
  {
    "id": 1637,
    "word": "mask",
    "meaning": "가면",
    "level": "MidHigh"
  },
  {
    "id": 1638,
    "word": "mass",
    "meaning": "대량",
    "level": "MidHigh"
  },
  {
    "id": 1639,
    "word": "master",
    "meaning": "주인",
    "level": "MidHigh"
  },
  {
    "id": 1640,
    "word": "match",
    "meaning": "경기",
    "level": "MidHigh"
  },
  {
    "id": 1641,
    "word": "mate",
    "meaning": "동료",
    "level": "MidHigh"
  },
  {
    "id": 1642,
    "word": "mathematics",
    "meaning": "수학",
    "level": "Elementary",
    "variation": "maths, math"
  },
  {
    "id": 1643,
    "word": "matter",
    "meaning": "문제",
    "level": "MidHigh",
    "variation": "material"
  },
  {
    "id": 1644,
    "word": "mature",
    "meaning": "성숙한",
    "level": "Extended"
  },
  {
    "id": 1645,
    "word": "maximum",
    "meaning": "최대의",
    "level": "MidHigh"
  },
  {
    "id": 1646,
    "word": "may",
    "meaning": "~일지도 모른다",
    "level": "Elementary"
  },
  {
    "id": 1647,
    "word": "maybe",
    "meaning": "아마도",
    "level": "MidHigh"
  },
  {
    "id": 1648,
    "word": "mayor",
    "meaning": "시장",
    "level": "Extended"
  },
  {
    "id": 1649,
    "word": "meal",
    "meaning": "식사",
    "level": "MidHigh"
  },
  {
    "id": 1650,
    "word": "mean",
    "meaning": "의미하다",
    "level": "MidHigh"
  },
  {
    "id": 1651,
    "word": "meanwhile",
    "meaning": "그동안",
    "level": "Extended"
  },
  {
    "id": 1652,
    "word": "measure",
    "meaning": "측정하다",
    "level": "MidHigh"
  },
  {
    "id": 1653,
    "word": "meat",
    "meaning": "고기",
    "level": "Elementary"
  },
  {
    "id": 1654,
    "word": "mechanic",
    "meaning": "정비사",
    "level": "Extended"
  },
  {
    "id": 1655,
    "word": "mechanism",
    "meaning": "기제",
    "level": "Extended"
  },
  {
    "id": 1656,
    "word": "medal",
    "meaning": "메달",
    "level": "Elementary"
  },
  {
    "id": 1657,
    "word": "mediate",
    "meaning": "중재하다",
    "level": "Extended"
  },
  {
    "id": 1658,
    "word": "medical",
    "meaning": "의료의",
    "level": "MidHigh"
  },
  {
    "id": 1659,
    "word": "medicine",
    "meaning": "약",
    "level": "MidHigh"
  },
  {
    "id": 1660,
    "word": "medieval",
    "meaning": "중세의",
    "level": "Extended"
  },
  {
    "id": 1661,
    "word": "medium",
    "meaning": "매체",
    "level": "Extended",
    "variation": "media"
  },
  {
    "id": 1662,
    "word": "meet",
    "meaning": "만나다",
    "level": "Elementary"
  },
  {
    "id": 1663,
    "word": "melon",
    "meaning": "멜론",
    "level": "MidHigh"
  },
  {
    "id": 1664,
    "word": "melt",
    "meaning": "녹다",
    "level": "MidHigh"
  },
  {
    "id": 1665,
    "word": "member",
    "meaning": "구성원",
    "level": "Elementary",
    "variation": "membership"
  },
  {
    "id": 1666,
    "word": "memory",
    "meaning": "기억",
    "level": "Elementary"
  },
  {
    "id": 1667,
    "word": "mental",
    "meaning": "정신적인",
    "level": "MidHigh"
  },
  {
    "id": 1668,
    "word": "mention",
    "meaning": "언급하다",
    "level": "MidHigh"
  },
  {
    "id": 1669,
    "word": "menu",
    "meaning": "메뉴",
    "level": "MidHigh"
  },
  {
    "id": 1670,
    "word": "merchant",
    "meaning": "상인",
    "level": "Extended"
  },
  {
    "id": 1671,
    "word": "mere",
    "meaning": "단순한",
    "level": "Extended"
  },
  {
    "id": 1672,
    "word": "merge",
    "meaning": "합병하다",
    "level": "Extended"
  },
  {
    "id": 1673,
    "word": "merit",
    "meaning": "장점",
    "level": "Extended"
  },
  {
    "id": 1674,
    "word": "mess",
    "meaning": "혼란",
    "level": "MidHigh"
  },
  {
    "id": 1675,
    "word": "message",
    "meaning": "메시지",
    "level": "MidHigh"
  },
  {
    "id": 1676,
    "word": "metal",
    "meaning": "금속",
    "level": "MidHigh"
  },
  {
    "id": 1677,
    "word": "method",
    "meaning": "방법",
    "level": "MidHigh"
  },
  {
    "id": 1678,
    "word": "metropolitan",
    "meaning": "대도시의",
    "level": "Extended"
  },
  {
    "id": 1679,
    "word": "microphone",
    "meaning": "마이크",
    "level": "Extended"
  },
  {
    "id": 1680,
    "word": "microwave",
    "meaning": "전자레인지",
    "level": "MidHigh"
  },
  {
    "id": 1681,
    "word": "middle",
    "meaning": "중간",
    "level": "Elementary"
  },
  {
    "id": 1682,
    "word": "might",
    "meaning": "~할지도 모른다",
    "level": "Elementary"
  },
  {
    "id": 1683,
    "word": "migrate",
    "meaning": "이주하다",
    "level": "Extended",
    "variation": "migrant"
  },
  {
    "id": 1684,
    "word": "mild",
    "meaning": "온화한",
    "level": "Extended"
  },
  {
    "id": 1685,
    "word": "military",
    "meaning": "군대의",
    "level": "MidHigh"
  },
  {
    "id": 1686,
    "word": "milk",
    "meaning": "우유",
    "level": "Elementary"
  },
  {
    "id": 1687,
    "word": "mill",
    "meaning": "방앗간",
    "level": "MidHigh"
  },
  {
    "id": 1688,
    "word": "million",
    "meaning": "백만",
    "level": "Extended"
  },
  {
    "id": 1689,
    "word": "mind",
    "meaning": "마음",
    "level": "Elementary"
  },
  {
    "id": 1690,
    "word": "mine",
    "meaning": "광산",
    "level": "Extended",
    "variation": "miner"
  },
  {
    "id": 1691,
    "word": "mineral",
    "meaning": "광물",
    "level": "Extended"
  },
  {
    "id": 1692,
    "word": "minimal",
    "meaning": "최소의",
    "level": "Extended"
  },
  {
    "id": 1693,
    "word": "minimum",
    "meaning": "최소한",
    "level": "Extended"
  },
  {
    "id": 1694,
    "word": "ministry",
    "meaning": "부처",
    "level": "Extended"
  },
  {
    "id": 1695,
    "word": "minor",
    "meaning": "사소한",
    "level": "MidHigh"
  },
  {
    "id": 1696,
    "word": "minute",
    "meaning": "분",
    "level": "MidHigh"
  },
  {
    "id": 1697,
    "word": "miracle",
    "meaning": "기적",
    "level": "Extended"
  },
  {
    "id": 1698,
    "word": "mirror",
    "meaning": "거울",
    "level": "MidHigh"
  },
  {
    "id": 1699,
    "word": "miss",
    "meaning": "놓치다",
    "level": "Elementary"
  },
  {
    "id": 1700,
    "word": "missile",
    "meaning": "미사일",
    "level": "Extended"
  },
  {
    "id": 1701,
    "word": "mission",
    "meaning": "임무",
    "level": "MidHigh"
  },
  {
    "id": 1702,
    "word": "mix",
    "meaning": "섞다",
    "level": "MidHigh"
  },
  {
    "id": 1703,
    "word": "mobile",
    "meaning": "이동식의",
    "level": "Extended"
  },
  {
    "id": 1704,
    "word": "mock",
    "meaning": "흉내 내다",
    "level": "Extended"
  },
  {
    "id": 1705,
    "word": "mode",
    "meaning": "방식",
    "level": "Extended"
  },
  {
    "id": 1706,
    "word": "modify",
    "meaning": "수정하다",
    "level": "Extended"
  },
  {
    "id": 1707,
    "word": "model",
    "meaning": "모형",
    "level": "Elementary"
  },
  {
    "id": 1708,
    "word": "moderate",
    "meaning": "적당한",
    "level": "Extended"
  },
  {
    "id": 1709,
    "word": "modern",
    "meaning": "현대의",
    "level": "MidHigh"
  },
  {
    "id": 1710,
    "word": "modest",
    "meaning": "겸손한",
    "level": "Extended"
  },
  {
    "id": 1711,
    "word": "moist",
    "meaning": "축축한",
    "level": "Extended",
    "variation": "moisture"
  },
  {
    "id": 1712,
    "word": "molecule",
    "meaning": "분자",
    "level": "Extended"
  },
  {
    "id": 1713,
    "word": "moment",
    "meaning": "순간",
    "level": "MidHigh"
  },
  {
    "id": 1714,
    "word": "money",
    "meaning": "돈",
    "level": "Elementary"
  },
  {
    "id": 1715,
    "word": "monitor",
    "meaning": "감시하다",
    "level": "MidHigh"
  },
  {
    "id": 1716,
    "word": "monkey",
    "meaning": "원숭이",
    "level": "Elementary"
  },
  {
    "id": 1717,
    "word": "monster",
    "meaning": "괴물",
    "level": "Extended"
  },
  {
    "id": 1718,
    "word": "month",
    "meaning": "달",
    "level": "Elementary"
  },
  {
    "id": 1719,
    "word": "monument",
    "meaning": "기념물",
    "level": "Extended"
  },
  {
    "id": 1720,
    "word": "mood",
    "meaning": "기분",
    "level": "MidHigh"
  },
  {
    "id": 1721,
    "word": "moon",
    "meaning": "달",
    "level": "Elementary",
    "variation": "half-moon"
  },
  {
    "id": 1722,
    "word": "moral",
    "meaning": "도덕적인",
    "level": "MidHigh"
  },
  {
    "id": 1723,
    "word": "moreover",
    "meaning": "게다가",
    "level": "MidHigh"
  },
  {
    "id": 1724,
    "word": "morning",
    "meaning": "아침",
    "level": "Elementary"
  },
  {
    "id": 1725,
    "word": "mortal",
    "meaning": "죽을 운명의",
    "level": "Extended"
  },
  {
    "id": 1726,
    "word": "mother",
    "meaning": "어머니",
    "level": "Elementary",
    "variation": "mom, mommy"
  },
  {
    "id": 1727,
    "word": "motion",
    "meaning": "움직임",
    "level": "MidHigh"
  },
  {
    "id": 1728,
    "word": "motive",
    "meaning": "동기",
    "level": "Extended"
  },
  {
    "id": 1729,
    "word": "motor",
    "meaning": "모터",
    "level": "MidHigh"
  },
  {
    "id": 1730,
    "word": "mount",
    "meaning": "오르다",
    "level": "MidHigh"
  },
  {
    "id": 1731,
    "word": "mountain",
    "meaning": "산",
    "level": "Elementary"
  },
  {
    "id": 1732,
    "word": "mouse",
    "meaning": "쥐",
    "level": "Elementary"
  },
  {
    "id": 1733,
    "word": "mouth",
    "meaning": "입",
    "level": "Elementary"
  },
  {
    "id": 1734,
    "word": "move",
    "meaning": "움직이다",
    "level": "Elementary"
  },
  {
    "id": 1735,
    "word": "movie",
    "meaning": "영화",
    "level": "Elementary"
  },
  {
    "id": 1736,
    "word": "much",
    "meaning": "많은",
    "level": "Elementary"
  },
  {
    "id": 1737,
    "word": "mud",
    "meaning": "진흙",
    "level": "MidHigh"
  },
  {
    "id": 1738,
    "word": "multiple",
    "meaning": "다수의",
    "level": "Extended"
  },
  {
    "id": 1739,
    "word": "murder",
    "meaning": "살인",
    "level": "Extended"
  },
  {
    "id": 1740,
    "word": "muscle",
    "meaning": "근육",
    "level": "MidHigh"
  },
  {
    "id": 1741,
    "word": "museum",
    "meaning": "박물관",
    "level": "MidHigh"
  },
  {
    "id": 1742,
    "word": "mushroom",
    "meaning": "버섯",
    "level": "MidHigh"
  },
  {
    "id": 1743,
    "word": "music",
    "meaning": "음악",
    "level": "Elementary"
  },
  {
    "id": 1744,
    "word": "must",
    "meaning": "~해야 한다",
    "level": "Elementary"
  },
  {
    "id": 1745,
    "word": "mutual",
    "meaning": "상호의",
    "level": "Extended"
  },
  {
    "id": 1746,
    "word": "mystery",
    "meaning": "수수께끼",
    "level": "MidHigh"
  },
  {
    "id": 1747,
    "word": "myth",
    "meaning": "신화",
    "level": "Extended"
  },
  {
    "id": 1748,
    "word": "nail",
    "meaning": "손톱",
    "level": "MidHigh"
  },
  {
    "id": 1749,
    "word": "naive",
    "meaning": "순진한",
    "level": "Extended"
  },
  {
    "id": 1750,
    "word": "naked",
    "meaning": "벌거벗은",
    "level": "Extended"
  },
  {
    "id": 1751,
    "word": "name",
    "meaning": "이름",
    "level": "Elementary"
  },
  {
    "id": 1752,
    "word": "narrate",
    "meaning": "이야기하다",
    "level": "Extended"
  },
  {
    "id": 1753,
    "word": "narrow",
    "meaning": "좁은",
    "level": "MidHigh"
  },
  {
    "id": 1754,
    "word": "nasty",
    "meaning": "불쾌한",
    "level": "Extended"
  },
  {
    "id": 1755,
    "word": "nation",
    "meaning": "국가",
    "level": "Elementary",
    "variation": "international"
  },
  {
    "id": 1756,
    "word": "native",
    "meaning": "토박이의",
    "level": "MidHigh"
  },
  {
    "id": 1757,
    "word": "nature",
    "meaning": "자연",
    "level": "Elementary"
  },
  {
    "id": 1758,
    "word": "navy",
    "meaning": "해군",
    "level": "MidHigh"
  },
  {
    "id": 1759,
    "word": "near",
    "meaning": "가까운",
    "level": "Elementary"
  },
  {
    "id": 1760,
    "word": "neat",
    "meaning": "단정한",
    "level": "MidHigh"
  },
  {
    "id": 1761,
    "word": "necessary",
    "meaning": "필요한",
    "level": "MidHigh"
  },
  {
    "id": 1762,
    "word": "neck",
    "meaning": "목",
    "level": "Elementary"
  },
  {
    "id": 1763,
    "word": "need",
    "meaning": "필요하다",
    "level": "Elementary"
  },
  {
    "id": 1764,
    "word": "needle",
    "meaning": "바늘",
    "level": "Extended"
  },
  {
    "id": 1765,
    "word": "negate",
    "meaning": "부정하다",
    "level": "Extended",
    "variation": "negative"
  },
  {
    "id": 1766,
    "word": "neglect",
    "meaning": "소홀히 하다",
    "level": "Extended"
  },
  {
    "id": 1767,
    "word": "negotiate",
    "meaning": "협상하다",
    "level": "Extended"
  },
  {
    "id": 1768,
    "word": "neighbor",
    "meaning": "이웃",
    "level": "MidHigh",
    "variation": "neighbour"
  },
  {
    "id": 1769,
    "word": "neither",
    "meaning": "둘 다 아닌",
    "level": "MidHigh"
  },
  {
    "id": 1770,
    "word": "nephew",
    "meaning": "조카",
    "level": "Extended"
  },
  {
    "id": 1771,
    "word": "nerve",
    "meaning": "신경",
    "level": "MidHigh",
    "variation": "nervous"
  },
  {
    "id": 1772,
    "word": "nest",
    "meaning": "둥지",
    "level": "MidHigh"
  },
  {
    "id": 1773,
    "word": "net",
    "meaning": "그물",
    "level": "MidHigh"
  },
  {
    "id": 1774,
    "word": "network",
    "meaning": "네트워크",
    "level": "Extended"
  },
  {
    "id": 1775,
    "word": "neutral",
    "meaning": "중립적인",
    "level": "Extended"
  },
  {
    "id": 1776,
    "word": "never",
    "meaning": "결코",
    "level": "Elementary"
  },
  {
    "id": 1777,
    "word": "nevertheless",
    "meaning": "그럼에도 불구하고",
    "level": "Extended"
  },
  {
    "id": 1778,
    "word": "new",
    "meaning": "새로운",
    "level": "Elementary"
  },
  {
    "id": 1779,
    "word": "news",
    "meaning": "뉴스",
    "level": "Elementary"
  },
  {
    "id": 1780,
    "word": "newspaper",
    "meaning": "신문",
    "level": "Elementary"
  },
  {
    "id": 1781,
    "word": "next",
    "meaning": "다음의",
    "level": "Elementary"
  },
  {
    "id": 1782,
    "word": "nice",
    "meaning": "좋은",
    "level": "Elementary"
  },
  {
    "id": 1783,
    "word": "night",
    "meaning": "밤",
    "level": "Elementary"
  },
  {
    "id": 1784,
    "word": "nightmare",
    "meaning": "악몽",
    "level": "Extended"
  },
  {
    "id": 1785,
    "word": "nine",
    "meaning": "아홉",
    "level": "Elementary"
  },
  {
    "id": 1786,
    "word": "no",
    "meaning": "아니",
    "level": "Elementary",
    "variation": "nope, nay"
  },
  {
    "id": 1787,
    "word": "noble",
    "meaning": "고귀한",
    "level": "Extended"
  },
  {
    "id": 1788,
    "word": "nod",
    "meaning": "끄덕이다",
    "level": "Extended"
  },
  {
    "id": 1789,
    "word": "noise",
    "meaning": "소음",
    "level": "MidHigh"
  },
  {
    "id": 1790,
    "word": "nominate",
    "meaning": "지명하다",
    "level": "Extended"
  },
  {
    "id": 1791,
    "word": "none",
    "meaning": "아무것도 없는",
    "level": "MidHigh"
  },
  {
    "id": 1792,
    "word": "nonetheless",
    "meaning": "그렇지만",
    "level": "Extended"
  },
  {
    "id": 1793,
    "word": "noon",
    "meaning": "정오",
    "level": "MidHigh"
  },
  {
    "id": 1794,
    "word": "nor",
    "meaning": "~도 아니다",
    "level": "MidHigh"
  },
  {
    "id": 1795,
    "word": "norm",
    "meaning": "규범",
    "level": "Extended",
    "variation": "normal"
  },
  {
    "id": 1796,
    "word": "north",
    "meaning": "북쪽",
    "level": "Elementary"
  },
  {
    "id": 1797,
    "word": "nose",
    "meaning": "코",
    "level": "Elementary"
  },
  {
    "id": 1798,
    "word": "not",
    "meaning": "~않다",
    "level": "Elementary"
  },
  {
    "id": 1799,
    "word": "note",
    "meaning": "메모",
    "level": "Elementary",
    "variation": "notion"
  },
  {
    "id": 1800,
    "word": "notebook",
    "meaning": "공책",
    "level": "Elementary"
  },
  {
    "id": 1801,
    "word": "nothing",
    "meaning": "아무것도",
    "level": "Elementary"
  },
  {
    "id": 1802,
    "word": "notice",
    "meaning": "알아채다",
    "level": "MidHigh"
  },
  {
    "id": 1803,
    "word": "novel",
    "meaning": "소설",
    "level": "Extended"
  },
  {
    "id": 1804,
    "word": "now",
    "meaning": "지금",
    "level": "Elementary"
  },
  {
    "id": 1805,
    "word": "nowadays",
    "meaning": "요즘",
    "level": "MidHigh"
  },
  {
    "id": 1806,
    "word": "nowhere",
    "meaning": "아무 데도",
    "level": "MidHigh"
  },
  {
    "id": 1807,
    "word": "nuclear",
    "meaning": "핵의",
    "level": "Extended"
  },
  {
    "id": 1808,
    "word": "number",
    "meaning": "숫자",
    "level": "Elementary"
  },
  {
    "id": 1809,
    "word": "numerous",
    "meaning": "수많은",
    "level": "Extended"
  },
  {
    "id": 1810,
    "word": "nurse",
    "meaning": "간호사",
    "level": "Elementary"
  },
  {
    "id": 1811,
    "word": "nut",
    "meaning": "견과",
    "level": "MidHigh"
  },
  {
    "id": 1812,
    "word": "oak",
    "meaning": "참나무",
    "level": "MidHigh"
  },
  {
    "id": 1813,
    "word": "obey",
    "meaning": "복종하다",
    "level": "Extended"
  },
  {
    "id": 1814,
    "word": "object",
    "meaning": "물체",
    "level": "MidHigh",
    "variation": "objective"
  },
  {
    "id": 1815,
    "word": "oblige",
    "meaning": "의무를 지우다",
    "level": "Extended"
  },
  {
    "id": 1816,
    "word": "observe",
    "meaning": "관찰하다",
    "level": "MidHigh"
  },
  {
    "id": 1817,
    "word": "obsess",
    "meaning": "집착하다",
    "level": "Extended"
  },
  {
    "id": 1818,
    "word": "obtain",
    "meaning": "획득하다",
    "level": "Extended"
  },
  {
    "id": 1819,
    "word": "obvious",
    "meaning": "명백한",
    "level": "MidHigh"
  },
  {
    "id": 1820,
    "word": "occasion",
    "meaning": "경우",
    "level": "MidHigh"
  },
  {
    "id": 1821,
    "word": "occupy",
    "meaning": "차지하다",
    "level": "Extended",
    "variation": "occupation"
  },
  {
    "id": 1822,
    "word": "occur",
    "meaning": "발생하다",
    "level": "MidHigh",
    "variation": "occurrence"
  },
  {
    "id": 1823,
    "word": "ocean",
    "meaning": "대양",
    "level": "MidHigh"
  },
  {
    "id": 1824,
    "word": "odd",
    "meaning": "이상한",
    "level": "MidHigh"
  },
  {
    "id": 1825,
    "word": "of",
    "meaning": "~의",
    "level": "Elementary"
  },
  {
    "id": 1826,
    "word": "off",
    "meaning": "떨어져",
    "level": "Elementary"
  },
  {
    "id": 1827,
    "word": "offend",
    "meaning": "기분을 상하게 하다",
    "level": "Extended"
  },
  {
    "id": 1828,
    "word": "offer",
    "meaning": "제안하다",
    "level": "MidHigh"
  },
  {
    "id": 1829,
    "word": "office",
    "meaning": "사무실",
    "level": "Elementary",
    "variation": "official"
  },
  {
    "id": 1830,
    "word": "officer",
    "meaning": "직원",
    "level": "MidHigh"
  },
  {
    "id": 1831,
    "word": "often",
    "meaning": "자주",
    "level": "Elementary"
  },
  {
    "id": 1832,
    "word": "oil",
    "meaning": "기름",
    "level": "Elementary"
  },
  {
    "id": 1833,
    "word": "okay",
    "meaning": "괜찮은",
    "level": "Elementary",
    "variation": "okey, OK"
  },
  {
    "id": 1834,
    "word": "old",
    "meaning": "오래된",
    "level": "Elementary"
  },
  {
    "id": 1835,
    "word": "on",
    "meaning": "~위에",
    "level": "Elementary"
  },
  {
    "id": 1836,
    "word": "once",
    "meaning": "한 번",
    "level": "MidHigh"
  },
  {
    "id": 1837,
    "word": "one",
    "meaning": "하나",
    "level": "Elementary"
  },
  {
    "id": 1838,
    "word": "only",
    "meaning": "오직",
    "level": "Elementary"
  },
  {
    "id": 1839,
    "word": "open",
    "meaning": "열다",
    "level": "Elementary"
  },
  {
    "id": 1840,
    "word": "opera",
    "meaning": "오페라",
    "level": "MidHigh"
  },
  {
    "id": 1841,
    "word": "operate",
    "meaning": "작동하다",
    "level": "MidHigh"
  },
  {
    "id": 1842,
    "word": "opinion",
    "meaning": "의견",
    "level": "MidHigh"
  },
  {
    "id": 1843,
    "word": "opportune",
    "meaning": "시기적절한",
    "level": "Extended",
    "variation": "opportunity"
  },
  {
    "id": 1844,
    "word": "oppose",
    "meaning": "반대하다",
    "level": "MidHigh"
  },
  {
    "id": 1845,
    "word": "opt",
    "meaning": "선택하다",
    "level": "Extended",
    "variation": "option"
  },
  {
    "id": 1846,
    "word": "optimist",
    "meaning": "낙관주의자",
    "level": "Extended"
  },
  {
    "id": 1847,
    "word": "or",
    "meaning": "또는",
    "level": "Elementary"
  },
  {
    "id": 1848,
    "word": "oral",
    "meaning": "구술의",
    "level": "Extended"
  },
  {
    "id": 1849,
    "word": "orange",
    "meaning": "오렌지",
    "level": "Elementary"
  },
  {
    "id": 1850,
    "word": "orbit",
    "meaning": "궤도",
    "level": "Extended"
  },
  {
    "id": 1851,
    "word": "orchestra",
    "meaning": "관현악단",
    "level": "Extended"
  },
  {
    "id": 1852,
    "word": "order",
    "meaning": "명령",
    "level": "MidHigh",
    "variation": "disorder"
  },
  {
    "id": 1853,
    "word": "ordinary",
    "meaning": "보통의",
    "level": "MidHigh"
  },
  {
    "id": 1854,
    "word": "organ",
    "meaning": "기관",
    "level": "Extended",
    "variation": "organic, organize, organise"
  },
  {
    "id": 1855,
    "word": "orient",
    "meaning": "방향을 정하다",
    "level": "Extended",
    "variation": "orientation"
  },
  {
    "id": 1856,
    "word": "origin",
    "meaning": "기원",
    "level": "Extended",
    "variation": "original"
  },
  {
    "id": 1857,
    "word": "other",
    "meaning": "다른",
    "level": "MidHigh"
  },
  {
    "id": 1858,
    "word": "otherwise",
    "meaning": "그렇지 않으면",
    "level": "MidHigh"
  },
  {
    "id": 1859,
    "word": "ought",
    "meaning": "~해야 한다",
    "level": "MidHigh"
  },
  {
    "id": 1860,
    "word": "out",
    "meaning": "밖으로",
    "level": "Elementary"
  },
  {
    "id": 1861,
    "word": "outcome",
    "meaning": "결과",
    "level": "Extended"
  },
  {
    "id": 1862,
    "word": "outline",
    "meaning": "개요",
    "level": "Extended"
  },
  {
    "id": 1863,
    "word": "output",
    "meaning": "출력",
    "level": "Extended"
  },
  {
    "id": 1864,
    "word": "outrage",
    "meaning": "격분",
    "level": "Extended"
  },
  {
    "id": 1865,
    "word": "outstanding",
    "meaning": "뛰어난",
    "level": "Extended"
  },
  {
    "id": 1866,
    "word": "oven",
    "meaning": "오븐",
    "level": "MidHigh"
  },
  {
    "id": 1867,
    "word": "over",
    "meaning": "~너머로",
    "level": "Elementary"
  },
  {
    "id": 1868,
    "word": "overall",
    "meaning": "전체의",
    "level": "MidHigh"
  },
  {
    "id": 1869,
    "word": "overcome",
    "meaning": "극복하다",
    "level": "Extended"
  },
  {
    "id": 1870,
    "word": "overhead",
    "meaning": "머리 위의",
    "level": "Extended"
  },
  {
    "id": 1871,
    "word": "overlap",
    "meaning": "겹치다",
    "level": "Extended"
  },
  {
    "id": 1872,
    "word": "overlook",
    "meaning": "간과하다",
    "level": "Extended"
  },
  {
    "id": 1873,
    "word": "overnight",
    "meaning": "밤사이에",
    "level": "Extended"
  },
  {
    "id": 1874,
    "word": "oversea",
    "meaning": "해외의",
    "level": "Extended",
    "variation": "overseas"
  },
  {
    "id": 1875,
    "word": "overwhelm",
    "meaning": "압도하다",
    "level": "Extended"
  },
  {
    "id": 1876,
    "word": "owe",
    "meaning": "빚지다",
    "level": "Extended"
  },
  {
    "id": 1877,
    "word": "own",
    "meaning": "소유하다",
    "level": "MidHigh"
  },
  {
    "id": 1878,
    "word": "pace",
    "meaning": "속도",
    "level": "Extended"
  },
  {
    "id": 1879,
    "word": "pack",
    "meaning": "꾸러미",
    "level": "MidHigh"
  },
  {
    "id": 1880,
    "word": "pad",
    "meaning": "받침",
    "level": "Extended"
  },
  {
    "id": 1881,
    "word": "page",
    "meaning": "쪽",
    "level": "Elementary"
  },
  {
    "id": 1882,
    "word": "pain",
    "meaning": "고통",
    "level": "MidHigh"
  },
  {
    "id": 1883,
    "word": "paint",
    "meaning": "칠하다",
    "level": "Elementary"
  },
  {
    "id": 1884,
    "word": "pair",
    "meaning": "한 쌍",
    "level": "MidHigh"
  },
  {
    "id": 1885,
    "word": "palace",
    "meaning": "궁전",
    "level": "MidHigh"
  },
  {
    "id": 1886,
    "word": "pale",
    "meaning": "창백한",
    "level": "Extended"
  },
  {
    "id": 1887,
    "word": "palm",
    "meaning": "손바닥",
    "level": "Extended"
  },
  {
    "id": 1888,
    "word": "pan",
    "meaning": "팬",
    "level": "MidHigh"
  },
  {
    "id": 1889,
    "word": "panel",
    "meaning": "위원단",
    "level": "Extended"
  },
  {
    "id": 1890,
    "word": "panic",
    "meaning": "공황",
    "level": "MidHigh"
  },
  {
    "id": 1891,
    "word": "pants",
    "meaning": "바지",
    "level": "Elementary"
  },
  {
    "id": 1892,
    "word": "paper",
    "meaning": "종이",
    "level": "Elementary"
  },
  {
    "id": 1893,
    "word": "parade",
    "meaning": "행진",
    "level": "MidHigh"
  },
  {
    "id": 1894,
    "word": "paragraph",
    "meaning": "문단",
    "level": "MidHigh"
  },
  {
    "id": 1895,
    "word": "parallel",
    "meaning": "평행한",
    "level": "Extended"
  },
  {
    "id": 1896,
    "word": "pardon",
    "meaning": "용서하다",
    "level": "MidHigh"
  },
  {
    "id": 1897,
    "word": "parent",
    "meaning": "부모",
    "level": "Elementary"
  },
  {
    "id": 1898,
    "word": "park",
    "meaning": "공원",
    "level": "Elementary"
  },
  {
    "id": 1899,
    "word": "parliament",
    "meaning": "의회",
    "level": "Extended"
  },
  {
    "id": 1900,
    "word": "part",
    "meaning": "부분",
    "level": "Elementary"
  },
  {
    "id": 1901,
    "word": "participate",
    "meaning": "참가하다",
    "level": "Extended"
  },
  {
    "id": 1902,
    "word": "particle",
    "meaning": "입자",
    "level": "Extended"
  },
  {
    "id": 1903,
    "word": "particular",
    "meaning": "특정한",
    "level": "MidHigh",
    "variation": "particularly"
  },
  {
    "id": 1904,
    "word": "partner",
    "meaning": "동반자",
    "level": "Elementary"
  },
  {
    "id": 1905,
    "word": "party",
    "meaning": "파티",
    "level": "Elementary"
  },
  {
    "id": 1906,
    "word": "pass",
    "meaning": "통과하다",
    "level": "Elementary"
  },
  {
    "id": 1907,
    "word": "passage",
    "meaning": "통로",
    "level": "Extended"
  },
  {
    "id": 1908,
    "word": "passenger",
    "meaning": "승객",
    "level": "Extended"
  },
  {
    "id": 1909,
    "word": "passion",
    "meaning": "열정",
    "level": "Extended"
  },
  {
    "id": 1910,
    "word": "passport",
    "meaning": "여권",
    "level": "Extended"
  },
  {
    "id": 1911,
    "word": "past",
    "meaning": "과거",
    "level": "MidHigh"
  },
  {
    "id": 1912,
    "word": "pat",
    "meaning": "가볍게 두드리다",
    "level": "Extended"
  },
  {
    "id": 1913,
    "word": "patch",
    "meaning": "헝겊 조각",
    "level": "Extended"
  },
  {
    "id": 1914,
    "word": "patent",
    "meaning": "특허",
    "level": "Extended"
  },
  {
    "id": 1915,
    "word": "path",
    "meaning": "길",
    "level": "MidHigh"
  },
  {
    "id": 1916,
    "word": "patient",
    "meaning": "참을성 있는",
    "level": "MidHigh"
  },
  {
    "id": 1917,
    "word": "pattern",
    "meaning": "무늬",
    "level": "MidHigh"
  },
  {
    "id": 1918,
    "word": "pause",
    "meaning": "잠시 멈춤",
    "level": "MidHigh"
  },
  {
    "id": 1919,
    "word": "pave",
    "meaning": "포장하다",
    "level": "Extended"
  },
  {
    "id": 1920,
    "word": "pay",
    "meaning": "지불하다",
    "level": "Elementary"
  },
  {
    "id": 1921,
    "word": "peace",
    "meaning": "평화",
    "level": "MidHigh",
    "variation": "peaceful"
  },
  {
    "id": 1922,
    "word": "peak",
    "meaning": "정상",
    "level": "Extended"
  },
  {
    "id": 1923,
    "word": "pear",
    "meaning": "배",
    "level": "MidHigh"
  },
  {
    "id": 1924,
    "word": "peasant",
    "meaning": "농민",
    "level": "Extended"
  },
  {
    "id": 1925,
    "word": "peel",
    "meaning": "껍질을 벗기다",
    "level": "Extended"
  },
  {
    "id": 1926,
    "word": "peer",
    "meaning": "동료",
    "level": "Extended"
  },
  {
    "id": 1927,
    "word": "pen",
    "meaning": "펜",
    "level": "Elementary"
  },
  {
    "id": 1928,
    "word": "penalty",
    "meaning": "벌칙",
    "level": "Extended"
  },
  {
    "id": 1929,
    "word": "pencil",
    "meaning": "연필",
    "level": "Elementary"
  },
  {
    "id": 1930,
    "word": "people",
    "meaning": "사람들",
    "level": "Elementary"
  },
  {
    "id": 1931,
    "word": "pepper",
    "meaning": "후추",
    "level": "MidHigh"
  },
  {
    "id": 1932,
    "word": "per",
    "meaning": "~마다",
    "level": "MidHigh"
  },
  {
    "id": 1933,
    "word": "perceive",
    "meaning": "인식하다",
    "level": "Extended",
    "variation": "perception"
  },
  {
    "id": 1934,
    "word": "perfect",
    "meaning": "완벽한",
    "level": "MidHigh"
  },
  {
    "id": 1935,
    "word": "perform",
    "meaning": "수행하다",
    "level": "MidHigh"
  },
  {
    "id": 1936,
    "word": "perhaps",
    "meaning": "아마도",
    "level": "MidHigh"
  },
  {
    "id": 1937,
    "word": "period",
    "meaning": "기간",
    "level": "MidHigh"
  },
  {
    "id": 1938,
    "word": "permanent",
    "meaning": "영구적인",
    "level": "Extended"
  },
  {
    "id": 1939,
    "word": "permit",
    "meaning": "허가하다",
    "level": "Extended"
  },
  {
    "id": 1940,
    "word": "persist",
    "meaning": "지속하다",
    "level": "Extended"
  },
  {
    "id": 1941,
    "word": "person",
    "meaning": "사람",
    "level": "MidHigh",
    "variation": "personality"
  },
  {
    "id": 1942,
    "word": "perspective",
    "meaning": "관점",
    "level": "Extended"
  },
  {
    "id": 1943,
    "word": "persuade",
    "meaning": "설득하다",
    "level": "Extended"
  },
  {
    "id": 1944,
    "word": "pet",
    "meaning": "애완동물",
    "level": "MidHigh"
  },
  {
    "id": 1945,
    "word": "phase",
    "meaning": "단계",
    "level": "Extended"
  },
  {
    "id": 1946,
    "word": "phenomenon",
    "meaning": "현상",
    "level": "Extended"
  },
  {
    "id": 1947,
    "word": "philosophy",
    "meaning": "철학",
    "level": "Extended"
  },
  {
    "id": 1948,
    "word": "photograph",
    "meaning": "사진",
    "level": "MidHigh",
    "variation": "photo"
  },
  {
    "id": 1949,
    "word": "phrase",
    "meaning": "구",
    "level": "Extended"
  },
  {
    "id": 1950,
    "word": "physical",
    "meaning": "신체적인",
    "level": "MidHigh"
  },
  {
    "id": 1951,
    "word": "physics",
    "meaning": "물리학",
    "level": "Extended"
  },
  {
    "id": 1952,
    "word": "piano",
    "meaning": "피아노",
    "level": "Elementary"
  },
  {
    "id": 1953,
    "word": "pick",
    "meaning": "고르다",
    "level": "Elementary"
  },
  {
    "id": 1954,
    "word": "picnic",
    "meaning": "소풍",
    "level": "MidHigh"
  },
  {
    "id": 1955,
    "word": "picture",
    "meaning": "그림",
    "level": "Elementary"
  },
  {
    "id": 1956,
    "word": "pie",
    "meaning": "파이",
    "level": "MidHigh"
  },
  {
    "id": 1957,
    "word": "piece",
    "meaning": "조각",
    "level": "MidHigh"
  },
  {
    "id": 1958,
    "word": "pig",
    "meaning": "돼지",
    "level": "Elementary"
  },
  {
    "id": 1959,
    "word": "pile",
    "meaning": "더미",
    "level": "MidHigh"
  },
  {
    "id": 1960,
    "word": "pill",
    "meaning": "알약",
    "level": "Extended"
  },
  {
    "id": 1961,
    "word": "pilot",
    "meaning": "조종사",
    "level": "Elementary"
  },
  {
    "id": 1962,
    "word": "pin",
    "meaning": "핀",
    "level": "MidHigh"
  },
  {
    "id": 1963,
    "word": "pinch",
    "meaning": "꼬집다",
    "level": "Extended"
  },
  {
    "id": 1964,
    "word": "pine",
    "meaning": "소나무",
    "level": "MidHigh"
  },
  {
    "id": 1965,
    "word": "pink",
    "meaning": "분홍색",
    "level": "Elementary"
  },
  {
    "id": 1966,
    "word": "pioneer",
    "meaning": "선구자",
    "level": "Extended"
  },
  {
    "id": 1967,
    "word": "pipe",
    "meaning": "파이프",
    "level": "MidHigh"
  },
  {
    "id": 1968,
    "word": "pitch",
    "meaning": "던지다",
    "level": "MidHigh"
  },
  {
    "id": 1969,
    "word": "pity",
    "meaning": "연민",
    "level": "MidHigh"
  },
  {
    "id": 1970,
    "word": "pizza",
    "meaning": "피자",
    "level": "Elementary"
  },
  {
    "id": 1971,
    "word": "place",
    "meaning": "장소",
    "level": "Elementary",
    "variation": "displace"
  },
  {
    "id": 1972,
    "word": "plain",
    "meaning": "평범한",
    "level": "MidHigh"
  },
  {
    "id": 1973,
    "word": "plan",
    "meaning": "계획",
    "level": "Elementary"
  },
  {
    "id": 1974,
    "word": "plane",
    "meaning": "비행기",
    "level": "MidHigh"
  },
  {
    "id": 1975,
    "word": "planet",
    "meaning": "행성",
    "level": "MidHigh"
  },
  {
    "id": 1976,
    "word": "plant",
    "meaning": "식물",
    "level": "MidHigh"
  },
  {
    "id": 1977,
    "word": "plastic",
    "meaning": "플라스틱",
    "level": "Elementary"
  },
  {
    "id": 1978,
    "word": "plate",
    "meaning": "접시",
    "level": "MidHigh"
  },
  {
    "id": 1979,
    "word": "platform",
    "meaning": "승강장",
    "level": "Extended"
  },
  {
    "id": 1980,
    "word": "play",
    "meaning": "놀다",
    "level": "Elementary"
  },
  {
    "id": 1981,
    "word": "please",
    "meaning": "기쁘게 하다",
    "level": "Elementary",
    "variation": "pleasant, pleasure"
  },
  {
    "id": 1982,
    "word": "plenty",
    "meaning": "풍부함",
    "level": "MidHigh"
  },
  {
    "id": 1983,
    "word": "plot",
    "meaning": "줄거리",
    "level": "Extended"
  },
  {
    "id": 1984,
    "word": "plus",
    "meaning": "더하기",
    "level": "MidHigh"
  },
  {
    "id": 1985,
    "word": "pocket",
    "meaning": "주머니",
    "level": "MidHigh"
  },
  {
    "id": 1986,
    "word": "poem",
    "meaning": "시",
    "level": "MidHigh"
  },
  {
    "id": 1987,
    "word": "poet",
    "meaning": "시인",
    "level": "MidHigh"
  },
  {
    "id": 1988,
    "word": "point",
    "meaning": "지점",
    "level": "Elementary"
  },
  {
    "id": 1989,
    "word": "poison",
    "meaning": "독",
    "level": "MidHigh"
  },
  {
    "id": 1990,
    "word": "pole",
    "meaning": "막대",
    "level": "MidHigh",
    "variation": "polar"
  },
  {
    "id": 1991,
    "word": "police",
    "meaning": "경찰",
    "level": "Elementary"
  },
  {
    "id": 1992,
    "word": "policy",
    "meaning": "정책",
    "level": "MidHigh"
  },
  {
    "id": 1993,
    "word": "polish",
    "meaning": "닦다",
    "level": "Extended"
  },
  {
    "id": 1994,
    "word": "polite",
    "meaning": "예의 바른",
    "level": "MidHigh"
  },
  {
    "id": 1995,
    "word": "politics",
    "meaning": "정치",
    "level": "MidHigh"
  },
  {
    "id": 1996,
    "word": "poll",
    "meaning": "여론 조사",
    "level": "Extended"
  },
  {
    "id": 1997,
    "word": "pollute",
    "meaning": "오염시키다",
    "level": "MidHigh"
  },
  {
    "id": 1998,
    "word": "pond",
    "meaning": "연못",
    "level": "Extended"
  },
  {
    "id": 1999,
    "word": "pool",
    "meaning": "수영장",
    "level": "MidHigh"
  },
  {
    "id": 2000,
    "word": "poor",
    "meaning": "가난한",
    "level": "Elementary"
  },
  {
    "id": 2001,
    "word": "pop",
    "meaning": "펑 하는 소리",
    "level": "MidHigh"
  },
  {
    "id": 2002,
    "word": "popular",
    "meaning": "인기 있는",
    "level": "MidHigh"
  },
  {
    "id": 2003,
    "word": "populate",
    "meaning": "거주시키다",
    "level": "Extended",
    "variation": "population"
  },
  {
    "id": 2004,
    "word": "pork",
    "meaning": "돼지고기",
    "level": "MidHigh"
  },
  {
    "id": 2005,
    "word": "port",
    "meaning": "항구",
    "level": "MidHigh"
  },
  {
    "id": 2006,
    "word": "portion",
    "meaning": "부분",
    "level": "Extended"
  },
  {
    "id": 2007,
    "word": "portrait",
    "meaning": "초상화",
    "level": "Extended"
  },
  {
    "id": 2008,
    "word": "pose",
    "meaning": "자세를 취하다",
    "level": "Extended",
    "variation": "dispose"
  },
  {
    "id": 2009,
    "word": "posit",
    "meaning": "위치시키다",
    "level": "Extended",
    "variation": "position, positive"
  },
  {
    "id": 2010,
    "word": "possess",
    "meaning": "소유하다",
    "level": "MidHigh"
  },
  {
    "id": 2011,
    "word": "possible",
    "meaning": "가능한",
    "level": "MidHigh"
  },
  {
    "id": 2012,
    "word": "post",
    "meaning": "우편",
    "level": "MidHigh",
    "variation": "poster"
  },
  {
    "id": 2013,
    "word": "pot",
    "meaning": "냄비",
    "level": "MidHigh"
  },
  {
    "id": 2014,
    "word": "potato",
    "meaning": "감자",
    "level": "Elementary"
  },
  {
    "id": 2015,
    "word": "potential",
    "meaning": "잠재적인",
    "level": "MidHigh"
  },
  {
    "id": 2016,
    "word": "pour",
    "meaning": "붓다",
    "level": "MidHigh"
  },
  {
    "id": 2017,
    "word": "powder",
    "meaning": "가루",
    "level": "MidHigh"
  },
  {
    "id": 2018,
    "word": "power",
    "meaning": "힘",
    "level": "Elementary"
  },
  {
    "id": 2019,
    "word": "practical",
    "meaning": "실용적인",
    "level": "MidHigh"
  },
  {
    "id": 2020,
    "word": "practice",
    "meaning": "연습하다",
    "level": "MidHigh",
    "variation": "practise"
  },
  {
    "id": 2021,
    "word": "praise",
    "meaning": "칭찬하다",
    "level": "Extended"
  },
  {
    "id": 2022,
    "word": "pray",
    "meaning": "기도하다",
    "level": "MidHigh"
  },
  {
    "id": 2023,
    "word": "preach",
    "meaning": "설교하다",
    "level": "Extended"
  },
  {
    "id": 2024,
    "word": "precede",
    "meaning": "앞서다",
    "level": "Extended",
    "variation": "unprecedented"
  },
  {
    "id": 2025,
    "word": "precise",
    "meaning": "정확한",
    "level": "Extended"
  },
  {
    "id": 2026,
    "word": "predator",
    "meaning": "포식자",
    "level": "Extended"
  },
  {
    "id": 2027,
    "word": "predict",
    "meaning": "예측하다",
    "level": "Extended"
  },
  {
    "id": 2028,
    "word": "prefer",
    "meaning": "선호하다",
    "level": "MidHigh"
  },
  {
    "id": 2029,
    "word": "pregnant",
    "meaning": "임신한",
    "level": "MidHigh"
  },
  {
    "id": 2030,
    "word": "prejudice",
    "meaning": "편견",
    "level": "Extended"
  },
  {
    "id": 2031,
    "word": "premium",
    "meaning": "할증금",
    "level": "Extended"
  },
  {
    "id": 2032,
    "word": "prepare",
    "meaning": "준비하다",
    "level": "MidHigh"
  },
  {
    "id": 2033,
    "word": "prescribe",
    "meaning": "처방하다",
    "level": "Extended"
  },
  {
    "id": 2034,
    "word": "presence",
    "meaning": "존재",
    "level": "MidHigh"
  },
  {
    "id": 2035,
    "word": "present",
    "meaning": "현재의",
    "level": "Elementary"
  },
  {
    "id": 2036,
    "word": "preserve",
    "meaning": "보존하다",
    "level": "Extended"
  },
  {
    "id": 2037,
    "word": "preside",
    "meaning": "주재하다",
    "level": "Extended",
    "variation": "president"
  },
  {
    "id": 2038,
    "word": "press",
    "meaning": "누르다",
    "level": "MidHigh"
  },
  {
    "id": 2039,
    "word": "presume",
    "meaning": "추정하다",
    "level": "Extended"
  },
  {
    "id": 2040,
    "word": "pretend",
    "meaning": "~인 척하다",
    "level": "MidHigh"
  },
  {
    "id": 2041,
    "word": "pretty",
    "meaning": "예쁜",
    "level": "Elementary"
  },
  {
    "id": 2042,
    "word": "prevail",
    "meaning": "우세하다",
    "level": "Extended"
  },
  {
    "id": 2043,
    "word": "prevent",
    "meaning": "막다",
    "level": "MidHigh"
  },
  {
    "id": 2044,
    "word": "previous",
    "meaning": "이전의",
    "level": "MidHigh"
  },
  {
    "id": 2045,
    "word": "prey",
    "meaning": "먹이",
    "level": "Extended"
  },
  {
    "id": 2046,
    "word": "price",
    "meaning": "가격",
    "level": "MidHigh"
  },
  {
    "id": 2047,
    "word": "pride",
    "meaning": "자부심",
    "level": "MidHigh"
  },
  {
    "id": 2048,
    "word": "priest",
    "meaning": "성직자",
    "level": "Extended"
  },
  {
    "id": 2049,
    "word": "prime",
    "meaning": "주요한",
    "level": "MidHigh",
    "variation": "primary"
  },
  {
    "id": 2050,
    "word": "primitive",
    "meaning": "원시적인",
    "level": "Extended"
  },
  {
    "id": 2051,
    "word": "prince",
    "meaning": "왕자",
    "level": "Elementary"
  },
  {
    "id": 2052,
    "word": "principal",
    "meaning": "교장",
    "level": "Extended"
  },
  {
    "id": 2053,
    "word": "principle",
    "meaning": "원칙",
    "level": "MidHigh"
  },
  {
    "id": 2054,
    "word": "print",
    "meaning": "인쇄하다",
    "level": "Elementary"
  },
  {
    "id": 2055,
    "word": "prior",
    "meaning": "이전의",
    "level": "Extended"
  },
  {
    "id": 2056,
    "word": "prison",
    "meaning": "감옥",
    "level": "MidHigh"
  },
  {
    "id": 2057,
    "word": "privacy",
    "meaning": "사생활",
    "level": "MidHigh"
  },
  {
    "id": 2058,
    "word": "private",
    "meaning": "사적인",
    "level": "MidHigh"
  },
  {
    "id": 2059,
    "word": "privilege",
    "meaning": "특권",
    "level": "Extended"
  },
  {
    "id": 2060,
    "word": "prize",
    "meaning": "상",
    "level": "MidHigh"
  },
  {
    "id": 2061,
    "word": "probable",
    "meaning": "있을 법한",
    "level": "MidHigh",
    "variation": "probably"
  },
  {
    "id": 2062,
    "word": "problem",
    "meaning": "문제",
    "level": "Elementary"
  },
  {
    "id": 2063,
    "word": "proceed",
    "meaning": "진행하다",
    "level": "MidHigh",
    "variation": "procedure"
  },
  {
    "id": 2064,
    "word": "process",
    "meaning": "과정",
    "level": "MidHigh"
  },
  {
    "id": 2065,
    "word": "produce",
    "meaning": "생산하다",
    "level": "MidHigh"
  },
  {
    "id": 2066,
    "word": "profession",
    "meaning": "직업",
    "level": "MidHigh"
  },
  {
    "id": 2067,
    "word": "professor",
    "meaning": "교수",
    "level": "Extended"
  },
  {
    "id": 2068,
    "word": "profile",
    "meaning": "프로필",
    "level": "Extended"
  },
  {
    "id": 2069,
    "word": "profit",
    "meaning": "이익",
    "level": "MidHigh"
  },
  {
    "id": 2070,
    "word": "profound",
    "meaning": "심오한",
    "level": "Extended"
  },
  {
    "id": 2071,
    "word": "program",
    "meaning": "프로그램",
    "level": "Elementary",
    "variation": "programme, programmatic"
  },
  {
    "id": 2072,
    "word": "progress",
    "meaning": "진전",
    "level": "MidHigh"
  },
  {
    "id": 2073,
    "word": "prohibit",
    "meaning": "금지하다",
    "level": "Extended"
  },
  {
    "id": 2074,
    "word": "project",
    "meaning": "프로젝트",
    "level": "Elementary"
  },
  {
    "id": 2075,
    "word": "prominent",
    "meaning": "저명한",
    "level": "Extended"
  },
  {
    "id": 2076,
    "word": "promise",
    "meaning": "약속",
    "level": "MidHigh"
  },
  {
    "id": 2077,
    "word": "promote",
    "meaning": "촉진하다",
    "level": "MidHigh"
  },
  {
    "id": 2078,
    "word": "prompt",
    "meaning": "즉각적인",
    "level": "Extended"
  },
  {
    "id": 2079,
    "word": "pronounce",
    "meaning": "발음하다",
    "level": "MidHigh",
    "variation": "pronunciation"
  },
  {
    "id": 2080,
    "word": "proof",
    "meaning": "증거",
    "level": "Extended"
  },
  {
    "id": 2081,
    "word": "proper",
    "meaning": "적절한",
    "level": "MidHigh"
  },
  {
    "id": 2082,
    "word": "property",
    "meaning": "재산",
    "level": "MidHigh"
  },
  {
    "id": 2083,
    "word": "proportion",
    "meaning": "비율",
    "level": "Extended"
  },
  {
    "id": 2084,
    "word": "propose",
    "meaning": "제안하다",
    "level": "MidHigh"
  },
  {
    "id": 2085,
    "word": "prospect",
    "meaning": "전망",
    "level": "Extended"
  },
  {
    "id": 2086,
    "word": "prosper",
    "meaning": "번창하다",
    "level": "Extended"
  },
  {
    "id": 2087,
    "word": "protect",
    "meaning": "보호하다",
    "level": "MidHigh"
  },
  {
    "id": 2088,
    "word": "protein",
    "meaning": "단백질",
    "level": "Extended"
  },
  {
    "id": 2089,
    "word": "protest",
    "meaning": "항의하다",
    "level": "MidHigh"
  },
  {
    "id": 2090,
    "word": "proud",
    "meaning": "자랑스러운",
    "level": "MidHigh"
  },
  {
    "id": 2091,
    "word": "prove",
    "meaning": "증명하다",
    "level": "MidHigh"
  },
  {
    "id": 2092,
    "word": "provide",
    "meaning": "제공하다",
    "level": "MidHigh"
  },
  {
    "id": 2093,
    "word": "province",
    "meaning": "지방",
    "level": "Extended"
  },
  {
    "id": 2094,
    "word": "provoke",
    "meaning": "자극하다",
    "level": "Extended"
  },
  {
    "id": 2095,
    "word": "psychology",
    "meaning": "심리학",
    "level": "Extended"
  },
  {
    "id": 2096,
    "word": "pub",
    "meaning": "술집",
    "level": "MidHigh"
  },
  {
    "id": 2097,
    "word": "public",
    "meaning": "공공의",
    "level": "MidHigh"
  },
  {
    "id": 2098,
    "word": "publish",
    "meaning": "출판하다",
    "level": "Extended",
    "variation": "publisher"
  },
  {
    "id": 2099,
    "word": "pull",
    "meaning": "당기다",
    "level": "MidHigh"
  },
  {
    "id": 2100,
    "word": "pump",
    "meaning": "펌프",
    "level": "MidHigh"
  },
  {
    "id": 2101,
    "word": "punch",
    "meaning": "주먹으로 치다",
    "level": "MidHigh"
  },
  {
    "id": 2102,
    "word": "punish",
    "meaning": "벌하다",
    "level": "MidHigh"
  },
  {
    "id": 2103,
    "word": "pupil",
    "meaning": "학생",
    "level": "Extended"
  },
  {
    "id": 2104,
    "word": "puppy",
    "meaning": "강아지",
    "level": "Elementary"
  },
  {
    "id": 2105,
    "word": "purchase",
    "meaning": "구매하다",
    "level": "MidHigh"
  },
  {
    "id": 2106,
    "word": "pure",
    "meaning": "순수한",
    "level": "MidHigh"
  },
  {
    "id": 2107,
    "word": "purple",
    "meaning": "보라색",
    "level": "MidHigh"
  },
  {
    "id": 2108,
    "word": "purpose",
    "meaning": "목적",
    "level": "MidHigh"
  },
  {
    "id": 2109,
    "word": "pursue",
    "meaning": "추구하다",
    "level": "Extended"
  },
  {
    "id": 2110,
    "word": "push",
    "meaning": "밀다",
    "level": "Elementary"
  },
  {
    "id": 2111,
    "word": "put",
    "meaning": "놓다",
    "level": "Elementary"
  },
  {
    "id": 2112,
    "word": "puzzle",
    "meaning": "퍼즐",
    "level": "MidHigh"
  },
  {
    "id": 2113,
    "word": "quality",
    "meaning": "품질",
    "level": "MidHigh",
    "variation": "qualify"
  },
  {
    "id": 2114,
    "word": "quantity",
    "meaning": "양",
    "level": "Extended"
  },
  {
    "id": 2115,
    "word": "quarter",
    "meaning": "4분의 1",
    "level": "MidHigh"
  },
  {
    "id": 2116,
    "word": "queen",
    "meaning": "여왕",
    "level": "Elementary"
  },
  {
    "id": 2117,
    "word": "question",
    "meaning": "질문",
    "level": "Elementary"
  },
  {
    "id": 2118,
    "word": "questionnaire",
    "meaning": "설문지",
    "level": "Extended"
  },
  {
    "id": 2119,
    "word": "quick",
    "meaning": "빠른",
    "level": "Elementary"
  },
  {
    "id": 2120,
    "word": "quiet",
    "meaning": "조용한",
    "level": "Elementary"
  },
  {
    "id": 2121,
    "word": "quit",
    "meaning": "그만두다",
    "level": "MidHigh"
  },
  {
    "id": 2122,
    "word": "quite",
    "meaning": "꽤",
    "level": "MidHigh"
  },
  {
    "id": 2123,
    "word": "quiz",
    "meaning": "퀴즈",
    "level": "Elementary"
  },
  {
    "id": 2124,
    "word": "quote",
    "meaning": "인용하다",
    "level": "MidHigh"
  },
  {
    "id": 2125,
    "word": "rabbit",
    "meaning": "토끼",
    "level": "Elementary"
  },
  {
    "id": 2126,
    "word": "race",
    "meaning": "경주",
    "level": "Elementary",
    "variation": "racial"
  },
  {
    "id": 2127,
    "word": "radio",
    "meaning": "라디오",
    "level": "Elementary"
  },
  {
    "id": 2128,
    "word": "rage",
    "meaning": "격노",
    "level": "Extended"
  },
  {
    "id": 2129,
    "word": "rail",
    "meaning": "철도",
    "level": "MidHigh"
  },
  {
    "id": 2130,
    "word": "rain",
    "meaning": "비",
    "level": "Elementary"
  },
  {
    "id": 2131,
    "word": "rainbow",
    "meaning": "무지개",
    "level": "MidHigh"
  },
  {
    "id": 2132,
    "word": "raise",
    "meaning": "올리다",
    "level": "MidHigh"
  },
  {
    "id": 2133,
    "word": "rally",
    "meaning": "집회",
    "level": "Extended"
  },
  {
    "id": 2134,
    "word": "random",
    "meaning": "무작위의",
    "level": "Extended"
  },
  {
    "id": 2135,
    "word": "range",
    "meaning": "범위",
    "level": "MidHigh"
  },
  {
    "id": 2136,
    "word": "rank",
    "meaning": "순위",
    "level": "Extended"
  },
  {
    "id": 2137,
    "word": "rapid",
    "meaning": "빠른",
    "level": "MidHigh"
  },
  {
    "id": 2138,
    "word": "rare",
    "meaning": "드문",
    "level": "MidHigh"
  },
  {
    "id": 2139,
    "word": "rat",
    "meaning": "쥐",
    "level": "MidHigh"
  },
  {
    "id": 2140,
    "word": "rate",
    "meaning": "비율",
    "level": "MidHigh"
  },
  {
    "id": 2141,
    "word": "rather",
    "meaning": "오히려",
    "level": "MidHigh"
  },
  {
    "id": 2142,
    "word": "rational",
    "meaning": "합리적인",
    "level": "Extended"
  },
  {
    "id": 2143,
    "word": "raw",
    "meaning": "날것의",
    "level": "Extended"
  },
  {
    "id": 2144,
    "word": "reach",
    "meaning": "도달하다",
    "level": "MidHigh"
  },
  {
    "id": 2145,
    "word": "react",
    "meaning": "반응하다",
    "level": "MidHigh"
  },
  {
    "id": 2146,
    "word": "read",
    "meaning": "읽다",
    "level": "Elementary"
  },
  {
    "id": 2147,
    "word": "ready",
    "meaning": "준비된",
    "level": "Elementary"
  },
  {
    "id": 2148,
    "word": "real",
    "meaning": "진짜의",
    "level": "MidHigh",
    "variation": "realize, realise"
  },
  {
    "id": 2149,
    "word": "rear",
    "meaning": "뒤쪽",
    "level": "Extended"
  },
  {
    "id": 2150,
    "word": "reason",
    "meaning": "이유",
    "level": "MidHigh",
    "variation": "reasonable"
  },
  {
    "id": 2151,
    "word": "rebel",
    "meaning": "반역자",
    "level": "Extended"
  },
  {
    "id": 2152,
    "word": "receipt",
    "meaning": "영수증",
    "level": "Extended"
  },
  {
    "id": 2153,
    "word": "receive",
    "meaning": "받다",
    "level": "MidHigh",
    "variation": "reception"
  },
  {
    "id": 2154,
    "word": "recent",
    "meaning": "최근의",
    "level": "MidHigh"
  },
  {
    "id": 2155,
    "word": "recipe",
    "meaning": "요리법",
    "level": "MidHigh"
  },
  {
    "id": 2156,
    "word": "recognize",
    "meaning": "알아보다",
    "level": "MidHigh"
  },
  {
    "id": 2157,
    "word": "recommend",
    "meaning": "추천하다",
    "level": "MidHigh"
  },
  {
    "id": 2158,
    "word": "record",
    "meaning": "기록하다",
    "level": "MidHigh"
  },
  {
    "id": 2159,
    "word": "recover",
    "meaning": "회복하다",
    "level": "MidHigh"
  },
  {
    "id": 2160,
    "word": "recreation",
    "meaning": "오락",
    "level": "Elementary"
  },
  {
    "id": 2161,
    "word": "recruit",
    "meaning": "모집하다",
    "level": "Extended"
  },
  {
    "id": 2162,
    "word": "red",
    "meaning": "빨간색",
    "level": "Elementary"
  },
  {
    "id": 2163,
    "word": "reduce",
    "meaning": "줄이다",
    "level": "MidHigh"
  },
  {
    "id": 2164,
    "word": "refer",
    "meaning": "언급하다",
    "level": "MidHigh"
  },
  {
    "id": 2165,
    "word": "refine",
    "meaning": "개선하다",
    "level": "Extended"
  },
  {
    "id": 2166,
    "word": "reflect",
    "meaning": "반영하다",
    "level": "MidHigh"
  },
  {
    "id": 2167,
    "word": "reform",
    "meaning": "개혁하다",
    "level": "Extended"
  },
  {
    "id": 2168,
    "word": "refrigerate",
    "meaning": "냉장하다",
    "level": "Extended",
    "variation": "refrigerator"
  },
  {
    "id": 2169,
    "word": "refuse",
    "meaning": "거절하다",
    "level": "MidHigh"
  },
  {
    "id": 2170,
    "word": "regard",
    "meaning": "여기다",
    "level": "MidHigh"
  },
  {
    "id": 2171,
    "word": "region",
    "meaning": "지역",
    "level": "MidHigh"
  },
  {
    "id": 2172,
    "word": "register",
    "meaning": "등록하다",
    "level": "MidHigh"
  },
  {
    "id": 2173,
    "word": "regret",
    "meaning": "후회하다",
    "level": "Extended"
  },
  {
    "id": 2174,
    "word": "regular",
    "meaning": "규칙적인",
    "level": "MidHigh"
  },
  {
    "id": 2175,
    "word": "regulate",
    "meaning": "규제하다",
    "level": "Extended"
  },
  {
    "id": 2176,
    "word": "reinforce",
    "meaning": "강화하다",
    "level": "Extended"
  },
  {
    "id": 2177,
    "word": "reject",
    "meaning": "거부하다",
    "level": "Extended"
  },
  {
    "id": 2178,
    "word": "relate",
    "meaning": "관련시키다",
    "level": "MidHigh",
    "variation": "relative, relation, relationship"
  },
  {
    "id": 2179,
    "word": "relax",
    "meaning": "긴장을 풀다",
    "level": "MidHigh"
  },
  {
    "id": 2180,
    "word": "release",
    "meaning": "풀어주다",
    "level": "MidHigh"
  },
  {
    "id": 2181,
    "word": "relevant",
    "meaning": "관련 있는",
    "level": "Extended"
  },
  {
    "id": 2182,
    "word": "relief",
    "meaning": "안도",
    "level": "MidHigh"
  },
  {
    "id": 2183,
    "word": "relieve",
    "meaning": "완화하다",
    "level": "Extended"
  },
  {
    "id": 2184,
    "word": "religion",
    "meaning": "종교",
    "level": "Extended"
  },
  {
    "id": 2185,
    "word": "reluctant",
    "meaning": "꺼리는",
    "level": "Extended"
  },
  {
    "id": 2186,
    "word": "rely",
    "meaning": "의지하다",
    "level": "MidHigh"
  },
  {
    "id": 2187,
    "word": "remain",
    "meaning": "남다",
    "level": "MidHigh"
  },
  {
    "id": 2188,
    "word": "remark",
    "meaning": "언급하다",
    "level": "MidHigh"
  },
  {
    "id": 2189,
    "word": "remedy",
    "meaning": "치료책",
    "level": "Extended"
  },
  {
    "id": 2190,
    "word": "remember",
    "meaning": "기억하다",
    "level": "Elementary"
  },
  {
    "id": 2191,
    "word": "remind",
    "meaning": "상기시키다",
    "level": "MidHigh"
  },
  {
    "id": 2192,
    "word": "remote",
    "meaning": "먼",
    "level": "Extended"
  },
  {
    "id": 2193,
    "word": "remove",
    "meaning": "제거하다",
    "level": "MidHigh"
  },
  {
    "id": 2194,
    "word": "rent",
    "meaning": "빌리다",
    "level": "MidHigh"
  },
  {
    "id": 2195,
    "word": "repair",
    "meaning": "수리하다",
    "level": "MidHigh"
  },
  {
    "id": 2196,
    "word": "repeat",
    "meaning": "반복하다",
    "level": "MidHigh"
  },
  {
    "id": 2197,
    "word": "replace",
    "meaning": "대신하다",
    "level": "MidHigh"
  },
  {
    "id": 2198,
    "word": "reply",
    "meaning": "대답하다",
    "level": "MidHigh"
  },
  {
    "id": 2199,
    "word": "report",
    "meaning": "보고하다",
    "level": "MidHigh"
  },
  {
    "id": 2200,
    "word": "represent",
    "meaning": "대표하다",
    "level": "MidHigh"
  },
  {
    "id": 2201,
    "word": "republic",
    "meaning": "공화국",
    "level": "Extended"
  },
  {
    "id": 2202,
    "word": "reputation",
    "meaning": "명성",
    "level": "Extended"
  },
  {
    "id": 2203,
    "word": "request",
    "meaning": "요청하다",
    "level": "MidHigh"
  },
  {
    "id": 2204,
    "word": "require",
    "meaning": "요구하다",
    "level": "MidHigh"
  },
  {
    "id": 2205,
    "word": "rescue",
    "meaning": "구조하다",
    "level": "Extended"
  },
  {
    "id": 2206,
    "word": "research",
    "meaning": "연구",
    "level": "MidHigh"
  },
  {
    "id": 2207,
    "word": "resemble",
    "meaning": "닮다",
    "level": "Extended"
  },
  {
    "id": 2208,
    "word": "reserve",
    "meaning": "예약하다",
    "level": "MidHigh"
  },
  {
    "id": 2209,
    "word": "reside",
    "meaning": "거주하다",
    "level": "Extended",
    "variation": "resident"
  },
  {
    "id": 2210,
    "word": "resign",
    "meaning": "사임하다",
    "level": "Extended"
  },
  {
    "id": 2211,
    "word": "resist",
    "meaning": "저항하다",
    "level": "MidHigh"
  },
  {
    "id": 2212,
    "word": "resolve",
    "meaning": "해결하다",
    "level": "Extended"
  },
  {
    "id": 2213,
    "word": "resort",
    "meaning": "휴양지",
    "level": "Extended"
  },
  {
    "id": 2214,
    "word": "resource",
    "meaning": "자원",
    "level": "MidHigh"
  },
  {
    "id": 2215,
    "word": "respect",
    "meaning": "존중하다",
    "level": "MidHigh",
    "variation": "respective"
  },
  {
    "id": 2216,
    "word": "respond",
    "meaning": "응답하다",
    "level": "MidHigh"
  },
  {
    "id": 2217,
    "word": "responsible",
    "meaning": "책임 있는",
    "level": "MidHigh"
  },
  {
    "id": 2218,
    "word": "rest",
    "meaning": "휴식",
    "level": "MidHigh"
  },
  {
    "id": 2219,
    "word": "restaurant",
    "meaning": "음식점",
    "level": "Elementary"
  },
  {
    "id": 2220,
    "word": "restore",
    "meaning": "복구하다",
    "level": "Extended"
  },
  {
    "id": 2221,
    "word": "restrain",
    "meaning": "억제하다",
    "level": "Extended"
  },
  {
    "id": 2222,
    "word": "restrict",
    "meaning": "제한하다",
    "level": "Extended"
  },
  {
    "id": 2223,
    "word": "restroom",
    "meaning": "화장실",
    "level": "Elementary"
  },
  {
    "id": 2224,
    "word": "result",
    "meaning": "결과",
    "level": "MidHigh"
  },
  {
    "id": 2225,
    "word": "resume",
    "meaning": "재개하다",
    "level": "Extended"
  },
  {
    "id": 2226,
    "word": "retail",
    "meaning": "소매",
    "level": "Extended"
  },
  {
    "id": 2227,
    "word": "retain",
    "meaning": "유지하다",
    "level": "Extended"
  },
  {
    "id": 2228,
    "word": "retire",
    "meaning": "은퇴하다",
    "level": "MidHigh"
  },
  {
    "id": 2229,
    "word": "retreat",
    "meaning": "후퇴하다",
    "level": "Extended"
  },
  {
    "id": 2230,
    "word": "return",
    "meaning": "돌아오다",
    "level": "Elementary"
  },
  {
    "id": 2231,
    "word": "reveal",
    "meaning": "드러내다",
    "level": "Extended"
  },
  {
    "id": 2232,
    "word": "revenge",
    "meaning": "복수",
    "level": "Extended"
  },
  {
    "id": 2233,
    "word": "reverse",
    "meaning": "반대",
    "level": "Extended"
  },
  {
    "id": 2234,
    "word": "revise",
    "meaning": "수정하다",
    "level": "Extended"
  },
  {
    "id": 2235,
    "word": "revive",
    "meaning": "소생시키다",
    "level": "Extended"
  },
  {
    "id": 2236,
    "word": "revolution",
    "meaning": "혁명",
    "level": "Extended"
  },
  {
    "id": 2237,
    "word": "reward",
    "meaning": "보상",
    "level": "Extended"
  },
  {
    "id": 2238,
    "word": "rhythm",
    "meaning": "리듬",
    "level": "Extended"
  },
  {
    "id": 2239,
    "word": "ribbon",
    "meaning": "리본",
    "level": "Elementary"
  },
  {
    "id": 2240,
    "word": "rice",
    "meaning": "쌀",
    "level": "MidHigh"
  },
  {
    "id": 2241,
    "word": "rich",
    "meaning": "부유한",
    "level": "Elementary"
  },
  {
    "id": 2242,
    "word": "rid",
    "meaning": "없애다",
    "level": "Extended"
  },
  {
    "id": 2243,
    "word": "ride",
    "meaning": "타다",
    "level": "MidHigh"
  },
  {
    "id": 2244,
    "word": "ridicule",
    "meaning": "조롱하다",
    "level": "Extended",
    "variation": "ridiculous"
  },
  {
    "id": 2245,
    "word": "right",
    "meaning": "옳은",
    "level": "Elementary"
  },
  {
    "id": 2246,
    "word": "ring",
    "meaning": "반지",
    "level": "Elementary"
  },
  {
    "id": 2247,
    "word": "riot",
    "meaning": "폭동",
    "level": "Extended"
  },
  {
    "id": 2248,
    "word": "rise",
    "meaning": "오르다",
    "level": "MidHigh"
  },
  {
    "id": 2249,
    "word": "risk",
    "meaning": "위험",
    "level": "MidHigh"
  },
  {
    "id": 2250,
    "word": "rival",
    "meaning": "경쟁자",
    "level": "Extended"
  },
  {
    "id": 2251,
    "word": "river",
    "meaning": "강",
    "level": "Elementary"
  },
  {
    "id": 2252,
    "word": "road",
    "meaning": "도로",
    "level": "Elementary"
  },
  {
    "id": 2253,
    "word": "roar",
    "meaning": "포효하다",
    "level": "Extended"
  },
  {
    "id": 2254,
    "word": "roast",
    "meaning": "굽다",
    "level": "Extended"
  },
  {
    "id": 2255,
    "word": "rob",
    "meaning": "강탈하다",
    "level": "MidHigh"
  },
  {
    "id": 2256,
    "word": "robot",
    "meaning": "로봇",
    "level": "Elementary"
  },
  {
    "id": 2257,
    "word": "rock",
    "meaning": "바위",
    "level": "Elementary"
  },
  {
    "id": 2258,
    "word": "rocket",
    "meaning": "로켓",
    "level": "MidHigh"
  },
  {
    "id": 2259,
    "word": "rod",
    "meaning": "막대",
    "level": "Extended"
  },
  {
    "id": 2260,
    "word": "role",
    "meaning": "역할",
    "level": "MidHigh"
  },
  {
    "id": 2261,
    "word": "roll",
    "meaning": "굴리다",
    "level": "MidHigh",
    "variation": "enroll, enrol"
  },
  {
    "id": 2262,
    "word": "romantic",
    "meaning": "낭만적인",
    "level": "Extended"
  },
  {
    "id": 2263,
    "word": "roof",
    "meaning": "지붕",
    "level": "MidHigh"
  },
  {
    "id": 2264,
    "word": "room",
    "meaning": "방",
    "level": "Elementary"
  },
  {
    "id": 2265,
    "word": "root",
    "meaning": "뿌리",
    "level": "MidHigh"
  },
  {
    "id": 2266,
    "word": "rope",
    "meaning": "밧줄",
    "level": "MidHigh"
  },
  {
    "id": 2267,
    "word": "rose",
    "meaning": "장미",
    "level": "Elementary"
  },
  {
    "id": 2268,
    "word": "rot",
    "meaning": "썩다",
    "level": "Extended"
  },
  {
    "id": 2269,
    "word": "rough",
    "meaning": "거친",
    "level": "MidHigh"
  },
  {
    "id": 2270,
    "word": "round",
    "meaning": "둥근",
    "level": "MidHigh"
  },
  {
    "id": 2271,
    "word": "route",
    "meaning": "경로",
    "level": "MidHigh"
  },
  {
    "id": 2272,
    "word": "routine",
    "meaning": "일상",
    "level": "Extended"
  },
  {
    "id": 2273,
    "word": "row",
    "meaning": "줄",
    "level": "MidHigh"
  },
  {
    "id": 2274,
    "word": "royal",
    "meaning": "왕실의",
    "level": "MidHigh"
  },
  {
    "id": 2275,
    "word": "rub",
    "meaning": "문지르다",
    "level": "MidHigh",
    "variation": "rubber"
  },
  {
    "id": 2276,
    "word": "rude",
    "meaning": "무례한",
    "level": "MidHigh"
  },
  {
    "id": 2277,
    "word": "ruin",
    "meaning": "파멸",
    "level": "MidHigh"
  },
  {
    "id": 2278,
    "word": "rule",
    "meaning": "규칙",
    "level": "MidHigh"
  },
  {
    "id": 2279,
    "word": "rumor",
    "meaning": "소문",
    "level": "Extended",
    "variation": "rumour"
  },
  {
    "id": 2280,
    "word": "run",
    "meaning": "달리다",
    "level": "Elementary"
  },
  {
    "id": 2281,
    "word": "rural",
    "meaning": "시골의",
    "level": "Extended"
  },
  {
    "id": 2282,
    "word": "rush",
    "meaning": "서두르다",
    "level": "MidHigh"
  },
  {
    "id": 2283,
    "word": "sack",
    "meaning": "자루",
    "level": "Extended"
  },
  {
    "id": 2284,
    "word": "sacred",
    "meaning": "신성한",
    "level": "Extended"
  },
  {
    "id": 2285,
    "word": "sacrifice",
    "meaning": "희생",
    "level": "Extended"
  },
  {
    "id": 2286,
    "word": "sad",
    "meaning": "슬픈",
    "level": "Elementary"
  },
  {
    "id": 2287,
    "word": "safe",
    "meaning": "안전한",
    "level": "Elementary"
  },
  {
    "id": 2288,
    "word": "sail",
    "meaning": "항해하다",
    "level": "MidHigh"
  },
  {
    "id": 2289,
    "word": "salad",
    "meaning": "샐러드",
    "level": "Elementary"
  },
  {
    "id": 2290,
    "word": "salary",
    "meaning": "급여",
    "level": "MidHigh"
  },
  {
    "id": 2291,
    "word": "sale",
    "meaning": "판매",
    "level": "Elementary"
  },
  {
    "id": 2292,
    "word": "salt",
    "meaning": "소금",
    "level": "Elementary"
  },
  {
    "id": 2293,
    "word": "same",
    "meaning": "같은",
    "level": "Elementary"
  },
  {
    "id": 2294,
    "word": "sample",
    "meaning": "견본",
    "level": "MidHigh"
  },
  {
    "id": 2295,
    "word": "sand",
    "meaning": "모래",
    "level": "Elementary"
  },
  {
    "id": 2296,
    "word": "sandwich",
    "meaning": "샌드위치",
    "level": "Elementary"
  },
  {
    "id": 2297,
    "word": "satellite",
    "meaning": "위성",
    "level": "Extended"
  },
  {
    "id": 2298,
    "word": "satisfy",
    "meaning": "만족시키다",
    "level": "MidHigh"
  },
  {
    "id": 2299,
    "word": "sauce",
    "meaning": "소스",
    "level": "MidHigh"
  },
  {
    "id": 2300,
    "word": "save",
    "meaning": "구하다",
    "level": "Elementary"
  },
  {
    "id": 2301,
    "word": "say",
    "meaning": "말하다",
    "level": "Elementary"
  },
  {
    "id": 2302,
    "word": "scale",
    "meaning": "규모",
    "level": "MidHigh"
  },
  {
    "id": 2303,
    "word": "scan",
    "meaning": "스캔하다",
    "level": "Extended"
  },
  {
    "id": 2304,
    "word": "scandal",
    "meaning": "추문",
    "level": "Extended"
  },
  {
    "id": 2305,
    "word": "scarce",
    "meaning": "부족한",
    "level": "Extended"
  },
  {
    "id": 2306,
    "word": "scare",
    "meaning": "겁주다",
    "level": "MidHigh"
  },
  {
    "id": 2307,
    "word": "scarf",
    "meaning": "목도리",
    "level": "MidHigh"
  },
  {
    "id": 2308,
    "word": "scatter",
    "meaning": "흩뿌리다",
    "level": "Extended"
  },
  {
    "id": 2309,
    "word": "scene",
    "meaning": "장면",
    "level": "MidHigh"
  },
  {
    "id": 2310,
    "word": "schedule",
    "meaning": "일정",
    "level": "MidHigh"
  },
  {
    "id": 2311,
    "word": "scheme",
    "meaning": "계획",
    "level": "Extended"
  },
  {
    "id": 2312,
    "word": "scholar",
    "meaning": "학자",
    "level": "Extended"
  },
  {
    "id": 2313,
    "word": "school",
    "meaning": "학교",
    "level": "Elementary"
  },
  {
    "id": 2314,
    "word": "science",
    "meaning": "과학",
    "level": "Elementary"
  },
  {
    "id": 2315,
    "word": "scissors",
    "meaning": "가위",
    "level": "Elementary"
  },
  {
    "id": 2316,
    "word": "scope",
    "meaning": "범위",
    "level": "Extended"
  },
  {
    "id": 2317,
    "word": "score",
    "meaning": "점수",
    "level": "Elementary"
  },
  {
    "id": 2318,
    "word": "scramble",
    "meaning": "기어오르다",
    "level": "Extended"
  },
  {
    "id": 2319,
    "word": "scratch",
    "meaning": "긁다",
    "level": "MidHigh"
  },
  {
    "id": 2320,
    "word": "scream",
    "meaning": "비명을 지르다",
    "level": "MidHigh"
  },
  {
    "id": 2321,
    "word": "screen",
    "meaning": "화면",
    "level": "MidHigh"
  },
  {
    "id": 2322,
    "word": "screw",
    "meaning": "나사",
    "level": "Extended"
  },
  {
    "id": 2323,
    "word": "sculpt",
    "meaning": "조각하다",
    "level": "Extended",
    "variation": "sculpture"
  },
  {
    "id": 2324,
    "word": "sea",
    "meaning": "바다",
    "level": "Elementary"
  },
  {
    "id": 2325,
    "word": "seal",
    "meaning": "봉인하다",
    "level": "MidHigh"
  },
  {
    "id": 2326,
    "word": "search",
    "meaning": "찾다",
    "level": "MidHigh"
  },
  {
    "id": 2327,
    "word": "season",
    "meaning": "계절",
    "level": "Elementary"
  },
  {
    "id": 2328,
    "word": "seat",
    "meaning": "자리",
    "level": "MidHigh"
  },
  {
    "id": 2329,
    "word": "second",
    "meaning": "두 번째",
    "level": "Elementary",
    "variation": "secondary"
  },
  {
    "id": 2330,
    "word": "secret",
    "meaning": "비밀",
    "level": "MidHigh"
  },
  {
    "id": 2331,
    "word": "secretary",
    "meaning": "비서",
    "level": "MidHigh"
  },
  {
    "id": 2332,
    "word": "section",
    "meaning": "부분",
    "level": "MidHigh"
  },
  {
    "id": 2333,
    "word": "sector",
    "meaning": "부문",
    "level": "Extended"
  },
  {
    "id": 2334,
    "word": "secure",
    "meaning": "안전한",
    "level": "MidHigh"
  },
  {
    "id": 2335,
    "word": "see",
    "meaning": "보다",
    "level": "Elementary"
  },
  {
    "id": 2336,
    "word": "seed",
    "meaning": "씨앗",
    "level": "MidHigh"
  },
  {
    "id": 2337,
    "word": "seek",
    "meaning": "찾다",
    "level": "MidHigh"
  },
  {
    "id": 2338,
    "word": "seem",
    "meaning": "~처럼 보이다",
    "level": "MidHigh"
  },
  {
    "id": 2339,
    "word": "seize",
    "meaning": "붙잡다",
    "level": "Extended"
  },
  {
    "id": 2340,
    "word": "select",
    "meaning": "선택하다",
    "level": "MidHigh"
  },
  {
    "id": 2341,
    "word": "self",
    "meaning": "자기 자신",
    "level": "MidHigh"
  },
  {
    "id": 2342,
    "word": "sell",
    "meaning": "팔다",
    "level": "Elementary"
  },
  {
    "id": 2343,
    "word": "send",
    "meaning": "보내다",
    "level": "Elementary"
  },
  {
    "id": 2344,
    "word": "senior",
    "meaning": "선배",
    "level": "MidHigh"
  },
  {
    "id": 2345,
    "word": "sense",
    "meaning": "감각",
    "level": "MidHigh",
    "variation": "sensation"
  },
  {
    "id": 2346,
    "word": "sensible",
    "meaning": "분별 있는",
    "level": "Extended"
  },
  {
    "id": 2347,
    "word": "sentence",
    "meaning": "문장",
    "level": "MidHigh"
  },
  {
    "id": 2348,
    "word": "sentiment",
    "meaning": "감정",
    "level": "Extended"
  },
  {
    "id": 2349,
    "word": "separate",
    "meaning": "분리하다",
    "level": "MidHigh"
  },
  {
    "id": 2350,
    "word": "sequence",
    "meaning": "순서",
    "level": "Extended"
  },
  {
    "id": 2351,
    "word": "series",
    "meaning": "연속물",
    "level": "MidHigh"
  },
  {
    "id": 2352,
    "word": "serious",
    "meaning": "진지한",
    "level": "MidHigh"
  },
  {
    "id": 2353,
    "word": "serve",
    "meaning": "봉사하다",
    "level": "MidHigh"
  },
  {
    "id": 2354,
    "word": "service",
    "meaning": "서비스",
    "level": "Elementary"
  },
  {
    "id": 2355,
    "word": "session",
    "meaning": "회기",
    "level": "MidHigh"
  },
  {
    "id": 2356,
    "word": "set",
    "meaning": "놓다",
    "level": "Elementary"
  },
  {
    "id": 2357,
    "word": "settle",
    "meaning": "정착하다",
    "level": "MidHigh"
  },
  {
    "id": 2358,
    "word": "seven",
    "meaning": "일곱",
    "level": "Elementary"
  },
  {
    "id": 2359,
    "word": "several",
    "meaning": "몇몇의",
    "level": "MidHigh"
  },
  {
    "id": 2360,
    "word": "severe",
    "meaning": "심각한",
    "level": "Extended"
  },
  {
    "id": 2361,
    "word": "sew",
    "meaning": "바느질하다",
    "level": "MidHigh"
  },
  {
    "id": 2362,
    "word": "sex",
    "meaning": "성별",
    "level": "MidHigh"
  },
  {
    "id": 2363,
    "word": "shade",
    "meaning": "그늘",
    "level": "MidHigh"
  },
  {
    "id": 2364,
    "word": "shadow",
    "meaning": "그림자",
    "level": "MidHigh"
  },
  {
    "id": 2365,
    "word": "shake",
    "meaning": "흔들다",
    "level": "MidHigh"
  },
  {
    "id": 2366,
    "word": "shall",
    "meaning": "~할 것이다",
    "level": "MidHigh"
  },
  {
    "id": 2367,
    "word": "shallow",
    "meaning": "얕은",
    "level": "Extended"
  },
  {
    "id": 2368,
    "word": "shame",
    "meaning": "수치심",
    "level": "MidHigh"
  },
  {
    "id": 2369,
    "word": "shape",
    "meaning": "모양",
    "level": "MidHigh"
  },
  {
    "id": 2370,
    "word": "share",
    "meaning": "공유하다",
    "level": "MidHigh"
  },
  {
    "id": 2371,
    "word": "sharp",
    "meaning": "날카로운",
    "level": "MidHigh"
  },
  {
    "id": 2372,
    "word": "shave",
    "meaning": "면도하다",
    "level": "MidHigh"
  },
  {
    "id": 2373,
    "word": "she",
    "meaning": "그녀",
    "level": "Elementary"
  },
  {
    "id": 2374,
    "word": "sheep",
    "meaning": "양",
    "level": "MidHigh"
  },
  {
    "id": 2375,
    "word": "sheet",
    "meaning": "종이 한 장",
    "level": "MidHigh"
  },
  {
    "id": 2376,
    "word": "shelf",
    "meaning": "선반",
    "level": "MidHigh"
  },
  {
    "id": 2377,
    "word": "shell",
    "meaning": "껍데기",
    "level": "MidHigh"
  },
  {
    "id": 2378,
    "word": "shelter",
    "meaning": "피난처",
    "level": "MidHigh"
  },
  {
    "id": 2379,
    "word": "shift",
    "meaning": "옮기다",
    "level": "MidHigh"
  },
  {
    "id": 2380,
    "word": "shine",
    "meaning": "빛나다",
    "level": "MidHigh"
  },
  {
    "id": 2381,
    "word": "ship",
    "meaning": "배",
    "level": "Elementary"
  },
  {
    "id": 2382,
    "word": "shirt",
    "meaning": "셔츠",
    "level": "Elementary"
  },
  {
    "id": 2383,
    "word": "shock",
    "meaning": "충격",
    "level": "MidHigh"
  },
  {
    "id": 2384,
    "word": "shoe",
    "meaning": "신발",
    "level": "Elementary"
  },
  {
    "id": 2385,
    "word": "shoot",
    "meaning": "쏘다",
    "level": "MidHigh"
  },
  {
    "id": 2386,
    "word": "shop",
    "meaning": "가게",
    "level": "Elementary"
  },
  {
    "id": 2387,
    "word": "shore",
    "meaning": "해안",
    "level": "MidHigh"
  },
  {
    "id": 2388,
    "word": "short",
    "meaning": "짧은",
    "level": "Elementary"
  },
  {
    "id": 2389,
    "word": "should",
    "meaning": "~해야 한다",
    "level": "Elementary"
  },
  {
    "id": 2390,
    "word": "shoulder",
    "meaning": "어깨",
    "level": "MidHigh"
  },
  {
    "id": 2391,
    "word": "shout",
    "meaning": "소리치다",
    "level": "MidHigh"
  },
  {
    "id": 2392,
    "word": "show",
    "meaning": "보여 주다",
    "level": "Elementary"
  },
  {
    "id": 2393,
    "word": "shower",
    "meaning": "샤워",
    "level": "MidHigh"
  },
  {
    "id": 2394,
    "word": "shut",
    "meaning": "닫다",
    "level": "MidHigh"
  },
  {
    "id": 2395,
    "word": "shy",
    "meaning": "수줍은",
    "level": "Elementary"
  },
  {
    "id": 2396,
    "word": "sick",
    "meaning": "아픈",
    "level": "Elementary"
  },
  {
    "id": 2397,
    "word": "side",
    "meaning": "옆",
    "level": "Elementary"
  },
  {
    "id": 2398,
    "word": "sigh",
    "meaning": "한숨 쉬다",
    "level": "Extended"
  },
  {
    "id": 2399,
    "word": "sight",
    "meaning": "시력",
    "level": "MidHigh"
  },
  {
    "id": 2400,
    "word": "sign",
    "meaning": "표시",
    "level": "MidHigh",
    "variation": "significant"
  },
  {
    "id": 2401,
    "word": "silent",
    "meaning": "조용한",
    "level": "Extended"
  },
  {
    "id": 2402,
    "word": "silly",
    "meaning": "어리석은",
    "level": "MidHigh"
  },
  {
    "id": 2403,
    "word": "silver",
    "meaning": "은",
    "level": "MidHigh"
  },
  {
    "id": 2404,
    "word": "similar",
    "meaning": "비슷한",
    "level": "MidHigh"
  },
  {
    "id": 2405,
    "word": "simple",
    "meaning": "간단한",
    "level": "MidHigh"
  },
  {
    "id": 2406,
    "word": "simulate",
    "meaning": "모의실험하다",
    "level": "Extended"
  },
  {
    "id": 2407,
    "word": "simultaneous",
    "meaning": "동시의",
    "level": "Extended"
  },
  {
    "id": 2408,
    "word": "sin",
    "meaning": "죄",
    "level": "Extended"
  },
  {
    "id": 2409,
    "word": "since",
    "meaning": "~이래로",
    "level": "MidHigh"
  },
  {
    "id": 2410,
    "word": "sing",
    "meaning": "노래하다",
    "level": "Elementary"
  },
  {
    "id": 2411,
    "word": "single",
    "meaning": "하나의",
    "level": "MidHigh"
  },
  {
    "id": 2412,
    "word": "sink",
    "meaning": "가라앉다",
    "level": "MidHigh"
  },
  {
    "id": 2413,
    "word": "sister",
    "meaning": "자매",
    "level": "Elementary"
  },
  {
    "id": 2414,
    "word": "sit",
    "meaning": "앉다",
    "level": "Elementary"
  },
  {
    "id": 2415,
    "word": "site",
    "meaning": "장소",
    "level": "MidHigh"
  },
  {
    "id": 2416,
    "word": "situate",
    "meaning": "위치시키다",
    "level": "MidHigh",
    "variation": "situation"
  },
  {
    "id": 2417,
    "word": "six",
    "meaning": "여섯",
    "level": "Elementary"
  },
  {
    "id": 2418,
    "word": "size",
    "meaning": "크기",
    "level": "Elementary"
  },
  {
    "id": 2419,
    "word": "skate",
    "meaning": "스케이트를 타다",
    "level": "Elementary"
  },
  {
    "id": 2420,
    "word": "ski",
    "meaning": "스키를 타다",
    "level": "Elementary"
  },
  {
    "id": 2421,
    "word": "skill",
    "meaning": "기술",
    "level": "MidHigh"
  },
  {
    "id": 2422,
    "word": "skin",
    "meaning": "피부",
    "level": "Elementary"
  },
  {
    "id": 2423,
    "word": "skip",
    "meaning": "건너뛰다",
    "level": "Extended"
  },
  {
    "id": 2424,
    "word": "skirt",
    "meaning": "치마",
    "level": "Elementary"
  },
  {
    "id": 2425,
    "word": "sky",
    "meaning": "하늘",
    "level": "Elementary"
  },
  {
    "id": 2426,
    "word": "slave",
    "meaning": "노예",
    "level": "MidHigh"
  },
  {
    "id": 2427,
    "word": "sleep",
    "meaning": "자다",
    "level": "Elementary"
  },
  {
    "id": 2428,
    "word": "slice",
    "meaning": "얇은 조각",
    "level": "Extended"
  },
  {
    "id": 2429,
    "word": "slide",
    "meaning": "미끄러지다",
    "level": "MidHigh"
  },
  {
    "id": 2430,
    "word": "slight",
    "meaning": "약간의",
    "level": "MidHigh"
  },
  {
    "id": 2431,
    "word": "slim",
    "meaning": "날씬한",
    "level": "Extended"
  },
  {
    "id": 2432,
    "word": "slip",
    "meaning": "미끄러지다",
    "level": "MidHigh"
  },
  {
    "id": 2433,
    "word": "slope",
    "meaning": "경사",
    "level": "Extended"
  },
  {
    "id": 2434,
    "word": "slow",
    "meaning": "느린",
    "level": "Elementary"
  },
  {
    "id": 2435,
    "word": "small",
    "meaning": "작은",
    "level": "Elementary"
  },
  {
    "id": 2436,
    "word": "smart",
    "meaning": "똑똑한",
    "level": "MidHigh"
  },
  {
    "id": 2437,
    "word": "smash",
    "meaning": "부수다",
    "level": "MidHigh"
  },
  {
    "id": 2438,
    "word": "smell",
    "meaning": "냄새",
    "level": "Elementary"
  },
  {
    "id": 2439,
    "word": "smile",
    "meaning": "미소",
    "level": "Elementary"
  },
  {
    "id": 2440,
    "word": "smoke",
    "meaning": "연기",
    "level": "MidHigh"
  },
  {
    "id": 2441,
    "word": "smooth",
    "meaning": "매끄러운",
    "level": "MidHigh"
  },
  {
    "id": 2442,
    "word": "snack",
    "meaning": "간식",
    "level": "MidHigh"
  },
  {
    "id": 2443,
    "word": "snake",
    "meaning": "뱀",
    "level": "MidHigh"
  },
  {
    "id": 2444,
    "word": "snap",
    "meaning": "딱 소리를 내다",
    "level": "MidHigh"
  },
  {
    "id": 2445,
    "word": "sneak",
    "meaning": "살금살금 가다",
    "level": "Extended"
  },
  {
    "id": 2446,
    "word": "snow",
    "meaning": "눈",
    "level": "Elementary"
  },
  {
    "id": 2447,
    "word": "so",
    "meaning": "그래서",
    "level": "Elementary"
  },
  {
    "id": 2448,
    "word": "soak",
    "meaning": "흠뻑 적시다",
    "level": "Extended"
  },
  {
    "id": 2449,
    "word": "soap",
    "meaning": "비누",
    "level": "Extended"
  },
  {
    "id": 2450,
    "word": "soccer",
    "meaning": "축구",
    "level": "Elementary"
  },
  {
    "id": 2451,
    "word": "social",
    "meaning": "사회의",
    "level": "MidHigh"
  },
  {
    "id": 2452,
    "word": "society",
    "meaning": "사회",
    "level": "MidHigh"
  },
  {
    "id": 2453,
    "word": "sociology",
    "meaning": "사회학",
    "level": "Extended"
  },
  {
    "id": 2454,
    "word": "sock",
    "meaning": "양말",
    "level": "Elementary"
  },
  {
    "id": 2455,
    "word": "soft",
    "meaning": "부드러운",
    "level": "Elementary"
  },
  {
    "id": 2456,
    "word": "software",
    "meaning": "소프트웨어",
    "level": "Elementary"
  },
  {
    "id": 2457,
    "word": "soil",
    "meaning": "토양",
    "level": "MidHigh"
  },
  {
    "id": 2458,
    "word": "soldier",
    "meaning": "군인",
    "level": "MidHigh"
  },
  {
    "id": 2459,
    "word": "sole",
    "meaning": "유일한",
    "level": "Extended"
  },
  {
    "id": 2460,
    "word": "solid",
    "meaning": "고체의",
    "level": "MidHigh"
  },
  {
    "id": 2461,
    "word": "solve",
    "meaning": "해결하다",
    "level": "MidHigh"
  },
  {
    "id": 2462,
    "word": "some",
    "meaning": "어떤",
    "level": "Elementary"
  },
  {
    "id": 2463,
    "word": "somewhat",
    "meaning": "다소",
    "level": "MidHigh"
  },
  {
    "id": 2464,
    "word": "son",
    "meaning": "아들",
    "level": "Elementary"
  },
  {
    "id": 2465,
    "word": "song",
    "meaning": "노래",
    "level": "Elementary"
  },
  {
    "id": 2466,
    "word": "soon",
    "meaning": "곧",
    "level": "MidHigh"
  },
  {
    "id": 2467,
    "word": "sophisticate",
    "meaning": "세련되게 하다",
    "level": "Extended"
  },
  {
    "id": 2468,
    "word": "sore",
    "meaning": "아픈",
    "level": "MidHigh"
  },
  {
    "id": 2469,
    "word": "sorry",
    "meaning": "미안한",
    "level": "Elementary"
  },
  {
    "id": 2470,
    "word": "sort",
    "meaning": "종류",
    "level": "MidHigh"
  },
  {
    "id": 2471,
    "word": "soul",
    "meaning": "영혼",
    "level": "MidHigh"
  },
  {
    "id": 2472,
    "word": "sound",
    "meaning": "소리",
    "level": "Elementary"
  },
  {
    "id": 2473,
    "word": "soup",
    "meaning": "수프",
    "level": "Elementary"
  },
  {
    "id": 2474,
    "word": "sour",
    "meaning": "신맛이 나는",
    "level": "MidHigh"
  },
  {
    "id": 2475,
    "word": "source",
    "meaning": "원천",
    "level": "MidHigh"
  },
  {
    "id": 2476,
    "word": "south",
    "meaning": "남쪽",
    "level": "Elementary"
  },
  {
    "id": 2477,
    "word": "space",
    "meaning": "공간",
    "level": "Elementary"
  },
  {
    "id": 2478,
    "word": "spaghetti",
    "meaning": "스파게티",
    "level": "Elementary"
  },
  {
    "id": 2479,
    "word": "span",
    "meaning": "기간",
    "level": "Extended"
  },
  {
    "id": 2480,
    "word": "spare",
    "meaning": "여분의",
    "level": "MidHigh"
  },
  {
    "id": 2481,
    "word": "spark",
    "meaning": "불꽃",
    "level": "Extended"
  },
  {
    "id": 2482,
    "word": "speak",
    "meaning": "말하다",
    "level": "Elementary"
  },
  {
    "id": 2483,
    "word": "species",
    "meaning": "종",
    "level": "MidHigh",
    "variation": "special"
  },
  {
    "id": 2484,
    "word": "specific",
    "meaning": "구체적인",
    "level": "MidHigh"
  },
  {
    "id": 2485,
    "word": "spectacle",
    "meaning": "광경",
    "level": "Extended"
  },
  {
    "id": 2486,
    "word": "spectrum",
    "meaning": "스펙트럼",
    "level": "Extended"
  },
  {
    "id": 2487,
    "word": "speech",
    "meaning": "연설",
    "level": "MidHigh"
  },
  {
    "id": 2488,
    "word": "speed",
    "meaning": "속도",
    "level": "Elementary"
  },
  {
    "id": 2489,
    "word": "spell",
    "meaning": "철자를 쓰다",
    "level": "MidHigh"
  },
  {
    "id": 2490,
    "word": "spend",
    "meaning": "쓰다",
    "level": "MidHigh"
  },
  {
    "id": 2491,
    "word": "sphere",
    "meaning": "구",
    "level": "Extended"
  },
  {
    "id": 2492,
    "word": "spill",
    "meaning": "쏟다",
    "level": "Extended"
  },
  {
    "id": 2493,
    "word": "spin",
    "meaning": "회전하다",
    "level": "MidHigh"
  },
  {
    "id": 2494,
    "word": "spirit",
    "meaning": "정신",
    "level": "MidHigh"
  },
  {
    "id": 2495,
    "word": "spit",
    "meaning": "침을 뱉다",
    "level": "Extended"
  },
  {
    "id": 2496,
    "word": "splash",
    "meaning": "튀기다",
    "level": "Extended"
  },
  {
    "id": 2497,
    "word": "split",
    "meaning": "나누다",
    "level": "Extended"
  },
  {
    "id": 2498,
    "word": "spoil",
    "meaning": "망치다",
    "level": "MidHigh"
  },
  {
    "id": 2499,
    "word": "sponsor",
    "meaning": "후원자",
    "level": "MidHigh"
  },
  {
    "id": 2500,
    "word": "spoon",
    "meaning": "숟가락",
    "level": "Elementary"
  },
  {
    "id": 2501,
    "word": "sport",
    "meaning": "운동",
    "level": "Elementary"
  },
  {
    "id": 2502,
    "word": "spot",
    "meaning": "장소",
    "level": "MidHigh"
  },
  {
    "id": 2503,
    "word": "spouse",
    "meaning": "배우자",
    "level": "Extended"
  },
  {
    "id": 2504,
    "word": "spray",
    "meaning": "뿌리다",
    "level": "MidHigh"
  },
  {
    "id": 2505,
    "word": "spread",
    "meaning": "퍼뜨리다",
    "level": "MidHigh"
  },
  {
    "id": 2506,
    "word": "spring",
    "meaning": "봄",
    "level": "Elementary"
  },
  {
    "id": 2507,
    "word": "spy",
    "meaning": "스파이",
    "level": "MidHigh"
  },
  {
    "id": 2508,
    "word": "square",
    "meaning": "정사각형",
    "level": "MidHigh"
  },
  {
    "id": 2509,
    "word": "squeeze",
    "meaning": "짜다",
    "level": "Extended"
  },
  {
    "id": 2510,
    "word": "stable",
    "meaning": "안정된",
    "level": "MidHigh"
  },
  {
    "id": 2511,
    "word": "stack",
    "meaning": "더미",
    "level": "Extended"
  },
  {
    "id": 2512,
    "word": "staff",
    "meaning": "직원",
    "level": "Elementary"
  },
  {
    "id": 2513,
    "word": "stage",
    "meaning": "무대",
    "level": "MidHigh"
  },
  {
    "id": 2514,
    "word": "stain",
    "meaning": "얼룩",
    "level": "Extended"
  },
  {
    "id": 2515,
    "word": "stairs",
    "meaning": "계단",
    "level": "MidHigh"
  },
  {
    "id": 2516,
    "word": "stamp",
    "meaning": "우표",
    "level": "MidHigh"
  },
  {
    "id": 2517,
    "word": "stand",
    "meaning": "서다",
    "level": "Elementary"
  },
  {
    "id": 2518,
    "word": "standard",
    "meaning": "표준",
    "level": "MidHigh"
  },
  {
    "id": 2519,
    "word": "star",
    "meaning": "별",
    "level": "Elementary"
  },
  {
    "id": 2520,
    "word": "stare",
    "meaning": "응시하다",
    "level": "MidHigh"
  },
  {
    "id": 2521,
    "word": "start",
    "meaning": "시작하다",
    "level": "Elementary"
  },
  {
    "id": 2522,
    "word": "starve",
    "meaning": "굶주리다",
    "level": "Extended"
  },
  {
    "id": 2523,
    "word": "state",
    "meaning": "상태",
    "level": "MidHigh"
  },
  {
    "id": 2524,
    "word": "station",
    "meaning": "역",
    "level": "MidHigh"
  },
  {
    "id": 2525,
    "word": "statistic",
    "meaning": "통계량",
    "level": "Extended"
  },
  {
    "id": 2526,
    "word": "statue",
    "meaning": "동상",
    "level": "Extended"
  },
  {
    "id": 2527,
    "word": "status",
    "meaning": "지위",
    "level": "Extended"
  },
  {
    "id": 2528,
    "word": "stay",
    "meaning": "머무르다",
    "level": "Elementary"
  },
  {
    "id": 2529,
    "word": "steady",
    "meaning": "꾸준한",
    "level": "MidHigh"
  },
  {
    "id": 2530,
    "word": "steak",
    "meaning": "스테이크",
    "level": "Elementary"
  },
  {
    "id": 2531,
    "word": "steal",
    "meaning": "훔치다",
    "level": "MidHigh"
  },
  {
    "id": 2532,
    "word": "steam",
    "meaning": "증기",
    "level": "MidHigh"
  },
  {
    "id": 2533,
    "word": "steel",
    "meaning": "강철",
    "level": "MidHigh"
  },
  {
    "id": 2534,
    "word": "steep",
    "meaning": "가파른",
    "level": "Extended"
  },
  {
    "id": 2535,
    "word": "stem",
    "meaning": "줄기",
    "level": "Extended"
  },
  {
    "id": 2536,
    "word": "step",
    "meaning": "걸음",
    "level": "MidHigh"
  },
  {
    "id": 2537,
    "word": "stick",
    "meaning": "막대기",
    "level": "MidHigh"
  },
  {
    "id": 2538,
    "word": "stiff",
    "meaning": "뻣뻣한",
    "level": "Extended"
  },
  {
    "id": 2539,
    "word": "still",
    "meaning": "여전히",
    "level": "MidHigh"
  },
  {
    "id": 2540,
    "word": "stimulate",
    "meaning": "자극하다",
    "level": "Extended"
  },
  {
    "id": 2541,
    "word": "stir",
    "meaning": "젓다",
    "level": "MidHigh"
  },
  {
    "id": 2542,
    "word": "stitch",
    "meaning": "바느질하다",
    "level": "Extended"
  },
  {
    "id": 2543,
    "word": "stock",
    "meaning": "재고",
    "level": "MidHigh"
  },
  {
    "id": 2544,
    "word": "stomach",
    "meaning": "위",
    "level": "MidHigh"
  },
  {
    "id": 2545,
    "word": "stone",
    "meaning": "돌",
    "level": "Elementary"
  },
  {
    "id": 2546,
    "word": "stop",
    "meaning": "멈추다",
    "level": "Elementary"
  },
  {
    "id": 2547,
    "word": "store",
    "meaning": "상점",
    "level": "Elementary"
  },
  {
    "id": 2548,
    "word": "storm",
    "meaning": "폭풍",
    "level": "MidHigh"
  },
  {
    "id": 2549,
    "word": "story",
    "meaning": "이야기",
    "level": "Elementary"
  },
  {
    "id": 2550,
    "word": "stove",
    "meaning": "난로",
    "level": "Extended"
  },
  {
    "id": 2551,
    "word": "straight",
    "meaning": "곧은",
    "level": "MidHigh"
  },
  {
    "id": 2552,
    "word": "strain",
    "meaning": "긴장",
    "level": "Extended"
  },
  {
    "id": 2553,
    "word": "strange",
    "meaning": "이상한",
    "level": "MidHigh"
  },
  {
    "id": 2554,
    "word": "strategy",
    "meaning": "전략",
    "level": "MidHigh"
  },
  {
    "id": 2555,
    "word": "strawberry",
    "meaning": "딸기",
    "level": "MidHigh"
  },
  {
    "id": 2556,
    "word": "stream",
    "meaning": "시내",
    "level": "MidHigh"
  },
  {
    "id": 2557,
    "word": "street",
    "meaning": "거리",
    "level": "Elementary"
  },
  {
    "id": 2558,
    "word": "stress",
    "meaning": "스트레스",
    "level": "MidHigh"
  },
  {
    "id": 2559,
    "word": "stretch",
    "meaning": "늘이다",
    "level": "MidHigh"
  },
  {
    "id": 2560,
    "word": "strict",
    "meaning": "엄격한",
    "level": "Extended"
  },
  {
    "id": 2561,
    "word": "strike",
    "meaning": "치다",
    "level": "MidHigh"
  },
  {
    "id": 2562,
    "word": "string",
    "meaning": "끈",
    "level": "MidHigh"
  },
  {
    "id": 2563,
    "word": "strip",
    "meaning": "벗기다",
    "level": "Extended"
  },
  {
    "id": 2564,
    "word": "stripe",
    "meaning": "줄무늬",
    "level": "Extended"
  },
  {
    "id": 2565,
    "word": "stroke",
    "meaning": "타격",
    "level": "Extended"
  },
  {
    "id": 2566,
    "word": "strong",
    "meaning": "강한",
    "level": "Elementary"
  },
  {
    "id": 2567,
    "word": "structure",
    "meaning": "구조",
    "level": "MidHigh"
  },
  {
    "id": 2568,
    "word": "struggle",
    "meaning": "분투하다",
    "level": "MidHigh"
  },
  {
    "id": 2569,
    "word": "studio",
    "meaning": "작업실",
    "level": "MidHigh"
  },
  {
    "id": 2570,
    "word": "study",
    "meaning": "공부하다",
    "level": "Elementary",
    "variation": "student"
  },
  {
    "id": 2571,
    "word": "stuff",
    "meaning": "물건",
    "level": "MidHigh"
  },
  {
    "id": 2572,
    "word": "style",
    "meaning": "방식",
    "level": "Elementary"
  },
  {
    "id": 2573,
    "word": "subject",
    "meaning": "주제",
    "level": "MidHigh",
    "variation": "subjective"
  },
  {
    "id": 2574,
    "word": "submarine",
    "meaning": "잠수함",
    "level": "Extended"
  },
  {
    "id": 2575,
    "word": "submit",
    "meaning": "제출하다",
    "level": "Extended",
    "variation": "submission"
  },
  {
    "id": 2576,
    "word": "subscribe",
    "meaning": "구독하다",
    "level": "Extended"
  },
  {
    "id": 2577,
    "word": "substance",
    "meaning": "물질",
    "level": "Extended",
    "variation": "substantial"
  },
  {
    "id": 2578,
    "word": "substitute",
    "meaning": "대체하다",
    "level": "Extended"
  },
  {
    "id": 2579,
    "word": "subtle",
    "meaning": "미묘한",
    "level": "Extended"
  },
  {
    "id": 2580,
    "word": "suburb",
    "meaning": "교외",
    "level": "Extended"
  },
  {
    "id": 2581,
    "word": "subway",
    "meaning": "지하철",
    "level": "Elementary"
  },
  {
    "id": 2582,
    "word": "succeed",
    "meaning": "성공하다",
    "level": "MidHigh"
  },
  {
    "id": 2583,
    "word": "success",
    "meaning": "성공",
    "level": "MidHigh"
  },
  {
    "id": 2584,
    "word": "such",
    "meaning": "그러한",
    "level": "MidHigh"
  },
  {
    "id": 2585,
    "word": "suck",
    "meaning": "빨다",
    "level": "Extended"
  },
  {
    "id": 2586,
    "word": "sudden",
    "meaning": "갑작스러운",
    "level": "MidHigh"
  },
  {
    "id": 2587,
    "word": "suffer",
    "meaning": "고통받다",
    "level": "MidHigh"
  },
  {
    "id": 2588,
    "word": "suffice",
    "meaning": "충분하다",
    "level": "Extended",
    "variation": "sufficient"
  },
  {
    "id": 2589,
    "word": "sugar",
    "meaning": "설탕",
    "level": "Elementary"
  },
  {
    "id": 2590,
    "word": "suggest",
    "meaning": "제안하다",
    "level": "MidHigh"
  },
  {
    "id": 2591,
    "word": "suicide",
    "meaning": "자살",
    "level": "Extended"
  },
  {
    "id": 2592,
    "word": "suit",
    "meaning": "정장",
    "level": "MidHigh"
  },
  {
    "id": 2593,
    "word": "suite",
    "meaning": "객실",
    "level": "Extended"
  },
  {
    "id": 2594,
    "word": "sum",
    "meaning": "합계",
    "level": "MidHigh",
    "variation": "summary"
  },
  {
    "id": 2595,
    "word": "summer",
    "meaning": "여름",
    "level": "Elementary"
  },
  {
    "id": 2596,
    "word": "summit",
    "meaning": "정상회담",
    "level": "Extended"
  },
  {
    "id": 2597,
    "word": "sun",
    "meaning": "태양",
    "level": "Elementary"
  },
  {
    "id": 2598,
    "word": "super",
    "meaning": "초월적인",
    "level": "MidHigh"
  },
  {
    "id": 2599,
    "word": "superb",
    "meaning": "훌륭한",
    "level": "Extended"
  },
  {
    "id": 2600,
    "word": "superior",
    "meaning": "우수한",
    "level": "Extended"
  },
  {
    "id": 2601,
    "word": "supervise",
    "meaning": "감독하다",
    "level": "Extended"
  },
  {
    "id": 2602,
    "word": "supper",
    "meaning": "저녁 식사",
    "level": "MidHigh"
  },
  {
    "id": 2603,
    "word": "supplement",
    "meaning": "보충하다",
    "level": "Extended"
  },
  {
    "id": 2604,
    "word": "supply",
    "meaning": "공급하다",
    "level": "MidHigh"
  },
  {
    "id": 2605,
    "word": "support",
    "meaning": "지원하다",
    "level": "MidHigh"
  },
  {
    "id": 2606,
    "word": "suppose",
    "meaning": "추측하다",
    "level": "MidHigh"
  },
  {
    "id": 2607,
    "word": "sure",
    "meaning": "확실한",
    "level": "Elementary",
    "variation": "ensure"
  },
  {
    "id": 2608,
    "word": "surface",
    "meaning": "표면",
    "level": "MidHigh"
  },
  {
    "id": 2609,
    "word": "surgery",
    "meaning": "수술",
    "level": "Extended"
  },
  {
    "id": 2610,
    "word": "surprise",
    "meaning": "놀라게 하다",
    "level": "MidHigh"
  },
  {
    "id": 2611,
    "word": "surrender",
    "meaning": "항복하다",
    "level": "Extended"
  },
  {
    "id": 2612,
    "word": "surround",
    "meaning": "둘러싸다",
    "level": "MidHigh"
  },
  {
    "id": 2613,
    "word": "survey",
    "meaning": "설문조사",
    "level": "MidHigh"
  },
  {
    "id": 2614,
    "word": "survive",
    "meaning": "살아남다",
    "level": "MidHigh"
  },
  {
    "id": 2615,
    "word": "suspect",
    "meaning": "의심하다",
    "level": "MidHigh"
  },
  {
    "id": 2616,
    "word": "suspend",
    "meaning": "중지하다",
    "level": "Extended"
  },
  {
    "id": 2617,
    "word": "sustain",
    "meaning": "유지하다",
    "level": "Extended"
  },
  {
    "id": 2618,
    "word": "swallow",
    "meaning": "삼키다",
    "level": "MidHigh"
  },
  {
    "id": 2619,
    "word": "swear",
    "meaning": "맹세하다",
    "level": "Extended"
  },
  {
    "id": 2620,
    "word": "sweat",
    "meaning": "땀",
    "level": "Extended"
  },
  {
    "id": 2621,
    "word": "sweater",
    "meaning": "스웨터",
    "level": "MidHigh"
  },
  {
    "id": 2622,
    "word": "sweep",
    "meaning": "쓸다",
    "level": "MidHigh"
  },
  {
    "id": 2623,
    "word": "sweet",
    "meaning": "달콤한",
    "level": "MidHigh"
  },
  {
    "id": 2624,
    "word": "swell",
    "meaning": "부풀다",
    "level": "Extended"
  },
  {
    "id": 2625,
    "word": "swift",
    "meaning": "빠른",
    "level": "Extended"
  },
  {
    "id": 2626,
    "word": "swim",
    "meaning": "수영하다",
    "level": "Elementary"
  },
  {
    "id": 2627,
    "word": "swing",
    "meaning": "흔들다",
    "level": "MidHigh"
  },
  {
    "id": 2628,
    "word": "switch",
    "meaning": "전환하다",
    "level": "MidHigh"
  },
  {
    "id": 2629,
    "word": "symbol",
    "meaning": "상징",
    "level": "Extended"
  },
  {
    "id": 2630,
    "word": "sympathy",
    "meaning": "동정심",
    "level": "Extended"
  },
  {
    "id": 2631,
    "word": "symphony",
    "meaning": "교향곡",
    "level": "Extended"
  },
  {
    "id": 2632,
    "word": "symptom",
    "meaning": "증상",
    "level": "Extended"
  },
  {
    "id": 2633,
    "word": "system",
    "meaning": "체계",
    "level": "MidHigh"
  },
  {
    "id": 2634,
    "word": "table",
    "meaning": "탁자",
    "level": "Elementary"
  },
  {
    "id": 2635,
    "word": "tackle",
    "meaning": "해결하다",
    "level": "Extended"
  },
  {
    "id": 2636,
    "word": "tag",
    "meaning": "꼬리표",
    "level": "Extended"
  },
  {
    "id": 2637,
    "word": "tail",
    "meaning": "꼬리",
    "level": "Elementary"
  },
  {
    "id": 2638,
    "word": "take",
    "meaning": "가지다",
    "level": "Elementary",
    "variation": "mistake"
  },
  {
    "id": 2639,
    "word": "tale",
    "meaning": "이야기",
    "level": "MidHigh"
  },
  {
    "id": 2640,
    "word": "talent",
    "meaning": "재능",
    "level": "Extended"
  },
  {
    "id": 2641,
    "word": "talk",
    "meaning": "말하다",
    "level": "Elementary"
  },
  {
    "id": 2642,
    "word": "tall",
    "meaning": "키가 큰",
    "level": "Elementary"
  },
  {
    "id": 2643,
    "word": "tank",
    "meaning": "탱크",
    "level": "MidHigh"
  },
  {
    "id": 2644,
    "word": "tap",
    "meaning": "가볍게 두드리다",
    "level": "MidHigh"
  },
  {
    "id": 2645,
    "word": "tape",
    "meaning": "테이프",
    "level": "Elementary"
  },
  {
    "id": 2646,
    "word": "target",
    "meaning": "표적",
    "level": "MidHigh"
  },
  {
    "id": 2647,
    "word": "task",
    "meaning": "과제",
    "level": "Extended"
  },
  {
    "id": 2648,
    "word": "taste",
    "meaning": "맛",
    "level": "Elementary"
  },
  {
    "id": 2649,
    "word": "tax",
    "meaning": "세금",
    "level": "MidHigh"
  },
  {
    "id": 2650,
    "word": "taxi",
    "meaning": "택시",
    "level": "Elementary"
  },
  {
    "id": 2651,
    "word": "tea",
    "meaning": "차",
    "level": "MidHigh"
  },
  {
    "id": 2652,
    "word": "teach",
    "meaning": "가르치다",
    "level": "Elementary"
  },
  {
    "id": 2653,
    "word": "team",
    "meaning": "팀",
    "level": "Elementary"
  },
  {
    "id": 2654,
    "word": "tear",
    "meaning": "찢다",
    "level": "MidHigh"
  },
  {
    "id": 2655,
    "word": "tease",
    "meaning": "놀리다",
    "level": "Extended"
  },
  {
    "id": 2656,
    "word": "technique",
    "meaning": "기술",
    "level": "MidHigh",
    "variation": "technic"
  },
  {
    "id": 2657,
    "word": "technology",
    "meaning": "과학 기술",
    "level": "MidHigh"
  },
  {
    "id": 2658,
    "word": "teenage",
    "meaning": "십대의",
    "level": "MidHigh"
  },
  {
    "id": 2659,
    "word": "telegraph",
    "meaning": "전신",
    "level": "Extended"
  },
  {
    "id": 2660,
    "word": "telephone",
    "meaning": "전화",
    "level": "Elementary",
    "variation": "phone"
  },
  {
    "id": 2661,
    "word": "television",
    "meaning": "텔레비전",
    "level": "Elementary"
  },
  {
    "id": 2662,
    "word": "tell",
    "meaning": "말하다",
    "level": "Elementary"
  },
  {
    "id": 2663,
    "word": "temperature",
    "meaning": "온도",
    "level": "MidHigh"
  },
  {
    "id": 2664,
    "word": "temple",
    "meaning": "사원",
    "level": "Extended"
  },
  {
    "id": 2665,
    "word": "temporary",
    "meaning": "일시적인",
    "level": "Extended"
  },
  {
    "id": 2666,
    "word": "tempt",
    "meaning": "유혹하다",
    "level": "Extended"
  },
  {
    "id": 2667,
    "word": "ten",
    "meaning": "열",
    "level": "Elementary"
  },
  {
    "id": 2668,
    "word": "tenant",
    "meaning": "세입자",
    "level": "Extended"
  },
  {
    "id": 2669,
    "word": "tend",
    "meaning": "~하는 경향이 있다",
    "level": "MidHigh"
  },
  {
    "id": 2670,
    "word": "tender",
    "meaning": "부드러운",
    "level": "Extended"
  },
  {
    "id": 2671,
    "word": "tennis",
    "meaning": "테니스",
    "level": "Elementary"
  },
  {
    "id": 2672,
    "word": "tense",
    "meaning": "긴장된",
    "level": "MidHigh"
  },
  {
    "id": 2673,
    "word": "tent",
    "meaning": "천막",
    "level": "Elementary"
  },
  {
    "id": 2674,
    "word": "term",
    "meaning": "용어",
    "level": "MidHigh"
  },
  {
    "id": 2675,
    "word": "terminal",
    "meaning": "종착역",
    "level": "Extended"
  },
  {
    "id": 2676,
    "word": "terminate",
    "meaning": "종결하다",
    "level": "Extended"
  },
  {
    "id": 2677,
    "word": "terrace",
    "meaning": "테라스",
    "level": "Extended"
  },
  {
    "id": 2678,
    "word": "terrible",
    "meaning": "끔찍한",
    "level": "MidHigh"
  },
  {
    "id": 2679,
    "word": "terrific",
    "meaning": "굉장한",
    "level": "Extended"
  },
  {
    "id": 2680,
    "word": "territory",
    "meaning": "영토",
    "level": "Extended"
  },
  {
    "id": 2681,
    "word": "terror",
    "meaning": "공포",
    "level": "Extended",
    "variation": "terrorist"
  },
  {
    "id": 2682,
    "word": "test",
    "meaning": "시험",
    "level": "Elementary"
  },
  {
    "id": 2683,
    "word": "text",
    "meaning": "글",
    "level": "MidHigh"
  },
  {
    "id": 2684,
    "word": "textbook",
    "meaning": "교과서",
    "level": "Elementary"
  },
  {
    "id": 2685,
    "word": "than",
    "meaning": "~보다",
    "level": "Elementary"
  },
  {
    "id": 2686,
    "word": "thank",
    "meaning": "감사하다",
    "level": "Elementary"
  },
  {
    "id": 2687,
    "word": "that",
    "meaning": "저것",
    "level": "Elementary"
  },
  {
    "id": 2688,
    "word": "the",
    "meaning": "그",
    "level": "Elementary"
  },
  {
    "id": 2689,
    "word": "theater",
    "meaning": "극장",
    "level": "MidHigh",
    "variation": "theatre"
  },
  {
    "id": 2690,
    "word": "theme",
    "meaning": "주제",
    "level": "Extended"
  },
  {
    "id": 2691,
    "word": "then",
    "meaning": "그때",
    "level": "MidHigh"
  },
  {
    "id": 2692,
    "word": "theory",
    "meaning": "이론",
    "level": "MidHigh"
  },
  {
    "id": 2693,
    "word": "therapy",
    "meaning": "치료",
    "level": "Extended"
  },
  {
    "id": 2694,
    "word": "there",
    "meaning": "거기에",
    "level": "Elementary"
  },
  {
    "id": 2695,
    "word": "therefore",
    "meaning": "그러므로",
    "level": "MidHigh"
  },
  {
    "id": 2696,
    "word": "they",
    "meaning": "그들",
    "level": "Elementary"
  },
  {
    "id": 2697,
    "word": "thick",
    "meaning": "두꺼운",
    "level": "MidHigh"
  },
  {
    "id": 2698,
    "word": "thief",
    "meaning": "도둑",
    "level": "MidHigh"
  },
  {
    "id": 2699,
    "word": "thin",
    "meaning": "얇은",
    "level": "MidHigh"
  },
  {
    "id": 2700,
    "word": "thing",
    "meaning": "것",
    "level": "Elementary"
  },
  {
    "id": 2701,
    "word": "think",
    "meaning": "생각하다",
    "level": "Elementary"
  },
  {
    "id": 2702,
    "word": "third",
    "meaning": "세 번째",
    "level": "Elementary"
  },
  {
    "id": 2703,
    "word": "thirst",
    "meaning": "갈증",
    "level": "Elementary"
  },
  {
    "id": 2704,
    "word": "thirteen",
    "meaning": "열셋",
    "level": "Elementary"
  },
  {
    "id": 2705,
    "word": "thirty",
    "meaning": "서른",
    "level": "Elementary"
  },
  {
    "id": 2706,
    "word": "this",
    "meaning": "이것",
    "level": "Elementary"
  },
  {
    "id": 2707,
    "word": "thorough",
    "meaning": "철저한",
    "level": "Extended"
  },
  {
    "id": 2708,
    "word": "though",
    "meaning": "비록",
    "level": "MidHigh"
  },
  {
    "id": 2709,
    "word": "thousand",
    "meaning": "천",
    "level": "MidHigh"
  },
  {
    "id": 2710,
    "word": "thread",
    "meaning": "실",
    "level": "Extended"
  },
  {
    "id": 2711,
    "word": "threat",
    "meaning": "위협",
    "level": "MidHigh"
  },
  {
    "id": 2712,
    "word": "three",
    "meaning": "셋",
    "level": "Elementary"
  },
  {
    "id": 2713,
    "word": "thrill",
    "meaning": "전율",
    "level": "Extended"
  },
  {
    "id": 2714,
    "word": "throat",
    "meaning": "목구멍",
    "level": "MidHigh"
  },
  {
    "id": 2715,
    "word": "through",
    "meaning": "~을 통하여",
    "level": "MidHigh"
  },
  {
    "id": 2716,
    "word": "throw",
    "meaning": "던지다",
    "level": "MidHigh"
  },
  {
    "id": 2717,
    "word": "thumb",
    "meaning": "엄지손가락",
    "level": "Extended"
  },
  {
    "id": 2718,
    "word": "thus",
    "meaning": "따라서",
    "level": "MidHigh"
  },
  {
    "id": 2719,
    "word": "tick",
    "meaning": "째깍거리다",
    "level": "Extended"
  },
  {
    "id": 2720,
    "word": "ticket",
    "meaning": "표",
    "level": "Elementary"
  },
  {
    "id": 2721,
    "word": "tide",
    "meaning": "조수",
    "level": "MidHigh",
    "variation": "tidy"
  },
  {
    "id": 2722,
    "word": "tie",
    "meaning": "묶다",
    "level": "MidHigh"
  },
  {
    "id": 2723,
    "word": "tiger",
    "meaning": "호랑이",
    "level": "Elementary"
  },
  {
    "id": 2724,
    "word": "tight",
    "meaning": "꽉 끼는",
    "level": "MidHigh"
  },
  {
    "id": 2725,
    "word": "till",
    "meaning": "~까지",
    "level": "MidHigh"
  },
  {
    "id": 2726,
    "word": "timber",
    "meaning": "목재",
    "level": "Extended"
  },
  {
    "id": 2727,
    "word": "time",
    "meaning": "시간",
    "level": "Elementary"
  },
  {
    "id": 2728,
    "word": "tin",
    "meaning": "주석",
    "level": "MidHigh"
  },
  {
    "id": 2729,
    "word": "tiny",
    "meaning": "아주 작은",
    "level": "MidHigh"
  },
  {
    "id": 2730,
    "word": "tip",
    "meaning": "끝",
    "level": "MidHigh"
  },
  {
    "id": 2731,
    "word": "tire",
    "meaning": "피곤하게 하다",
    "level": "Elementary",
    "variation": "tired"
  },
  {
    "id": 2732,
    "word": "tissue",
    "meaning": "조직",
    "level": "Extended"
  },
  {
    "id": 2733,
    "word": "title",
    "meaning": "제목",
    "level": "MidHigh",
    "variation": "entitle"
  },
  {
    "id": 2734,
    "word": "to",
    "meaning": "~에",
    "level": "Elementary"
  },
  {
    "id": 2735,
    "word": "toast",
    "meaning": "토스트",
    "level": "MidHigh"
  },
  {
    "id": 2736,
    "word": "today",
    "meaning": "오늘",
    "level": "Elementary"
  },
  {
    "id": 2737,
    "word": "toe",
    "meaning": "발가락",
    "level": "MidHigh"
  },
  {
    "id": 2738,
    "word": "together",
    "meaning": "함께",
    "level": "Elementary"
  },
  {
    "id": 2739,
    "word": "toilet",
    "meaning": "화장실",
    "level": "MidHigh"
  },
  {
    "id": 2740,
    "word": "tomato",
    "meaning": "토마토",
    "level": "Elementary"
  },
  {
    "id": 2741,
    "word": "tomorrow",
    "meaning": "내일",
    "level": "Elementary"
  },
  {
    "id": 2742,
    "word": "tone",
    "meaning": "어조",
    "level": "MidHigh"
  },
  {
    "id": 2743,
    "word": "tongue",
    "meaning": "혀",
    "level": "MidHigh"
  },
  {
    "id": 2744,
    "word": "tonight",
    "meaning": "오늘 밤",
    "level": "Elementary"
  },
  {
    "id": 2745,
    "word": "too",
    "meaning": "너무",
    "level": "Elementary"
  },
  {
    "id": 2746,
    "word": "tool",
    "meaning": "도구",
    "level": "MidHigh"
  },
  {
    "id": 2747,
    "word": "tooth",
    "meaning": "이",
    "level": "Elementary"
  },
  {
    "id": 2748,
    "word": "top",
    "meaning": "꼭대기",
    "level": "Elementary"
  },
  {
    "id": 2749,
    "word": "topic",
    "meaning": "주제",
    "level": "MidHigh"
  },
  {
    "id": 2750,
    "word": "torture",
    "meaning": "고문",
    "level": "Extended"
  },
  {
    "id": 2751,
    "word": "toss",
    "meaning": "던지다",
    "level": "Extended"
  },
  {
    "id": 2752,
    "word": "total",
    "meaning": "전체의",
    "level": "MidHigh"
  },
  {
    "id": 2753,
    "word": "touch",
    "meaning": "만지다",
    "level": "Elementary"
  },
  {
    "id": 2754,
    "word": "tough",
    "meaning": "힘든",
    "level": "MidHigh"
  },
  {
    "id": 2755,
    "word": "tour",
    "meaning": "여행",
    "level": "MidHigh"
  },
  {
    "id": 2756,
    "word": "toward",
    "meaning": "~쪽으로",
    "level": "MidHigh",
    "variation": "towards"
  },
  {
    "id": 2757,
    "word": "towel",
    "meaning": "수건",
    "level": "MidHigh"
  },
  {
    "id": 2758,
    "word": "tower",
    "meaning": "탑",
    "level": "MidHigh"
  },
  {
    "id": 2759,
    "word": "town",
    "meaning": "마을",
    "level": "Elementary"
  },
  {
    "id": 2760,
    "word": "toxic",
    "meaning": "독성의",
    "level": "Extended"
  },
  {
    "id": 2761,
    "word": "toy",
    "meaning": "장난감",
    "level": "Elementary"
  },
  {
    "id": 2762,
    "word": "trace",
    "meaning": "흔적",
    "level": "MidHigh"
  },
  {
    "id": 2763,
    "word": "track",
    "meaning": "자취",
    "level": "Elementary"
  },
  {
    "id": 2764,
    "word": "trade",
    "meaning": "무역",
    "level": "MidHigh"
  },
  {
    "id": 2765,
    "word": "tradition",
    "meaning": "전통",
    "level": "MidHigh"
  },
  {
    "id": 2766,
    "word": "traffic",
    "meaning": "교통",
    "level": "MidHigh"
  },
  {
    "id": 2767,
    "word": "tragic",
    "meaning": "비극적인",
    "level": "Extended"
  },
  {
    "id": 2768,
    "word": "trail",
    "meaning": "오솔길",
    "level": "Extended"
  },
  {
    "id": 2769,
    "word": "train",
    "meaning": "기차",
    "level": "Elementary"
  },
  {
    "id": 2770,
    "word": "transact",
    "meaning": "거래하다",
    "level": "Extended"
  },
  {
    "id": 2771,
    "word": "transfer",
    "meaning": "옮기다",
    "level": "MidHigh"
  },
  {
    "id": 2772,
    "word": "transform",
    "meaning": "변형시키다",
    "level": "Extended"
  },
  {
    "id": 2773,
    "word": "transition",
    "meaning": "전환",
    "level": "Extended"
  },
  {
    "id": 2774,
    "word": "translate",
    "meaning": "번역하다",
    "level": "Extended"
  },
  {
    "id": 2775,
    "word": "transmit",
    "meaning": "전달하다",
    "level": "Extended"
  },
  {
    "id": 2776,
    "word": "transport",
    "meaning": "수송하다",
    "level": "MidHigh",
    "variation": "transportation"
  },
  {
    "id": 2777,
    "word": "trap",
    "meaning": "덫",
    "level": "MidHigh"
  },
  {
    "id": 2778,
    "word": "travel",
    "meaning": "여행하다",
    "level": "Elementary"
  },
  {
    "id": 2779,
    "word": "tray",
    "meaning": "쟁반",
    "level": "MidHigh"
  },
  {
    "id": 2780,
    "word": "treasure",
    "meaning": "보물",
    "level": "Extended"
  },
  {
    "id": 2781,
    "word": "treat",
    "meaning": "대우하다",
    "level": "MidHigh"
  },
  {
    "id": 2782,
    "word": "treaty",
    "meaning": "조약",
    "level": "Extended"
  },
  {
    "id": 2783,
    "word": "tree",
    "meaning": "나무",
    "level": "Elementary"
  },
  {
    "id": 2784,
    "word": "tremendous",
    "meaning": "엄청난",
    "level": "Extended"
  },
  {
    "id": 2785,
    "word": "trend",
    "meaning": "경향",
    "level": "Extended"
  },
  {
    "id": 2786,
    "word": "triangle",
    "meaning": "삼각형",
    "level": "MidHigh"
  },
  {
    "id": 2787,
    "word": "tribe",
    "meaning": "부족",
    "level": "Extended"
  },
  {
    "id": 2788,
    "word": "trick",
    "meaning": "속임수",
    "level": "MidHigh"
  },
  {
    "id": 2789,
    "word": "trigger",
    "meaning": "촉발하다",
    "level": "Extended"
  },
  {
    "id": 2790,
    "word": "trim",
    "meaning": "다듬다",
    "level": "Extended"
  },
  {
    "id": 2791,
    "word": "trip",
    "meaning": "여행",
    "level": "Elementary"
  },
  {
    "id": 2792,
    "word": "triumph",
    "meaning": "승리",
    "level": "Extended"
  },
  {
    "id": 2793,
    "word": "troop",
    "meaning": "부대",
    "level": "Extended"
  },
  {
    "id": 2794,
    "word": "trouble",
    "meaning": "문제",
    "level": "MidHigh"
  },
  {
    "id": 2795,
    "word": "truck",
    "meaning": "트럭",
    "level": "Elementary"
  },
  {
    "id": 2796,
    "word": "true",
    "meaning": "진실한",
    "level": "Elementary"
  },
  {
    "id": 2797,
    "word": "trunk",
    "meaning": "줄기",
    "level": "MidHigh"
  },
  {
    "id": 2798,
    "word": "trust",
    "meaning": "신뢰하다",
    "level": "MidHigh"
  },
  {
    "id": 2799,
    "word": "truth",
    "meaning": "진실",
    "level": "MidHigh"
  },
  {
    "id": 2800,
    "word": "try",
    "meaning": "시도하다",
    "level": "Elementary",
    "variation": "trial"
  },
  {
    "id": 2801,
    "word": "tube",
    "meaning": "관",
    "level": "Extended"
  },
  {
    "id": 2802,
    "word": "tune",
    "meaning": "곡조",
    "level": "MidHigh"
  },
  {
    "id": 2803,
    "word": "tunnel",
    "meaning": "터널",
    "level": "Extended"
  },
  {
    "id": 2804,
    "word": "turn",
    "meaning": "돌다",
    "level": "Elementary"
  },
  {
    "id": 2805,
    "word": "turnover",
    "meaning": "이직률",
    "level": "Extended"
  },
  {
    "id": 2806,
    "word": "twelve",
    "meaning": "열둘",
    "level": "Elementary"
  },
  {
    "id": 2807,
    "word": "twenty",
    "meaning": "스물",
    "level": "Elementary"
  },
  {
    "id": 2808,
    "word": "twenty-first",
    "meaning": "스물한 번째",
    "level": "Elementary"
  },
  {
    "id": 2809,
    "word": "twenty-second",
    "meaning": "스물두 번째",
    "level": "Elementary"
  },
  {
    "id": 2810,
    "word": "twenty-third",
    "meaning": "스물세 번째",
    "level": "Elementary"
  },
  {
    "id": 2811,
    "word": "twice",
    "meaning": "두 번",
    "level": "Elementary"
  },
  {
    "id": 2812,
    "word": "twin",
    "meaning": "쌍둥이",
    "level": "MidHigh"
  },
  {
    "id": 2813,
    "word": "twist",
    "meaning": "비틀다",
    "level": "MidHigh"
  },
  {
    "id": 2814,
    "word": "two",
    "meaning": "둘",
    "level": "Elementary"
  },
  {
    "id": 2815,
    "word": "type",
    "meaning": "유형",
    "level": "Elementary"
  },
  {
    "id": 2816,
    "word": "ugly",
    "meaning": "못생긴",
    "level": "Elementary"
  },
  {
    "id": 2817,
    "word": "ultimate",
    "meaning": "궁극적인",
    "level": "Extended"
  },
  {
    "id": 2818,
    "word": "umbrella",
    "meaning": "우산",
    "level": "Elementary"
  },
  {
    "id": 2819,
    "word": "uncle",
    "meaning": "삼촌",
    "level": "Elementary"
  },
  {
    "id": 2820,
    "word": "under",
    "meaning": "아래에",
    "level": "Elementary"
  },
  {
    "id": 2821,
    "word": "undergo",
    "meaning": "겪다",
    "level": "Extended"
  },
  {
    "id": 2822,
    "word": "underlie",
    "meaning": "기저를 이루다",
    "level": "Extended"
  },
  {
    "id": 2823,
    "word": "undermine",
    "meaning": "약화시키다",
    "level": "Extended"
  },
  {
    "id": 2824,
    "word": "understand",
    "meaning": "이해하다",
    "level": "Elementary"
  },
  {
    "id": 2825,
    "word": "undertake",
    "meaning": "떠맡다",
    "level": "Extended"
  },
  {
    "id": 2826,
    "word": "uniform",
    "meaning": "제복",
    "level": "MidHigh"
  },
  {
    "id": 2827,
    "word": "unify",
    "meaning": "통합하다",
    "level": "Extended"
  },
  {
    "id": 2828,
    "word": "unique",
    "meaning": "독특한",
    "level": "Extended"
  },
  {
    "id": 2829,
    "word": "unit",
    "meaning": "단위",
    "level": "MidHigh"
  },
  {
    "id": 2830,
    "word": "unite",
    "meaning": "연합하다",
    "level": "MidHigh",
    "variation": "union"
  },
  {
    "id": 2831,
    "word": "universe",
    "meaning": "우주",
    "level": "Extended"
  },
  {
    "id": 2832,
    "word": "university",
    "meaning": "대학교",
    "level": "MidHigh"
  },
  {
    "id": 2833,
    "word": "unless",
    "meaning": "~하지 않는 한",
    "level": "MidHigh"
  },
  {
    "id": 2834,
    "word": "until",
    "meaning": "~까지",
    "level": "MidHigh"
  },
  {
    "id": 2835,
    "word": "up",
    "meaning": "위로",
    "level": "Elementary"
  },
  {
    "id": 2836,
    "word": "update",
    "meaning": "갱신하다",
    "level": "Extended"
  },
  {
    "id": 2837,
    "word": "upon",
    "meaning": "~위에",
    "level": "MidHigh"
  },
  {
    "id": 2838,
    "word": "upper",
    "meaning": "위쪽의",
    "level": "MidHigh"
  },
  {
    "id": 2839,
    "word": "upset",
    "meaning": "속상하게 하다",
    "level": "MidHigh"
  },
  {
    "id": 2840,
    "word": "upward",
    "meaning": "위쪽으로",
    "level": "Extended",
    "variation": "upwards"
  },
  {
    "id": 2841,
    "word": "urban",
    "meaning": "도시의",
    "level": "Extended"
  },
  {
    "id": 2842,
    "word": "urge",
    "meaning": "촉구하다",
    "level": "Extended",
    "variation": "urgent"
  },
  {
    "id": 2843,
    "word": "use",
    "meaning": "사용하다",
    "level": "Elementary",
    "variation": "usual"
  },
  {
    "id": 2844,
    "word": "utilize",
    "meaning": "활용하다",
    "level": "Extended",
    "variation": "utilise"
  },
  {
    "id": 2845,
    "word": "utter",
    "meaning": "말을 내뱉다",
    "level": "Extended"
  },
  {
    "id": 2846,
    "word": "vacate",
    "meaning": "비우다",
    "level": "Extended",
    "variation": "vacation"
  },
  {
    "id": 2847,
    "word": "vaccine",
    "meaning": "백신",
    "level": "Extended"
  },
  {
    "id": 2848,
    "word": "vacuum",
    "meaning": "진공",
    "level": "Extended"
  },
  {
    "id": 2849,
    "word": "vague",
    "meaning": "막연한",
    "level": "Extended"
  },
  {
    "id": 2850,
    "word": "valid",
    "meaning": "유효한",
    "level": "Extended"
  },
  {
    "id": 2851,
    "word": "valley",
    "meaning": "계곡",
    "level": "MidHigh"
  },
  {
    "id": 2852,
    "word": "value",
    "meaning": "가치",
    "level": "MidHigh"
  },
  {
    "id": 2853,
    "word": "van",
    "meaning": "승합차",
    "level": "MidHigh"
  },
  {
    "id": 2854,
    "word": "vanish",
    "meaning": "사라지다",
    "level": "Extended"
  },
  {
    "id": 2855,
    "word": "various",
    "meaning": "다양한",
    "level": "MidHigh"
  },
  {
    "id": 2856,
    "word": "vary",
    "meaning": "달라지다",
    "level": "MidHigh"
  },
  {
    "id": 2857,
    "word": "vast",
    "meaning": "광대한",
    "level": "Extended"
  },
  {
    "id": 2858,
    "word": "vegetable",
    "meaning": "채소",
    "level": "Elementary"
  },
  {
    "id": 2859,
    "word": "vehicle",
    "meaning": "차량",
    "level": "MidHigh"
  },
  {
    "id": 2860,
    "word": "venture",
    "meaning": "모험",
    "level": "Extended"
  },
  {
    "id": 2861,
    "word": "verb",
    "meaning": "동사",
    "level": "Extended",
    "variation": "verbal"
  },
  {
    "id": 2862,
    "word": "verse",
    "meaning": "시구",
    "level": "Extended"
  },
  {
    "id": 2863,
    "word": "version",
    "meaning": "판",
    "level": "MidHigh"
  },
  {
    "id": 2864,
    "word": "versus",
    "meaning": "~대",
    "level": "Extended"
  },
  {
    "id": 2865,
    "word": "vertical",
    "meaning": "수직의",
    "level": "Extended"
  },
  {
    "id": 2866,
    "word": "very",
    "meaning": "매우",
    "level": "Elementary"
  },
  {
    "id": 2867,
    "word": "vessel",
    "meaning": "배",
    "level": "Extended"
  },
  {
    "id": 2868,
    "word": "veterinarian",
    "meaning": "수의사",
    "level": "Extended"
  },
  {
    "id": 2869,
    "word": "via",
    "meaning": "~을 거쳐",
    "level": "Extended"
  },
  {
    "id": 2870,
    "word": "vice",
    "meaning": "악덕",
    "level": "Extended"
  },
  {
    "id": 2871,
    "word": "victim",
    "meaning": "희생자",
    "level": "MidHigh"
  },
  {
    "id": 2872,
    "word": "victory",
    "meaning": "승리",
    "level": "Extended"
  },
  {
    "id": 2873,
    "word": "video",
    "meaning": "동영상",
    "level": "Elementary"
  },
  {
    "id": 2874,
    "word": "view",
    "meaning": "관점",
    "level": "MidHigh",
    "variation": "interview, review"
  },
  {
    "id": 2875,
    "word": "vigor",
    "meaning": "활력",
    "level": "Extended",
    "variation": "vigorous"
  },
  {
    "id": 2876,
    "word": "villa",
    "meaning": "별장",
    "level": "MidHigh"
  },
  {
    "id": 2877,
    "word": "village",
    "meaning": "마을",
    "level": "MidHigh"
  },
  {
    "id": 2878,
    "word": "violent",
    "meaning": "폭력적인",
    "level": "MidHigh"
  },
  {
    "id": 2879,
    "word": "violin",
    "meaning": "바이올린",
    "level": "Elementary"
  },
  {
    "id": 2880,
    "word": "virgin",
    "meaning": "처녀",
    "level": "Extended"
  },
  {
    "id": 2881,
    "word": "virtue",
    "meaning": "미덕",
    "level": "Extended",
    "variation": "virtual"
  },
  {
    "id": 2882,
    "word": "virus",
    "meaning": "바이러스",
    "level": "Extended"
  },
  {
    "id": 2883,
    "word": "visible",
    "meaning": "보이는",
    "level": "Extended"
  },
  {
    "id": 2884,
    "word": "vision",
    "meaning": "시야",
    "level": "MidHigh"
  },
  {
    "id": 2885,
    "word": "visit",
    "meaning": "방문하다",
    "level": "Elementary"
  },
  {
    "id": 2886,
    "word": "visual",
    "meaning": "시각의",
    "level": "Extended"
  },
  {
    "id": 2887,
    "word": "vital",
    "meaning": "필수적인",
    "level": "Extended"
  },
  {
    "id": 2888,
    "word": "vivid",
    "meaning": "생생한",
    "level": "Extended"
  },
  {
    "id": 2889,
    "word": "vocabulary",
    "meaning": "어휘",
    "level": "Extended"
  },
  {
    "id": 2890,
    "word": "vocation",
    "meaning": "직업",
    "level": "Extended"
  },
  {
    "id": 2891,
    "word": "voice",
    "meaning": "목소리",
    "level": "Elementary"
  },
  {
    "id": 2892,
    "word": "volume",
    "meaning": "음량",
    "level": "MidHigh"
  },
  {
    "id": 2893,
    "word": "volunteer",
    "meaning": "자원봉사자",
    "level": "MidHigh"
  },
  {
    "id": 2894,
    "word": "vote",
    "meaning": "투표하다",
    "level": "MidHigh"
  },
  {
    "id": 2895,
    "word": "wage",
    "meaning": "임금",
    "level": "MidHigh"
  },
  {
    "id": 2896,
    "word": "wait",
    "meaning": "기다리다",
    "level": "Elementary"
  },
  {
    "id": 2897,
    "word": "wake",
    "meaning": "깨다",
    "level": "Elementary"
  },
  {
    "id": 2898,
    "word": "walk",
    "meaning": "걷다",
    "level": "Elementary"
  },
  {
    "id": 2899,
    "word": "wall",
    "meaning": "벽",
    "level": "Elementary"
  },
  {
    "id": 2900,
    "word": "wander",
    "meaning": "돌아다니다",
    "level": "Extended"
  },
  {
    "id": 2901,
    "word": "want",
    "meaning": "원하다",
    "level": "Elementary"
  },
  {
    "id": 2902,
    "word": "war",
    "meaning": "전쟁",
    "level": "Elementary"
  },
  {
    "id": 2903,
    "word": "warehouse",
    "meaning": "창고",
    "level": "Extended"
  },
  {
    "id": 2904,
    "word": "warm",
    "meaning": "따뜻한",
    "level": "Elementary"
  },
  {
    "id": 2905,
    "word": "warn",
    "meaning": "경고하다",
    "level": "MidHigh"
  },
  {
    "id": 2906,
    "word": "warrant",
    "meaning": "정당화하다",
    "level": "Extended"
  },
  {
    "id": 2907,
    "word": "wash",
    "meaning": "씻다",
    "level": "Elementary"
  },
  {
    "id": 2908,
    "word": "waste",
    "meaning": "낭비",
    "level": "MidHigh"
  },
  {
    "id": 2909,
    "word": "watch",
    "meaning": "보다",
    "level": "Elementary"
  },
  {
    "id": 2910,
    "word": "water",
    "meaning": "물",
    "level": "Elementary"
  },
  {
    "id": 2911,
    "word": "watermelon",
    "meaning": "수박",
    "level": "Elementary"
  },
  {
    "id": 2912,
    "word": "wave",
    "meaning": "파도",
    "level": "MidHigh"
  },
  {
    "id": 2913,
    "word": "way",
    "meaning": "길",
    "level": "Elementary"
  },
  {
    "id": 2914,
    "word": "we",
    "meaning": "우리",
    "level": "Elementary"
  },
  {
    "id": 2915,
    "word": "weak",
    "meaning": "약한",
    "level": "MidHigh"
  },
  {
    "id": 2916,
    "word": "wealth",
    "meaning": "부",
    "level": "Extended"
  },
  {
    "id": 2917,
    "word": "weapon",
    "meaning": "무기",
    "level": "MidHigh"
  },
  {
    "id": 2918,
    "word": "wear",
    "meaning": "입다",
    "level": "Elementary"
  },
  {
    "id": 2919,
    "word": "weather",
    "meaning": "날씨",
    "level": "Elementary"
  },
  {
    "id": 2920,
    "word": "weave",
    "meaning": "짜다",
    "level": "Extended"
  },
  {
    "id": 2921,
    "word": "website",
    "meaning": "웹사이트",
    "level": "Elementary"
  },
  {
    "id": 2922,
    "word": "wedding",
    "meaning": "결혼식",
    "level": "Elementary"
  },
  {
    "id": 2923,
    "word": "weed",
    "meaning": "잡초",
    "level": "Extended"
  },
  {
    "id": 2924,
    "word": "week",
    "meaning": "주",
    "level": "Elementary"
  },
  {
    "id": 2925,
    "word": "weekend",
    "meaning": "주말",
    "level": "Elementary"
  },
  {
    "id": 2926,
    "word": "weigh",
    "meaning": "무게가 나가다",
    "level": "MidHigh"
  },
  {
    "id": 2927,
    "word": "weight",
    "meaning": "무게",
    "level": "Elementary"
  },
  {
    "id": 2928,
    "word": "weird",
    "meaning": "이상한",
    "level": "Extended"
  },
  {
    "id": 2929,
    "word": "welcome",
    "meaning": "환영하다",
    "level": "Elementary"
  },
  {
    "id": 2930,
    "word": "welfare",
    "meaning": "복지",
    "level": "Extended"
  },
  {
    "id": 2931,
    "word": "well",
    "meaning": "잘",
    "level": "Elementary"
  },
  {
    "id": 2932,
    "word": "west",
    "meaning": "서쪽",
    "level": "Elementary"
  },
  {
    "id": 2933,
    "word": "wet",
    "meaning": "젖은",
    "level": "Elementary"
  },
  {
    "id": 2934,
    "word": "whale",
    "meaning": "고래",
    "level": "MidHigh"
  },
  {
    "id": 2935,
    "word": "what",
    "meaning": "무엇",
    "level": "Elementary"
  },
  {
    "id": 2936,
    "word": "wheat",
    "meaning": "밀",
    "level": "Extended"
  },
  {
    "id": 2937,
    "word": "wheel",
    "meaning": "바퀴",
    "level": "MidHigh"
  },
  {
    "id": 2938,
    "word": "when",
    "meaning": "언제",
    "level": "Elementary"
  },
  {
    "id": 2939,
    "word": "where",
    "meaning": "어디",
    "level": "Elementary"
  },
  {
    "id": 2940,
    "word": "whereas",
    "meaning": "반면에",
    "level": "Extended"
  },
  {
    "id": 2941,
    "word": "whether",
    "meaning": "~인지 아닌지",
    "level": "MidHigh"
  },
  {
    "id": 2942,
    "word": "which",
    "meaning": "어느 것",
    "level": "MidHigh"
  },
  {
    "id": 2943,
    "word": "while",
    "meaning": "~하는 동안",
    "level": "MidHigh"
  },
  {
    "id": 2944,
    "word": "whip",
    "meaning": "채찍",
    "level": "Extended"
  },
  {
    "id": 2945,
    "word": "whisper",
    "meaning": "속삭이다",
    "level": "MidHigh"
  },
  {
    "id": 2946,
    "word": "whistle",
    "meaning": "휘파람",
    "level": "MidHigh"
  },
  {
    "id": 2947,
    "word": "white",
    "meaning": "하얀",
    "level": "Elementary"
  },
  {
    "id": 2948,
    "word": "who",
    "meaning": "누구",
    "level": "Elementary"
  },
  {
    "id": 2949,
    "word": "whole",
    "meaning": "전체의",
    "level": "MidHigh"
  },
  {
    "id": 2950,
    "word": "why",
    "meaning": "왜",
    "level": "Elementary"
  },
  {
    "id": 2951,
    "word": "wicked",
    "meaning": "사악한",
    "level": "Extended"
  },
  {
    "id": 2952,
    "word": "wide",
    "meaning": "넓은",
    "level": "MidHigh"
  },
  {
    "id": 2953,
    "word": "wife",
    "meaning": "아내",
    "level": "Elementary"
  },
  {
    "id": 2954,
    "word": "wild",
    "meaning": "야생의",
    "level": "MidHigh"
  },
  {
    "id": 2955,
    "word": "will",
    "meaning": "의지",
    "level": "Elementary"
  },
  {
    "id": 2956,
    "word": "win",
    "meaning": "이기다",
    "level": "Elementary"
  },
  {
    "id": 2957,
    "word": "wind",
    "meaning": "바람",
    "level": "Elementary"
  },
  {
    "id": 2958,
    "word": "window",
    "meaning": "창문",
    "level": "Elementary"
  },
  {
    "id": 2959,
    "word": "wine",
    "meaning": "포도주",
    "level": "Elementary"
  },
  {
    "id": 2960,
    "word": "wing",
    "meaning": "날개",
    "level": "MidHigh"
  },
  {
    "id": 2961,
    "word": "winter",
    "meaning": "겨울",
    "level": "Elementary"
  },
  {
    "id": 2962,
    "word": "wipe",
    "meaning": "닦다",
    "level": "MidHigh"
  },
  {
    "id": 2963,
    "word": "wire",
    "meaning": "철사",
    "level": "MidHigh"
  },
  {
    "id": 2964,
    "word": "wise",
    "meaning": "현명한",
    "level": "MidHigh"
  },
  {
    "id": 2965,
    "word": "wish",
    "meaning": "소망하다",
    "level": "Elementary"
  },
  {
    "id": 2966,
    "word": "wit",
    "meaning": "재치",
    "level": "Extended"
  },
  {
    "id": 2967,
    "word": "with",
    "meaning": "~와 함께",
    "level": "Elementary"
  },
  {
    "id": 2968,
    "word": "withdraw",
    "meaning": "철수하다",
    "level": "Extended"
  },
  {
    "id": 2969,
    "word": "within",
    "meaning": "~안에",
    "level": "MidHigh"
  },
  {
    "id": 2970,
    "word": "without",
    "meaning": "~없이",
    "level": "MidHigh"
  },
  {
    "id": 2971,
    "word": "witness",
    "meaning": "목격자",
    "level": "Extended"
  },
  {
    "id": 2972,
    "word": "woman",
    "meaning": "여자",
    "level": "Elementary"
  },
  {
    "id": 2973,
    "word": "wonder",
    "meaning": "궁금해하다",
    "level": "MidHigh"
  },
  {
    "id": 2974,
    "word": "wood",
    "meaning": "나무",
    "level": "Elementary"
  },
  {
    "id": 2975,
    "word": "wool",
    "meaning": "양모",
    "level": "MidHigh"
  },
  {
    "id": 2976,
    "word": "word",
    "meaning": "단어",
    "level": "Elementary"
  },
  {
    "id": 2977,
    "word": "work",
    "meaning": "일하다",
    "level": "Elementary"
  },
  {
    "id": 2978,
    "word": "world",
    "meaning": "세계",
    "level": "Elementary"
  },
  {
    "id": 2979,
    "word": "worry",
    "meaning": "걱정하다",
    "level": "Elementary"
  },
  {
    "id": 2980,
    "word": "worship",
    "meaning": "숭배하다",
    "level": "Extended"
  },
  {
    "id": 2981,
    "word": "worth",
    "meaning": "가치가 있는",
    "level": "MidHigh"
  },
  {
    "id": 2982,
    "word": "would",
    "meaning": "~하곤 했다",
    "level": "MidHigh"
  },
  {
    "id": 2983,
    "word": "wound",
    "meaning": "상처",
    "level": "MidHigh"
  },
  {
    "id": 2984,
    "word": "wrap",
    "meaning": "싸다",
    "level": "MidHigh"
  },
  {
    "id": 2985,
    "word": "wreck",
    "meaning": "난파",
    "level": "Extended"
  },
  {
    "id": 2986,
    "word": "write",
    "meaning": "쓰다",
    "level": "Elementary"
  },
  {
    "id": 2987,
    "word": "wrong",
    "meaning": "잘못된",
    "level": "Elementary"
  },
  {
    "id": 2988,
    "word": "year",
    "meaning": "해",
    "level": "Elementary"
  },
  {
    "id": 2989,
    "word": "yell",
    "meaning": "소리치다",
    "level": "MidHigh"
  },
  {
    "id": 2990,
    "word": "yellow",
    "meaning": "노란색",
    "level": "Elementary"
  },
  {
    "id": 2991,
    "word": "yes",
    "meaning": "예",
    "level": "Elementary",
    "variation": "yeah, yep"
  },
  {
    "id": 2992,
    "word": "yesterday",
    "meaning": "어제",
    "level": "Elementary"
  },
  {
    "id": 2993,
    "word": "yet",
    "meaning": "아직",
    "level": "MidHigh"
  },
  {
    "id": 2994,
    "word": "yield",
    "meaning": "산출하다",
    "level": "Extended"
  },
  {
    "id": 2995,
    "word": "you",
    "meaning": "너",
    "level": "Elementary"
  },
  {
    "id": 2996,
    "word": "young",
    "meaning": "젊은",
    "level": "Elementary"
  },
  {
    "id": 2997,
    "word": "zebra",
    "meaning": "얼룩말",
    "level": "MidHigh"
  },
  {
    "id": 2998,
    "word": "zero",
    "meaning": "영",
    "level": "MidHigh"
  },
  {
    "id": 2999,
    "word": "zone",
    "meaning": "구역",
    "level": "Extended"
  },
  {
    "id": 3000,
    "word": "zoo",
    "meaning": "동물원",
    "level": "Elementary"
  }
]


def load_words(uploaded_json=None) -> list[dict]:
    """업로드된 JSON 파일이 있으면 사용하고, 없으면 내장 3,000단어(BUILTIN_WORDS)를 사용합니다."""
    if uploaded_json is not None:
        raw = json.load(uploaded_json)
        words = []
        for idx, item in enumerate(raw, start=1):
            word = str(item.get("word", "")).strip()
            meaning = str(item.get("meaning", "")).strip()
            if word and meaning:
                entry = {
                    "id": int(item.get("id", idx)),
                    "word": word,
                    "meaning": meaning,
                }
                if item.get("level"):
                    entry["level"] = str(item["level"]).strip()
                if item.get("variation"):
                    entry["variation"] = str(item["variation"]).strip()
                words.append(entry)
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
        "다른 JSON 단어장 불러오기 (선택)",
        type=["json"],
        help="기본값으로 Voca_3000.csv의 3,000개 단어가 내장되어 있습니다.",
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

st.title("📖 20단어 랜덤 학습 & 오답 복습 (3,000단어)")

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

meta_parts = [f"세트 진행: {idx + 1} / {len(batch)}", f"No. #{wid}"]
if item.get("level"):
    meta_parts.append(f"레벨: {item['level']}")
st.caption("  |  ".join(meta_parts))

with st.container(border=True):
    st.markdown(f"## {item['word']}")
    if item.get("variation"):
        st.caption(f"변형/관련어: {item['variation']}")
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
