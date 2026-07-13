import { motion } from "framer-motion";
import {
  Pill,
  FlaskConical,
  AlertTriangle,
  Stethoscope,
  ClipboardCheck,
  Clock3,
} from "lucide-react";

import { useClinicalAI } from "../../context/ClinicalAIContext";

export default function ClinicalTimeline() {
  const { selectedPatient } = useClinicalAI();
  const timelineData = selectedPatient?.timeline || [];

  const getEventConfig = (type) => {
    const t = type?.toLowerCase() || "";
    if (t.includes("admission")) {
      return { title: type || "Admission", icon: ClipboardCheck, color: "bg-emerald-500" };
    }
    if (t.includes("medication")) {
      return { title: type || "Medication", icon: Pill, color: "bg-blue-500" };
    }
    if (t.includes("lab") || t.includes("laboratory")) {
      return { title: type || "Laboratory", icon: FlaskConical, color: "bg-orange-500" };
    }
    if (t.includes("alert")) {
      return { title: type || "Alert", icon: AlertTriangle, color: "bg-red-500" };
    }
    return { title: type || "Assessment", icon: Stethoscope, color: "bg-cyan-600" };
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="rounded-[30px] bg-white border border-slate-200 shadow-xl p-7"
    >
      <div className="flex items-center justify-between">

        <div>

          <h2 className="text-3xl font-black">

            Clinical Timeline

          </h2>

          <p className="mt-2 text-slate-500">

            Latest ICU Events

          </p>

        </div>

        <Clock3
          size={28}
          className="text-cyan-600"
        />

      </div>

      <div className="mt-8">

        {timelineData.length > 0 ? (
          timelineData.map((event, index) => {
            const config = getEventConfig(event.type);
            const Icon = config.icon;

            return (
              <motion.div
                key={event.id ?? index}
                whileHover={{ x: 5 }}
                className="flex gap-5 pb-8 last:pb-0"
              >

                <div className="flex flex-col items-center">

                  <div
                    className={`flex h-14 w-14 items-center justify-center rounded-2xl ${config.color}`}
                  >

                    <Icon
                      className="text-white"
                      size={24}
                    />

                  </div>

                  {index !== timelineData.length - 1 && (
                    <div className="mt-2 h-full w-1 rounded-full bg-slate-200"></div>
                  )}

                </div>

                <div className="flex-1 rounded-2xl border border-slate-200 bg-slate-50 p-5">

                  <div className="flex items-center justify-between">

                    <h3 className="text-xl font-bold">

                      {config.title}

                    </h3>

                    <span className="rounded-full bg-white px-3 py-1 text-sm font-semibold">

                      {event.time}

                    </span>

                  </div>

                  <p className="mt-3 leading-7 text-slate-600">

                    {event.description}

                  </p>

                </div>

              </motion.div>
            );
          })
        ) : (
          <p className="text-center text-slate-500 py-6">
            No timeline events recorded.
          </p>
        )}

      </div>

    </motion.div>
  );
}