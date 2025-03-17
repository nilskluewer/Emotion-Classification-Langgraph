# Human-centric Evaluation

“Human-Centric Evaluation. Human evaluation is the most important for developing NLG systems and is considered the gold standard when developing automatic metrics. But it is expensive to execute, and the evaluation results are difficult to reproduce.” ([Celikyilmaz et al., 2021, p. 45](zotero://select/groups/5477470/items/JJ43FCSA)) ([pdf](zotero://open-pdf/groups/5477470/items/VS76SVIQ?page=45&annotation=29J7WKHV))


## Evaluation of Halluciantion between Classification and User Report generation

Berberette, Elijah, Jack Hutchins, and Amir Sadovnik. 
**"Redefining" Hallucination" in LLMs: Towards a psychology-informed framework for mitigating misinformation."**
 arXiv preprint arXiv:2402.01769 (2024).
**4 citations**
Confabulation, in the context of Large Language Models (LLMs), is defined as a confident but misleading output generated with the intention of accurately fulfilling the user's prompt.  The term "intention" is used metaphorically here, referring to the LLM's ability to generate coherent and contextually relevant text based on the input it receives, even if that text is factually incorrect.  It's a broad category encompassing many incorrect outputs that don't fit neatly into other classifications of LLM errors.  In humans, confabulation refers to the production of false memories without the intent to deceive.

Celikyilmaz, Asli, Elizabeth Clark, and Jianfeng Gao. 
**"Evaluation of text generation: A survey."** 
arXiv preprint arXiv:2006.14799 (2020). 
**410 citations**


• Coherence and Cohesion
• Readability and Fluency
• Focus
• Informativeness

Full Sources:
“• Coherence and Cohesion measure how clearly the ideas are expressed in the summary (Lapata & Barzilay, 2005). In particular, the idea that, in conjunction with cohesion, which is to hold the context as a whole, coherence should measure how well the text is organised and “hangs together.” Consider the examples in Table 5, from the scientific article abstract generation task. The models must include factual information, but it must also be presented in the right order to be coherent.
• Readability and Fluency, associated with non-redundancy, are linguistic quality metrics used to measure how repetitive the generated summary is and how many spelling and grammar errors there are in the generated summary (Lapata, 2003). 
• Focus indicates how many of the main ideas of the document are captured, while avoiding superfluous details. 
• Informativeness, which is mostly used to evaluate question-focused summarization, measures how well the summary answers a question. Auto-regressive generation models trained to generate a short summary text given a longer document(s) may yield shorter summaries due to reasons relating to bias in the training data or type of the decoding method (e.g., beam search can yield more coherent text compared to top-k decoding but can yield shorter text if a large beam size is used) (Huang et al., 2017). Thus, in comparing different model generations, the summary text length has also been used as an informativeness measure since a shorter text typically preserves less information (Singh & Jin, 2016).” ([Celikyilmaz et al., 2021, p. 39](zotero://select/groups/5477470/items/JJ43FCSA)) ([pdf](zotero://open-pdf/groups/5477470/items/VS76SVIQ?page=39&annotation=ALFYQBV8))

“Factual Consistency. One thing that is usually overlooked in document summarization tasks is evaluating the generated summaries’ factual correctness. It has been shown in many recent work on summarization that models frequently generate factually incorrect text.” ([Celikyilmaz et al., 2021, p. 39](zotero://select/groups/5477470/items/JJ43FCSA)) ([pdf](zotero://open-pdf/groups/5477470/items/VS76SVIQ?page=39&annotation=G7KEYKPY))


## User Study Evaluating User Report




**Terms related to Intrinsic Evaluation:**

* **Adequacy:** How much of the meaning expressed in the source text or a gold-standard translation is also expressed in the generated text.  (See Section 2.1 of the paper).  For a definition, see the Linguistic Data Consortium's description linked in footnote 4 of the paper.  This term is primarily used in Machine Translation evaluation.
* **Fluency:** Measures the quality of the generated text in terms of grammar, spelling, word choice, and style, *without* considering the source text. (See Section 2.1). This term is used across many text generation tasks.  Many papers using this term do not provide an explicit definition, relying on intuitive understanding.  Look for papers specific to your task for operationalizations of fluency.
* **Factuality:**  How accurately the generated text reflects facts described in the source text or context. (See Section 2.1 and 4.5).  There isn't a single, universal definition. Operationalize this based on the specific requirements of your task.  For example, in summarization, factuality could be measured by the number of hallucinations (statements inconsistent with the source).
* **Coherence/Consistency:** How well the generated text fits the provided context and whether the flow of information makes sense. (See Section 2.1). Lapata & Barzilay (2005) is a good starting point for understanding coherence, though it is often used intuitively in NLG evaluations.
* **Grammaticality:**  The extent to which the generated text adheres to the rules of grammar. (See Section 2.1). This can be evaluated by asking human judges to rate how grammatical the text is.
* **Style/Formality/Tone:** The overall style, level of formality, and tone of the generated text. (See Section 2.1). These are often task-specific and require clear guidelines for evaluators.
* **Typicality:** How often one would expect to see text like the generated output. (See Section 2.1).  Hashimoto et al. (2019) discuss this dimension.
* **Repetition/Redundancy:**  The extent to which the generated text contains unnecessary repetition or redundancy. (See Section 2.1).  Evaluators can be asked to rate the level of repetition.
* **Informativeness:** How much information the generated text conveys, often used in question-focused summarization and related to text length. (See Section 2.1, 6.1.1). Singh & Jin (2016) relate informativeness to text length in summarization.

* **Inter-annotator Agreement:**  Measuring and reporting the level of agreement between human evaluators is crucial.  (See Section 2.4).  The paper describes methods like percent agreement, Cohen's kappa, Fleiss' kappa, and Krippendorff's alpha. Artstein & Poesio (2008) provide a more detailed overview of agreement measures in NLP.
* **Task Specificity:** The authors emphasize that evaluation should be tailored to the specific NLG task.  The appropriate dimensions and metrics will vary depending on the task's goals and constraints.
* **Clear Guidelines and Training:** Providing clear guidelines and training for human evaluators is essential for obtaining reliable and consistent results.



## What does the results say about the generated content

- It is fluent, grammatically correct, ... but does not give an value if the output represetns Barretts theory of constructed emotions

- Coherence/Consistency

- Do you think this Output can be Helpfull when doing Content Moderation in Online Discussion Forums?

- Do you think the emotion analysis conducted goes beyond simple lables, such as [Anger, Contempt, Disgust, Enjoyment, Fear, Sadness, Surprise] ?