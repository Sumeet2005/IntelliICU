import React from "react";

export default function ClinicalPipeline() {
  const steps = [
    { step: "01", name: "Patient Data", desc: "Ingests EMR records & baseline health history" },
    { step: "02", name: "Live Telemetry", desc: "High-frequency vital sign streaming feeds" },
    { step: "03", name: "Risk Analysis", desc: "Automated scoring models for early detection" },
    { step: "04", name: "Clinical AI", desc: "LLM-assisted reasoning over multi-parameter context" },
    { step: "05", name: "Alert Intelligence", desc: "Prioritized alerts with L1-L3 escalation protocols" },
    { step: "06", name: "Clinician Action", desc: "Empowers care teams with explainable insights" }
  ];

  return (
    <section id="pipeline" className="space-y-6 pt-4">
      <div className="text-center space-y-2 max-w-2xl mx-auto">
        <span className="text-[10px] font-mono font-bold text-cyan-400 uppercase tracking-widest bg-cyan-950/60 border border-cyan-800/60 px-3 py-1 rounded-full">
          CLINICAL ARCHITECTURE
        </span>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
          End-to-End Decision Pipeline
        </h2>
        <p className="text-slate-300 text-xs sm:text-sm">
          Continuous transformation of raw physiological signals into actionable clinical decisions.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {steps.map((st, i) => (
          <div key={i} className="bg-[#040b18]/80 border border-slate-800/90 p-3.5 rounded-2xl space-y-1.5 backdrop-blur-md">
            <span className="font-mono text-xs font-bold text-cyan-400">{st.step}</span>
            <h4 className="text-xs font-bold text-white">{st.name}</h4>
            <p className="text-[10px] text-slate-300 leading-snug">{st.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
