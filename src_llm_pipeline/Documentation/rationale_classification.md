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