Certainly! Let's work on outlining Chapter 2, the Literature Review, in LaTeX format. We'll build a clear structure that bridges both psychological concepts and informatics, ensuring that readers from both fields can grasp the content. I'll include suggested literature to cite in each section, formatted in LaTeX. Please note that actual content writing is beyond this scope, but this outline will provide a solid foundation for you to build upon.

---

```latex
\chapter{Literature Review}

\section{Introduction to Emotion Classification in Informatics and Psychology}
% Briefly introduce emotion classification as a broader term to also make it understandable for ppl. who are not famimilar with it from informmatics.
% Set the stage for the comparison between traditional and contemporary theories

\subsection{Paul Ekman's Theory of Basic Emotions}
% Discuss Ekman's theory and its impact on emotion research
% over 50+ years old etc.
% Traditional methods and the focus on universal facial expressions
% Cite foundational papers by Ekman

\subsubsection{Constructed Emotion Theory of Lisa Feldmann Barrett}
\label{sec:universal_expressions}
% Detail the concept of universal expressions and how they are used to identify emotions
% Discuss cross-cultural studies supporting this concept

\subsubsection{Contrast both theories}
\label{sec:limitations_ekman}
% Present criticisms from the psychological community
% Address issues like cultural variability and context neglect
% Reference papers that critique Ekman's work
Problem Definition
Paul Ekman proposed his theory of universal emotions in the 1960s. In basic terms, it posits that there are six universal emotions—happiness, sadness, surprise, fear, anger, and disgust—each associated with distinct facial expressions that are recognizable across cultures. Ekman represents the position these emotions are hardwired and innate, implying that we are born with the ability to express and experience these basic emotions. He acknowledeges that the manner how these emotions are expressed and interpreted can be significantly influenced and shaped by cultural norms through the concept of "display rules." [1,2]

Lisa Feldman Barrett has challenged Ekman's view on emotions by providing an alternative view. She views emotions as a psychological construct, which do not have standard "fingerprints" specific expressions associated with them universally. She disagree with Ekman on the role of facial expressions, for her, emotions do not have a specific facial expression. The way we interpret facial expressions is highly dependent on our individual experiences and cultural backgrounds. The way we feel and what we label as emotions is constructed from a range of more basic physical sensations in response to the environment (theory of constructed emotions). Barrett although agrees with Ekman that culture and individual experiences significantly shape how we perceive and express emotions. Barrett is not entirely denying the role of biology in emotions but criticises Ekman's approach and the simplicity of linking specific emotions to specific facial expressions. [3,4]

Since the theory of universal emotions by Ekman is established and many times proven and build onto, the theory of constructed emotions by Barrett questions some “fundamental assumptions lurking within the field’s dominant methodological tradition” [4, p. 894]. The following problems arise from these different viewpoints on emotions. 

[1]           Ekman P. Emotions revealed. BMJ 2004;328:0405184. https://doi.org/10.1136/sbmj.0405184.

[2]           Unmasking the Face: A Guide to Recognizing Emotions from Facial Clues - Paul Ekman, Wallace V. Friesen - Google Books n.d. https://books.google.at/books?hl=en&lr=&id=TukNoJDgMTUC&oi=fnd&pg=PR3&dq=Ekman,+P.,+%26+Friesen,+W.+V.+Unmasking+the+face.&ots=GXDq8j93fb&sig=4KKk5-RPvPO-AKnJA-A4cS4aOKU&redir_esc=y#v=onepage&q&f=false (accessed April 27, 2024).

[3]           Barrett LF. The theory of constructed emotion: an active inference account of interoception and categorization. Soc Cogn Affect Neurosci 2016:nsw154. https://doi.org/10.1093/scan/nsw154.

[4]           Barrett LF. Context reconsidered: Complex signal ensembles, relational meaning, and population thinking in psychological science. Am Psychol 2022;77:894–920. https://doi.org/10.1037/amp0001054.


\subsection{What we should and should not do in emotion classificatiokn after Lisa Feldmann barrett}
<context>
# Rationale for classification using context

The question to answer in this document is, how we want to classify the context sphere created in the preprocessing step. What is the foundation in the litrature and how do we reason the classification. 

Barrett does not state clearly how the actual Output should look like. She focuses on why other concepts are flawed or why context is important. But the Output never defined, it is often defined how it should not look like. 

## How should classification not look like.
### Classification Shouldn't Look Like...
1. Choice-from-array methods constrain emotional meanings and should not be used.
These methods, common in emotion recognition studies, limit participant choices, forcing them to select from a predetermined set of options, like "anger," "disgust," "fear," etc. This prevents participants from expressing more nuanced or culturally specific emotions. This artificial harmonization of responses, particularly from non-Western cultures, might be why this method was favored, as it creates a semblance of universality.
“participants with a stimulus (e.g., a face, a set of eyes, a vocalization, a scenario, a word) and asks them to select the corresponding target from a small array of choices” ([Barrett, 2022, p. 897](zotero://select/groups/5477470/items/EE2G9Z2S)) ([pdf](zotero://open-pdf/groups/5477470/items/PQPMU4FH?page=4&annotation=FY8TZDXK))

2. Context effects within repeated trials can subtly teach participants the expected answers, creating false evidence of universality.
Participants, being adept statistical learners, pick up on contextual cues within repeated trials. This can lead to above-chance matching of emotion words with posed facial configurations, even in cultures with limited exposure to U.S. cultural practices. These findings, often interpreted as evidence for universal emotion recognition, may instead reflect learned responses due to the experimental design.
“evidence for universal emotion recognition (and are interpreted as evidence for universal emotional expressions)” ([Barrett, 2022, p. 897](zotero://select/groups/5477470/items/EE2G9Z2S)) ([pdf](zotero://open-pdf/groups/5477470/items/PQPMU4FH?page=4&annotation=V9VKJX9D))

3. The use of prototypes in stimuli selection can bias results.
Even if researchers state their stimuli aren't chosen to match prototypes, biases can seep into the process. If an experimenter has a prototype in mind, participants can infer it, even without direct exposure. Studies using vast datasets and complex machine learning can still fall prey to this bias, resulting in a limited sampling of real-world variation. 
“And experimental evidence shows that if an experimenter has a prototype in mind and curates stimuli guided by that belief, participants will be able to infer the prototype, even if they were never exposed to it” ([Barrett, 2022, p. 900](zotero://select/groups/5477470/items/EE2G9Z2S)) ([pdf](zotero://open-pdf/groups/5477470/items/PQPMU4FH?page=7&annotation=RWRIN3FX))

4. Supervised Machine Learning approaches searching for prototypic brain signal patterns for specific emotions misinterpret findings as brain biomarkers.
These patterns, touted as "fingerprints" or "signatures," are often inconsistent across studies and might indicate meaningful, structured variation instead. Studies documenting variations in neural correlates within the same emotion category support this idea. Emotion category labels likely represent diverse, context-specific instances, not stable biological kinds.

“indicate the presence of meaningful, structured variation, a hypothesis supported by brain imaging studies that have documented variation in the neural correlates of different instances of emotion within the same emotion category” ([Barrett, 2022, p. 907](zotero://select/groups/5477470/items/EE2G9Z2S)) ([pdf](zotero://open-pdf/groups/5477470/items/PQPMU4FH?page=14&annotation=GLRNWVKE))


5. The reliance on a typological view of emotion categories in experimental design and measurement is problematic.
This view, assuming fixed, essential categories, doesn't align with the abundant data showing significant variation in emotional expression. Studies designed to induce stereotypical emotions often reveal unexpected variation in facial movements, autonomic patterns, and brain activity. Focusing on this variation as the norm, rather than a nuisance, would revolutionize our understanding of emotions.
Litrature posists that the typological view is not sufficient to grasph the complexity of emotions. It is there hard to but emotions into types or categories and expect it to be accurate and representative. 

“The major stumbling block in using a typological view to guide measurement of emotional instances is that it does not fit the majority of data that have been collected to study it” ([Barrett and Westlin, 2021, p. 55](zotero://select/groups/5477470/items/YQBX6ZH6)) ([pdf](zotero://open-pdf/groups/5477470/items/PRXQBJAV?page=17&annotation=ZHRNNDBD))

6. Pattern classification techniques, while potentially helpful, are prone to essentialist misinterpretations.
The patterns identified, despite their ability to distinguish between emotion categories, shouldn't be mistaken for defining essences or biomarkers. These patterns are statistical summaries of a category's instances, not a representation of an unchanging core found in every instance. Assuming otherwise is mistaking an abstract statistical representation for the actual lived experience of emotions. Successful pattern classification, rather than proving essential categories, actually supports the idea of emotions as conceptual categories with diverse and unique instances.

“Whether you rely on the assumption of emotion essences or not, it is important to be vigilant for the use of an essentialist mindset where it does not belong, lest you misinterpret your own (or someone else’s) findings.” ([Barrett and Westlin, 2021, p. 68](zotero://select/groups/5477470/items/YQBX6ZH6)) ([pdf](zotero://open-pdf/groups/5477470/items/PRXQBJAV?page=30&annotation=QEMCGT4M))

“These recent pattern classification studies interpret their findings as support for the typological view of emotion categories, when, in fact, they actually found evidence in support of the theory of constructed emotion” ([Barrett and Westlin, 2021, p. 70](zotero://select/groups/5477470/items/YQBX6ZH6)) ([pdf](zotero://open-pdf/groups/5477470/items/PRXQBJAV?page=32&annotation=KSWVWU9I))

“To assume that a pattern is the fingerprint or biomarker for an emotion category is to mistake a statistical summary for the norm, when it is in fact a statistical abstraction that may not exist in nature.” ([Barrett and Westlin, 2021, p. 70](zotero://select/groups/5477470/items/YQBX6ZH6)) ([pdf](zotero://open-pdf/groups/5477470/items/PRXQBJAV?page=32&annotation=WCNPX5DP))

7. Inconsistent findings from pattern classification studies might reflect actual variation in the data, not a failure to replicate objective categories.
The so-called "fingerprints" or "biomarkers" might be study-specific statistical abstractions summarizing real-world variation. Comparisons with unsupervised clustering, which doesn't rely on pre-assigned labels, support this view. These findings further emphasize that emotion category labels encompass diverse, context-specific instances, not fixed biological entities.

“If this explanation is correct, then the ‘fingerprints’ or ‘biomarkers’ for different emotion categories that have been reported in pattern classification studies do not reflect objective categories that fail to replicate, but are better understood as statistical abstractions for a given study that may not exist in the real world but that summarize real variation that does exist in the real world.” ([Barrett and Westlin, 2021, p. 71](zotero://select/groups/5477470/items/YQBX6ZH6)) ([pdf](zotero://open-pdf/groups/5477470/items/PRXQBJAV?page=33&annotation=JWWGH2W2))

“These findings suggest that emotion category labels refer to populations of highly variable, context-specific instances, rather than biological kinds that are stable across individuals.” ([Barrett and Westlin, 2021, p. 71](zotero://select/groups/5477470/items/YQBX6ZH6)) ([pdf](zotero://open-pdf/groups/5477470/items/PRXQBJAV?page=33&annotation=UQGSX25L))

The sources highlight the dangers of applying an essentialist framework to emotion classification. Instead, the focus should be on understanding the rich tapestry of variation within and across emotion categories. This shift in perspective requires moving away from methods like choice-from-array and prototypical stimuli selection and embracing approaches that acknowledge the dynamic and context-dependent nature of emotions.

## Variant 1: (short) Disclaimer for classification
This classification follows Barrett's theory of constructed emotion, acknowledging that emotional categories are conceptual abstractions rather than fixed natural types. While our classification system aims to identify meaningful patterns, it's important to note that these patterns represent statistical summaries rather than definitive categories. Like approaching a limit in mathematics, we can work toward increasingly accurate classifications while recognizing that no classification system can perfectly capture the full complexity and variability of emotional experiences. Each instance within a category may be unique, and the boundaries between categories are inherently fuzzy rather than absolute.

## Variant 2: Longer Disclaimer 
This classification follows Barrett's theory of constructed emotion and employs pattern classification techniques while acknowledging several fundamental limitations:

First, like statistical abstractions (such as the notion of an average family having 3.13 children), our emotional classifications represent theoretical constructs rather than naturally occurring phenomena. Even with 100% classification accuracy, no single instance may perfectly match the identified patterns.

Second, we approach emotions through 'population thinking,' viewing them as diverse populations of instances rather than fixed types. Just as a chair category encompasses various forms (from traditional four-legged chairs to beanbags), emotional categories contain varied instances that may share family resemblances without sharing any single defining feature.

We explicitly avoid terms like 'biomarkers,' 'fingerprints,' or 'signatures,' as these incorrectly imply unchanging, unique identifiers. Instead, we recognize that emotional expressions vary across:
- Individual experiences
- Cultural contexts
- Situational circumstances
- Temporal conditions

Our classification system serves as a map rather than territory - a useful tool for understanding patterns while acknowledging that:
1. There is no 'pure form' or 'true essence' of any emotion
2. Each emotional instance is unique
3. Category boundaries are inherently fuzzy
4. Physical correlates (such as facial expressions or physiological responses) are indicative rather than definitive

Like approaching a mathematical limit, our classification system strives for accuracy while recognizing that perfect categorization of emotional experiences is theoretically impossible. This work represents a pragmatic approach to understanding emotional patterns while maintaining awareness of the inherent complexity and variability of human emotional experience.


## Variant 3: Disclaimer for classification: 
### Theoretical Framework and Methodological Considerations for Emotion Classification

Our approach to emotion classification acknowledges fundamental theoretical and methodological considerations drawn from contemporary emotion research, particularly Barrett's theory of constructed emotion. This section outlines crucial limitations and interpretative frameworks that guide our analysis.

#### Statistical Abstraction vs. Natural Occurrence

Pattern classification techniques, while valuable for analysis, must be understood within their proper conceptual framework. As Barrett and Westlin (2021) demonstrate, even patterns that achieve 100% classification accuracy should not be interpreted as "fingerprints" or "biomarkers" of emotions. These patterns represent statistical abstractions rather than naturally occurring phenomena, similar to how the average U.S. family has 3.13 children—a mathematically valid but naturally impossible figure.

#### Population Thinking and Variation

Our approach embraces what Barrett (2022) terms "population thinking," viewing emotions as populations of diverse instances rather than fixed types. This perspective acknowledges that:

1. Emotional instances within the same category can vary significantly across:
   - Individual experiences
   - Cultural contexts
   - Situational circumstances
   - Temporal conditions

2. No single instance needs to perfectly match the statistical pattern to be valid (Barrett and Westlin, 2021)

#### Methodological Constraints and Considerations

We explicitly avoid several problematic approaches identified in the literature:

1. Choice-from-array methods, which artificially constrain emotional meanings (Barrett, 2022, p. 897)
2. Prototype-based stimuli selection, which can introduce implicit biases (Barrett, 2022, p. 900)
3. Supervised machine learning approaches that misinterpret findings as brain biomarkers (Barrett, 2022, p. 907)

#### Interpretation Framework

Our classification results should be interpreted with several key principles in mind:

1. Pattern Recognition vs. Essence: "To assume that a pattern is the fingerprint or biomarker for an emotion category is to mistake a statistical summary for the norm, when it is in fact a statistical abstraction that may not exist in nature" (Barrett and Westlin, 2021, p. 70).

2. Contextual Dependency: "Emotion category labels refer to populations of highly variable, context-specific instances, rather than biological kinds that are stable across individuals" (Barrett and Westlin, 2021, p. 71).

3. Variation as Feature, Not Bug: Inconsistent findings across studies might reflect actual variation rather than failed replication (Barrett and Westlin, 2021, p. 71).

#### Implications for Current Research

Our classification approach acknowledges these limitations while leveraging the power of pattern recognition. We treat our results as useful abstractions that help understand emotional patterns while maintaining awareness that:

1. The classifications represent conceptual categories with fuzzy boundaries
2. Each emotional instance is unique and context-dependent
3. Statistical patterns are tools for understanding, not definitive truths
4. Physical correlates are indicative rather than definitive

This framework allows us to make meaningful classifications while avoiding essentialist interpretations that have historically limited emotion research. Our approach aligns with Barrett's theory of constructed emotion, acknowledging both the utility and limitations of classification in emotional analysis.

## What to expect when classfying emotions with typological approach
Imagine trying to classify "chairs":
- You might create a statistical pattern: "typically has 4 legs, a back, and a seat"
- But this pattern doesn't mean every chair must have these features (bean bags, hanging chairs, etc.)
- The pattern is useful for recognition but isn't a rigid definition

Key assumptions to avoid when classifying emotions:

1. Don't assume there's a "pure form":
- Emotions don't have a fixed "essence" or "true form"
- Each instance of an emotion can be unique
- There's no perfect prototype of "anger" or "happiness"

2. Don't confuse the map for the territory:
- Statistical patterns are useful tools, not absolute truths
- They're abstractions that help us understand, not rigid rules
- Real emotional experiences are more complex than their classifications

3. Don't expect consistency:
- The same emotion category can manifest differently across:
  - Different people
  - Different situations
  - Different cultures
  - Different times

4. Don't treat biomarkers as definitive:
- Physical patterns (like brain activity or facial expressions)
- Are correlations, not defining characteristics
- Can vary significantly within the same emotion category

The main takeaway is that emotions are more like fuzzy concepts than rigid categories, and our classification systems should reflect this flexibility rather than trying to force emotions into fixed boxes.
</context>

\section{Emotion Classification in Informatics}
\label{sec:emotion_informatics}


\subsection{Traditional Computational Approaches}
\label{sec:traditional_methods}
% Describe how informatics has historically approached emotion classification
% Focus on classification into discrete categories (Ekman-style)
% Cite key algorithms and models used in sentiment analysis and emotion recognition

\subsection{Advancements in Natural Language Processing}
\label{sec:advancements_nlp}
% Introduce the progression towards more sophisticated models
% Mention the use of machine learning and deep learning in emotion classification


\section{Integrating Psychological Theories with LLMs}
\section{Large Language Models (LLMs) and Their Capabilities}
\label{sec:llms_capabilities}

\subsection{Constroled Generation}
\label{sec:llms_emotion_classification}
% Discuss how LLMs have been used in emotion and sentiment analysis
% Highlight their ability to handle context and generate human-like text
% Reference recent studies utilizing LLMs for emotion tasks

\subsection{Role Play prompting}
\label{sec:context_handling_llms}
% Explain how LLMs process and retain context over longer text spans
% Discuss improvements in context window sizes
% Cite technical papers on context mechanisms in LLMs

\subsection{Challenges and Limitations of LLMs}
\label{sec:llm_challenges}
% Address issues like non-determinism, biases, and computational resources
% Reference studies on LLM limitations and efforts to mitigate them

\section{Integrating Psychological Theories with LLMs}
\label{sec:integrating_theories_llms}

\subsection{Synergies Between Barrett's Theory and LLMs}
\label{sec:synergies_barrett_llms}
% Discuss how LLMs can operationalize Barrett's theory in computational models
% Explain the potential for context-aware emotion classification
% Reference any existing frameworks or attempts

\subsection{Techniques for Guiding LLMs}
\label{sec:techniques_guiding_llms}
% Introduce role-play prompting, controlled generation, structured output
% Explain how these techniques help align LLM outputs with specific theories
% Cite relevant methodological papers

\subsection{Preprocessing and Context Sphere Construction}
\label{sec:preprocessing_context_sphere}
% Discuss the importance of data preprocessing in enhancing LLM performance
% Explain how building a "Context Sphere" captures user-centric information
% Reference studies on context augmentation in NLP

\subsection{Current Research Gaps}
\label{sec:research_gaps}
% Identify gaps between psychological theories and informatics implementations
% Emphasize the lack of interdisciplinary approaches
% Set the stage for how your research addresses these gaps

\section{Summary}
\label{sec:summary}
% Summarize the key points from the literature review
% Reinforce the need for your research integrating Barrett's theory with LLMs

% Bibliography
\bibliographystyle{apalike}
\bibliography{references}

```

<additional_context>

2).
Overall, the proposed classification system aims to capture the dynamic and multifaceted
nature of emotions, using parameters that reflect the individual’s context and experi-
ences (CoppiniE xperimentsonreallif e20230612N GA9F U E4pages2 − 3).
Answer: Lisa Feldman Barrett proposes a nuanced approach to classifying emotions,
emphasizing the complexity and variability of emotional experiences. Her framework
suggests that emotions should not be classified based on fixed categories but rather
through a high-dimensional, idiographic, and multimodal sampling approach. This in-
volves measuring a combination of biological features, such as autonomic physiology
changes, eye-tracking, and brain imaging, alongside psychological features like cogni-
tive appraisal and functional aspects, to account for both internal and external contexts
(Barrett2021 pages 29-32).
Barrett’s Conceptual Act Theory posits that emotions are constructed in the moment
from core affect—a combination of valence (pleasure-displeasure) and arousal—and the
individual’s conceptual understanding of the situation. This theory challenges tradi-
tional views of emotions as biologically hardwired and discrete, suggesting instead that
emotions are shaped by personal and cultural factors and are context-dependent (Bar-
rett2021 pages 44-46).
Additionally, Barrett distinguishes between core affect and prototypical emotional episodes.
Core affect refers to basic feelings that are not necessarily directed at anything specific,
while prototypical emotional episodes involve complex cognitive processes and are di-
rected at specific objects or events (Barrett1999 pages 2-3). This classification considers
the intensity and duration of core affect and the cognitive structures involved in these
episodes (Barrett1999 pages 2-3).
8 Research Methodology
8.1 Proposed Research Methods
The methodology for this research is based on the Design Science Research (DSR) frame-
work, as outlined by Alan R. Hevner [43, 44]. The primary research output is the creation
of an artefact—a context-aware emotion classification pipeline. This approach is struc-
tured into three main cycles:
5
8.1.1 Relevance Cycle
This connects the research to real-world applications, ensuring relevance and applicabil-
ity. The requirement for a context-aware emotion classification pipeline stems from the
need to accurately capture and classify emotions in online forums. This addresses the
call by Lisa Feldman Barrett to investigate and reconsider how emotions are classified
[4].
Real-world applications include all text classifications where additional context is avail-
able for a deeper understanding. Particularly in online news forums, where there is an
interplay that is difficult to analyze so far, this application can offer a possible solution
to achieve a more nuanced analysis compared to traditional single-sentence sentiment
analysis or bag-of-words approaches.
8.1.2 Rigor Cycle
This cycle grounds the research in theoretical foundations, including the work of Lisa
Feldman Barrett, NLP, machine learning, and recent developments in LLMs. The inno-
vation in this research is the integration of various ideas on guiding LLMs to reason and
provide formatted output, building context from text data, and making use of the LLMs’
capabilities to understand and generate complex text. While some preprocessing steps
are well-known, they are crucial for working with the data [44].
The theoretical foundation is Barrett’s theory of constructed emotions, which informs the
design of the classification pipeline. This approach combines theories of psychology with
concepts from computer science, creating a comprehensive framework for context-aware
emotion classification.
8.1.3 Design Cycle
This cycle involves the design and evaluation of the artefact. The steps include pre-
processing the dataset, developing the classification pipeline, and evaluating its perfor-
mance.
Design Steps:
1. Preprocessing: Clean and prepare the dataset, ensuring it is suitable for analysis
by LLMs. This involves a significant effort to structure and gather the relevant
data into the "context sphere." This sphere of a user will be transferred into a
6
structured format to represent the online forum context, making it easier for the
LLM to understand and process.
2. Context Sphere: The context sphere represents the online presence of a user. This
includes all threads a user was active in, all comments made by the user, as well
as all comments from other users. Information about the articles where comments
were published and metadata of the articles are also included. All available meta-
data is aggregated into a file that represents a user’s context sphere.
Each user will be represented using a mix of Markdown (.md) and possibly XML
tags. This structured format ensures that the LLM can better grasp the context and
structure of the data. This preprocessing step is crucial to build the user context
and will require considerable effort to implement correctly. It also requires careful
consideration of what to include and what to omit to reduce noise in the context
while providing enough information to maintain a comprehensive understanding of
the user’s online interactions.
3. LLM Integration: Use LLMs to analyze the context sphere and generate nuanced
classifications across multiple emotional attributes. The parameters are derived
from multiple sources and follow the concept of providing a diverse classification,
proposing an alternative to the choose-from-array approach used by Ekman. Pa-
rameters could be valence and arousal, measuring the core affect, as well as cog-
nitive appraisal, cultural influence, and emotional dynamics derived from Barrett’s
concept of constructed emotions [28, 29].
4. Guided Generation: The LLM will receive the context and will be guided through
various techniques, including role-play prompting [45], advanced reasoning through
chain-of-thought prompting [46], and structured output format through controlled
generation mode [47]. Companies like Google and OpenAI are using constrained
sampling or constrained decoding that restrict the LLM’s output to adhere to a
predefined structure, ensuring the generation of valid structured output [27].
5. System Integration: The integration of the preprocessing and LLM pipeline is chal-
lenging due to the interconnects between both steps. Adjusted preprocessing will
lead to different outputs in the LLM pipeline. Integrating both systems to work
harmoniously is the main task. This involves preprocessing the data into con-
text spheres and LLM-usable formats, employing Barrett’s concepts, and utilizing
7
state-of-the-art techniques to guide the LLM, ultimately producing high-quality text
output that can be used for evaluation. Achieving this harmony requires a deep un-
derstanding of both the psychological and computational aspects of the project.
8.2 Data Collection Techniques
The dataset used for this research is from Der Standard, with a size of 2 TB. Preprocessing
is essential to manage and prepare this data for analysis. Fan, Cheng, et al. provide a
comprehensive overview of data preprocessing techniques, including cleaning, reduction,
scaling, transformation, and partitioning [48]. For this thesis, non-linear methods will
be particularly relevant due to the use of LLMs, which involve several layers of non-linear
transformations.
8.3 Analysis Approaches
Due to the non-deterministic nature of LLMs, an iterative approach is used to improve
the prompts and usage of the LLM during development. Through multi-sampling, we en-
sure that the results are not merely random but reproducible. Approaches like majority
voting, as demonstrated by Li et al., are employed to ensure a reproducible output. It’s
important to note that a 1:1 reproduction will not be possible due to the inherent nature
of LLMs.
The collected output will be gathered and linked to the initial raw user data, the LLM call
with input, and the output with each attribute that was classified and the corresponding
reasoning of the LLM justifying the classification (from the perspective of the LLM). The
"reasons" the LLM generates and the corresponding classifications are the input for the
evaluation.
To assess the LLM’s performance, we will focus on the relevance of the LLM’s reasoning
and the consistency between reasoning and classification. This comprehensive data col-
lection and analysis process will enable iterative improvements to the LLM’s classification
accuracy and reasoning capabilities.
8.4 Evaluation
The evaluation of our context-aware emotion classification pipeline will be conducted
through qualitative surveys. This approach aims to assess the coherence and effec-
8
tiveness of the LLM’s reasoning and classifications, grounded in Lisa Feldman Barrett’s
theoretical framework on emotions. Chang et al., in "A Survey on Evaluation of Large
Language Models," outline how human evaluation can be done based on their findings.
Novikova, Jekaterina, et al. show that human evaluation is more reliable in "open-
generation tasks," and automatic evaluation through LLMs cannot replace human judg-
ment of system outputs. In the thesis, it is therefore suitable to use human evaluation
through a survey to evaluate the performance of the LLM output.
Central to our evaluation process is the presentation of classified attributes, such as
valence or arousal, along with the LLM’s corresponding reasoning for each classification.
For instance, we will provide human evaluators with statements like:
"The user’s posts exhibit high arousal because they frequently use intense
and expressive language, indicating a heightened emotional state."
Or:
"The user’s comments reflect a positive valence as they consistently employ
positive emotion words and convey supportive sentiments."
This allows us to directly query human judgment on the LLM’s reasoning process.
Human evaluators will be asked to assess:
1. The coherence of the LLM’s reasoning.
2. The alignment between the reasoning and the classification.
3. The overall plausibility of the classification given the provided context.
This is only one example to show how such an evaluation can look. The actual survey
using the finalized parameters will look different and still needs to be developed with the
corresponding items. van der Lee et al. and Awasthi et al. show what to consider when
building survey items.
This approach acknowledges that while LLMs can simulate human-like reasoning pro-
cesses, they cannot truly "think" in the way humans do. By leveraging human judgment,
we aim to evaluate aspects of emotional understanding that LLMs might struggle to fully
comprehend or may only superficially simulate.
The evaluation will also consider the effectiveness of our pipeline in capturing the nu-
anced, context-dependent nature of emotions as proposed by Barrett’s theory. Evalua-
tors will be asked to consider whether the classifications and reasoning reflect an under-
standing of emotions as constructed experiences rather than fixed, universal categories.
9
Through this evaluation process, we aim to not only assess the performance of our LLM-
based pipeline but also to gain insights into the strengths and limitations of using LLMs
for complex, context-dependent tasks such as emotion classification in online forums.
8.5 Potential Challenges and Limitations
It’s important to acknowledge that the field of emotion recognition using LLMs is still in
its infancy. As such, this research represents an early step in a rapidly evolving area.
The approach and findings presented here are not expected to be perfect but rather to
contribute to the ongoing development of this field, which will likely progress alongside
advancements in LLM technology and emotion research.
The research is limited by the timeframe of the master’s thesis, approximately 675 hours.
There will be a lot of biases in the data and in the LLMs, which is currently unavoidable.
The complexity of LLMs presents a significant challenge, as while there are techniques
and methods available to work with them, their inner workings are not yet fully un-
derstood by researchers. Mitigating issues like hallucinations and ethical concerns is
essential and will be part of the process when developing the pipeline.
The evaluation will not include long-term studies or extensive user feedback, which are
beyond the scope of this thesis but could be explored in future research. It should also
be acknowledged that emotion classification is a complex and nuanced field, and this
research represents an initial exploration rather than a definitive solution.
By addressing these challenges and leveraging recent advancements in LLMs and emo-
tion theory, this research aims to provide a meaningful contribution to the field of emo-
tion classification and the broader understanding of online discourse dynamics.
</additional_context>


---

# **Explanation and Suggested Literature**

Below are detailed explanations for each section, along with suggested papers to cite. You can include these citations in your `references.bib` file.

---

## \section{Introduction to Emotion Classification}

- **Purpose:** Set the stage for the literature review by highlighting the importance of emotion classification in both psychology and informatics.
- **Suggested Content:** Briefly introduce how emotions play a crucial role in human interaction and the growing need to accurately classify emotions in digital communication.

---

## \section{Psychological Theories of Emotion}
\label{sec:psychological_theories}

### \subsection{Paul Ekman's Theory of Basic Emotions}
\label{sec:ekman_theory}

- **Purpose:** Explain Ekman's theory, which posits that there are universal emotions recognizable through facial expressions.
- **Suggested Citations:**
  - Ekman, P. (1992). An argument for basic emotions. *Cognition & Emotion*, 6(3-4), 169-200.
  - Ekman, P., & Friesen, W. V. (1971). Constants across cultures in the face and emotion. *Journal of Personality and Social Psychology*, 17(2), 124.

#### \subsubsection{Universal Facial Expressions}
\label{sec:universal_expressions}

- **Discuss:** The six basic emotions and the evidence supporting universal facial expressions.
- **Citations:** Ekman's cross-cultural studies.

#### \subsubsection{Critiques and Limitations of Ekman's Theory}
\label{sec:limitations_ekman}

- **Discuss:** Criticisms regarding cultural differences and contextual factors.
- **Suggested Citations:**
  - Russell, J. A. (1994). Is there universal recognition of emotion from facial expression? A review of the cross-cultural studies. *Psychological Bulletin*, 115(1), 102-141.

### \subsection{Lisa Feldman Barrett's Theory of Constructed Emotion}
\label{sec:barrett_theory}

- **Purpose:** Introduce Barrett's theory, emphasizing emotions as constructed experiences influenced by context.
- **Suggested Citations:**
  - Barrett, L. F. (2017). *How emotions are made: The secret life of the brain*. Houghton Mifflin Harcourt.
  - Barrett, L. F. (2006). Solving the emotion paradox: Categorization and the experience of emotion. *Personality and Social Psychology Review*, 10(1), 20-46.

#### \subsubsection{Concept of Emotional Granularity}
\label{sec:emotional_granularity}

- **Discuss:** The idea that individuals experience emotions with varying granularity.
- **Citations:** Barrett's work on affective science.

#### \subsubsection{Evidence Supporting Constructed Emotion}
\label{sec:evidence_constructed_emotion}

- **Discuss:** Neuroscientific and psychological studies supporting the theory.
- **Suggested Citations:**
  - Lindquist, K. A., & Barrett, L. F. (2012). A functional architecture of the human brain: Emerging insights from the science of emotion. *Trends in Cognitive Sciences*, 16(11), 533-540.

### \subsection{Comparison of Ekman's and Barrett's Theories}
\label{sec:comparison_theories}

- **Purpose:** Highlight the key differences and their implications for emotion classification.
- **Discuss:** How Ekman's theory supports discrete categories, while Barrett's emphasizes dimensional and contextual aspects.

### \subsection{Development in Psychological Emotion Classification}
\label{sec:development_psychology}

- **Purpose:** Trace the evolution of emotion theories in psychology.
- **Suggested Citations:**
  - Russell, J. A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*, 39(6), 1161.

---

## \section{Emotion Classification in Informatics}
\label{sec:emotion_informatics}

### \subsection{Traditional Computational Approaches}
\label{sec:traditional_methods}

- **Purpose:** Describe how early computational models relied on discrete categories influenced by Ekman's theory.
- **Suggested Citations:**
  - Picard, R. W. (1997). *Affective computing*. MIT Press.
  - Poria, S., Cambria, E., Bajpai, R., & Hussain, A. (2017). A review of affective computing: From unimodal analysis to multimodal fusion. *Information Fusion*, 37, 98-125.

### \subsection{Limitations of Discrete Classification Models}
\label{sec:limitations_discrete_models}

- **Discuss:** The inability of these models to capture nuanced emotions and context.
- **Suggested Citations:**
  - Calvo, R. A., & D'Mello, S. (2010). Affect detection: An interdisciplinary review of models, methods, and their applications. *IEEE Transactions on Affective Computing*, 1(1), 18-37.

### \subsection{Advancements in Natural Language Processing}
\label{sec:advancements_nlp}

- **Purpose:** Introduce how machine learning and deep learning have advanced emotion classification.
- **Suggested Citations:**
  - Young, T., Hazarika, D., Poria, S., & Cambria, E. (2018). Recent trends in deep learning based natural language processing. *IEEE Computational Intelligence Magazine*, 13(3), 55-75.

### \subsection{Multimodal Emotion Recognition}
\label{sec:multimodal_recognition}

- **Discuss:** The benefits of combining textual, visual, and audio data.
- **Suggested Citations:**
  - Poria, S., Cambria, E., Hazarika, D., & Vij, P. (2018). Multimodal sentiment analysis: Addressing key issues and setting up the baselines. *IEEE Intelligent Systems*, 33(6), 17-25.

---

## \section{Large Language Models (LLMs) and Their Capabilities}
\label{sec:llms_capabilities}

### \subsection{Overview of LLMs}
\label{sec:overview_llms}

- **Purpose:** Explain what LLMs are, their architectures, and capabilities.
- **Suggested Citations:**
  - Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. *NAACL*.
  - Brown, T. B., et al. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, 33, 1877-1901.

### \subsection{LLMs in Emotion Classification}
\label{sec:llms_emotion_classification}

- **Discuss:** How LLMs have been applied to sentiment analysis and emotion recognition tasks.
- **Suggested Citations:**
  - Zhang, J., & Wang, H. (2021). BERT-based emotional dynamics detection in text. *IEEE Access*, 9, 138403-138413.

### \subsection{Context Handling in LLMs}
\label{sec:context_handling_llms}

- **Explain:** Mechanisms like attention that allow LLMs to process context.
- **Suggested Citations:**
  - Vaswani, A., et al. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 5998-6008.

### \subsection{Challenges and Limitations of LLMs}
\label{sec:llm_challenges}

- **Discuss:** Issues like non-determinism, biases, large computational requirements.
- **Suggested Citations:**
  - Bender, E. M., et al. (2021). On the dangers of stochastic parrots: Can language models be too big? *FAccT*, 610-623.

---

## \section{Integrating Psychological Theories with LLMs}
\label{sec:integrating_theories_llms}

### \subsection{Synergies Between Barrett's Theory and LLMs}
\label{sec:synergies_barrett_llms}

- **Discuss:** The compatibility of context-dependent theories with LLMs' ability to handle context.
- **Suggested Citations:**
  - Hollenstein, N., & Zhang, C. (2019). Entity recognition at first sight: Improving NER with eye movement information. *ACL*, 1-10.

### \subsection{Techniques for Guiding LLMs}
\label{sec:techniques_guiding_llms}

- **Explain:** Role-play prompting, controlled text generation, and ensuring structured outputs.
- **Suggested Citations:**
  - Reynolds, L., & McDonell, K. (2021). Prompt programming for large language models: Beyond the few-shot paradigm. *arXiv preprint arXiv:2102.07350*.

### \subsection{Preprocessing and Context Sphere Construction}
\label{sec:preprocessing_context_sphere}

- **Discuss:** How preprocessing enhances model performance and the creation of context spheres from user data.
- **Suggested Citations:**
  - Liu, H., & Singh, P. (2004). ConceptNet—a practical commonsense reasoning tool-kit. *BT technology journal*, 22(4), 211-226.

### \subsection{Current Research Gaps}
\label{sec:research_gaps}

- **Identify:** The lack of models that fully integrate contemporary psychological theories with advanced computational methods.
- **Emphasize:** The need for interdisciplinary approaches.

---

## \section{Summary}
\label{sec:summary}

- **Purpose:** Recap the key points and reinforce the necessity of your research.
- **Tie Together:** How integrating Barrett's theory with LLMs addresses the identified gaps.

---

# **Additional Tips**

- **Maintain Clarity:** Ensure that each section logically leads to the next.
- **Use Transitional Sentences:** At the end of each section or subsection, include a brief sentence that connects to the subsequent section.
- **Define Technical Terms:** When introducing psychological concepts or informatics techniques, provide definitions for readers unfamiliar with the terms.
- **Figures and Tables:** Consider including diagrams that illustrate the theories, model architectures, or processes.
  - For example, a comparison chart between Ekman's and Barrett's theories.

# **Creating the References File**

- Your `references.bib` file should include all the citations with proper BibTeX entries. For example:

```bibtex
@book{barrett2017how,
  title={How emotions are made: The secret life of the brain},
  author={Barrett, Lisa Feldman},
  year={2017},
  publisher={Houghton Mifflin Harcourt}
}

@article{ekman1992argument,
  title={An argument for basic emotions},
  author={Ekman, Paul},
  journal={Cognition & Emotion},
  volume={6},
  number={3-4},
  pages={169--200},
  year={1992},
  publisher={Taylor \& Francis}
}
```

- Ensure all references are properly formatted and included in your bibliography.

# **Moving Forward**

- **Begin Writing:** Start filling in each section with detailed content, integrating your ideas and additional literature you've identified.
- **Iterative Refinement:** As you write, you may find the need to adjust the structure slightly. That's perfectly fine; the outline is a guideline.
- **Seek Feedback:** Share drafts of your literature review with your supervisor or peers for feedback.

---

Remember, the literature review sets the foundation for your research. It demonstrates your understanding of the field, identifies gaps, and positions your work within the existing body of knowledge. By carefully crafting this chapter, you'll provide a strong basis for the rest of your thesis.

If you have any further questions or need assistance with specific sections, feel free to ask!