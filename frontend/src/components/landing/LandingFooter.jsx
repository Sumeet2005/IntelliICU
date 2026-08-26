import React from "react";
import { ShieldCheck } from "lucide-react";

export default function LandingFooter() {
  return (
    <footer className="w-full border-t border-slate-900 bg-[#02060d]/95 py-5 px-4 sm:px-8 relative z-10">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-slate-400">
        
        {/* Medical Disclaimer */}
        <div className="flex items-center gap-2 text-left text-[11px] max-w-xl">
          <ShieldCheck size={16} className="text-cyan-400 shrink-0" />
          <span>
            IntelliICU is an educational and research-oriented clinical decision-support system. Not a certified medical device. Not a replacement for professional medical judgment.
          </span>
        </div>

        {/* Copyright & System Ver */}
        <div className="text-center text-[11px] font-mono text-slate-400">
          © 2026 IntelliICU System v2.0.0 • All rights reserved
        </div>

        {/* Made for Critical Care Badge */}
        <div className="flex items-center gap-1.5 text-xs text-slate-200 font-medium">
          <span className="text-red-500">❤️</span> Made for Critical Care
        </div>

      </div>
    </footer>
  );
}
