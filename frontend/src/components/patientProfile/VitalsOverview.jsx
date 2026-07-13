import { useClinicalAI } from "../../context/ClinicalAIContext";
import { useEffect, useState, useMemo } from "react";
import { motion } from "framer-motion";
import {
  HeartPulse,
  Activity,
  Thermometer,
  Droplets,
  Loader2,
} from "lucide-react";

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  CartesianGrid,
  XAxis,
  Tooltip,
} from "recharts";

export default function VitalsOverview() {
  const { selectedPatient, recommendation } = useClinicalAI();
  const patientId = selectedPatient?.patient?.id;
  const vitalsData = selectedPatient?.vitals || {};
  const risk = recommendation?.risk_progress;

  const [activeMetric, setActiveMetric] = useState("heartRate");
  const [history, setHistory] = useState([]);

  // Reset history when active patient changes
  useEffect(() => {
    setHistory([]);
  }, [patientId]);

  // Record rolling vital history from live context updates
  useEffect(() => {
    if (!patientId || !vitalsData.heart_rate) return;

    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    setHistory(prev => {
      if (prev.length > 0 && prev[prev.length - 1].time === time) {
        return prev;
      }
      
      const newPoint = {
        time,
        heartRate: vitalsData.heart_rate,
        systolic: vitalsData.blood_pressure?.systolic ?? vitalsData.systolic_bp ?? 82,
        diastolic: vitalsData.blood_pressure?.diastolic ?? vitalsData.diastolic_bp ?? 48,
        spo2: vitalsData.spo2 ?? 89,
        respiratoryRate: vitalsData.respiratory_rate ?? 31,
        temperature: vitalsData.temperature ?? 39.2,
        risk: (selectedPatient?.patient?.risk_score ?? selectedPatient?.ai?.risk_progress?.current_risk ?? 0) * 100,
      };

      const updated = [...prev, newPoint];
      if (updated.length > 60) {
        return updated.slice(updated.length - 60);
      }
      return updated;
    });
  }, [vitalsData, patientId, selectedPatient]);

  const systolic = vitalsData.blood_pressure?.systolic ?? vitalsData.systolic_bp;
  const diastolic = vitalsData.blood_pressure?.diastolic ?? vitalsData.diastolic_bp;
  const bpValue = systolic && diastolic ? `${systolic} / ${diastolic}` : "-";

  const vitals = [
    {
      title: "Heart Rate",
      value: vitalsData.heart_rate ?? "-",
      unit: "bpm",
      icon: HeartPulse,
      color: "text-red-500",
      bg: "bg-red-50",
      border: "border-red-100",
    },
    {
      title: "Blood Pressure",
      value: bpValue,
      unit: "mmHg",
      icon: Activity,
      color: "text-cyan-600",
      bg: "bg-cyan-50",
      border: "border-cyan-100",
    },
    {
      title: "SpO₂",
      value: vitalsData.spo2 ? `${vitalsData.spo2}` : "-",
      unit: "%",
      icon: Droplets,
      color: "text-blue-600",
      bg: "bg-blue-50",
      border: "border-blue-100",
    },
    {
      title: "Temperature",
      value: vitalsData.temperature ? `${vitalsData.temperature}` : "-",
      unit: "°C",
      icon: Thermometer,
      color: "text-orange-500",
      bg: "bg-orange-50",
      border: "border-orange-100",
    },
  ];

  const metricColors = {
    heartRate: { stroke: "#ef4444", fill: "#ef4444" },
    bloodPressure: { stroke: "#0891b2", fill: "#0891b2" },
    spo2: { stroke: "#2563eb", fill: "#2563eb" },
    respiratoryRate: { stroke: "#0d9488", fill: "#0d9488" },
    temperature: { stroke: "#ea580c", fill: "#ea580c" },
    risk: { stroke: "#06b6d4", fill: "#06b6d4" },
  };

  const getMetricTitle = () => {
    switch (activeMetric) {
      case "heartRate": return "Heart Rate Trend";
      case "bloodPressure": return "Blood Pressure Trend";
      case "spo2": return "SpO₂ Trend";
      case "respiratoryRate": return "Respiratory Rate Trend";
      case "temperature": return "Temperature Trend";
      case "risk": return "AI Sepsis Risk Trend";
      default: return "Physiological Trend";
    }
  };

  return (
    <div className="space-y-6">

      {/* Header */}

      <div className="rounded-[30px] bg-white border border-slate-200 shadow-xl p-6">

        <div className="flex items-center justify-between">

          <div>

            <h2 className="text-3xl font-black">

              Live Vital Signs

            </h2>

            <p className="mt-2 text-slate-500">

              ICU Physiological Monitoring

            </p>

          </div>

          <div className="flex items-center gap-2 rounded-full bg-emerald-50 px-4 py-2">

            <span className="h-3 w-3 rounded-full bg-emerald-500 animate-pulse"></span>

            <span className="font-semibold text-emerald-700">

              Live

            </span>

          </div>

        </div>

      </div>

      {/* Vital Cards */}

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

        {vitals.map((item) => {

          const Icon = item.icon;

          return (

            <motion.div
              key={item.title}
              whileHover={{
                y: -6,
              }}
              className={`rounded-[24px] border ${item.border} ${item.bg} p-6 shadow-lg`}
            >

              <div className="flex items-center justify-between">

                <Icon
                  className={item.color}
                  size={34}
                />

                <span className="rounded-full bg-white px-3 py-1 text-xs font-semibold shadow">

                  Normal Range

                </span>

              </div>

              <h2 className="mt-8 text-5xl font-black">

                {item.value}

              </h2>

              <p className="mt-2 text-slate-500">

                {item.unit}

              </p>

              <div className="mt-6 h-2 rounded-full bg-white overflow-hidden">

                <div
                  className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-blue-600"
                  style={{ width: "75%" }}
                />

              </div>

              <p className="mt-4 font-semibold">

                {item.title}

              </p>

            </motion.div>

          );

        })}

      </div>

      {/* AI Risk Trend */}

      <motion.div
        whileHover={{
          scale: 1.01,
        }}
        className="rounded-[30px] bg-white border border-slate-200 shadow-xl p-6"
      >

        <div className="flex flex-col md:flex-row md:items-center md:justify-between border-b pb-4 gap-4">

          <div>

            <h2 className="text-2xl font-bold">

              {getMetricTitle()}

            </h2>

            <p className="mt-2 text-slate-500">

              Rolling live patient history

            </p>

          </div>

          <div className="flex flex-wrap gap-2">

            {[
              { id: "heartRate", label: "HR" },
              { id: "bloodPressure", label: "BP" },
              { id: "spo2", label: "SpO₂" },
              { id: "respiratoryRate", label: "RR" },
              { id: "temperature", label: "Temp" },
              { id: "risk", label: "Risk" },
            ].map((tab) => (

              <button
                key={tab.id}
                onClick={() => setActiveMetric(tab.id)}
                className={`rounded-lg px-3 py-1.5 text-xs font-bold transition ${
                  activeMetric === tab.id
                    ? "bg-cyan-600 text-white"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
              >

                {tab.label}

              </button>

            ))}

          </div>

        </div>

        {history.length === 0 ? (
          <div className="flex h-80 flex-col items-center justify-center rounded-2xl bg-slate-50 border border-dashed border-slate-200 mt-6">
            <Loader2 className="animate-spin text-slate-400 mb-2" size={28} />
            <p className="text-slate-500 font-semibold">Waiting for live data...</p>
          </div>
        ) : (
          <div className="mt-8 h-80">

            <ResponsiveContainer>

              <AreaChart
                data={history}
              >

                <defs>

                  <linearGradient
                    id="chartColor"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >

                    <stop
                      offset="0%"
                      stopColor={metricColors[activeMetric]?.stroke}
                      stopOpacity={0.4}
                    />

                    <stop
                      offset="100%"
                      stopColor={metricColors[activeMetric]?.stroke}
                      stopOpacity={0}
                    />

                  </linearGradient>

                </defs>

                <CartesianGrid strokeDasharray="4 4" />

                <XAxis dataKey="time" />

                <Tooltip />

                {activeMetric === "bloodPressure" ? (
                  <>
                    <Area
                      type="monotone"
                      dataKey="systolic"
                      name="Systolic BP"
                      stroke="#0891b2"
                      fill="url(#chartColor)"
                      strokeWidth={3}
                    />
                    <Area
                      type="monotone"
                      dataKey="diastolic"
                      name="Diastolic BP"
                      stroke="#3b82f6"
                      fill="none"
                      strokeWidth={2}
                    />
                  </>
                ) : (
                  <Area
                    type="monotone"
                    dataKey={activeMetric}
                    name={getMetricTitle()}
                    stroke={metricColors[activeMetric]?.stroke}
                    fill="url(#chartColor)"
                    strokeWidth={3}
                  />
                )}

              </AreaChart>

            </ResponsiveContainer>

            <div className="mt-6 flex justify-between rounded-xl bg-slate-50 p-4">

              <div>

                <p className="text-sm text-slate-500">

                  Previous Risk

                </p>

                <p className="text-xl font-bold">

                  {((risk?.previous_risk ?? 0) * 100).toFixed(0)}%

                </p>

              </div>

              <div>

                <p className="text-sm text-slate-500">

                  Current Risk

                </p>

                <p className="text-xl font-bold">

                  {((risk?.current_risk ?? 0) * 100).toFixed(0)}%

                </p>

              </div>

              <div>

                <p className="text-sm text-slate-500">

                  Trend

                </p>

                <p className="text-xl font-bold">

                  {risk?.trend ?? "-"}

                </p>

              </div>

            </div>

          </div>
        )}

      </motion.div>

    </div>
  );
}