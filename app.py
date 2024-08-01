import streamlit as st
import random

# List of words for the game
words = ["apple", "elephant", "computer", "ocean", "book", "moon", "guitar", "coffee", "bicycle", "rainbow"]

def init_game():
    if 'answer' not in st.session_state:
        st.session_state.answer = random.choice(words)
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def reset_game():
    st.session_state.answer = random.choice(words)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.messages = []

def main():
    st.title("스무고개 (Twenty Questions) Game")

    init_game()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display chances left
    st.sidebar.write(f"Chances left: {20 - st.session_state.attempts}")

    # Reveal answer button
    if st.sidebar.button("Reveal Answer"):
        st.sidebar.write(f"The answer is: {st.session_state.answer}")

    if not st.session_state.game_over:
        # Get user input
        user_input = st.chat_input("Ask a yes/no question or make a guess:")

        if user_input:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Process user input (TODO: Replace this part with LLM inference)
            if user_input.lower().startswith(("is ", "are ", "does ", "do ", "can ", "has ", "have ")):
                st.session_state.attempts += 1
                answer = "Yes" if random.random() > 0.5 else "No"
                st.session_state.messages.append({"role": "assistant", "content": answer})
            elif user_input.lower() == st.session_state.answer:
                st.session_state.attempts += 1
                st.session_state.messages.append({"role": "assistant", "content": f"Congratulations! You guessed the word '{st.session_state.answer}' correctly!"})
                st.session_state.game_over = True
            else:
                st.session_state.attempts += 1
                st.session_state.messages.append({"role": "assistant", "content": "Incorrect guess. Try again!"})

            if st.session_state.attempts >= 20:
                st.session_state.messages.append({"role": "assistant", "content": f"Game over! You've used all 20 attempts. The word was '{st.session_state.answer}'."})
                st.session_state.game_over = True

            st.experimental_rerun()

    if st.session_state.game_over:
        if st.sidebar.button("Play Again"):
            reset_game()
            st.experimental_rerun()

if __name__ == "__main__":
    main()
