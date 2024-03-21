from langchain.prompts import PromptTemplate


code_explaination_prompt = """

Human: Here is some java code:

<context>
{context}
</context>

Understand the provided code carefully and answer according to the following instructions:

1. Name: Give the name of the file/code class
2. Purpose: Explain what the code does in one sentence
3. Functionalities: Give a few bullet points describing the functionalities of the code 

answer without using too much space. Don't add space between each bullet points line.

Assistant:"""


code_comparaison_prompt = """

Human: Here are 2 pieces of java code from 2 application BILLI and FAM:

This is BILLI's code:
<code1>
{billi_code}
</code1>

This is FAM's code:
<code2>
{fam_code}
</code2>

Understand the provided code carefully, answer according to the following instructions and explain in detail your answers:

1. What are the functional differences between BILLI's and FAM's code?
2. What are the functional similarities between BILLI's and FAM's code?
3. Say how similar are the codes using a scale from 0 to 10 
    (0 if they are not doing the same thing, 10 if they are doing exactly the same thing)

answer without using too much space. Don't add space between each bullet points line.

Assistant:"""


CODE_EXPLANATION = PromptTemplate(
    template=code_explaination_prompt, input_variables=["context"]
)

CODE_COMPARAISON = PromptTemplate(
    template=code_comparaison_prompt, input_variables=["billi_code", "fam_code"]
)

# CODE_EXTRACT = PromptTemplate(
#     template=code_explaination_prompt, input_variables=["context"]
# )

