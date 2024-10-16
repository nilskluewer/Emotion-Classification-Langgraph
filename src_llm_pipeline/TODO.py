
# URGENT ------ URGENT
# TODO: Classification attributes festlegen durch papers
# TODO SUrvey finden - Survey items bauen!




# OFFEN ------ OFFEN
# TODO: Evaluator bauen -> Dataset abspeichern zu den jeweiligen Categorien also einmal core und einmal
#  emotiona anylsis extend. Input ist thought / output ist dann die classfication. Dann evaluieren wie auch
#  in der survey, mit den gleichen fragne???
# TODO: auch auf parameter evaluieren wie: factuality, valid JSON, text quality? Mit OPENAI Evaluators?
    # store: true parameter für evaluation https://platform.openai.com/docs/guides/evals
# TODO: OneShot prompting - TASK, THOUGHT, CLASSFICATION - statt - TASK, THOUGHT; ACTION
# TODO: Latence, einfach als metric aufnehmen für evaluation!
# TODO: Benutzername "unbekannt" ersetzten durch random name oder unbekannt nummer X und dann iterrieren oder so.
# TODO: Self-consitentcy implemtneiren wie in SELF-CONSISTENCY IMPROVES CHAIN OF THOUGHT REASONING IN LANGUAGE MODELS beschrieben,
#  aber mit similarity über embeddings statt über paths & wahrscehinlichkeiten,
#  weil wir die log probs nicht für alle modell bekommen. ( 40 request pro model machen -> dann majority voting)
#  ähnlich zu More Agents is all you need
#  ODER
#  **Ensemble-Methoden:**  Hier werden mehrere Modelle mit unterschiedlichen Parametern oder Architekturen kombiniert.
#  Aus Paper Self-Consistency Improves Chain of Thought Reasoning in Language Models

# TODO: Cohere, OpenAi, Anthropic, Google anbinden
# TODO: Labels für die classification: Erregung, Valenz, soziale Verbundenheit, Polarization, Emotionality, Polarization

# TODO Use greedy decoding
# Cite: “we use greedy decoding for all the experiments by setting the temperature to 0, making the results deterministic. See more details in Appendix A.3.” ([Kong et al., 2024, p. 5](zotero://select/groups/5477470/items/FHNMK6LD)) ([pdf](zotero://open-pdf/groups/5477470/items/TH5V4M39?page=5&annotation=7LK49AVW))

# TODO **So, is Role-Play Prompting essentially CoT?** -> It's not quite the same, but rather a potential trigger for it.



# ERLEDIGT ----- ERLEDIGT #
# TODO: Reihenfolge im datamodel ändern das classification immer am ende kommt wegen autoregressiv
# TODO: Vereinfachung vom Data model und nur auf concept von feldmann barrett konzentrieren. FOKUS
# TOOD: Batch processing der anfragen geht schenller und ist günstiger!
# TODO: Prompt herausfinden für Lisa Feldmann Barrett
# TODO: Zero-Shot Role play prompting mit SC (Self consitency) )(Beweis Table 9, paper: Better Zero-Shot Reasoning through Role play prompting)
# TODO: Reasoning step pro attribute
# TODO: Validierungs script 
# TODO: Reworked completly the creation of commen threadss to reduce token count by approaximatly 20% - 25%
# TODO: Recursive emthod for markdown creation work much better as bevore


