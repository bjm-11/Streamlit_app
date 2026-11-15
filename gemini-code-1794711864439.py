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
    "until": ("The library stays open until nine in the evening.", "도서