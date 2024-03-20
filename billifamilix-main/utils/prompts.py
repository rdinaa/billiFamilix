from langchain.prompts import PromptTemplate


code_explaination_prompt = """

Human: Here is some java code:

<context>
{context}
</context>

Answer as follow:

1. Give the name of the file/code class
2. Explain what the code does in one sentence
3. Give fiew bullet points of the different parts of the code 

aswer whithout using too much space. Don't add space between each bullet points line.

Assistant:"""

code_comparaison_prompt = """

Human: Here are 2 piece of java code from 2 application BILLI and FAM:

This is BILLI's code:
<code1>
{billi_code}
</code1>

This is FAM's code:
<code2>
{fam_code}
</code2>

Answer as follow:

1. What is the difference between BILLI and FAM ?
2. What is similar between BILLI and FAM ?
3. Say how similar are the codes with a grade from 0 to 10 
    (0 if they are not doing the same thing, 10 if they are doing exactly the same thing)

aswer whithout using too much space. Don't add space between each bullet points line.

Assistant:"""

CODE_EXPLANATION = PromptTemplate(
    template=code_explaination_prompt, input_variables=["context"]
)

CODE_COMPARAISON = PromptTemplate(
    template=code_comparaison_prompt, input_variables=["billi_code", "fam_code"]
)

