import React, { useState } from 'react';
import { Search, ShieldAlert, BadgeInfo, AlertTriangle, ArrowUpDown, Sparkles, Filter, FileSpreadsheet } from 'lucide-react';
import { ScoringResult, Candidate } from '../types';

interface CandidatesTableProps {
  scoredCandidates: ScoringResult[];
  onSelectCandidate: (candidateId: string) => void;
  onExportCSV: () => void;
}

type FilterTag = 'all' | 'superstar' | 'plain_language' | 'normal' | 'ghost' | 'honeypot';

export default function CandidatesTable({ scoredCandidates, onSelectCandidate, onExportCSV }: CandidatesTableProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState<FilterTag>('all');
  const [sortBy, setSortBy] = useState<'score' | 'experience' | 'github'>('score');

  // Filter candidates according to state
  const filteredCandidates = scoredCandidates.filter(res => {
    // 1. Tag filters
    if (activeFilter === 'superstar' && res.candidate.tag !== 'superstar') return false;
    if (activeFilter === 'plain_language' && res.candidate.tag !== 'plain_language') return false;
    if (activeFilter === 'ghost' && res.candidate.tag !== 'ghost') return false;
    if (activeFilter === 'honeypot' && !res.is_honeypot) return false;
    if (activeFilter === 'normal' && (res.candidate.tag !== 'normal' || res.is_honeypot)) return false;

    // 2. Search query filter
    const nameMatch = res.candidate.profile.name.toLowerCase().includes(searchQuery.toLowerCase());
    const titleMatch = res.candidate.profile.current_title.toLowerCase().includes(searchQuery.toLowerCase());
    const skillMatch = res.candidate.skills.some(s => s.name.toLowerCase().includes(searchQuery.toLowerCase()));
    const idMatch = res.candidate_id.toLowerCase().includes(searchQuery.toLowerCase());
    
    return nameMatch || titleMatch || skillMatch || idMatch;
  });

  // Sort candidates
  const sortedCandidates = [...filteredCandidates].sort((a, b) => {
    if (sortBy === 'experience') {
      return b.candidate.profile.years_of_experience - a.candidate.profile.years_of_experience;
    }
    if (sortBy === 'github') {
      return b.candidate.redrob_signals.github_activity_score - a.candidate.redrob_signals.github_activity_score;
    }
    return b.score - a.score;
  });

  const getTagStyles = (tag?: string, isHoneypot?: boolean) => {
    if (isHoneypot) {
      return 'bg-red-50 text-red-700 border-red-200';
    }
    switch (tag) {
      case 'superstar':
        return 'bg-green-50 text-green-700 border-green-200';
      case 'plain_language':
        return 'bg-purple-50 text-purple-700 border-purple-200';
      case 'ghost':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      default:
        return 'bg-[#f0f0ef] text-[#1a1a1a] border-[#ececeb]';
    }
  };

  const getTagLabel = (tag?: string, isHoneypot?: boolean) => {
    if (isHoneypot) return 'Honeypot Trap';
    switch (tag) {
      case 'superstar': return 'AI Superstar';
      case 'plain_language': return 'Plain-Language Fit';
      case 'ghost': return 'Behavioral Ghost';
      case 'keyword_stuffer': return 'Keyword Stuffer';
      default: return 'Applicant';
    }
  };

  return (
    <div id="candidates_table_card" className="bg-white border border-[#ececeb] rounded-xl shadow-sm overflow-hidden flex flex-col">
      {/* Table Header with Search and Export */}
      <div className="p-8 pb-5 border-b border-[#ececeb] flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white">
        <div>
          <h2 className="font-sans font-bold text-lg text-[#1a1a1a] flex items-center space-x-2 uppercase tracking-tight">
            <span>Search & Shortlist Workspace</span>
          </h2>
          <p className="text-xs text-[#888] font-mono mt-1">
            Analyzing {scoredCandidates.length} profiles against parameters ({sortedCandidates.length} match search criteria)
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Search bar */}
          <div className="relative">
            <input
              type="text"
              placeholder="Search by name, skill, title..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-4 py-2 w-64 bg-white border border-[#ececeb] rounded-full text-xs text-[#1a1a1a] placeholder-[#888] focus:outline-none focus:border-[#1a1a1a] transition-colors shadow-sm font-sans"
            />
            <Search className="absolute left-3 top-3 w-3.5 h-3.5 text-[#888]" />
          </div>

          <button
            onClick={onExportCSV}
            className="flex items-center space-x-2 text-xs font-mono font-bold text-[#1a1a1a] hover:bg-[#fafaf9] border border-[#ececeb] px-4 py-2 rounded-full transition-colors bg-white uppercase tracking-wider"
          >
            <FileSpreadsheet className="w-4 h-4 text-[#1a1a1a]" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {/* Categories Filter Rail */}
      <div className="px-8 py-3 border-b border-[#ececeb] bg-[#fafaf9] flex flex-wrap items-center gap-2">
        <span className="text-[10px] text-[#888] uppercase font-mono tracking-widest mr-3 flex items-center gap-1 font-bold">
          <Filter className="w-3.5 h-3.5 text-[#888]" /> Filters:
        </span>
        
        {(['all', 'superstar', 'plain_language', 'normal', 'ghost', 'honeypot'] as FilterTag[]).map(tag => (
          <button
            key={tag}
            onClick={() => setActiveFilter(tag)}
            className={`text-xs px-3.5 py-1.5 rounded-full font-sans transition-all border ${
              activeFilter === tag
                ? 'bg-[#1a1a1a] text-white border-[#1a1a1a] font-bold uppercase tracking-wider text-[11px]'
                : 'bg-white text-[#666] border-[#ececeb] hover:text-[#1a1a1a] hover:bg-[#f0f0ef] transition-colors text-[11px] font-semibold uppercase tracking-wider shadow-sm'
            }`}
          >
            {tag === 'all' && 'All applicants'}
            {tag === 'superstar' && '✨ Superstars'}
            {tag === 'plain_language' && '💡 Plain-Language'}
            {tag === 'normal' && '👨‍💻 General devs'}
            {tag === 'ghost' && '👻 Ghosts'}
            {tag === 'honeypot' && '🚨 Honeypots'}
          </button>
        ))}
      </div>

      {/* Sort controller */}
      <div className="px-8 py-3.5 border-b border-[#ececeb] bg-white flex items-center justify-between text-xs font-mono text-[#888]">
        <span className="text-[10px] uppercase text-[#888] tracking-widest font-bold">Candidate list sorted by metric</span>
        <div className="flex items-center space-x-4">
          <span className="text-[10px] text-[#888] font-bold">Order by:</span>
          <button 
            onClick={() => setSortBy('score')}
            className={`flex items-center space-x-1 hover:text-[#1a1a1a] transition-colors ${sortBy === 'score' ? 'text-[#1a1a1a] font-bold underline underline-offset-4' : ''}`}
          >
            <ArrowUpDown className="w-3 h-3" />
            <span>AI Rank Score</span>
          </button>
          <button 
            onClick={() => setSortBy('experience')}
            className={`flex items-center space-x-1 hover:text-[#1a1a1a] transition-colors ${sortBy === 'experience' ? 'text-[#1a1a1a] font-bold underline underline-offset-4' : ''}`}
          >
            <ArrowUpDown className="w-3 h-3" />
            <span>Experience</span>
          </button>
          <button 
            onClick={() => setSortBy('github')}
            className={`flex items-center space-x-1 hover:text-[#1a1a1a] transition-colors ${sortBy === 'github' ? 'text-[#1a1a1a] font-bold underline underline-offset-4' : ''}`}
          >
            <ArrowUpDown className="w-3 h-3" />
            <span>GitHub Commits</span>
          </button>
        </div>
      </div>

      {/* Table grid */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-[#ececeb] text-[10px] font-mono text-[#888] uppercase tracking-wider bg-[#fafaf9]">
              <th className="py-4 px-8 text-center w-16">Rank</th>
              <th className="py-4 px-4">Candidate & Headline</th>
              <th className="py-4 px-4">Location</th>
              <th className="py-4 px-4">Signals Status</th>
              <th className="py-4 px-4 text-center w-36">Classification</th>
              <th className="py-4 px-8 text-right w-28">NDCG Score</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#ececeb]">
            {sortedCandidates.length === 0 ? (
              <tr>
                <td colSpan={6} className="py-16 text-center text-[#888] font-mono text-xs">
                  No applicants matching parameters found.
                </td>
              </tr>
            ) : (
              sortedCandidates.slice(0, 100).map((res, index) => {
                const rank = index + 1;
                const isDisqualified = res.disqualified || res.score < 0.04;
                
                return (
                  <tr
                    key={res.candidate_id}
                    onClick={() => onSelectCandidate(res.candidate_id)}
                    className={`hover:bg-[#fafaf9] cursor-pointer transition-colors ${
                      res.is_honeypot 
                        ? 'bg-red-50/40 border-l-2 border-l-red-500 hover:bg-rose-50/60' 
                        : isDisqualified
                        ? 'opacity-65 hover:opacity-100 hover:bg-slate-50'
                        : 'border-l border-l-transparent'
                    }`}
                  >
                    {/* Rank cell */}
                    <td className="py-4 px-8 text-center font-mono font-bold text-[#1a1a1a]">
                      {res.is_honeypot ? (
                        <ShieldAlert className="w-4 h-4 text-red-500 mx-auto" />
                      ) : (
                        <span className={rank <= 10 ? 'text-[#1a1a1a] text-sm' : 'text-[#888]'}>
                          #{rank}
                        </span>
                      )}
                    </td>

                    {/* Candidate Identity cell */}
                    <td className="py-4 px-4">
                      <div className="flex items-center space-x-3">
                        <img
                          src={res.candidate.profile.avatar_url || `https://api.dicebear.com/7.x/initials/svg?seed=${res.candidate.profile.name}`}
                          alt={res.candidate.profile.name}
                          className="w-8 h-8 rounded-full border border-[#ececeb] bg-white shrink-0"
                          onError={(e) => {
                            (e.target as HTMLImageElement).src = `https://api.dicebear.com/7.x/initials/svg?seed=${res.candidate.profile.name}`;
                          }}
                        />
                        <div className="min-w-0 max-w-md">
                          <div className="flex items-center space-x-2">
                            <span className={`text-xs font-bold truncate ${res.is_honeypot ? 'text-[#888] line-through' : 'text-[#1a1a1a]'}`}>
                              {res.candidate.profile.name}
                            </span>
                            <span className="text-[10px] font-mono text-[#888] leading-none shrink-0 bg-[#f0f0ef] px-1.5 py-0.5 rounded border border-[#ececeb]">
                              {res.candidate_id}
                            </span>
                          </div>
                          <p className="text-[11px] text-[#666] truncate font-light mt-0.5">
                            {res.candidate.profile.current_title} at {res.candidate.profile.current_company}
                          </p>
                        </div>
                      </div>
                    </td>

                    {/* Location and relocation */}
                    <td className="py-4 px-4 text-xs font-light text-[#1a1a1a]">
                      <div>{res.candidate.profile.location}</div>
                      <div className="text-[9px] text-[#888] font-mono mt-0.5">
                        {res.candidate.redrob_signals.willing_to_relocate ? '✓ Willing to relocate' : '• Stated origin'}
                      </div>
                    </td>

                    {/* Signals details */}
                    <td className="py-4 px-4 text-xs">
                      {res.is_honeypot ? (
                        <span className="text-red-650 font-mono text-[10px] leading-tight flex items-center space-x-1 font-semibold text-red-600">
                          <AlertTriangle className="w-3.5 h-3.5" />
                          <span>Timeline conflict detected</span>
                        </span>
                      ) : (
                        <div className="flex items-center space-x-4">
                          <div className="text-center font-mono">
                            <span className="text-[9px] text-[#888] block">YOE</span>
                            <span className="text-xs font-bold text-[#1a1a1a]">{res.candidate.profile.years_of_experience} yrs</span>
                          </div>
                          <div className="text-center font-mono">
                            <span className="text-[9px] text-[#888] block">NOTICE</span>
                            <span className="text-xs font-bold text-[#1a1a1a]">{res.candidate.redrob_signals.notice_period_days}d</span>
                          </div>
                          <div className="text-center font-mono">
                            <span className="text-[9px] text-[#888] block">ACTIVE</span>
                            <span className="text-xs font-bold text-[#1a1a1a]">
                              {res.candidate.redrob_signals.applications_submitted_30d > 0 ? 'Active' : 'Passive'}
                            </span>
                          </div>
                        </div>
                      )}
                    </td>

                    {/* Tag label */}
                    <td className="py-4 px-4 text-center">
                      <span className={`text-[9px] font-mono uppercase tracking-wider px-2.5 py-0.5 rounded-full border ${getTagStyles(res.candidate.tag, res.is_honeypot)} font-bold`}>
                        {getTagLabel(res.candidate.tag, res.is_honeypot)}
                      </span>
                    </td>

                    {/* Scored score */}
                    <td className="py-4 px-8 text-right font-mono font-bold">
                      {res.is_honeypot ? (
                        <span className="text-red-500 text-xs text-opacity-80">0.0000</span>
                      ) : (
                        <span className={rank <= 10 ? 'text-[#1a1a1a] text-xs' : 'text-[#666] text-xs'}>
                          {res.score.toFixed(4)}
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
