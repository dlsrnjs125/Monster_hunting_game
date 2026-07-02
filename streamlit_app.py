import streamlit as st
from player import Player
from monster import BlueMushroom
from battle import BattleManager

# Streamlit 페이지 설정
st.set_page_config(page_title="간단한 몹 잡기 게임", page_icon="🎮", layout="centered")

st.title("🎮 간단한 몹 잡기 게임")
st.markdown("이 게임은 Streamlit을 사용하여 구현한 웹 기반 RPG 전투 시뮬레이션입니다.")

# 세션 상태 초기화 (Streamlit은 매 상호작용마다 스크립트를 재실행하므로 상태 저장이 필요합니다)
if "player" not in st.session_state:
    st.session_state.player = Player("용사", hp=100, attack_power=30)
if "monster" not in st.session_state:
    st.session_state.monster = BlueMushroom()
if "battle_manager" not in st.session_state:
    st.session_state.battle_manager = BattleManager()
if "log" not in st.session_state:
    st.session_state.log = []

player = st.session_state.player
monster = st.session_state.monster
battle_manager = st.session_state.battle_manager

# 레이아웃 구성
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"👤 플레이어: {player.name}")
    if player.hp > 0:
        st.progress(player.hp / 100.0)
        st.metric(label="체력 (HP)", value=f"{player.hp} / 100")
    else:
        st.progress(0.0)
        st.metric(label="체력 (HP)", value="0 / 100 (사망)")
    st.write(f"공격력: **{player.attack_power}**")

with col2:
    st.subheader(f"👾 몬스터: {monster.name}")
    if monster.hp > 0:
        st.progress(monster.hp / 50.0)
        st.metric(label="체력 (HP)", value=f"{monster.hp} / 50")
    else:
        st.progress(0.0)
        st.metric(label="체력 (HP)", value="0 / 50 (처치됨)")
    st.write(f"공격력: **{monster.attack_power}** | 방어력: **{monster.defense}**")

st.markdown("---")

# 게임 상태에 따른 인터랙션 처리
if player.hp <= 0:
    st.error("💀 용사가 쓰러졌습니다... 게임 오버!")
    if st.button("🔄 게임 다시 시작", use_container_width=True):
        st.session_state.player = Player("용사", hp=100, attack_power=30)
        st.session_state.monster = BlueMushroom()
        st.session_state.log = []
        st.rerun()

elif monster.hp <= 0:
    st.success(f"🎉 축하합니다! {monster.name}을(를) 물리치고 승리했습니다!")
    if st.button("🔄 다음 몬스터 상대하기", use_container_width=True):
        st.session_state.monster = BlueMushroom()
        st.session_state.log = []
        st.rerun()

else:
    # 게임 전투 버튼
    if st.button("⚔️ 공격하기", use_container_width=True):
        # 1. 플레이어 공격
        damage = player.attack_power - monster.defense
        if damage < 1:
            damage = 1
        monster.hp -= damage
        if monster.hp < 0:
            monster.hp = 0

        st.session_state.log.append(f"⚔️ {player.name}이(가) {monster.name}에게 {damage}의 피해를 입혔습니다!")

        # 2. 몬스터 사망 판단 (BattleManager 사용)
        if battle_manager.is_monster_dead(monster):
            st.session_state.log.append(f"🎉 {monster.name}을(를) 처치했습니다!")
        else:
            # 3. 몬스터가 살아있다면 반격
            player.hp -= monster.attack_power
            if player.hp < 0:
                player.hp = 0
            st.session_state.log.append(f"💥 {monster.name}이(가) 반격하여 {player.name}에게 {monster.attack_power}의 피해를 입혔습니다!")
            
            if player.hp <= 0:
                st.session_state.log.append(f"💀 {player.name}이(가) 결국 쓰러졌습니다...")

        st.rerun()

# 전투 로그 출력
st.markdown("### 📜 전투 기록")
if st.session_state.log:
    for log_entry in reversed(st.session_state.log):
        st.write(log_entry)
else:
    st.info("아직 전투 기록이 없습니다. '공격하기' 버튼을 클릭해 전투를 시작하세요.")
