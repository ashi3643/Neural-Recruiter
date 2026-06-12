# NeuralRecruiter (Track 01) — India Runs 2026 Hackathon

**Intelligent Candidate Discovery Engine for Redrob AI**  
*A Competition-Grade, Offline-First, Multi-Stage Hybrid Ranking Pipeline*

NeuralRecruiter is an elite, high-performance candidate discovery and ranking system engineered to process massive talent pools (100,000+ profiles) and identify the top 100 candidates for a highly nuanced **Senior AI Engineer** role at Redrob AI. 

Our core design principle is **architectural honesty over AI-slop**. Instead of relying on expensive, black-box, or network-bound LLM API calls during the ranking loop (which violates competition speed and connectivity constraints), NeuralRecruiter utilizes a highly optimized, fully deterministic **Multi-Stage Hybrid Scoring Pipeline**.

---

## 🚀 Key Features & Performance Metrics

- **Extremely Fast**: Processes **100,000+ profiles in ~30–45 seconds** on a standard single-core CPU, using streaming file IO with zero external package dependencies.
- **Robust Guardrails**: Features a comprehensive 8-point **Honeypot Filter** that automatically flags and disqualifies profiles with fraudulent credentials, timeline paradoxes, or fake expert skill histories.
- **Semantic Precision**: Implements an offline semantic key-phrase alignment scorer assessing breadth and frequency of Information Retrieval (IR), recommendation, and search system concepts over headlines, summaries, and career histories.
- **Recruiter Guardrails**: Applies severe penalties for massive consulting systems (TCS, Infosys, Genpact, Deloitte, etc.) and wrong-domain AI specialists (e.g., computer vision and speech engineers) to prioritize candidate alignment.
- **Fully Synchronized**: Includes a fully synchronized TypeScript mirror (`scorer.ts`) powering a reactive sandbox environment for the recruiter.

---

## 🛠️ Multi-Stage Pipeline Architecture

NeuralRecruiter passes each profile through a strict linear multi-stage funnel:

```
  📋 100,000 Candidates
         │
         ▼  (Stage 1)
  🛡️ Honeypot Scans (Timeline Paradoxes, Expert Hacks, Academic Paradoxes)
         │  ↳ [Fail] ➔ Blown to Score 0.0 (Absolute Disqualification)
         ▼  (Stage 2)
  🏷️ Title Tier Gate (Tier A: Core AI/Search, Tier B: Adjacent SWE, Tier C: Non-Tech)
         │  ↳ [Tier C] ➔ Suppressed to Floor (Score 0.01)
         │  ↳ [Tier B with 0 AI Skills] ➔ Suppressed to (Score 0.05)
         ▼  (Stage 3)
  🧠 Multi-Signal Scoring Engine (Career, verified Skills depth, Semantic JD Fit)
         │  ↳ Weighted Sum calculation (Career, Skills, JDFit, Exp, Behav, Loc, GitHub)
         ▼  (Stage 4)
  ⚠️ Multipliers & Penalties (Severe inactivity penalties, 0.5x Wrong-Domain CV/Speech Penalty)
         │
         ▼
  🏆 Precise Top 100 Shortlist (export ready)
```

### 1. Stage 1: Honeypot & Timeline Paradox Detection
Filters fraudulent profiles with:
- **Timeline Paradox**: Careers duration exceeds stated years of experience by more than 35%.
- **Expert Skills Hack**: Stating `expert` for multiple core tech skills with 0 months of actual duration.
- **Lack of Endorsements**: Claiming 8+ expert skills with under 5 total peer endorsements.
- **Future Timelines**: Claiming degree or certification completion in years past the current date ($2026$).

### 2. Stage 2: Title Tiering Gates & Suppression
- **Tier A (Core AI/Search/ML)**: Full scoring eligibility.
- **Tier B (Adjacent Tech, e.g., Backend Python Engineers)**: Eligible *only if* they possess core vector search or information retrieval skills, otherwise suppressed to exactly `0.05`.
- **Tier C (Non-Technical, e.g., HR/Finance/Operations managers stuffing keywords)**: Hard suppressed to a floor of exactly `0.01`.

### 3. Stage 3: Multi-Signal Scoring Engine
Candidate scores are computed against **canonical, normalized signal weights summing exactly to 1.00**:

| Signal Metric | Weight | Description |
| :--- | :---: | :--- |
| **Career Quality** | `0.20` | Strong product company backgrounds vs. heavy outsourcing consulting experience (e.g., Genpact, TCS, Deloitte penalties applied proportionally). |
| **Skills Depth + Verification** | `0.22` | Mastery/duration of core search technologies combined with verified Redrob candidate skill assessment scores. |
| **JD Semantic Fit** | `0.15` | Natural Language processing of headlines, summaries, and career role descriptions for search/indexing domain concepts. |
| **Title Alignment** | `0.15` | Perfect alignment of current title with senior ML, AI, or Information Retrieval roles. |
| **Experience Range** | `0.10` | Standard sweet-spot for Redrob's founding team: **6–8 years** gets 1.0; adjacent 5 or 9 years gets 0.85; others drop progressively. |
| **Behavioral Availability** | `0.10` | Active response rates, short notice periods, interview completion flags, and open-to-work signals. |
| **Location Fit** | `0.04` | Presence in elite Indian engineering hubs (Pune, Noida, Hyderabad, Bangalore, NCR) or relocation readiness. |
| **GitHub Coding Signal** | `0.04` | GitHub contribution scores parsed as engineering habit proxies. |

---

## 🏃 Reproducibility & Local Execution

### Prerequisites
NeuralRecruiter requires only a standard Python environment:
- **Python >= 3.10**
- Zero external package dependencies! Runs on the Python Standard Library.

### 1. Generating Test Candidate Data (Optional)
To test the pipeline locally using high-fidelity test profiles representing superstars, keyword stuffers, adjacent engineers, domain-penalized profiles, consulting, and timeline honeypots:
```bash
python generate_test_candidates.py
```
This writes a mock evaluation dataset to `candidates.jsonl`.

### 2. Running the Ranking Engine
Process the candidates and output the final, compliant top-100 shortlist CSV file:
```bash
python rank.py --candidates candidates.jsonl --out submission.csv
```

### 3. Validating your Submission
Verify that your generated shortlist meets 100% of the tournament rules and column constraints:
```bash
python validate_submission.py submission.csv
```

---

## 📁 Repository Structure

```
├── candidates.jsonl          # Evaluation dataset input
├── rank.py                   # Core ranking engine (Pure Python standard library)
├── validate_submission.py    # Submission validation rules script
├── submission_metadata.yaml  # Hackathon team and model configuration metadata
├── requirements.txt          # Environment dependencies list (Standard Library Only)
├── src/
│   ├── scorer.ts             # TypeScript mirror of the ranking algorithms
│   ├── constants.ts          # Consolidated weights and consulting/domain keyword lists
│   ├── types.ts              # System interfaces and types definitions
│   └── App.tsx               # Primary sandbox dashboard recruiter simulator
```

*Crafted for the India Runs 2026 Hackathon | Track 01: Intelligent Candidate Discovery*
