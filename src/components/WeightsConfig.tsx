import React from 'react';
import { Sliders, RotateCcw, HelpCircle } from 'lucide-react';
import { SignalWeights } from '../types';
import { DEFAULT_WEIGHTS } from '../constants';

interface WeightsConfigProps {
  weights: SignalWeights;
  onWeightsChange: (newWeights: SignalWeights) => void;
}

export default function WeightsConfig({ weights, onWeightsChange }: WeightsConfigProps) {
  const handleSliderChange = (key: keyof SignalWeights, val: number) => {
    onWeightsChange({
      ...weights,
      [key]: parseFloat(val.toFixed(2))
    });
  };

  const handleReset = () => {
    onWeightsChange(DEFAULT_WEIGHTS);
  };

  const totalWeight = Object.values(weights).reduce((a, b) => a + b, 0);

  const labels: Record<keyof SignalWeights, { name: string; desc: string; color: string }> = {
    career_quality: { 
      name: 'Career & Company Quality', 
      desc: 'Product background vs service consultants ratio',
      color: 'bg-teal-500' 
    },
    skills_depth: { 
      name: 'Skills Depths Alignment', 
      desc: 'Expertise & duration in core indexing databases', 
      color: 'bg-indigo-500' 
    },
    title_alignment: { 
      name: 'Current Title Fit', 
      desc: 'Direct match values for search & ranking roles', 
      color: 'bg-emerald-500' 
    },
    behavioral_availability: { 
      name: 'Availability & Connectivity', 
      desc: 'Notice period, activity dates, response speed', 
      color: 'bg-sky-500' 
    },
    experience_range: { 
      name: 'YoE sweet-spot', 
      desc: 'Strict curve alignment around 5-9 target years', 
      color: 'bg-amber-500' 
    },
    location_fit: { 
      name: 'Location hub alignment', 
      desc: 'Closeness to Noida/Pune physical teams', 
      color: 'bg-pink-500' 
    },
    github_signal: { 
      name: 'GitHub Activity', 
      desc: 'Recent commit and coding patterns', 
      color: 'bg-slate-400' 
    },
    jd_semantic_fit: {
      name: 'JD Semantic Relevance',
      desc: 'Density of search/retrieval domain terms in CV text',
      color: 'bg-rose-500'
    }
  };

  return (
    <div id="weights_config_card" className="bg-white border border-[#ececeb] rounded-xl p-6 text-[#1a1a1a] shadow-sm">
      <div className="flex items-center justify-between border-b border-[#ececeb] pb-4 mb-4">
        <div className="flex items-center space-x-3">
          <div className="bg-[#1a1a1a] text-white p-2 rounded-lg">
            <Sliders className="w-4 h-4" />
          </div>
          <div>
            <h2 className="font-sans font-bold text-md text-[#1a1a1a] tracking-tight leading-none uppercase">Calibration Signals</h2>
            <p className="text-[10px] text-[#888] font-mono mt-1 font-semibold uppercase tracking-tighter">Multi-signal additive parameters tuning</p>
          </div>
        </div>
        
        <button 
          onClick={handleReset}
          className="flex items-center space-x-1.5 text-xs text-[#1a1a1a] hover:bg-[#fafaf9] transition-colors font-mono uppercase tracking-wider px-3 py-1.5 rounded-full bg-white border border-[#ececeb] font-medium"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Reset Defaults</span>
        </button>
      </div>

      <div className="space-y-4">
        {Object.entries(weights).map(([scoreKey, value]) => {
          const key = scoreKey as keyof SignalWeights;
          const { name, desc, color } = labels[key];
          
          return (
            <div key={key} className="space-y-1.5 animate-fade-in">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-[#1a1a1a] flex items-center space-x-2">
                  <span className={`w-2.5 h-2.5 rounded-full bg-[#1a1a1a]`}></span>
                  <span>{name}</span>
                </span>
                <span className="font-mono bg-[#f0f0ef] px-2 py-0.5 rounded font-bold text-[#1a1a1a] border border-[#ececeb]">
                  {value.toFixed(2)}
                </span>
              </div>
              
              <div className="flex items-center space-x-3">
                <input 
                  type="range"
                  min="0.0"
                  max="0.6"
                  step="0.05"
                  value={value}
                  onChange={(e) => handleSliderChange(key, parseFloat(e.target.value))}
                  className="w-full h-1.5 bg-[#ececeb] rounded-lg cursor-pointer accent-[#1a1a1a] outline-none"
                />
              </div>
              <p className="text-[10px] text-[#888] font-light leading-none pl-4.5">
                {desc}
              </p>
            </div>
          );
        })}
      </div>

      <div className="mt-5 pt-4 border-t border-[#ececeb] flex items-center justify-between text-xs font-mono">
        <span className="text-[#666] font-medium">Total Signals Weights Sum:</span>
        <span className={`px-2.5 py-0.5 rounded font-bold border ${
          Math.abs(totalWeight - 1.00) < 0.01 
            ? 'bg-green-50 text-green-700 border-green-200' 
            : 'bg-yellow-50 text-yellow-700 border-yellow-200'
        }`}>
          {totalWeight.toFixed(2)} {Math.abs(totalWeight - 1.00) < 0.01 ? '(Nominal)' : '(Calibrated)'}
        </span>
      </div>
    </div>
  );
}
