import { motion } from "framer-motion";
import {
  BedDouble,
  Users,
  Ambulance,
  ShieldCheck,
  TrendingUp,
} from "lucide-react";
import {
  ResponsiveContainer,
  RadialBarChart,
  RadialBar,
  PolarAngleAxis,
} from "recharts";

import useWebSocket from "../../hooks/useWebSocket";

export default function HospitalAnalytics() {
  // New WebSocket Hook
  const { dashboardData } = useWebSocket();

  const occupancyValue = dashboardData?.bed_occupancy ?? 86;
  const totalPatients = dashboardData?.total_patients ?? 48;
  const icuCapacity = dashboardData?.icu_capacity ?? 56;
  const activeAlerts = dashboardData?.active_alerts ?? 6;

  const occupancy = [
    {
      name: "Occupancy",
      value: occupancyValue,
      fill: "#06b6d4",
    },
  ];

  const resources = [
    {
      title: "ICU Beds",
      value: `${totalPatients} / ${icuCapacity}`,
      icon: BedDouble,
      color: "bg-cyan-100 text-cyan-600",
    },
    {
      title: "Doctors On Duty",
      value: "18",
      icon: Users,
      color: "bg-violet-100 text-violet-600",
    },
    {
      title: "Emergency Admissions",
      value: activeAlerts,
      icon: Ambulance,
      color: "bg-red-100 text-red-600",
    },
    {
      title: "System Health",
      value: "99.8%",
      icon: ShieldCheck,
      color: "bg-emerald-100 text-emerald-600",
    },
  ];

  return (
    <section className="space-y-6">
      {/* Occupancy */}
      <motion.div
        whileHover={{ y: -5 }}
        className="rounded-[30px] border border-slate-200 bg-white p-6 shadow-xl"
      >
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">
              Hospital Analytics
            </h2>

            <p className="mt-2 text-slate-500">
              Operational Intelligence
            </p>
          </div>

          <TrendingUp className="text-cyan-600" />
        </div>

        <div className="mt-8 h-72">
          <ResponsiveContainer width="100%" height="100%">
            <RadialBarChart
              innerRadius="70%"
              outerRadius="100%"
              data={occupancy}
              startAngle={90}
              endAngle={-270}
            >
              <PolarAngleAxis
                type="number"
                domain={[0, 100]}
                tick={false}
              />

              <RadialBar
                background
                dataKey="value"
                cornerRadius={20}
              />
            </RadialBarChart>
          </ResponsiveContainer>
        </div>

        <div className="-mt-24 text-center">
          <motion.h1
            key={occupancyValue}
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.3 }}
            className="text-5xl font-black text-cyan-600"
          >
            {occupancyValue}%
          </motion.h1>

          <p className="text-slate-500">
            Bed Occupancy
          </p>
        </div>
      </motion.div>

      {/* Resource Cards */}
      <div className="space-y-5">
        {resources.map((item, index) => {
          const Icon = item.icon;

          return (
            <motion.div
              key={index}
              whileHover={{ scale: 1.02 }}
              className="rounded-2xl border border-slate-200 bg-white p-5 shadow-lg"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div
                    className={`flex h-14 w-14 items-center justify-center rounded-2xl ${item.color}`}
                  >
                    <Icon size={26} />
                  </div>

                  <div>
                    <p className="text-sm text-slate-500">
                      {item.title}
                    </p>

                    <motion.h3
                      key={item.value}
                      initial={{ opacity: 0.5 }}
                      animate={{ opacity: 1 }}
                      className="text-2xl font-bold"
                    >
                      {item.value}
                    </motion.h3>
                  </div>
                </div>

                <span className="block h-3 w-3 animate-pulse rounded-full bg-emerald-500"></span>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Footer */}
      <motion.div
        whileHover={{ scale: 1.02 }}
        className="rounded-3xl bg-gradient-to-br from-cyan-600 to-blue-700 p-6 text-white shadow-xl"
      >
        <p className="text-sm text-cyan-100">
          AI Operational Insight
        </p>

        <h3 className="mt-3 text-xl font-bold">
          ICU utilization is approaching capacity.
        </h3>

        <p className="mt-4 leading-7 text-cyan-100">
          Based on current admission trends, the AI predicts bed occupancy
          may exceed 90% within the next 8 hours. Consider preparing
          overflow resources and prioritizing discharge planning for
          clinically stable patients.
        </p>
      </motion.div>
    </section>
  );
}