import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Users,
  AlertTriangle,
  BedDouble,
  BrainCircuit,
  ArrowUpRight,
} from "lucide-react";

import { dashboardService } from "../../services/dashboardService";
import useWebSocket from "../../hooks/useWebSocket";

import { useClinicalAI } from "../../context/ClinicalAIContext";

export default function KPISection() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  // NEW
  const { dashboardData } = useWebSocket();
  const { alertCount } = useClinicalAI();

  useEffect(() => {
    loadDashboard();
  }, []);

  useEffect(() => {
    if (dashboardData) {
      setDashboard(dashboardData);
      setLoading(false);
    }
  }, [dashboardData]);

  async function loadDashboard() {
    try {
      const data = await dashboardService.getDashboard();
      setDashboard(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  if (loading || !dashboard) {
    return (
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <div
            key={i}
            className="h-40 animate-pulse rounded-3xl bg-slate-200"
          />
        ))}
      </div>
    );
  }

  const cards = [
    {
      title: "Patients",
      value: dashboard.total_patients,
      icon: Users,
      color: "from-cyan-500 to-blue-600",
    },
    {
      title: "Critical",
      value: dashboard.critical_patients,
      icon: AlertTriangle,
      color: "from-red-500 to-red-700",
    },
    {
      title: "Occupancy",
      value: `${dashboard.bed_occupancy}%`,
      icon: BedDouble,
      color: "from-green-500 to-emerald-600",
    },
    {
      title: "AI Alerts",
      value: alertCount ?? dashboard.active_alerts,
      icon: BrainCircuit,
      color: "from-violet-500 to-indigo-600",
    },
  ];

  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
      {cards.map((item) => {
        const Icon = item.icon;

        return (
          <motion.div
            key={item.title}
            whileHover={{ y: -6 }}
            className="rounded-3xl bg-white p-6 shadow-xl"
          >
            <div className="flex justify-between">
              <div>
                <p className="text-slate-500">{item.title}</p>

                <motion.h2
                  key={item.value}
                  initial={{ scale: 0.9, opacity: 0.6 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.25 }}
                  className="mt-3 text-5xl font-black"
                >
                  {item.value}
                </motion.h2>
              </div>

              <div
                className={`flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br ${item.color}`}
              >
                <Icon className="text-white" />
              </div>
            </div>

            <div className="mt-8 flex items-center justify-between">
              <div className="flex items-center gap-2 text-emerald-600">
                <ArrowUpRight size={18} />
                Live
              </div>

              <div className="h-2 w-2 animate-pulse rounded-full bg-emerald-500" />
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}