import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI


template = """
    You are a text re write assistant for different output languages and tone. Input will be as draft text.
    Your goal is to:
    - Properly re write the draft text
    - Convert the draft text to a specified tone
    - Convert the draft text to a specified langauge

  
    Below is the draft text, tone, and language:
    DRAFT: {draft}
    TONE: {tone}
    LANGUAGE: {language}

    YOUR RESPONSE:
"""

#PromptTemplate variables definition
prompt = PromptTemplate(
    input_variables=["tone", "dialect", "draft"],
    template=template,
)


#LLM and key loading function
def load_LLM(openai_api_key):
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm


#Page title and header
st.set_page_config(page_title="Re-write your text")
st.header("Re-write your text")


#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("Re-write your text in different styles.")

with col2:
    st.write("Convert to American, British, Spanish or French!!")


#Input OpenAI API Key
st.markdown("## Enter Your OpenAI API Key")

def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...",
                               key="openai_api_key_input", type="password")
    return input_text

openai_api_key = get_openai_api_key()


# Input
st.markdown("## Enter the text you want to re-write")

def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text goes here.Make sure "
                                                                                      "it's within 700 words.",
                              key="draft_input")
    if len(draft_text.split(" ")) > 700:
        st.write("Please enter a shorter text. The maximum length is 700 words.")
        st.stop()
    return draft_text

text_input = get_draft()

# if len(draft_input.split(" ")) > 700:
#     st.write("Please enter a shorter text. The maximum length is 700 words.")
#     st.stop()

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your re-written text to have?',
        ('Formal', 'Informal', 'Pirate'))
    
with col2:
    option_language = st.selectbox(
        'Which language would you like?',
        ('American', 'British', 'Spanish', 'French'))
    
    
# Output
st.markdown("## Your Re-written text:")

if text_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key.', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_draft = prompt.format(
        tone=option_tone, 
        language=option_language,
        draft=text_input
    )

    text_rewrite = llm(prompt_with_draft)

    st.write(text_rewrite)
