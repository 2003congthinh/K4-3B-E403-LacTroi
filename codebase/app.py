import os
from typing import Dict, List

import streamlit as st

from logger import log_event, log_prompt_response
from mock_knowledge import find_mock_answer
from providers import PROVIDER_CONFIG, call_llm, get_available_providers, get_default_model, get_models_for_provider


st.set_page_config(page_title="Trợ lý Học viên", page_icon="🤖", layout="wide")


SCENARIOS = {
    "happy": {
        "title": "Trả lời có căn cứ",
        "channel": "#hỏi-đáp-chung",
        "description": "Trợ lý trả lời khi được @tag",
        "status": "có căn cứ",
        "question": "Cho em hỏi hạn nộp lab 2 là khi nào ạ?",
        "system_prompt": "Bạn là trợ lý học viên của khóa AI20K. Trả lời dựa trên thông tin khóa học và kiến thức chung khi phù hợp. Nếu không chắc, hãy nói rõ bạn chưa xác minh, nhưng không cần từ chối mọi câu hỏi ngoài phạm vi học thuật. Về dữ liệu cá nhân hoặc điểm danh riêng tư, chuyển cho TA.",
    },
    "low": {
        "title": "Nghi ngờ — hỏi lại",
        "channel": "#hỏi-đáp-chung",
        "description": "Trợ lý trả lời khi được @tag",
        "status": "2 nguồn mâu thuẫn",
        "question": "Deadline nộp báo cáo cuối kỳ là ngày nào vậy ạ?",
        "system_prompt": "Bạn là trợ lý học viên. Nếu thấy nguồn mâu thuẫn, hãy nói rõ đang có xung đột và gợi ý kiểm tra TA, nhưng vẫn có thể trả lời theo quy tắc chung nếu có thông tin chắc chắn. Không suy đoán về dữ liệu riêng tư.",
    },
    "block": {
        "title": "Không có căn cứ",
        "channel": "#hỏi-đáp-chung",
        "description": "Trợ lý trả lời khi được @tag",
        "status": "không có quyền trả lời",
        "question": "Điểm danh hôm qua của em có bị thiếu không ạ?",
        "system_prompt": "Bạn là trợ lý học viên. Không trả lời hoặc suy đoán dữ liệu cá nhân hoặc điểm danh. Nếu người dùng hỏi về thông tin cá nhân, hãy nói rõ không có quyền truy cập và chuyển cho TA phụ trách. Còn với câu hỏi chung, hãy trả lời bình thường.",
    },
    "fix": {
        "title": "Sửa câu trả lời",
        "channel": "#hỏi-đáp-chung",
        "description": "Trợ lý trả lời khi được @tag",
        "status": "đã được TA sửa",
        "question": "Hạn nộp lab 3 là bao giờ ạ?",
        "system_prompt": "Bạn là trợ lý học viên. Khi có một thông báo mới thay thế nguồn cũ, ưu tiên thông báo mới nhất. Giữ lịch sử sửa rõ ràng. Với câu hỏi chung hoặc không liên quan khóa, trả lời bằng kiến thức chung và không cố từ chối.",
    },
}


CUSTOM_CSS = """
<style>
    .app-shell {
        background: #f3f4f8;
        color: #20242C;
        font-family: "Segoe UI", sans-serif;
    }
    .title-bar {
        background: #ffffff;
        border: 1px solid #dfe3ee;
        border-radius: 18px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(20,22,30,0.06);
    }
    .chat-window {
        background: #ffffff;
        border: 1px solid #dfe3ee;
        border-radius: 18px;
        min-height: 560px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(20,22,30,0.06);
    }
    .chat-header {
        padding: 0.9rem 1rem;
        border-bottom: 1px solid #e7eaf2;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #f9fafc;
    }
    .status-pill {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .status-green { background: #eaf7ee; color: #197d46; }
    .status-yellow { background: #fff3d9; color: #b77600; }
    .status-red { background: #fde8e4; color: #c84d3a; }
    .status-blue { background: #eaf1ff; color: #3d63d2; }
    .chat-body {
        padding: 1rem;
        background: #f8f9fb;
        min-height: 420px;
    }
    .bubble {
        padding: 0.8rem 1rem;
        border-radius: 14px 14px 14px 4px;
        margin-bottom: 0.8rem;
        max-width: 82%;
        line-height: 1.65;
        border: 1px solid #dfe3ee;
        background: #ffffff;
    }
    .bubble.user {
        margin-left: auto;
        background: #edf1fb;
        border-radius: 14px 14px 4px 14px;
    }
    .bubble.bot {
        background: #ffffff;
    }
    .source-tag {
        display: inline-block;
        margin-top: 0.45rem;
        padding: 0.18rem 0.55rem;
        border-radius: 8px;
        background: #ecf4ff;
        color: #315ec7;
        font-size: 0.72rem;
        font-weight: 700;
    }
    .metric-box {
        background: white;
        border: 1px solid #dfe3ee;
        border-radius: 14px;
        padding: 0.75rem 0.9rem;
        margin-bottom: 0.8rem;
    }
    .metric-box strong { font-size: 1.2rem; }
    .stTabs [role="tablist"] { gap: 0.5rem; }
    .stTabs [role="tab"] { border-radius: 10px; }
</style>
"""


st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


with st.sidebar:
    st.markdown("### Cấu hình AI")
    providers = get_available_providers()
    provider_options = providers or ["gpt", "gemini", "anthropic", "azure-openai"]
    provider = st.selectbox("Provider", options=provider_options, index=0 if provider_options else 0)
    models = get_models_for_provider(provider)
    model = st.selectbox("Model", options=models or [get_default_model(provider)], index=0)
    st.caption("API keys are read from environment variables, not entered in the UI.")
    st.caption("Supported keys: OPENAI_API_KEY, GEMINI_API_KEY, ANTHROPIC_API_KEY, AZURE_OPENAI_API_KEY")

    st.markdown("---")
    st.markdown("### Chế độ demo")
    scenario_key = st.radio("Scenario", options=list(SCENARIOS.keys()), horizontal=True)


st.markdown('<div class="app-shell">', unsafe_allow_html=True)

header = SCENARIOS[scenario_key]
col_left, col_right = st.columns([2.2, 1])
with col_left:
    st.markdown(
        f"""
        <div class="title-bar">
            <h2 style='margin:0;'>Trợ lý Học viên — Discord, khoá 4</h2>
            <p style='margin:0.45rem 0 0 0; color:#4A5061;'>Bản mẫu tương tác cho 4 đường xử lý: có căn cứ, nghi ngờ, không có căn cứ, và sửa trực tiếp.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_right:
    st.markdown(
        """
        <div class="metric-box">
            <div>21 / 1.092</div>
            <div style='color:#4A5061; font-size:0.8rem;'>tin nhắn là câu hỏi logistics/tiện ích</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

status_class = {
    "có căn cứ": "status-green",
    "2 nguồn mâu thuẫn": "status-yellow",
    "không có quyền trả lời": "status-red",
    "đã được TA sửa": "status-blue",
}.get(header["status"], "status-blue")

chat_col, trace_col = st.columns([1.7, 1])

with chat_col:
    st.markdown(
        f"""
        <div class="chat-window">
            <div class="chat-header">
                <div><strong>{header['channel']}</strong><br><span style='color:#4A5061; font-size:0.8rem;'>{header['description']}</span></div>
                <span class='status-pill {status_class}'>{header['status']}</span>
            </div>
            <div class='chat-body'>
        """,
        unsafe_allow_html=True,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "user", "content": header["question"]},
            {"role": "assistant", "content": ""},
        ]

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="bubble user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            if message["content"]:
                st.markdown(f'<div class="bubble bot">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="bubble bot">Đang xử lý...</div>', unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    user_input = st.text_area("Nhập câu hỏi của học viên", value=header["question"], height=120)
    if st.button("Gửi tới model"):
        mock_match = find_mock_answer(user_input)
        if mock_match:
            answer = f"{mock_match['answer']}\n\nNguồn: {mock_match['source']}"
            st.session_state.messages = [
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": answer},
            ]
            log_prompt_response(provider, model, user_input, answer, status=f"mock_{mock_match['action']}")
            st.rerun()

        st.session_state.messages = [{"role": "user", "content": user_input}]
        try:
            result = call_llm(
                provider_name=provider,
                model=model,
                user_input=user_input,
                system_prompt=header["system_prompt"],
            )
            answer = result["response"].strip() or "Không có phản hồi từ model."
            st.session_state.messages.append({"role": "assistant", "content": answer})
            log_prompt_response(provider, model, user_input, answer, status="ok")
            st.rerun()
        except Exception as exc:
            fallback = "Mình không đủ căn cứ để trả lời chắc chắn. Em có thể cho mình xác nhận thêm từ thông báo chính thức hoặc tag TA phụ trách để kiểm tra."
            st.session_state.messages.append({"role": "assistant", "content": fallback})
            log_prompt_response(provider, model, user_input, str(exc), status="error")
            st.toast(f"Model unavailable: {exc}", icon="⚠️")
            st.rerun()

with trace_col:
    st.markdown(
        """
        <div class="metric-box">
            <strong>Vì sao bot làm vậy</strong>
            <ul>
                <li>Ý định nhận diện: câu hỏi logistics</li>
                <li>Nguồn tìm được: chính thức / mâu thuẫn / không có quyền</li>
                <li>Độ tin cậy: cao / thấp / không được đoán</li>
                <li>Hành động: trả lời / hỏi lại / chuyển TA / sửa</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="metric-box">
            <strong>Mức tự động hóa</strong>
            <p>Conditional — bot tự làm khi có căn cứ, chuyển người khi mơ hồ hoặc không có thẩm quyền.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="metric-box">
            <strong>Nguyên tắc HAX</strong>
            <ul>
                <li>Make clear why</li>
                <li>Scope services when in doubt</li>
                <li>Support efficient correction</li>
                <li>Support efficient dismissal</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("API source switch is handled centrally in the provider module, so the app can move between GPT, Gemini, Anthropic, and Azure OpenAI without changing the UI logic.")

log_event("app_loaded", {"provider": provider, "scenario": scenario_key})
