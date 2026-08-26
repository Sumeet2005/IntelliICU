import React from "react";
import { Link } from "react-router-dom";
import { Activity, ExternalLink, Menu, X } from "lucide-react";

export default function LandingHeader({ mobileMenuOpen, setMobileMenuOpen, scrollToSection }) {
  return (
    <header className="w-full border-b border-cyan-950/40 bg-[#02060d]/85 backdrop-blur-xl sticky top-0 z-50 px-4 sm:px-8 py-3.5">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 shadow-lg shadow-cyan-500/30 group-hover:scale-105 transition duration-300">
            <Activity className="text-white" size={20} />
          </div>
          <div>
            <span className="text-base font-black tracking-wider uppercase text-white block leading-none">
              INTELLIICU
            </span>
            <span className="text-[9px] font-bold text-cyan-400 tracking-widest uppercase block mt-1">
              CLINICAL AI PLATFORM
            </span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden lg:flex items-center gap-8 text-xs font-semibold text-slate-300">
          <button onClick={() => scrollToSection("pipeline")} className="hover:text-cyan-400 transition cursor-pointer">
            Pipeline
          </button>
          <button onClick={() => scrollToSection("modules")} className="hover:text-cyan-400 transition cursor-pointer">
            Modules
          </button>
          <button onClick={() => scrollToSection("telemetry")} className="hover:text-cyan-400 transition cursor-pointer">
            Live Telemetry
          </button>
          <button onClick={() => scrollToSection("explainability")} className="hover:text-cyan-400 transition cursor-pointer">
            Explainable AI
          </button>
          <button onClick={() => scrollToSection("workflows")} className="hover:text-cyan-400 transition cursor-pointer">
            Workflows
          </button>
        </nav>

        {/* Desktop Right Action Buttons */}
        <div className="hidden lg:flex items-center gap-4">
          <a
            href="https://intelliicu.dockhosting.dev/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-300 hover:text-white transition"
          >
            API Docs <ExternalLink size={12} className="text-slate-400" />
          </a>
          <Link
            to="/login"
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-slate-900/90 border border-cyan-500/40 text-white font-bold px-5 py-2 text-xs transition duration-300 hover:border-cyan-400 hover:bg-cyan-950/60 active:scale-[0.98] shadow-lg shadow-cyan-950/60"
          >
            Sign In
          </Link>
        </div>

        {/* Mobile Menu Toggle Button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="lg:hidden p-2 text-slate-300 hover:text-white cursor-pointer"
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {/* Mobile Dropdown Navigation */}
      {mobileMenuOpen && (
        <div className="lg:hidden mt-3 border-t border-slate-800/80 pt-4 pb-2 space-y-3 font-semibold text-xs text-slate-300">
          <button onClick={() => scrollToSection("pipeline")} className="block w-full text-left py-1 hover:text-cyan-400">
            Pipeline
          </button>
          <button onClick={() => scrollToSection("modules")} className="block w-full text-left py-1 hover:text-cyan-400">
            Modules
          </button>
          <button onClick={() => scrollToSection("telemetry")} className="block w-full text-left py-1 hover:text-cyan-400">
            Live Telemetry
          </button>
          <button onClick={() => scrollToSection("explainability")} className="block w-full text-left py-1 hover:text-cyan-400">
            Explainable AI
          </button>
          <button onClick={() => scrollToSection("workflows")} className="block w-full text-left py-1 hover:text-cyan-400">
            Workflows
          </button>
          <div className="pt-3 border-t border-slate-800 flex items-center justify-between">
            <a
              href="https://intelliicu.dockhosting.dev/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-slate-400 hover:text-white"
            >
              API Docs <ExternalLink size={12} />
            </a>
            <Link
              to="/login"
              className="rounded-xl bg-cyan-500 text-slate-950 font-extrabold px-4 py-2 text-xs"
            >
              Sign In
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
