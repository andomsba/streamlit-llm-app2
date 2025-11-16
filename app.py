from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# セッション状態の初期化
if "legal_history" not in st.session_state:
    st.session_state.legal_history = []
if "labor_history" not in st.session_state:
    st.session_state.labor_history = []

# LLMの初期化
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

# 専門家のシステムプロンプト
LEGAL_SYSTEM_PROMPT = """あなたは法務の専門家です。契約書、法律、コンプライアンスに関する質問に詳しく、正確に答えてください。
専門用語を使う際は、わかりやすく説明を加えてください。"""

LABOR_SYSTEM_PROMPT = """あなたは労務の専門家です。労働法、人事制度、給与、勤怠管理に関する質問に詳しく、正確に答えてください。
実務的な観点から、わかりやすく説明してください。"""

def get_llm_response(input_text: str, selected_mode: str) -> str:
    """
    LLMから回答を取得する関数
    
    Args:
        input_text (str): ユーザーの入力テキスト
        selected_mode (str): 選択されたモード（"法務関連" or "労務関連"）
    
    Returns:
        str: LLMからの回答
    """
    # モードに応じてシステムプロンプトと履歴を選択
    if selected_mode == "法務関連":
        system_prompt = LEGAL_SYSTEM_PROMPT
        history = st.session_state.legal_history
    else:  # 労務関連
        system_prompt = LABOR_SYSTEM_PROMPT
        history = st.session_state.labor_history
    
    # メッセージリストを構築
    messages = [SystemMessage(content=system_prompt)]
    messages.extend(history)
    messages.append(HumanMessage(content=input_text))
    
    # LLMに問い合わせ
    result = llm.invoke(messages)
    
    # 履歴に追加
    if selected_mode == "法務関連":
        st.session_state.legal_history.append(HumanMessage(content=input_text))
        st.session_state.legal_history.append(AIMessage(content=result.content))
    else:
        st.session_state.labor_history.append(HumanMessage(content=input_text))
        st.session_state.labor_history.append(AIMessage(content=result.content))
    
    return result.content

st.title("社内質問箱")

st.write("##### 動作モード1: 法務関連")
st.write("契約書に関する質問ができます。")
st.write("##### 動作モード2: 労務関連")
st.write("労務に関する質問ができます。")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["法務関連", "労務関連"]
)

st.divider()

if selected_item == "法務関連":
    input_message = st.text_input(label="契約書に関する質問を入力してください。")

else:
    input_message = st.text_input(label="労務に関する質問を入力してください。")

if st.button("実行"):
    st.divider()

    if selected_item == "法務関連":
        if input_message:
            # LLMから回答を取得
            with st.spinner("法務専門家が回答を準備中..."):
                response = get_llm_response(input_message, selected_item)
                
            # 回答を表示
            st.write("### 回答:")
            st.write(response)
        else:
            st.error("契約書に関する質問を入力してから「実行」ボタンを押してください。")

    else:
        if input_message:
            # LLMから回答を取得
            with st.spinner("労務専門家が回答を準備中..."):
                response = get_llm_response(input_message, selected_item)
                
            # 回答を表示
            st.write("### 回答:")
            st.write(response)
        else:
            st.error("労務に関する質問を入力してから「実行」ボタンを押してください。")

# 履歴をクリアするボタン
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("法務の履歴をクリア"):
        st.session_state.legal_history = []
        st.success("法務の対話履歴をクリアしました")
with col2:
    if st.button("労務の履歴をクリア"):
        st.session_state.labor_history = []
        st.success("労務の対話履歴をクリアしました")

# 対話履歴の表示
if selected_item == "法務関連" and st.session_state.legal_history:
    with st.expander("法務の対話履歴を表示"):
        for i, msg in enumerate(st.session_state.legal_history):
            if isinstance(msg, HumanMessage):
                st.write(f"**質問 {i//2 + 1}:** {msg.content}")
            elif isinstance(msg, AIMessage):
                st.write(f"**回答 {i//2 + 1}:** {msg.content}")
                st.divider()

if selected_item == "労務関連" and st.session_state.labor_history:
    with st.expander("労務の対話履歴を表示"):
        for i, msg in enumerate(st.session_state.labor_history):
            if isinstance(msg, HumanMessage):
                st.write(f"**質問 {i//2 + 1}:** {msg.content}")
            elif isinstance(msg, AIMessage):
                st.write(f"**回答 {i//2 + 1}:** {msg.content}")
                st.divider()