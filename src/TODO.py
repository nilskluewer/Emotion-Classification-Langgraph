# TODO: Prompt herausfinden für Lisa Feldmann Barrett
# TODO: Zero-Shot Role play prompting mit SC (Self consitency) )(Beweis Table 9, paper: Better Zero-Shot Reasoning through Role play prompting)
# TODO: Langchain ansatz implementieren bei dem reasoning im textfeld und die ausgabe als tool call gemacht wird.
# TODO: Self-consitentcy implemtneiren wie in SELF-CONSISTENCY IMPROVES CHAIN OF THOUGHT REASONING IN LANGUAGE MODELS beschrieben, aber mit similarity über embeddings statt über paths & wahrscehinlichkeiten, weil wir die log probs nicht für alle modell bekommen. ( 40 request pro model machen -> dann majority voting) ähnlich zu More Agents is all you need
# TODO: Cohere, OpenAi, Anthropic, Google anbinden
# TODO: Labels für die classification: Erregung, Valenz, soziale Verbundenheit, Polarization, Emotionality, Polarization


# TODO Use greedy decoding
# Cite: “we use greedy decoding for all the experiments by setting the temperature to 0, making the results deterministic. See more details in Appendix A.3.” ([Kong et al., 2024, p. 5](zotero://select/groups/5477470/items/FHNMK6LD)) ([pdf](zotero://open-pdf/groups/5477470/items/TH5V4M39?page=5&annotation=7LK49AVW))

# TODO **So, is Role-Play Prompting essentially CoT?** -> It's not quite the same, but rather a potential trigger for it.

