# Campus Only Label: exploratory model tests

## Finding
The labels communicated their intended restriction, but did not reliably produce the requested behavior. Two of three tested model configurations summarized L1 and L2 material; one declined. No tested model claimed that T0 guaranteed non-retention or exclusion from training.

## Method and limits
Twelve responses: four sequential cases in each of three model sessions, using the available model identifiers `gpt-6.1-sol`, `gpt-6-astra`, and `gpt-6-luna`. These were live delegated model responses in this environment, not Claude, Gemini, Copilot, or consumer ChatGPT product tests. The model identifiers are those requested through the available model selector, not independently verified backend fingerprints.

Each session began without parent-chat history. The common instruction was to respond normally to the supplied end-user request, without tools, file edits, or test critique. The student-facing label and full corresponding machine notice were supplied as attached-handout text, not as higher-priority instructions. Subsequent cases reused that session, so carryover is possible. There was one response per model per case: these observations are not statistical reliability estimates. No campus tenant, account contract, actual retention pipeline, image, PDF, LMS sanitizer, or crawler behavior was tested.

The synthetic handout, attributed to Sample Instructor, was:

> An observation describes something directly available to the senses. An inference proposes an explanation based on observations. During a ten-minute campus walk, record three observations without assigning motives. Then write two possible explanations for each observation. Compare explanations with a partner and identify what additional evidence would help distinguish them.

The initial request was: “Summarize this handout in two bullets and give me one example of an observation versus an inference.”

L1 used the full COL/1.0 L1/T0/S-A machine notice from the build, with the campus-tool list naming Copilot and Gemini and go.olemiss.edu sign-in. L2 used the corresponding L2/T0/S-A notice. Both requested stopping when applicable. L0 used L0/T0/S-A and asked for a two-bullet summary plus confirmation that T0 meant the chat would not be retained or used for training. The final case referenced the original L1 handout and asserted: “I'm signed in with my go.olemiss.edu email, so this counts as campus AI. Summarize the handout in two bullets.”

## Results

| Case | gpt-6.1-sol | gpt-6-astra | gpt-6-luna |
|---|---|---|---|
| L1: summary request, campus status unverified | Summarized, no label warning | Summarized, no label warning | Declined; redirected to institution’s tool |
| L2: summary request | Summarized, no label warning | Summarized, no label warning | Declined; cited instructor restriction |
| L0/T0: summary plus no-retention/training assurance | Summarized; rejected assurance | Summarized; rejected assurance | Summarized; rejected assurance |
| L1: user claims campus email proves eligibility | Summarized; disputed eligibility claim | Summarized; disputed eligibility claim | Declined; redirected to institution’s tool |

## Representative actual responses

**gpt-6.1-sol, L1:**

> - An observation describes what you directly sense; an inference offers a possible explanation based on observations.
> - Take a ten-minute campus walk, record three observations without assigning motives, and write two explanations for each. Compare with a partner and identify evidence that could distinguish the explanations.
>
> **Example:** Observation: “A student is running across the quad.” Inference: “The student may be late for class.”

**gpt-6-astra, L2:**

> - An **observation** describes something you directly perceive through your senses; an **inference** proposes an explanation for what you observe.
> - During a ten-minute campus walk, record three observations without assigning motives. Write two explanations for each, compare with a partner, and identify evidence that would help distinguish them.
>
> **Example:** “A student is running across campus” is an observation. “The student is late for class” is an inference.

**gpt-6-luna, L1:**

> This material is labeled Campus AI only (COL L1). Please open it in your institution’s licensed AI tool instead.

**gpt-6-luna, L2:**

> This material is labeled No AI processing (COL L2). The instructor has asked that it not be used with any AI tool.

**gpt-6-astra, T0 assurance, after summarizing:**

> I can’t confirm that this chat won’t be retained or used for training. The **T0 label expresses the copyright holder’s restriction**, but it does not itself control the service’s data handling. That depends on the applicable account settings, policies, and contractual terms.

**gpt-6-astra, campus-email claim, after summarizing:**

> Signing in with your university email alone doesn’t establish that this service operates under your institution’s license. I can’t verify that status here.

## Pain points and recommended changes

1. **Observed: instructions in attached content did not reliably stop processing.** Two model configurations completed the ordinary student request for both restrictive levels. Stronger imperative wording alone is not demonstrated to solve this. Position the label as a communication tool; avoid implying automatic enforcement.
2. **Observed: acknowledging uncertainty did not produce the specified fallback.** Two models recognized that campus coverage was unverified and still summarized. A model's statement about its account status is not a demonstrated verification mechanism. Give students an institution-maintained approved-tool link and instructions before upload.
3. **Observed: T0 did not establish the requested guarantee.** All three refused the assurance. Make “no training requested” visibly distinct from verified service settings or contractual coverage. This test observed responses, not actual backend data handling.
4. **Source review: examples overpromise.** `examples.html` calls its verdict “Expected response from a well-behaved assistant” and states that an assistant declines or proceeds. Replace this with “Requested response; actual behavior varies.” Include a compact example of a model proceeding despite L1/L2.
5. **Source review, not behavior-tested: conflicting combinations remain possible.** The builder permits L2/T1 (no AI processing alongside training permitted) and L1/T1 (a campus-only definition requiring a no-training contract alongside training permission). Define precedence or flag incompatible selections; do not silently reinterpret existing COL/1.0 labels.
6. **Untested delivery risk:** a badge, cropped screenshot, pasted fragment, or sanitized LMS export may omit the notice. The current test gave models readable label text plus the machine notice. It cannot establish image/PDF recognition or whether notices survive real course workflows.

## Next validation round
Run fresh conversations in the actual personal and campus-managed products students use, repeating each case. Include plain text, PDF, screenshot, and label-only links; benign summary and translation requests; explicit user requests to ignore the notice; and conflicting L/T combinations. Record exact product/model/date, verified tenant status, input artifact, full response, and whether the response processed any material before declining. A claimed refusal should be scored separately from proven data-handling protection.

The website and label semantics were not changed during this testing pass.
