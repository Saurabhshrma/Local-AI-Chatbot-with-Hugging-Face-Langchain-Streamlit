import streamlit as st
from llm_chain import load_normal_chain
from langchain.memory import StreamlitChatMessageHistory
# from utils import save_chat_history_json,get_timestamp,load_chat_history_json
# import yaml
# import os

# with open("config.yaml","r") as f:
#     config = yaml.safe_load(f)



def load_chain(chat_history):
    return load_normal_chain(chat_history)

def clear_input_field():
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ""


def set_send_input():
    st.session_state.send_input = True
    clear_input_field()

# def save_chat_history():
#     if st.session_state.history.messages != []:
#         if st.session_state.session_key == "new_session":
#             st.session_state.new_session_key = get_timestamp()+".json"
#             save_chat_history_json(st.session_state.history, config["chat_history_path"] + st.session_state.new_session_key + ".json")
#         else:
#             save_chat_history_json(st.session_state.history, config["chat_history_path"] + st.session_state.session_key + ".json")

def main():
    st.title("Private GPT")
    chat_container = st.container()
    # st.sidebar.title("Chat Sessions")
    # chat_sessions = ["new_session"] + os.list(config["chat_history_path"])

    if "send_input" not in st.session_state:
        # st.session_state.session_key = "new_session"
        st.session_state.send_input = False
        st.session_state.user_question = ""
        # st.session_state.new_session_key = None
        # st.session_state.session_index_tracker = "new_session"
    # if st.session_state.session_key == "new_session" and st.session_state.new_session_key != None:
    #     st.session_state.session_inde_tracker = st.session_state.new_session_key
    #     st.session_state.new_session_key = None

    # index = chat_sessions.index(st.session_state.session_index_tracker)

    # st.sidebar.selectbox("Select a chat session",chat_sessions,key="session_key",index=index)

    # if st.session_state.session_key != "new_session":
    #     st.session_state.history = load_chat_history_json(config["chat_history_path"] + st.session_state.session_key)
    # else:
    #     st.session_state.history = []

    chat_history = StreamlitChatMessageHistory(key ="history")
    llm_chain = load_chain(chat_history)    

    user_input = st.text_input("Type your message here", key = "user_input",on_change=set_send_input)
    send_button = st.button("Send",key="send_button")

    if send_button or st.session_state.send_input:
        if st.session_state.user_question != "":

            with chat_container:
                st.chat_message("user").write(st.session_state.user_question)
                llm_response = llm_chain.run(st.session_state.user_question)
                st.session_state.user_question = ""

    
    if chat_history.messages != []:
        with chat_container:
            st.write("Chat History:")
            for message in chat_history.messages:
                st.chat_message(message.type).write(message.content)


# save_chat_history()


if __name__ == "__main__":
    main() 