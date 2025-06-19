import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import re



MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"

# Load Model & Tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True, token=token)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    trust_remote_code=True,
    token=token
)

def check_code(problem_desc, user_code):
    prompt = f"""
    You are an AI that verifies if the given code correctly solves the problem.
    If the code is correct but has small logical or syntax errors, fix them.
    If the code does not match the problem, return "Irrelevant Code".

    Problem Description:
    {problem_desc}

    User Code:
    ```cpp
    {user_code}
    ```

    Fixed Code (or "Irrelevant Code"):
    """

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "Fixed Code (or \"Irrelevant Code\"):" in response:
        corrected_code = response.split("Fixed Code (or \"Irrelevant Code\"):\n")[-1].strip()
    else:
        corrected_code = response.strip()

    return corrected_code

def compare_code_similarity(corrected_code, user_code):
    prompt = f"""
    You are an AI that compares two code snippets and assigns a similarity score from 1 to 10.
    - A score of **10** means the codes are identical.
    - A score of **1** means the codes are completely different.
    - Consider syntax, logic, structure, and variable usage when scoring.

    Output ONLY a single integer value from 1 to 10. Do NOT add any extra explanation.

    Correct Code:
    ```cpp
    {corrected_code}
    ```

    Incorrect Code:
    ```cpp
    {user_code}
    ```

    Similarity Score:
    """

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=3)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    match = re.search(r"\b(10|[1-9])\b", response)
    similarity_score = match.group(0) if match else "N/A"

    return similarity_score

# Streamlit UI
st.title("AI Code Correction & Similarity Checker")
st.markdown("Enter a problem description and your code. The AI will correct your code and compute a similarity score.")

problem_desc = st.text_area("Problem Description", "Write a function to compute the factorial of a number.")
user_code = st.text_area("Your Code", """int findFact(int n) {\n   int ans=1;\n   while(n>0){\n   ans+=n;\n   n--;\n   }\n   return ans;\n}""")

if st.button("Check Code"):
    corrected_code = check_code(problem_desc, user_code)
    st.subheader("Corrected Code")
    st.code(corrected_code, language="cpp")
    
    similarity_score = compare_code_similarity(corrected_code, user_code)
    st.subheader("Similarity Score")
    st.write(f"**{similarity_score}/10**")

