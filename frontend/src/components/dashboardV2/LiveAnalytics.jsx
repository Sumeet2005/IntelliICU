import { useEffect, useRef, useState } from "react";
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
import { Activity, HeartPulse, TrendingUp } from "lucide-react";
import { motion } from "framer-motion";
import useWebSocket from "../../hooks/useWebSocket";

export default function LiveAnalytics() {
  const { connected, patients = [], alerts = [] } = useWebSocket();
  const [series, setSeries] = useState([]);
  const lastSampleKey = useRef("");

  useEffect(() => {
    if (!Array.isArray(patients) || patients.length === 0) return;

    const count = patients.length;
    const avgHr = Math.round(patients.reduce((s, p) => s + (Number(p.heart_rate) || 0), 0) / count);
    const avgRisk = Math.round((patients.reduce((s, p) => s + (Number(p.risk_score) || 0), 0) / count) * 100);
    const key = `${avgHr}-${avgRisk}-${patients[0]?.heart_rate}`;
    if (key === lastSampleKey.current) return;
    lastSampleKey.current = key;

    const label = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
    setSeries((prev) => [...prev.slice(-11), { t: label, hr: avgHr, p: avgRisk }]);
  }, [patients]);

  const count = patients.length || 0;
  const latestHr = count ? Math.round(patients.reduce((s, p) => s + (Number(p.heart_rate) || 0), 0) / count) : null;
  const latestSpo2 = count ? Math.round(patients.reduce((s, p) => s + (Number(p.spo2) || 0), 0) / count) : null;
  const latestRr = count ? Math.round(patients.reduce((s, p) => s + (Number(p.respiratory_rate) || 0), 0) / count) : null;
  const latestTemp = count ? (patients.reduce((s, p) => s + (Number(p.temperature) || 0), 0) / count).toFixed(1) : null;

  return (
    <section className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Live ICU Analytics</h2>
          <p className="text-slate-500">
            Real-time unit telemetry aggregated from active ICU streams
          </p>
        </div>

        <div className={`flex items-center gap-2 rounded-full px-4 py-2 ${connected ? "bg-emerald-100" : "bg-slate-100"}`}>
          <span className={`h-2 w-2 rounded-full ${connected ? "bg-emerald-500 animate-pulse" : "bg-slate-400"}`} />
          <span className={`font-semibold ${connected ? "text-emerald-700" : "text-slate-600"}`}>
            {connected ? "LIVE" : "WAITING"}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        <motion.div
          whileHover={{ y: -3 }}
          className="col-span-12 xl:col-span-8 clinical-card p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2">
                <HeartPulse className="text-red-500" />
                <h3 className="font-bold text-xl text-slate-800">Mean Unit Heart Rate</h3>
              </div>
              <p className="mt-2 text-xs text-slate-500">
                Live streaming ICU telemetry (rolling window)
              </p>
            </div>

            <div className="rounded-xl bg-red-50 px-4 py-2">
              <span className="font-bold text-red-600 text-sm">
                {latestHr !== null ? `${latestHr} BPM` : "—"}
              </span>
            </div>
          </div>

          <div className="mt-8 h-80">
            {series.length === 0 ? (
              <div className="flex h-full items-center justify-center text-xs font-semibold text-slate-400">
                Waiting for live WebSocket telemetry samples...
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={series}>
                  <defs>
                    <linearGradient id="hrGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#ef4444" stopOpacity={0.2} />
                      <stop offset="100%" stopColor="#ef4444" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="t" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip />
                  <Area
                    type="monotone"
                    dataKey="hr"
                    stroke="#ef4444"
                    strokeWidth={3}
                    fill="url(#hrGradient)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </motion.div>

        <div className="col-span-12 xl:col-span-4 flex flex-col">
          <motion.div
            whileHover={{ y: -3 }}
            className="clinical-card p-6 flex-1 flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center gap-2">
                <TrendingUp className="text-cyan-600" />
                <h3 className="font-bold text-slate-800 text-lg">Mean Sepsis Risk Trend</h3>
              </div>
              <p className="mt-2 text-xs text-slate-500">Real-time unit risk index (%)</p>
            </div>

            <div className="mt-6 h-64">
              {series.length === 0 ? (
                <div className="flex h-full items-center justify-center text-xs font-semibold text-slate-400">
                  No live samples yet
                </div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={series}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                    <XAxis dataKey="t" stroke="#94a3b8" fontSize={11} />
                    <YAxis stroke="#94a3b8" fontSize={11} />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="p"
                      stroke="#0284c7"
                      strokeWidth={3}
                      dot={{ r: 4, strokeWidth: 2, fill: "#fff" }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </div>
          </motion.div>
        </div>
      </div>

      <div className="grid grid-cols-2 xl:grid-cols-4 gap-6">
        {[
          ["Mean SpO₂", latestSpo2 !== null ? `${latestSpo2}%` : "—", "text-cyan-600"],
          ["Mean Respiration", latestRr !== null ? `${latestRr} bpm` : "—", "text-emerald-600"],
          ["Mean Temperature", latestTemp !== null ? `${latestTemp}°C` : "—", "text-orange-600"],
          ["Active Alerts", String(alerts.length), "text-violet-600"],
        ].map(([title, value, color]) => (
          <motion.div
            whileHover={{ y: -2 }}
            key={title}
            className="clinical-card p-6"
          >
            <Activity className={color} size={18} />
            <h2 className="mt-4 text-3xl font-black text-slate-800">{value}</h2>
            <p className="mt-1 text-[10px] text-slate-400 font-extrabold uppercase tracking-wider">
              {title}
            </p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
