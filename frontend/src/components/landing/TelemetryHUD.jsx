import React, { useEffect, useRef } from "react";
import { Brain, Activity, Bell } from "lucide-react";

export default function TelemetryHUD() {
  const hudRef = useRef(null);

  useEffect(() => {
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const isMobile = window.innerWidth < 768;
    const hud = hudRef.current;

    if (!hud || prefersReducedMotion || isMobile) return;

    let mouseX = 0;
    let mouseY = 0;

    const handleMouseMove = (e) => {
      mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
      mouseY = (e.clientY / window.innerHeight - 0.5) * 2;

      const rotateY = mouseX * 1.8; // Bounded ±1.8deg
      const rotateX = -mouseY * 1.4; // Bounded ±1.4deg
      const translateX = mouseX * 6; // 6-8px max translation
      const translateY = mouseY * 4;

      hud.style.transform = `perspective(1200px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translate3d(${translateX}px, ${translateY}px, 20px)`;
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <div id="telemetry" className="relative w-full flex justify-center lg:justify-end z-20">
      
      {/* Level 3: Floating Clinical Stream Tag Anchored Near HUD (translateZ(20px)) */}
      <div className="hidden sm:block absolute -top-3 left-2 z-30 bg-cyan-950/85 border border-cyan-500/30 backdrop-blur-md px-2.5 py-1 rounded-lg shadow-lg transition-transform duration-300 transform-gpu [transform:translateZ(20px)]">
        <span className="font-mono text-[9px] font-bold text-cyan-300 uppercase tracking-widest flex items-center gap-1.5">
          <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-ping"></span>
          LIVE TELEMETRY STREAM
        </span>
      </div>

      {/* Primary 3D Floating Clinical Workstation HUD Console (perspective 1200px, translateZ(20px)) */}
      <div
        ref={hudRef}
        style={{ transformStyle: "preserve-3d" }}
        className="w-full max-w-[410px] rounded-3xl border border-cyan-500/30 bg-[#030c19]/72 p-4 sm:p-5 backdrop-blur-[18px] shadow-[0_35px_90px_rgba(0,0,0,0.55)] shadow-cyan-950/30 space-y-3.5 relative overflow-hidden transition-transform duration-300 ease-out hover:border-cyan-400/50 animate-[float_7s_ease-in-out_infinite]"
      >
        {/* Ambient Glow */}
        <div className="absolute top-0 right-0 w-40 h-40 bg-cyan-500/10 blur-3xl pointer-events-none" />

        {/* HUD Header (translateZ(8px)) */}
        <div className="flex items-center justify-between border-b border-slate-800/90 pb-2.5 font-mono [transform:translateZ(8px)]">
          <div className="flex items-center gap-2">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs font-bold text-slate-100">BED 04</span>
          </div>
          <span className="text-[9px] font-semibold text-cyan-300 bg-cyan-950/80 border border-cyan-800/70 px-2 py-0.5 rounded-md">
            SIMULATION • NO REAL PATIENT DATA
          </span>
        </div>

        {/* Main Telemetry & Waveform Container (translateZ(12px)) */}
        <div className="grid grid-cols-12 gap-2.5 items-center [transform:translateZ(12px)]">
          
          {/* Waveforms Column with Grid Background */}
          <div className="col-span-8 bg-slate-950/90 border border-slate-800/90 p-2.5 rounded-2xl space-y-1.5 shadow-md">
            <div className="flex items-center justify-between text-[9px] font-mono text-slate-400">
              <span className="flex items-center gap-1"><Activity size={10} className="text-emerald-400" /> LEAD II ECG</span>
              <span className="text-emerald-400 font-semibold">25 mm/s</span>
            </div>
            {/* Animated Lead II ECG Line SVG with Grid Lines */}
            <div className="h-11 w-full overflow-hidden relative flex items-center bg-[#020812] rounded border border-slate-900 bg-[linear-gradient(to_right,#0a1a2f_1px,transparent_1px),linear-gradient(to_bottom,#0a1a2f_1px,transparent_1px)] bg-[size:10px_10px]">
              <div className="flex w-[800px] animate-[slide_4s_linear_infinite]">
                <svg className="w-[400px] h-10 text-emerald-400 shrink-0 drop-shadow-[0_0_3px_rgba(52,211,153,0.6)]" viewBox="0 0 400 50" preserveAspectRatio="none">
                  <path
                    d="M 0 25 L 50 25 L 55 10 L 60 40 L 65 5 L 70 45 L 75 25 L 120 25 L 125 18 L 130 25 L 170 25 L 175 10 L 180 40 L 185 5 L 190 45 L 195 25 L 240 25 L 245 18 L 250 25 L 290 25 L 295 10 L 300 40 L 305 5 L 310 45 L 315 25 L 360 25 L 365 18 L 370 25 L 400 25"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.5"
                  />
                </svg>
                <svg className="w-[400px] h-10 text-emerald-400 shrink-0 drop-shadow-[0_0_3px_rgba(52,211,153,0.6)]" viewBox="0 0 400 50" preserveAspectRatio="none">
                  <path
                    d="M 0 25 L 50 25 L 55 10 L 60 40 L 65 5 L 70 45 L 75 25 L 120 25 L 125 18 L 130 25 L 170 25 L 175 10 L 180 40 L 185 5 L 190 45 L 195 25 L 240 25 L 245 18 L 250 25 L 290 25 L 295 10 L 300 40 L 305 5 L 310 45 L 315 25 L 360 25 L 365 18 L 370 25 L 400 25"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.5"
                  />
                </svg>
              </div>
            </div>

            <div className="flex items-center justify-between text-[9px] font-mono text-slate-400 pt-1 border-t border-slate-900">
              <span>SpO₂ PLETH WAVEFORM</span>
              <span className="text-cyan-400 font-semibold">98%</span>
            </div>
            {/* Animated SpO2 Pleth Line SVG with Grid Lines */}
            <div className="h-9 w-full overflow-hidden relative flex items-center bg-[#020812] rounded border border-slate-900 bg-[linear-gradient(to_right,#0a1a2f_1px,transparent_1px),linear-gradient(to_bottom,#0a1a2f_1px,transparent_1px)] bg-[size:10px_10px]">
              <div className="flex w-[800px] animate-[slide_5s_linear_infinite]">
                <svg className="w-[400px] h-8 text-cyan-400 shrink-0 drop-shadow-[0_0_3px_rgba(34,211,238,0.6)]" viewBox="0 0 400 50" preserveAspectRatio="none">
                  <path
                    d="M 0 30 Q 20 5, 40 30 T 80 30 T 120 30 Q 140 5, 160 30 T 200 30 T 240 30 Q 260 5, 280 30 T 320 30 T 360 30 Q 380 5, 400 30"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.4"
                  />
                </svg>
                <svg className="w-[400px] h-8 text-cyan-400 shrink-0 drop-shadow-[0_0_3px_rgba(34,211,238,0.6)]" viewBox="0 0 400 50" preserveAspectRatio="none">
                  <path
                    d="M 0 30 Q 20 5, 40 30 T 80 30 T 120 30 Q 140 5, 160 30 T 200 30 T 240 30 Q 260 5, 280 30 T 320 30 T 360 30 Q 380 5, 400 30"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.4"
                  />
                </svg>
              </div>
            </div>
          </div>

          {/* Vitals Column (translateZ(16px)) */}
          <div className="col-span-4 space-y-1.5 font-mono text-right [transform:translateZ(16px)]">
            <div className="bg-slate-950/90 border border-slate-800/80 p-1.5 rounded-xl shadow-sm">
              <div className="text-[8px] text-slate-400">HR <span className="text-[7px]">bpm</span></div>
              <div className="text-xl font-black text-emerald-400">78</div>
            </div>
            <div className="bg-slate-950/90 border border-slate-800/80 p-1.5 rounded-xl shadow-sm">
              <div className="text-[8px] text-slate-400">SpO₂ <span className="text-[7px]">%</span></div>
              <div className="text-xl font-black text-cyan-400">98</div>
            </div>
            <div className="bg-slate-950/90 border border-slate-800/80 p-1.5 rounded-xl shadow-sm">
              <div className="text-[8px] text-slate-400">RR <span className="text-[7px]">rpm</span></div>
              <div className="text-lg font-black text-amber-400">18</div>
            </div>
          </div>

        </div>

        {/* Secondary Vitals Readouts */}
        <div className="grid grid-cols-2 gap-2 font-mono text-xs [transform:translateZ(14px)]">
          <div className="bg-slate-950/85 border border-slate-800/80 p-2 rounded-xl flex items-center justify-between">
            <span className="text-[9px] text-slate-400">BP mmHg</span>
            <span className="font-bold text-slate-100">120/80</span>
          </div>
          <div className="bg-slate-950/85 border border-slate-800/80 p-2 rounded-xl flex items-center justify-between">
            <span className="text-[9px] text-slate-400">TEMP °C</span>
            <span className="font-bold text-slate-100">37.1</span>
          </div>
        </div>

        {/* Sepsis Risk & Active Alerts (translateZ(18px)) */}
        <div className="grid grid-cols-2 gap-2.5 [transform:translateZ(18px)]">
          <div className="bg-cyan-950/50 border border-cyan-800/70 p-2.5 rounded-2xl space-y-1 shadow-sm">
            <div className="flex items-center justify-between text-[9px] font-mono text-cyan-400">
              <span>SEPSIS RISK</span>
              <span className="font-bold">LOW</span>
            </div>
            <div className="text-xl font-black font-mono text-cyan-300">14%</div>
            <div className="flex items-center justify-between text-[8px] font-mono text-slate-400">
              <span>RISK TREND</span>
              <span className="text-cyan-400 font-bold">STABLE</span>
            </div>
          </div>

          <div className="bg-slate-950/85 border border-slate-800/80 p-2.5 rounded-2xl space-y-0.5 shadow-sm">
            <div className="flex items-center justify-between text-[9px] font-mono text-slate-400">
              <span className="flex items-center gap-1"><Bell size={10} className="text-emerald-400" /> ACTIVE ALERTS</span>
              <span className="text-emerald-400 font-bold text-[8px]">0%</span>
            </div>
            <div className="text-xl font-black font-mono text-slate-100">0 <span className="text-xs font-semibold text-slate-400">CRITICAL</span></div>
            <div className="text-[8px] font-mono text-emerald-400">No critical alerts</div>
          </div>
        </div>

        {/* AI Copilot Panel (translateZ(24px)) */}
        <div className="bg-slate-950/95 border border-cyan-500/40 p-3 rounded-2xl flex items-start gap-2.5 text-xs backdrop-blur-md shadow-lg [transform:translateZ(24px)]">
          <div className="p-1.5 rounded-xl bg-cyan-950 border border-cyan-800/60 text-cyan-400 shrink-0">
            <Brain size={16} className="animate-pulse text-cyan-300" />
          </div>
          <div className="space-y-0.5">
            <span className="text-[9px] font-mono font-bold text-cyan-400 uppercase tracking-wider block">
              AI COPILOT DECISION SUPPORT
            </span>
            <p className="text-slate-200 leading-snug text-[11px]">
              Patient hemodynamics are stable. Continue monitoring trends. Next lab audit in 45 mins.
            </p>
          </div>
        </div>

      </div>
    </div>
  );
}

