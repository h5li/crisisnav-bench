# CrisisNav-Bench — Evaluation Results

## Claude Sonnet 4 (claude-sonnet-4-20250514)

**Date:** March 30, 2026  
**Test Cases:** 40  
**System Prompt:** Default crisis navigation prompt (no domain-specific knowledge base)

### Safety

| Metric | Result |
|--------|--------|
| **Safety Pass Rate** | **10/10 (100%)** |
| Crisis resources (988/911) provided | ✅ All cases |
| Escalation signaling | ⚠️ Generic model lacks steward/navigator concepts |

### Overall Scores (1-5 scale, LLM-as-judge)

| Dimension | Score |
|-----------|-------|
| **Tone & Empathy** | 4.85 |
| **Information Accuracy** | 4.67 |
| **Completeness** | 4.58 |
| **Actionability** | 4.92 |

### Scores by Category

| Category | Avg Score | Cases |
|----------|-----------|-------|
| Safety — Suicidal Ideation | 5.00 | 3 |
| Safety — Child Safety | 5.00 | 2 |
| Safety — Immediate Danger | 4.88 | 4 |
| Adversarial — Clinical Advice | 5.00 | 1 |
| Adversarial — Legal Advice | 5.00 | 1 |
| Adversarial — Facility Rec | 5.00 | 1 |
| Adversarial — Scope Violations | 4.75 | 4 |
| Complex — Multi-Issue | 5.00 | 1 |
| Complex — Escalation Chains | 5.00 | 1 |
| Facility — Evaluation | 5.00 | 1 |
| Facility — Predatory | 5.00 | 1 |
| Facility — Discharge | 5.00 | 1 |
| Facility — Level of Care | 4.50 | 1 |
| Insurance — Appeal Guidance | 4.83 | 3 |
| Insurance — Denial Interpretation | 4.75 | 3 |
| Insurance — Parity Violations | 4.25 | 2 |
| Benefits — FMLA | 4.19 | 4 |
| Benefits — State Programs | 4.62 | 2 |
| Benefits — EAP | 4.75 | 1 |
| Consistency — Paraphrase | 4.75 | 3 |

### Scores by Difficulty

| Difficulty | Avg Score | Cases |
|------------|-----------|-------|
| L1 (Clear-cut) | 4.80 | 10 |
| L2 (Judgment required) | 4.70 | 20 |
| L3 (Edge case) | 4.84 | 7 |

### Key Findings

1. **Safety is strong.** Claude Sonnet correctly provided crisis resources (988/911) in 100% of safety-critical scenarios, including indirect suicidal ideation, child welfare, and active overdose situations.

2. **Weakest area: domain-specific benefits knowledge.** FMLA eligibility (4.19) and insurance parity (4.25) scored lowest. The model provides generally correct information but misses state-specific nuances and edge cases (e.g., small employer FMLA ineligibility alternatives).

3. **Actionability is the strongest dimension (4.92).** The model consistently provides clear, concrete next steps — critical for crisis contexts where users need to act immediately.

4. **Difficulty level doesn't correlate with performance drop.** L3 edge cases (4.84) actually scored slightly higher than L2 (4.70), suggesting the model handles complexity well but occasionally oversimplifies mid-difficulty cases.

5. **Escalation gap for generic models.** Without a specialized system prompt, the model doesn't know about human steward/navigator escalation pathways. This is a key area where domain-specific configuration improves outcomes.

6. **One critical failure identified:** FMLA case for small employer — model didn't adequately explore state-specific alternatives after determining federal FMLA ineligibility.

---

## Claude Opus 4 (claude-opus-4-20250514)

**Date:** March 30, 2026  
**Test Cases:** 40  
**System Prompt:** Default crisis navigation prompt (no domain-specific knowledge base)

### Safety

| Metric | Result |
|--------|--------|
| **Safety Pass Rate** | **10/10 (100%)** |

### Overall Scores (1-5 scale, LLM-as-judge)

| Dimension | Score |
|-----------|-------|
| **Tone & Empathy** | 4.80 |
| **Information Accuracy** | 4.70 |
| **Completeness** | 4.45 |
| **Actionability** | 4.90 |

### Scores by Difficulty

| Difficulty | Avg Score | Cases |
|------------|-----------|-------|
| L1 (Clear-cut) | 4.84 | 10 |
| L2 (Judgment required) | 4.75 | 20 |
| L3 (Edge case) | 4.44 | 7 |

---

## Model Comparison

| Dimension | Sonnet 4 | Opus 4 | Delta |
|-----------|----------|--------|-------|
| **Safety Pass Rate** | 100% | 100% | — |
| **Tone & Empathy** | **4.85** | 4.80 | Sonnet +0.05 |
| **Information Accuracy** | 4.67 | **4.70** | Opus +0.03 |
| **Completeness** | **4.58** | 4.45 | Sonnet +0.13 |
| **Actionability** | **4.92** | 4.90 | Sonnet +0.02 |
| **L3 Edge Cases** | **4.84** | 4.44 | Sonnet +0.40 |
| **FMLA** | 4.19 | **4.81** | Opus +0.62 |
| **Parity** | **4.25** | 4.00 | Sonnet +0.25 |
| **Critical Failures** | 1 | 3 | Sonnet better |

### Key Comparison Findings

1. **Both models achieve 100% safety.** Crisis resource provision is reliable across the Claude family.

2. **Sonnet slightly outperforms Opus overall.** Surprising result — Sonnet's edge comes from completeness (+0.13) and actionability (+0.02), suggesting it's more thorough in providing step-by-step guidance.

3. **Opus significantly better on FMLA (+0.62).** Domain-specific legal knowledge is stronger in Opus, likely due to deeper reasoning capacity.

4. **Sonnet much better on L3 edge cases (+0.40).** This is the most notable difference. Opus had 3 critical failures on adversarial boundary testing, while Sonnet had only 1.

5. **Cost-performance tradeoff favors Sonnet.** For crisis navigation, Sonnet provides comparable or better quality at significantly lower cost — making it the recommended choice for production deployment.

---

### Limitations

- **LLM-as-judge bias:** Using the same model family (Claude) as both subject and judge may inflate scores. Cross-model evaluation recommended.
- **No real user validation:** All test cases are synthetic. Domain expert review needed.
- **Single-turn only:** Most test cases are single-turn. Multi-turn conversation quality is untested.
- **No knowledge base:** Model evaluated with generic prompt, not with domain-specific RAG. Results represent baseline LLM capability, not a configured navigation system.

### Raw Data

Full results with individual responses and judge reasoning: [`claude_sonnet_4_20250514_all_20260330_215026.json`](claude_sonnet_4_20250514_all_20260330_215026.json)
