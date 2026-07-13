import {
  ResponsiveContainer,
  AreaChart,
  Area,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
  LineChart,
  Line,
} from "recharts";

import {
  Activity,
  HeartPulse,
  BrainCircuit,
  TrendingUp,
} from "lucide-react";

import { motion } from "framer-motion";

const heartRate = [
  { t: "08", hr: 82 },
  { t: "10", hr: 91 },
  { t: "12", hr: 88 },
  { t: "14", hr: 101 },
  { t: "16", hr: 111 },
  { t: "18", hr: 118 },
];

const prediction = [
  { t: "08", p: 21 },
  { t: "10", p: 33 },
  { t: "12", p: 46 },
  { t: "14", p: 60 },
  { t: "16", p: 79 },
  { t: "18", p: 96 },
];

export default function LiveAnalytics() {
  return (
    <section className="space-y-6">

      {/* Header */}

      <div className="flex items-center justify-between">

        <div>

          <h2 className="text-2xl font-bold">

            Live ICU Analytics

          </h2>

          <p className="text-slate-500">

            AI monitoring every patient in real time

          </p>

        </div>

        <div className="flex items-center gap-2 rounded-full bg-emerald-100 px-4 py-2">

          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"/>

          <span className="font-semibold text-emerald-700">

            LIVE

          </span>

        </div>

      </div>

      {/* Charts */}

      <div className="grid grid-cols-12 gap-6">

        {/* Heart Rate */}

        <motion.div

          whileHover={{ y: -5 }}

          className="col-span-12 xl:col-span-8 rounded-3xl bg-white p-6 shadow-xl border border-slate-200"

        >

          <div className="flex items-center justify-between">

            <div>

              <div className="flex items-center gap-2">

                <HeartPulse className="text-red-500"/>

                <h3 className="font-bold text-xl">

                  Heart Rate Trend

                </h3>

              </div>

              <p className="mt-2 text-slate-500">

                Live streaming ICU telemetry

              </p>

            </div>

            <div className="rounded-2xl bg-red-50 px-4 py-2">

              <span className="font-bold text-red-600">

                118 BPM

              </span>

            </div>

          </div>

          <div className="mt-8 h-80">

            <ResponsiveContainer>

              <AreaChart data={heartRate}>

                <defs>

                  <linearGradient id="hrGradient">

                    <stop offset="0%" stopColor="#ef4444" stopOpacity={0.8}/>

                    <stop offset="100%" stopColor="#ef4444" stopOpacity={0}/>

                  </linearGradient>

                </defs>

                <CartesianGrid strokeDasharray="3 3"/>

                <XAxis dataKey="t"/>

                <YAxis/>

                <Tooltip/>

                <Area

                  type="monotone"

                  dataKey="hr"

                  stroke="#ef4444"

                  strokeWidth={4}

                  fill="url(#hrGradient)"

                />

              </AreaChart>

            </ResponsiveContainer>

          </div>

        </motion.div>

        {/* Right Column */}

        <div className="col-span-12 xl:col-span-4 space-y-6">

          {/* AI Confidence */}

          <motion.div

            whileHover={{ y: -5 }}

            className="rounded-3xl bg-gradient-to-br from-indigo-600 to-violet-700 p-6 text-white shadow-xl"

          >

            <BrainCircuit size={32}/>

            <h3 className="mt-5 text-2xl font-bold">

              AI Prediction

            </h3>

            <h1 className="mt-4 text-6xl font-black">

              97.8%

            </h1>

            <p className="mt-3 text-indigo-100">

              Confidence Score

            </p>

            <div className="mt-6 h-3 rounded-full bg-white/20">

              <div

                className="h-full rounded-full bg-white"

                style={{ width: "97%" }}

              />

            </div>

          </motion.div>

          {/* Prediction Trend */}

          <motion.div

            whileHover={{ y: -5 }}

            className="rounded-3xl bg-white p-6 shadow-xl border border-slate-200"

          >

            <div className="flex items-center gap-2">

              <TrendingUp className="text-cyan-600"/>

              <h3 className="font-bold">

                Sepsis Prediction

              </h3>

            </div>

            <div className="mt-6 h-52">

              <ResponsiveContainer>

                <LineChart data={prediction}>

                  <CartesianGrid strokeDasharray="3 3"/>

                  <XAxis dataKey="t"/>

                  <YAxis/>

                  <Tooltip/>

                  <Line

                    type="monotone"

                    dataKey="p"

                    stroke="#06b6d4"

                    strokeWidth={4}

                    dot={{ r: 4 }}

                  />

                </LineChart>

              </ResponsiveContainer>

            </div>

          </motion.div>

        </div>

      </div>

      {/* Bottom Stats */}

      <div className="grid grid-cols-2 xl:grid-cols-4 gap-6">

        {[
          ["SpO₂", "98%", "text-cyan-600"],
          ["Respiration", "18 bpm", "text-emerald-600"],
          ["Temperature", "37.1°C", "text-orange-600"],
          ["AI Events", "124", "text-violet-600"],
        ].map(([title, value, color]) => (

          <motion.div

            whileHover={{ scale: 1.03 }}

            key={title}

            className="rounded-3xl bg-white border border-slate-200 p-6 shadow-lg"

          >

            <Activity className={color}/>

            <h2 className="mt-4 text-4xl font-black">

              {value}

            </h2>

            <p className="mt-2 text-slate-500">

              {title}

            </p>

          </motion.div>

        ))}

      </div>

    </section>
  );
}