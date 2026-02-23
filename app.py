import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# 약대 데이터 (여기서 37개를 다 채우시면 됩니다)
pharmacy_schools = [
    {"name": "가천대학교 약학대학", "lat": 37.4105, "lon": 126.7121, "address": "인천광역시 연수구 함박뫼로 191"},
    {"name": "가톨릭대학교 약학대학", "lat": 37.4855, "lon": 126.8025, "address": "경기도 부천시 지봉로 43"},
    {"name": "강원대학교 약학대학", "lat": 37.8690, "lon": 127.7447, "address": "강원특별자치도 춘천시 강원대학길 1"},
    {"name": "경북대학교 약학대학", "lat": 35.8888, "lon": 128.6103, "address": "대구광역시 북구 대학로 80"},
    {"name": "경상국립대학교 약학대학", "lat": 35.1539, "lon": 128.0991, "address": "경상남도 진주시 가좌길 74"},
    {"name": "경성대학교 약학대학", "lat": 35.1375, "lon": 129.0932, "address": "부산광역시 남구 수영로 309"},
    {"name": "경희대학교 약학대학", "lat": 37.5939, "lon": 127.0549, "address": "서울특별시 동대문구 경희대로 26"},
    {"name": "계명대학교 약학대학", "lat": 35.8563, "lon": 128.4842, "address": "대구광역시 달서구 달구벌대로 1095"},
    {"name": "고려대학교(세종) 약학대학", "lat": 36.6109, "lon": 127.2871, "address": "세종특별자치시 세종로 2511"},
    {"name": "단국대학교 약학대학", "lat": 36.8329, "lon": 127.1768, "address": "충청남도 천안시 동남구 단대로 119"},
    {"name": "대구가톨릭대학교 약학대학", "lat": 35.9126, "lon": 128.8078, "address": "경상북도 경산시 하양읍 하양로 13-13"},
    {"name": "덕성여자대학교 약학대학", "lat": 37.6514, "lon": 127.0163, "address": "서울특별시 도봉구 삼양로 144길 33"},
    {"name": "동국대학교 약학대학", "lat": 37.6791, "lon": 126.8152, "address": "경기도 고양시 일산동구 동국로 32"},
    {"name": "동덕여자대학교 약학대학", "lat": 37.6063, "lon": 127.0421, "address": "서울특별시 성북구 화랑로13길 60"},
    {"name": "목포대학교 약학대학", "lat": 34.9129, "lon": 126.4379, "address": "전라남도 무안군 청계면 영산로 1666"},
    {"name": "부산대학교 약학대학", "lat": 35.2339, "lon": 129.0783, "address": "부산광역시 금정구 부산대학로63번길 2"},
    {"name": "삼육대학교 약학대학", "lat": 37.6429, "lon": 127.1054, "address": "서울특별시 노원구 화랑로 815"},
    {"name": "서울대학교 약학대학", "lat": 37.4598, "lon": 126.9519, "address": "서울특별시 관악구 관악로 1"},
    {"name": "성균관대학교 약학대학", "lat": 37.2939, "lon": 126.9749, "address": "경기도 수원시 장안구 서부로 2066"},
    {"name": "숙명여자대학교 약학대학", "lat": 37.5455, "lon": 126.9650, "address": "서울특별시 용산구 청파로47길 100"},
    {"name": "순천대학교 약학대학", "lat": 34.9675, "lon": 127.4789, "address": "전라남도 순천시 중앙로 255"},
    {"name": "아주대학교 약학대학", "lat": 37.2831, "lon": 127.0463, "address": "경기도 수원시 영통구 월드컵로 206"},
    {"name": "연세대학교(송도) 약학대학", "lat": 37.3827, "lon": 126.6690, "address": "인천광역시 연수구 송도과학로 85"},
    {"name": "영남대학교 약학대학", "lat": 35.8299, "lon": 128.7535, "address": "경상북도 경산시 대학로 280"},
    {"name": "우석대학교 약학대학", "lat": 35.9189, "lon": 127.0543, "address": "전북특별자치도 완주군 삼례읍 삼례로 443"},
    {"name": "원광대학교 약학대학", "lat": 35.9694, "lon": 126.9573, "address": "전북특별자치도 익산시 익산대로 460"},
    {"name": "이화여자대학교 약학대학", "lat": 37.5618, "lon": 126.9468, "address": "서울특별시 서대문구 이화여대길 52"},
    {"name": "인제대학교 약학대학", "lat": 35.2505, "lon": 128.9022, "address": "경상남도 김해시 인제로 197"},
    {"name": "전남대학교 약학대학", "lat": 35.1764, "lon": 126.9077, "address": "광주광역시 북구 용봉로 77"},
    {"name": "전북대학교 약학대학", "lat": 35.8468, "lon": 127.1294, "address": "전북특별자치도 전주시 덕진구 백제대로 567"},
    {"name": "제주대학교 약학대학", "lat": 33.4560, "lon": 126.5618, "address": "제주특별자치도 제주시 제주대학로 102"},
    {"name": "조선대학교 약학대학", "lat": 35.1432, "lon": 126.9348, "address": "광주광역시 동구 필문대로 309"},
    {"name": "중앙대학교 약학대학", "lat": 37.5050, "lon": 126.9571, "address": "서울특별시 동작구 흑석로 84"},
    {"name": "차의과학대학교 약학대학", "lat": 37.8931, "lon": 127.2023, "address": "경기도 포천시 해룡로 120"},
    {"name": "충남대학교 약학대학", "lat": 36.3685, "lon": 127.3468, "address": "대전광역시 유성구 대학로 99"},
    {"name": "충북대학교 약학대학", "lat": 36.6285, "lon": 127.4571, "address": "충청북도 청주시 흥덕구 내수동로 52"},
    {"name": "한양대학교(ERICA) 약학대학", "lat": 37.2974, "lon": 126.8378, "address": "경기도 안산시 상록구 한양대학로 55"}
]

st.set_page_config(page_title="전국 약대 거리 탐색기", page_icon="💊")
st.title("🏥 전국 약학대학 거리 탐색기")

user_address = st.text_input("현재 위치(주소)를 입력하세요", placeholder="예: 서울시 강남구 역삼동")

if st.button("가장 가까운 약대 찾기"):
    if user_address:
        geolocator = Nominatim(user_agent="my_pharma_app_v1")
        location = geolocator.geocode(user_address)
        
        if location:
            user_coords = (location.latitude, location.longitude)
            results = []
            
            for school in pharmacy_schools:
                dist = geodesic(user_coords, (school['lat'], school['lon'])).kilometers
                results.append({**school, "distance": dist})
            
            # 거리순 정렬
            sorted_res = sorted(results, key=lambda x: x['distance'])
            
            st.subheader("📍 검색 결과 (가까운 순)")
            for i, res in enumerate(sorted_res[:3]): # 상위 3개 출력
                icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                st.info(f"{icon} **{i+1}순위: {res['name']}**\n\n거리: 약 {res['distance']:.2f}km  \n주소: {res['address']}")
        else:
            st.error("주소를 찾을 수 없습니다. 좀 더 정확하게 입력해주세요.")