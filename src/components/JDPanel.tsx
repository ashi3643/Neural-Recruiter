import React, { useState } from 'react';
import { Briefcase, MapPin, Award, Pencil, Check } from 'lucide-react';

export interface JobDescriptionConfig {
  title: string;
  company: string;
  experience_range: string;
  location: string;
  description: string;
  core_requirements: string[];
}

interface JDPanelProps {
  jd: JobDescriptionConfig;
  onJdChange: (jd: JobDescriptionConfig) => void;
}

export default function JDPanel({ jd, onJdChange }: JDPanelProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [draft, setDraft] = useState(jd);

  const startEditing = () => {
    setDraft(jd);
    setIsEditing(true);
  };

  const saveEdits = () => {
    onJdChange({
      ...draft,
      core_requirements: draft.core_requirements.filter(req => req.trim().length > 0),
    });
    setIsEditing(false);
  };

  const updateRequirement = (index: number, value: string) => {
    const next = [...draft.core_requirements];
    next[index] = value;
    setDraft({ ...draft, core_requirements: next });
  };

  const addRequirement = () => {
    setDraft({ ...draft, core_requirements: [...draft.core_requirements, ''] });
  };

  return (
    <div id="jd_panel_card" className="bg-white border border-[#ececeb] rounded-xl p-6 text-[#1a1a1a] shadow-sm h-full flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between border-b border-[#ececeb] pb-4 mb-4">
          <div className="flex items-center space-x-3">
            <div className="bg-[#1a1a1a] text-white p-2 rounded-lg">
              <Briefcase className="w-4 h-4" />
            </div>
            <div>
              <h2 className="font-sans font-bold text-md text-[#1a1a1a] tracking-tight leading-none uppercase">Primary Job Description</h2>
              <p className="text-[10px] text-[#888] font-mono mt-1">Hiring Org: {jd.company}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={isEditing ? saveEdits : startEditing}
              className="flex items-center gap-1.5 text-[10px] font-mono font-bold px-2.5 py-1 rounded-full border border-[#ececeb] uppercase tracking-wider hover:bg-[#fafaf9] transition-colors"
            >
              {isEditing ? <Check className="w-3 h-3" /> : <Pencil className="w-3 h-3" />}
              <span>{isEditing ? 'Save JD' : 'Edit JD'}</span>
            </button>
            <span className="bg-[#f0f0ef] text-[#1a1a1a] text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full border border-[#ececeb] uppercase tracking-wider">
              FOUNDING TEAM
            </span>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            {isEditing ? (
              <input
                value={draft.title}
                onChange={(e) => setDraft({ ...draft, title: e.target.value })}
                className="w-full text-sm font-bold text-[#1a1a1a] border border-[#ececeb] rounded-lg px-3 py-2 focus:outline-none focus:border-[#1a1a1a]"
              />
            ) : (
              <h3 className="text-sm font-bold text-[#1a1a1a]">{jd.title}</h3>
            )}

            {isEditing ? (
              <textarea
                value={draft.description}
                onChange={(e) => setDraft({ ...draft, description: e.target.value })}
                rows={5}
                className="w-full text-xs text-[#666] leading-relaxed mt-2 border border-[#ececeb] rounded-lg px-3 py-2 focus:outline-none focus:border-[#1a1a1a] resize-y"
              />
            ) : (
              <p className="text-xs text-[#666] leading-relaxed mt-2 font-serif italic">
                {jd.description}
              </p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-3 pt-1">
            <div className="bg-[#fafaf9] p-3 rounded-lg border border-[#ececeb]">
              <span className="text-[9px] text-[#888] block uppercase font-mono tracking-wider font-bold">Sweet Spot Experience</span>
              {isEditing ? (
                <input
                  value={draft.experience_range}
                  onChange={(e) => setDraft({ ...draft, experience_range: e.target.value })}
                  className="w-full text-xs font-bold text-[#1a1a1a] mt-1 border border-[#ececeb] rounded px-2 py-1"
                />
              ) : (
                <span className="text-xs font-bold text-[#1a1a1a] block mt-1">{jd.experience_range}</span>
              )}
            </div>
            <div className="bg-[#fafaf9] p-3 rounded-lg border border-[#ececeb]">
              <span className="text-[9px] text-[#888] block uppercase font-mono tracking-wider font-semibold flex items-center gap-1 font-bold">
                <MapPin className="w-3 h-3 text-red-500" /> Location Hubs
              </span>
              {isEditing ? (
                <input
                  value={draft.location}
                  onChange={(e) => setDraft({ ...draft, location: e.target.value })}
                  className="w-full text-xs font-bold text-[#1a1a1a] mt-1 border border-[#ececeb] rounded px-2 py-1"
                />
              ) : (
                <span className="text-xs font-bold text-[#1a1a1a] block mt-1 truncate">{jd.location}</span>
              )}
            </div>
          </div>

          <div>
            <h4 className="text-[10px] font-mono text-[#888] uppercase tracking-widest mb-3 flex items-center space-x-1.5 font-bold">
              <Award className="w-3.5 h-3.5 text-[#1a1a1a]" />
              <span>Critical Evaluation Parameters</span>
            </h4>
            <ul className="space-y-2.5">
              {(isEditing ? draft.core_requirements : jd.core_requirements).map((req, idx) => (
                <li key={idx} className="flex items-start space-x-2 text-xs text-[#333] font-light leading-relaxed">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#1a1a1a] shrink-0 mt-2"></span>
                  {isEditing ? (
                    <input
                      value={req}
                      onChange={(e) => updateRequirement(idx, e.target.value)}
                      className="flex-1 border border-[#ececeb] rounded px-2 py-1 text-xs"
                    />
                  ) : (
                    <span>{req}</span>
                  )}
                </li>
              ))}
            </ul>
            {isEditing && (
              <button
                onClick={addRequirement}
                className="mt-2 text-[10px] font-mono uppercase tracking-wider text-[#888] hover:text-[#1a1a1a]"
              >
                + Add requirement
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="mt-5 pt-3 border-t border-[#ececeb] p-3 bg-[#fafaf9] rounded-lg flex items-center space-x-2.5">
        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(34,197,94,0.5)]"></div>
        <p className="text-[10px] text-[#666] font-mono leading-tight">
          <strong>Evaluation Safeguards:</strong> Embedded traps reject raw resume keyword stuffers and impossible timeline datasets.
        </p>
      </div>
    </div>
  );
}
