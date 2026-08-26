import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Sparkles } from "lucide-react";

export default function HeroContent({ scrollToSection }) {
  return (
    <div className="space-y-6 text-left">
      {/* Pill Badge */}
      <div className="inline-flex items-center gap-2 rounded-full border border-cyan-500/40 bg-cyan-950/60 px-3.5 py-1.5 backdrop-blur-md">
        <span className="h-2 w-2 rounded-full bg-cyan-400 animate-pulse" />
        <span className="font-mono text-[10px] sm:text-[11px] font-bold text-cyan-300 tracking-wider uppercase">
          INTELLIGENT ICU • REAL-TIME CLINICAL DECISION SUPPORT
        </span>
      </div>

      {/* Main Headline (Clean 3-line layout on desktop with WHITE and CYAN gradient text) */}
      <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black leading-[1.12] tracking-tight text-white drop-shadow-md">
        Clinical Intelligence <br />
        for the <br />
        <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-sky-300 to-blue-500">
          Modern Intensive Care Unit
        </span>
      </h1>

      {/* Description */}
      <p className="text-sm sm:text-base text-slate-200 leading-relaxed max-w-xl font-normal drop-shadow">
        Unify real-time patient telemetry, clinical alerts, AI-assisted risk analysis, and hospital intelligence in one command centre.
      </p>

      {/* Hero Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3 pt-2">
        <Link
          to="/login"
          className="inline-flex items-center justify-center gap-2.5 rounded-xl bg-gradient-to-r from-cyan-500 via-sky-500 to-blue-600 text-slate-950 font-extrabold px-6 py-3.5 text-xs transition duration-300 hover:shadow-lg hover:shadow-cyan-500/40 active:scale-[0.98] shadow-md cursor-pointer"
        >
          Enter Clinical Command Centre
          <ArrowRight size={15} />
        </Link>
        <button
          onClick={() => scrollToSection("modules")}
          className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-600 bg-slate-900/80 text-slate-100 font-extrabold px-6 py-3.5 text-xs transition hover:bg-slate-800 hover:text-white hover:border-slate-500 cursor-pointer backdrop-blur-md"
        >
          <Sparkles size={14} className="text-cyan-400" />
          Explore Platform
        </button>
      </div>

      {/* System Status Panel */}
      <div className="pt-4 border-t border-slate-800/90 max-w-xl space-y-2">
        <span className="text-[10px] font-mono font-bold tracking-widest text-slate-300 uppercase block">
          SYSTEM STATUS
        </span>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
          <div className="bg-[#040b18]/85 border border-slate-800 rounded-xl p-2.5 backdrop-blur-md">
            <span className="text-[9px] font-mono text-slate-400 block uppercase">ICU MONITORING</span>
            <span className="text-[11px] font-mono font-bold text-emerald-400 flex items-center gap-1.5 mt-0.5">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" /> ONLINE
            </span>
          </div>
          <div className="bg-[#040b18]/85 border border-slate-800 rounded-xl p-2.5 backdrop-blur-md">
            <span className="text-[9px] font-mono text-slate-400 block uppercase">TELEMETRY</span>
            <span className="text-[11px] font-mono font-bold text-cyan-400 flex items-center gap-1.5 mt-0.5">
              <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-pulse" /> LIVE
            </span>
          </div>
          <div className="bg-[#040b18]/85 border border-slate-800 rounded-xl p-2.5 backdrop-blur-md">
            <span className="text-[9px] font-mono text-slate-400 block uppercase">CLINICAL AI</span>
            <span className="text-[11px] font-mono font-bold text-teal-400 flex items-center gap-1.5 mt-0.5">
              <span className="h-1.5 w-1.5 rounded-full bg-teal-400 animate-pulse" /> READY
            </span>
          </div>
          <div className="bg-[#040b18]/85 border border-slate-800 rounded-xl p-2.5 backdrop-blur-md">
            <span className="text-[9px] font-mono text-slate-400 block uppercase">ALERT ENGINE</span>
            <span className="text-[11px] font-mono font-bold text-blue-400 flex items-center gap-1.5 mt-0.5">
              <span className="h-1.5 w-1.5 rounded-full bg-blue-400 animate-pulse" /> ACTIVE
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

