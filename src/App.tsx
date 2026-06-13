import React, { useState, useMemo, useEffect, useRef, useCallback } from 'react';
import { 
  Sparkles, Sliders, Briefcase, FileText, Download, 
  Terminal, ShieldCheck, CheckCircle, RefreshCcw, HelpCircle, AlertOctagon, Upload
} from 'lucide-react';

import { generate_candidates } from './candidates';
import { compute_score } from './scorer';
import { DEFAULT_WEIGHTS, REDROB_JD } from './constants';
import { Candidate, ScoringResult, SignalWeights } from './types';
import { parseCandidatesFile } from './utils/importCandidates';

import JDPanel, { JobDescriptionConfig } from './components/JDPanel';
import WeightsConfig from './components/WeightsConfig';
import CandidatesTable from './components/CandidatesTable';
import CandidateDetailModal from './components/CandidateDetailModal';
import BlueprintView from './components/BlueprintView';

// Mode: 'demo' for synthetic candidates, 'submission' for official dataset only
const APP_MODE = 'submission'; // Change to 'demo' for UI testing with synthetic candidates

export default function App() {
  const [weights, setWeights] = useState<SignalWeights>(DEFAULT_WEIGHTS);
  const [jdConfig, setJdConfig] = useState<JobDescriptionConfig>(REDROB_JD);
  const [selectedCandidateId, setSelectedCandidateId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'ranker' | 'blueprint'>('ranker');
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Create state for notification/export banner
  const [exportBanner, setExportBanner] = useState<string | null>(null);
  const [importBanner, setImportBanner] = useState<string | null>(null);

  // Initialize candidates database based on mode
  const [candidatesList, setCandidatesList] = useState<Candidate[]>(() => {
    // In submission mode, never use synthetic candidates
    if (APP_MODE === 'submission') {
      return []; // Will be populated from official dataset via API or import
    }
    return generate_candidates(); // Demo mode: use synthetic candidates
  });
  const [isSyncing, setIsSyncing] = useState<boolean>(false);
  const [isImporting, setIsImporting] = useState<boolean>(false);
  const [isScoring, setIsScoring] = useState<boolean>(false);
  const [scoredCandidates, setScoredCandidates] = useState<ScoringResult[]>([]);
  const [dataSource, setDataSource] = useState<string | null>(null);

  // Synchronize candidates dynamically from server (candidates.csv or candidates.jsonl)
  useEffect(() => {
    let active = true;
    async function fetchCandidates() {
      try {
        setIsSyncing(true);
        const preferredFiles = ['candidates.csv', 'candidates.jsonl'];
        for (const file of preferredFiles) {
          const res = await fetch(`/api/candidates?file=${encodeURIComponent(file)}`);
          if (!res.ok) continue;
          const data = await res.json();
          if (active && data.candidates && data.candidates.length > 0) {
            setCandidatesList(data.candidates);
            setDataSource(file);
            console.log(`Loaded ${data.candidates.length} candidates from ${file}.`);
            return;
          }
        }
      } catch (err) {
        if (APP_MODE === 'submission') {
          console.warn("[SUBMISSION MODE] No server-side dataset found. Use Import to load your CSV/JSONL.", err);
        } else {
          console.warn("Could not sync with /api/candidates. Using robust local candidate list.", err);
        }
      } finally {
        if (active) {
          setIsSyncing(false);
        }
      }
    }
    fetchCandidates();
    return () => {
      active = false;
    };
  }, []);

  // Score candidates in chunks so large datasets (100k+) stay responsive
  useEffect(() => {
    if (candidatesList.length === 0) {
      setScoredCandidates([]);
      setIsScoring(false);
      return;
    }

    let cancelled = false;
    setIsScoring(true);
    const CHUNK_SIZE = 5000;
    const results: ScoringResult[] = [];

    const scoreChunk = (startIndex: number) => {
      if (cancelled) return;

      const endIndex = Math.min(startIndex + CHUNK_SIZE, candidatesList.length);
      for (let i = startIndex; i < endIndex; i++) {
        results.push(compute_score(candidatesList[i], weights));
      }

      const sorted = [...results].sort((a, b) => {
        if (b.score !== a.score) return b.score - a.score;
        return a.candidate_id.localeCompare(b.candidate_id);
      });
      setScoredCandidates(sorted);

      if (endIndex < candidatesList.length) {
        window.setTimeout(() => scoreChunk(endIndex), 0);
      } else {
        setIsScoring(false);
      }
    };

    scoreChunk(0);
    return () => {
      cancelled = true;
    };
  }, [candidatesList, weights]);

  const handleImportFile = useCallback(async (file: File) => {
    try {
      setIsImporting(true);
      setImportBanner(`Importing ${file.name}...`);
      const imported = await parseCandidatesFile(file);
      if (imported.length === 0) {
        throw new Error('No valid candidates found in the uploaded file.');
      }
      setCandidatesList(imported);
      setDataSource(file.name);
      setImportBanner(`Imported ${imported.length.toLocaleString()} candidates from ${file.name}.`);
      setTimeout(() => setImportBanner(null), 6000);
    } catch (err: any) {
      setImportBanner(err?.message || 'Failed to import candidate file.');
      setTimeout(() => setImportBanner(null), 6000);
    } finally {
      setIsImporting(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  }, []);

  // Retrieve current selected candidate detail
  const selectedCandidateResult = useMemo(() => {
    if (!selectedCandidateId) return null;
    return scoredCandidates.find(res => res.candidate_id === selectedCandidateId) || null;
  }, [selectedCandidateId, scoredCandidates]);

  // Export CSV handler matching predefined Challenge output format!
  const handleExportCSV = () => {
    // Top 100 or entire pool
    const targetRows = scoredCandidates.slice(0, 100);
    
    // Prefix CSV Columns header
    let csvContent = 'candidate_id,rank,score,reasoning\n';
    
    targetRows.forEach((row, idx) => {
      const rank = idx + 1;
      const cid = row.candidate_id;
      // Force honeypots to 0.0000 in accordance with challenge rules
      const score = row.is_honeypot ? '0.0000' : row.score.toFixed(4);
      // Clean text to avoid quotes breaking CSV columns
      const reasoning = row.reasoning.replace(/"/g, '""');
      csvContent += `${cid},${rank},${score},"${reasoning}"\n`;
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'redrob_search_shortlist_track01.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Trigger feedback banner
    setExportBanner(`Successfully exported list to redrob_search_shortlist_track01.csv containing ${targetRows.length} ranked candidates.`);
    setTimeout(() => setExportBanner(null), 5000);
  };

  // Re-roll random weights value helper for testing
  const handleRandomizeWeights = () => {
    const randomWeights: SignalWeights = {
      career_quality: Math.round(Math.random() * 50) / 100,
      skills_depth: Math.round(Math.random() * 50) / 100,
      title_alignment: Math.round(Math.random() * 50) / 100,
      behavioral_availability: Math.round(Math.random() * 50) / 100,
      experience_range: Math.round(Math.random() * 5) / 10,
      location_fit: Math.round(Math.random() * 2) / 10,
      github_signal: Math.round(Math.random() * 2) / 10,
      jd_semantic_fit: Math.round(Math.random() * 30) / 100,
    };
    setWeights(randomWeights);
  };

  // Calculate top stats
  const activeCandidateCount = scoredCandidates.filter(c => !c.is_honeypot && !c.disqualified).length;
  const honeypotsBlocked = scoredCandidates.filter(c => c.is_honeypot).length;
  const totalPoolSize = scoredCandidates.length;

  return (
    <div className="bg-[#fdfdfc] min-h-screen text-[#1a1a1a] flex flex-col font-sans select-none selection:bg-[#1a1a1a]/10 selection:text-[#1a1a1a]">
      
      {/* Upper Utility Navbar or Header margin details - Aesthetic precision matching guidelines */}
      <header className="h-16 border-b border-[#ececeb] flex items-center justify-between px-8 bg-white">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-[#1a1a1a] rounded-sm flex items-center justify-center">
              <div className="w-2.5 h-2.5 bg-white rotate-45"></div>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-[10px] bg-[#f0f0ef] text-[#1a1a1a] px-2 py-0.5 rounded font-mono tracking-wider font-bold uppercase border border-[#ececeb]">
                  Redrob.ai Challenge Tool
                </span>
                <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
                <span className="text-[10px] text-[#888] font-mono uppercase tracking-tighter">NDCG Engine Deployed</span>
              </div>
              <h1 className="font-sans font-bold tracking-tight text-md uppercase mt-0.5 text-[#1a1a1a]">
                NeuralRecruiter <span className="font-normal opacity-40">v1.0</span>
              </h1>
            </div>
          </div>
        </div>

        {/* Tab Selection controller and Action */}
        <div className="flex items-center space-x-4 shrink-0">
          <nav className="flex gap-2 text-[11px] font-semibold uppercase tracking-widest text-[#888]">
            <button
              onClick={() => setActiveTab('ranker')}
              className={`pb-1 border-b-2 transition-colors ${
                activeTab === 'ranker'
                  ? 'text-[#1a1a1a] border-[#1a1a1a]'
                  : 'border-transparent hover:text-[#1a1a1a]'
              }`}
            >
              Discovery
            </button>
            <button
              onClick={() => setActiveTab('blueprint')}
              className={`pb-1 border-b-2 transition-colors ${
                activeTab === 'blueprint'
                  ? 'text-[#1a1a1a] border-[#1a1a1a]'
                  : 'border-transparent hover:text-[#1a1a1a]'
              }`}
            >
              Architecture Blueprint
            </button>
          </nav>

          <div className="h-6 w-[1px] bg-[#ececeb] hidden sm:block"></div>

          <input
            ref={fileInputRef}
            type="file"
            accept=".csv,.jsonl"
            className="hidden"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) handleImportFile(file);
            }}
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isImporting}
            className="flex items-center gap-2 px-5 py-2 bg-white text-[#1a1a1a] hover:bg-[#fafaf9] border border-[#ececeb] transition-colors text-[11px] font-bold uppercase tracking-widest rounded-full disabled:opacity-50"
          >
            <Upload className="w-3.5 h-3.5" />
            <span>{isImporting ? 'Importing...' : 'Import Dataset'}</span>
          </button>

          <button
            onClick={handleExportCSV}
            className="px-5 py-2 bg-[#1a1a1a] text-white hover:bg-[#333] active:bg-black transition-colors text-[11px] font-bold uppercase tracking-widest rounded-full"
          >
            Export Shortlist
          </button>
        </div>
      </header>

      {/* Export Notifications feedback banner */}
      {exportBanner && (
        <div className="mx-8 mt-6 bg-[#fafaf9] border border-[#ececeb] text-[#1a1a1a] text-xs px-5 py-3.5 rounded-xl flex items-center space-x-2 animate-fade-in font-mono shadow-sm leading-relaxed">
          <CheckCircle className="w-4 h-4 shrink-0 text-green-600" />
          <span className="font-medium text-[#1a1a1a]">{exportBanner}</span>
        </div>
      )}

      {importBanner && (
        <div className="mx-8 mt-6 bg-[#fafaf9] border border-[#ececeb] text-[#1a1a1a] text-xs px-5 py-3.5 rounded-xl flex items-center space-x-2 animate-fade-in font-mono shadow-sm leading-relaxed">
          <Upload className="w-4 h-4 shrink-0 text-[#1a1a1a]" />
          <span className="font-medium text-[#1a1a1a]">{importBanner}</span>
        </div>
      )}

      {(isSyncing || isScoring) && (
        <div className="mx-8 mt-6 bg-amber-50 border border-amber-200 text-amber-900 text-xs px-5 py-3.5 rounded-xl flex items-center space-x-2 font-mono shadow-sm leading-relaxed">
          <RefreshCcw className="w-4 h-4 shrink-0 animate-spin" />
          <span>
            {isSyncing
              ? 'Loading candidate dataset from server...'
              : `Ranking ${candidatesList.length.toLocaleString()} candidates${dataSource ? ` from ${dataSource}` : ''}...`}
          </span>
        </div>
      )}

      {/* Main Core Dashboard Layout */}
      <main className="flex-1 p-8 max-w-7xl w-full mx-auto space-y-6">
        
        {activeTab === 'ranker' ? (
          <div className="space-y-6 animate-fade-in">
            
            {/* Top informational stats metric segment */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
              <div className="bg-white border border-[#ececeb] p-5 rounded-xl flex items-center justify-between shadow-sm">
                <div>
                  <span className="text-[10px] text-[#888] uppercase tracking-wider font-mono">Overall Candidates</span>
                  <span className="text-xl font-bold text-[#1a1a1a] block mt-1">{totalPoolSize.toLocaleString()} in Database</span>
                  {dataSource && (
                    <span className="text-[9px] text-[#888] font-mono mt-1 block">Source: {dataSource}</span>
                  )}
                </div>
                <div className="bg-[#f0f0ef] text-[#1a1a1a] font-mono text-[9px] uppercase font-bold px-2 py-0.5 rounded border border-[#ececeb]">
                  Total Pool
                </div>
              </div>

              <div className="bg-white border border-[#ececeb] p-5 rounded-xl flex items-center justify-between shadow-sm">
                <div>
                  <span className="text-[10px] text-[#888] uppercase tracking-wider font-mono">Admissible Matches</span>
                  <span className="text-xl font-bold text-green-700 block mt-1">{activeCandidateCount} Qualified</span>
                </div>
                <div className="bg-green-50 text-green-700 font-mono text-[9px] uppercase font-bold px-2 py-0.5 rounded border border-green-200">
                  Match Rate
                </div>
              </div>

              <div className="bg-white border border-[#ececeb] p-5 rounded-xl flex items-center justify-between shadow-sm">
                <div>
                  <span className="text-[10px] text-[#888] uppercase tracking-wider font-mono">Honeypots Screened</span>
                  <span className="text-xl font-bold text-red-650 block mt-1 text-red-600">{honeypotsBlocked} Blocks Deployed</span>
                </div>
                <div className="bg-red-50 text-red-700 font-mono text-[9px] uppercase font-bold px-2 py-0.5 rounded border border-red-200">
                  Safeguards Active
                </div>
              </div>
            </div>

            {/* Split JD and Controls Panel */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <JDPanel jd={jdConfig} onJdChange={setJdConfig} />
              <div className="space-y-4">
                <WeightsConfig weights={weights} onWeightsChange={setWeights} />
                {/* Micro utilities */}
                <div className="flex items-center justify-between text-xs bg-[#fafaf9] border border-[#ececeb] p-3.5 rounded-xl text-[#666] font-mono shadow-sm">
                  <span>Simulate weighting calibrations</span>
                  <button 
                    onClick={handleRandomizeWeights}
                    className="flex items-center space-x-1 hover:text-[#1a1a1a] text-[#888] transition-colors"
                  >
                    <RefreshCcw className="w-3.5 h-3.5" />
                    <span className="underline underline-offset-2">Scramble & test convergence</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Scored Shortlist Table Workspace */}
            <CandidatesTable 
              scoredCandidates={scoredCandidates} 
              onSelectCandidate={setSelectedCandidateId} 
              onExportCSV={handleExportCSV}
            />

          </div>
        ) : (
          <div className="animate-fade-in">
            <BlueprintView />
          </div>
        )}

      </main>

      {/* Candidate Deep-Dive detailed metric analysis Modal overlay */}
      {selectedCandidateResult && (
        <CandidateDetailModal 
          scoreResult={selectedCandidateResult}
          weights={weights}
          onClose={() => setSelectedCandidateId(null)}
        />
      )}

      {/* Symmetrical simple Footer credit */}
      <footer className="h-12 bg-white border-t border-[#ececeb] px-8 flex items-center justify-between text-[10px] text-[#888] uppercase font-bold tracking-[0.3em]">
        <span>Hack2Skill // India Runs Hackathon 2026</span>
        <span>Project Reference: Track-01-POC-Ranker</span>
      </footer>

    </div>
  );
}
