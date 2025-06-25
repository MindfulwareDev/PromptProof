# PromptProof

Why do I need to use this prompt before starting a new AI session?

"Hic sunt dracones"

Introduction: Yes, there are thousands of "AI's best top 100 prompts" list. This is not one. The only focus is to take responsibily for the outputs and not blindly accept as truth. A secondary goal is to reduce overall tokens used for any API call. 

A lightweight, plug-and-play guardrail pack for ChatGPT that replaces anxiety with accountability.

Verified facts
• Purpose – PromptProof is an open-source system-prompt template, licensed under GPL v3, that snaps into “Custom Instructions” or an API system message.
• What it does – It forces the assistant to cite sources, label every unverified claim, separate facts from speculation, and finish each reply with a self-estimated confidence score—so users always know what is certain and what is not.
• Why it matters – By adding these guardrails, PromptProof reduces the risk of hallucinations and gives everyday users a clear, transparent basis for trusting (or double-checking) AI answers.
• How to use – Copy the prompt block into ChatGPT’s settings or your API setup, save, and start any chat in “trust mode.” No extra software or coding is required.

Available Prompts:

- SpeculationSpeedBump.txt ("Slow Your Roll, GPT!")
Speculation Speed Bump is a one-file guardrail script that plugs into ChatGPT’s Custom Instructions or an API system prompt. It forces the assistant to cite real sources, label every unverified sentence, ask for clarification instead of guessing, and finish each reply with a self-estimated confidence score.

Value statement: By making uncertainty visible and blocking fabricated facts before they reach the user, Speculation Speed Bump turns AI output into a transparently trustworthy resource—reducing hallucination risk and helping anyone rely on ChatGPT for accurate, source-backed answers.

- Notify_of_AI_usage.txt ("Slow Your Roll, User!")
Notify_of_AI_usage is a one-line guardrail script that plugs into ChatGPT’s Custom Instructions or an API system prompt. Gives a clear, short message after the last output footer. It is up to the author to utilize the text. However, shame if you don't!

- Ethical-Guard.txt ("Slow Your Roll, Bad Boy!") The ethics_alert flag is a simple boolean indicator your “Ethical-Guard” uses to signal whether a user request or the model’s own draft response violates any core professional duty.
	•	"ethics_alert": false
Everything in the prompt or reply so far passes both the ACM Code of Ethics and duty-of-care principles (Hippocratic, legal, policing, etc.). No further action is needed.
	•	"ethics_alert": true
One or more rules have been tripped—e.g. advice that facilitates wrongdoing, breaches of privacy, or misrepresentation. In that case the guard will also supply:
	1.	acm_sections_triggered: exactly which sections of the ACM Code were violated
	2.	parallel_oaths: which professional-oath analogies apply (medicine, law, policing, etc.)
	3.	explanation: a concise rationale for why it’s a breach
	4.	suggested_remediation: either a refusal template or a safe-completion path

By checking ethics_alert first, your application can enforce or log policy breaches in a structured, auditable way.
