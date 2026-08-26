import React from "react";
import { Activity, Brain, Sliders, Bell, Users, ShieldCheck } from "lucide-react";

export default function FeatureGrid() {
  const capabilities = [
    {
      title: "Real-Time Monitoring",
      desc: "Continuous surveillance of vital signs and clinical parameters",
      icon: Activity
    },
    {
      title: "AI Risk Prediction",
      desc: "XGBoost-powered sepsis risk with real-time scoring and trend analysis.",
      icon: Brain
    },
    {
      title: "Explainable AI",
      desc: "SHAP-based explanations for transparent and trustworthy insights.",
      icon: Sliders
    },
    {
      title: "Intelligent Alerts",
      desc: "Prioritized alerts with escalation, acknowledgement and team notifications.",
      icon: Bell
    },
    {
      title: "Patient Intelligence",
      desc: "Comprehensive timeline, labs, notes, imaging and risk context.",
      icon: Users
    },
    {
      title: "Clinical Workflows",
      desc: "Role-based workflows for ICU teams and operations.",
      icon: ShieldCheck
    }
  ];

  return (
    <section id="modules" className="pt-2">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-3">
        {capabilities.map((card, idx) => (
          <div
            key={idx}
            className="bg-[#040b18]/80 border border-slate-800/90 p-3.5 rounded-2xl space-y-2 hover:border-cyan-500/50 transition duration-300 backdrop-blur-md group cursor-pointer"
          >
            <div className="p-1.5 rounded-xl bg-slate-900 border border-slate-800 text-cyan-400 w-fit group-hover:text-cyan-300 group-hover:border-cyan-800/60 transition">
              <card.icon size={16} />
            </div>
            <h3 className="text-xs font-bold text-white leading-snug">{card.title}</h3>
            <p className="text-[11px] text-slate-300 leading-normal font-normal">{card.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
