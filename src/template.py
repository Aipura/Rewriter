rewrite_prompt_template = """
### Task Background
I am preparing my {cj} paper for submission and require assistance in polishing each paragraph.
You are now acting as a/an {name} in the field of {field} for {cj}.
When I give you an academic paper on {topic}.
From a professional point of view, please polish the writing to meet the academic style, improve the spelling, grammar, clarity, concision and overall readability.
Be careful not to modify the full text or add any new content, just modify the original sentence.
Please take a global perspective after understanding the whole paper.
For each paragraph we need to improve, you need to put all modified sentences in a Markdown table, each column contains the following:
    1. Original Sentence: Full original sentence;
    2. Reasons: Explain why made these changes(highlight the revised part of this sentence and express in {language});
    3. Rewrited Sentence: Finally, Rewrite the full corrected sentence.


### Paper
{paper}


OK, let's start by touching up the Title and Abstract of the paper and think step by step.

### Response
"""