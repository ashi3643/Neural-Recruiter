import React from 'react';
import { FileText, Shield, Terminal, Settings2, Sparkles, CheckCircle2 } from 'lucide-react';

export default function BlueprintView() {
  return (
    <div id="blueprint_view_card" className="bg-white border border-[#ececeb] rounded-xl p-8 text-[#1a1a1a] shadow-sm space-y-8">
      
      {/* Header section representing the deliverables */}
      <div className="border-b border-[#ececeb] pb-5">
        <h2 className="font-sans font-bold text-lg text-[#1a1a1a] flex items-center space-x-2 uppercase tracking-tight">
          <FileText className="w-5.5 h-5.5 text-[#1a1a1a]" />
          <span>Hackathon Submission Deliverables</span>
        </h2>
        <p className="text-[11px] text-[#888] font-mono mt-1 font-semibold uppercase tracking-tighter">
          India Runs: Data & AI Challenge Track 01 submission guidelines representation
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        
        {/* Deliverable 1 Card */}
        <div className="bg-[#fafaf9] border border-[#ececeb] p-5 rounded-xl flex flex-col justify-between">
          <div className="space-y-3">
            <span className="text-[9px] bg-[#f0f0ef] text-[#1a1a1a] font-mono px-2 py-0.5 rounded-full border border-[#ececeb] uppercase tracking-wider font-bold">
              Deliverable #1
            </span>
            <h3 className="font-sans font-bold text-sm text-[#1a1a1a] mt-1">Ready Ranked Output</h3>
            <p className="text-xs text-[#666] font-light leading-relaxed">
              Precisely compiled rank list CSV file matching schema: <code className="font-mono bg-[#f0f0ef] px-1 py-0.5 rounded text-[#1a1a1a] border border-[#ececeb]">candidate_id, rank, score, reasoning</code>.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-[#ececeb] text-[10px] text-green-700 font-mono flex items-center gap-1 font-bold">
            <CheckCircle2 className="w-3.5 h-3.5" /> Ready for Export
          </div>
        </div>

        {/* Deliverable 2 Card */}
        <div className="bg-[#fafaf9] border border-[#ececeb] p-5 rounded-xl flex flex-col justify-between">
          <div className="space-y-3">
            <span className="text-[9px] bg-[#f0f0ef] text-[#1a1a1a] font-mono px-2 py-0.5 rounded-full border border-[#ececeb] uppercase tracking-wider font-bold">
              Deliverable #2
            </span>
            <h3 className="font-sans font-bold text-sm text-[#1a1a1a] mt-1">The Blueprint Deck</h3>
            <p className="text-xs text-[#666] font-light leading-relaxed">
              Clear methodologies detailing multicriterion tokenizing weight models, signal filters and anti-honeypot matrices.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-[#ececeb] text-[10px] text-green-700 font-mono flex items-center gap-1 font-bold">
            <CheckCircle2 className="w-3.5 h-3.5" /> PDF Transcript Synced
          </div>
        </div>

        {/* Deliverable 3 Card */}
        <div className="bg-[#fafaf9] border border-[#ececeb] p-5 rounded-xl flex flex-col justify-between">
          <div className="space-y-3">
            <span className="text-[9px] bg-[#f0f0ef] text-[#1a1a1a] font-mono px-2 py-0.5 rounded-full border border-[#ececeb] uppercase tracking-wider font-bold">
              Deliverable #3
            </span>
            <h3 className="font-sans font-bold text-sm text-[#1a1a1a] mt-1">The Clean Repository</h3>
            <p className="text-xs text-[#666] font-light leading-relaxed">
              Well-commented TypeScript/Python codebase modeling weights logic, and running under target resource boundaries.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-[#ececeb] text-[10px] text-green-700 font-mono flex items-center gap-1 font-bold">
            <CheckCircle2 className="w-3.5 h-3.5" /> Git history authenticated
          </div>
        </div>

      </div>

      {/* Structured documentation tabs represent README information */}
      <div className="space-y-4">
        
        {/* Concept tab */}
        <div className="bg-white border border-[#ececeb] rounded-xl p-6 space-y-4 shadow-sm">
          <h3 className="text-xs font-mono text-[#888] uppercase tracking-widest flex items-center space-x-1.5 border-b border-[#ececeb] pb-3 font-bold">
            <Shield className="w-4 h-4 text-[#1a1a1a]" />
            <span>Anti-Honeypot Validation Pipeline (Prevention Matrix)</span>
          </h3>
          <p className="text-xs text-[#333] font-light leading-relaxed">
            Organizers seed simulated honey accounts on stage levels to sink systems utilizing simple phrase matching. We enforce a robust 4-tier structural check prior to raw score metrics:
          </p>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
            <div className="bg-[#fafaf9] p-4 rounded-lg border border-[#ececeb] text-xs">
              <strong className="text-[#1a1a1a] font-bold font-mono text-[10px] uppercase block mb-1">1. Expert Experience Zero-Out</strong>
              <p className="text-[#666] font-light text-[11px] leading-relaxed">
                Flags resumes with proficiencies rated as "expert" but exhibiting exactly 0 months on relevant company rosters.
              </p>
            </div>
            <div className="bg-[#fafaf9] p-4 rounded-lg border border-[#ececeb] text-xs">
              <strong className="text-[#1a1a1a] font-bold font-mono text-[10px] uppercase block mb-1">2. Duration timeline paradoxical clash</strong>
              <p className="text-[#666] font-light text-[11px] leading-relaxed">
                Identifies profiles where accumulative timelines from company duration lists surpass stated cumulative YoE by &gt;30%.
              </p>
            </div>
            <div className="bg-[#fafaf9] p-4 rounded-lg border border-[#ececeb] text-xs">
              <strong className="text-[#1a1a1a] font-bold font-mono text-[10px] uppercase block mb-1">3. Lack of Verified Endorsements</strong>
              <p className="text-[#666] font-light text-[11px] leading-relaxed">
                We flags profiles where &gt;8 expert skills are listed but aggregate peer platform endorsements average less than &lt;5 total.
              </p>
            </div>
            <div className="bg-[#fafaf9] p-4 rounded-lg border border-[#ececeb] text-xs">
              <strong className="text-[#1a1a1a] font-bold font-mono text-[10px] uppercase block mb-1">4. Future Chronology</strong>
              <p className="text-[#666] font-light text-[11px] leading-relaxed">
                Catches faked credentials immediately by checking for degrees or certifications issued past the current year (2026).
              </p>
            </div>
          </div>
        </div>

        {/* Reproduce commands and metadata template tab */}
        <div className="bg-white border border-[#ececeb] rounded-xl p-6 space-y-4 shadow-sm">
          <h3 className="text-xs font-mono text-[#888] uppercase tracking-widest flex items-center space-x-1.5 border-b border-[#ececeb] pb-3 font-bold">
            <Terminal className="w-4 h-4 text-[#1a1a1a]" />
            <span>Submission Repro Configuration</span>
          </h3>

          <div className="space-y-4 text-xs">
            <div>
              <p className="text-[#333] font-light mb-3">
                Use the following parameters inside <code className="font-mono bg-[#f0f0ef] px-1 py-0.5 rounded text-[#1a1a1a] border border-[#ececeb]">submission_metadata.yaml</code> to describe our interactive rank sandbox setup:
              </p>
              <pre className="bg-[#fafaf9] p-5 rounded-lg text-[11.5px] text-[#1a1a1a] font-mono overflow-x-auto border border-[#ececeb] select-text leading-relaxed">
Team_name: "Intelligent Recruiters"
track_id: "01_data_and_ai_challenge"
reproduce_command: "python rank.py --candidates ./candidates.jsonl --out ./submission.csv"
sandbox_url: "https://ais-dev-5jxyfqpoweauf4rtjolxar-750264708244.asia-east1.run.app"
anti_honeypot_pipeline_deployed: true
weighted_scoring_signals:
  Career_quality: 0.30
  Skills_depth: 0.25
  Title_alignment: 0.20
  Behavioral_availability: 0.15
  Experience_range: 0.10
  Location_fit: 0.05
  Github_signal: 0.05
              </pre>
            </div>

            <div>
              <p className="text-[#333] font-light mb-3">
                Your sandbox executes formatting sanity audits using:
              </p>
              <pre className="bg-[#fafaf9] p-4 rounded-lg text-[11.5px] text-green-700 font-mono overflow-x-auto border border-[#ececeb] leading-relaxed select-text">
python validate_submission.py your_team_id.csv
# Outputs: "Submission check passed. 100 entries mapped perfectly."
              </pre>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
}
