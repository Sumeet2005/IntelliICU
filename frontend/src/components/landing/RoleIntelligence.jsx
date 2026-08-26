import React from "react";
import { Link } from "react-router-dom";

export default function RoleIntelligence() {
  return (
    <section id="explainability" className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-4">
      
      <div id="workflows" className="bg-[#040b18]/85 border border-slate-800/90 p-5 rounded-3xl space-y-3 backdrop-blur-md">
        <span className="text-[10px] font-mono font-bold text-cyan-400 uppercase tracking-widest block">
          ROLE-AWARE WORKFLOWS
        </span>
        <h3 className="text-xl font-bold text-white">Tailored Care Team Interfaces</h3>
        <p className="text-xs text-slate-300 leading-relaxed">
          Targeted role-based access control (RBAC) customized for intensivists, bedside nurses, medical directors, and IT administrators.
        </p>
        <div className="grid grid-cols-2 gap-2.5 font-mono text-xs pt-1">
          <div className="bg-slate-900/80 border border-slate-800 p-2.5 rounded-xl text-slate-200">
            <span className="text-cyan-400 font-bold block">DOCTORS</span>
            AI Copilot & Diagnostic Reasoning
          </div>
          <div className="bg-slate-900/80 border border-slate-800 p-2.5 rounded-xl text-slate-200">
            <span className="text-cyan-400 font-bold block">NURSES</span>
            Live Telemetry & Alert Workflows
          </div>
        </div>
      </div>

      <div className="bg-[#040b18]/85 border border-slate-800/90 p-5 rounded-3xl space-y-3 backdrop-blur-md flex flex-col justify-between">
        <div>
          <span className="text-[10px] font-mono font-bold text-cyan-400 uppercase tracking-widest block">
            EXPLAINABLE AI PRINCIPLE
          </span>
          <h3 className="text-xl font-bold text-white mt-1">Clinician Decision Support</h3>
          <p className="text-xs text-slate-300 leading-relaxed mt-1.5">
            IntelliICU is designed to augment clinical judgment, providing risk factors, laboratory trend context, and guidelines evidence to empower clinicians rather than automate clinical decisions.
          </p>
        </div>

        <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
          <span className="text-slate-300 font-mono text-[11px]">TRANSPARENT REASONING PATHWAYS</span>
          <Link to="/login" className="text-cyan-400 font-bold hover:underline">
            Access System →
          </Link>
        </div>
      </div>

    </section>
  );
}
