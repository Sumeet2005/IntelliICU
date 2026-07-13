import { motion } from "framer-motion";
import {
  BrainCircuit,
  Activity,
  ShieldCheck,
  Users,
  AlertTriangle,
  ArrowRight,
  Sparkles,
} from "lucide-react";

export default function HeroBanner() {
  return (
    <motion.section
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="relative overflow-hidden rounded-[32px] bg-gradient-to-br from-slate-900 via-[#0B2942] to-cyan-900 p-8 text-white shadow-2xl"
    >
      {/* Background Glow */}
      <div className="absolute -top-32 -right-20 h-80 w-80 rounded-full bg-cyan-400/20 blur-3xl"></div>
      <div className="absolute -bottom-32 -left-20 h-72 w-72 rounded-full bg-blue-500/20 blur-3xl"></div>

      <div className="relative grid grid-cols-12 gap-8">

        {/* Left Side */}
        <div className="col-span-12 lg:col-span-7">

          <div className="inline-flex items-center gap-2 rounded-full bg-cyan-500/20 border border-cyan-400/30 px-4 py-2 text-sm backdrop-blur">

            <BrainCircuit size={18} />

            AI Clinical Decision Support System

          </div>

          <h1 className="mt-6 text-5xl font-black leading-tight">

            IntelliICU

            <span className="block text-cyan-300">

              Clinical Command Center

            </span>

          </h1>

          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-300">

            Monitor ICU patients in real time, predict clinical deterioration,
            receive explainable AI recommendations, and support evidence-based
            medical decisions.

          </p>

          <div className="mt-10 flex flex-wrap gap-4">

            <button className="rounded-xl bg-cyan-500 px-6 py-3 font-semibold hover:bg-cyan-400 transition flex items-center gap-2">

              Launch AI Assistant

              <ArrowRight size={18} />

            </button>

            <button className="rounded-xl border border-white/20 bg-white/10 px-6 py-3 backdrop-blur hover:bg-white/20 transition">

              View Live Monitoring

            </button>

          </div>

        </div>

        {/* Right Side */}
        <div className="col-span-12 lg:col-span-5">

          <div className="grid grid-cols-2 gap-5">

            <div className="rounded-2xl border border-white/10 bg-white/10 p-5 backdrop-blur">

              <Users className="text-cyan-300" />

              <h2 className="mt-4 text-4xl font-bold">

                48

              </h2>

              <p className="text-slate-300">

                Active Patients

              </p>

            </div>

            <div className="rounded-2xl border border-white/10 bg-white/10 p-5 backdrop-blur">

              <AlertTriangle className="text-red-400" />

              <h2 className="mt-4 text-4xl font-bold">

                7

              </h2>

              <p className="text-slate-300">

                Critical Alerts

              </p>

            </div>

            <div className="rounded-2xl border border-white/10 bg-white/10 p-5 backdrop-blur">

              <ShieldCheck className="text-emerald-400" />

              <h2 className="mt-4 text-4xl font-bold">

                97.8%

              </h2>

              <p className="text-slate-300">

                AI Confidence

              </p>

            </div>

            <div className="rounded-2xl border border-white/10 bg-white/10 p-5 backdrop-blur">

              <Activity className="text-cyan-300 animate-pulse" />

              <h2 className="mt-4 text-4xl font-bold text-emerald-400">

                LIVE

              </h2>

              <p className="text-slate-300">

                Monitoring

              </p>

            </div>

          </div>

          <div className="mt-6 rounded-2xl border border-cyan-400/20 bg-black/20 p-6 backdrop-blur">

            <div className="flex items-center gap-3">

              <Sparkles className="text-cyan-300" />

              <h3 className="font-semibold">

                AI Clinical Summary

              </h3>

            </div>

            <p className="mt-4 leading-7 text-slate-300">

              AI has identified <strong>3 high-risk patients</strong> with an
              elevated probability of sepsis. Early intervention is recommended
              within the next hour based on current vitals and laboratory trends.

            </p>

          </div>

        </div>

      </div>

    </motion.section>
  );
}