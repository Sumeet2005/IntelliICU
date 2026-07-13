import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { alertService } from "../../services/alertService";
import {
  X,
  HeartPulse,
  Thermometer,
  Droplets,
  Activity,
  BrainCircuit,
  BedDouble,
  User,
} from "lucide-react";

export default function AlertDrawer({
  open,
  alert,
  patient,
  onClose,
}) {
  const [loading, setLoading] = useState(false);

  async function handleAcknowledge() {
    if (!alert) return;

    setLoading(true);

    try {
      await alertService.acknowledge(alert.id);

      window.alert("Alert acknowledged successfully.");

      onClose();
    } catch (error) {
      console.error(error);

      window.alert("Failed to acknowledge alert.");
    } finally {
      setLoading(false);
    }
  }

  async function handleResolve() {
    if (!alert) return;

    setLoading(true);

    try {
      await alertService.resolve(alert.id);

      window.alert("Alert resolved successfully.");

      onClose();
    } catch (error) {
      console.error(error);

      window.alert("Failed to resolve alert.");
    } finally {
      setLoading(false);
    }
  }

  async function handleEscalate() {
    if (!alert) return;

    setLoading(true);

    try {
      await alertService.escalate(alert.id);

      window.alert("Alert escalated successfully.");

      onClose();
    } catch (error) {
      console.error(error);

      window.alert("Failed to escalate alert.");
    } finally {
      setLoading(false);
    }
  }
  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Backdrop */}

          <motion.div
            className="fixed inset-0 z-40 bg-black/40"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Drawer */}

          <motion.div
            initial={{ x: 500 }}
            animate={{ x: 0 }}
            exit={{ x: 500 }}
            transition={{ duration: 0.3 }}
            className="fixed right-0 top-0 z-50 h-screen w-[480px] overflow-y-auto border-l bg-white shadow-2xl"
          >
            {/* Header */}

            <div className="flex items-center justify-between border-b p-6">

              <div>

                <h2 className="text-2xl font-bold">

                  Clinical Alert

                </h2>

                <p className="text-slate-500">

                  AI Clinical Details

                </p>

              </div>

              <button
                onClick={onClose}
                className="rounded-xl p-2 hover:bg-slate-100"
              >
                <X />
              </button>

            </div>

            {/* Patient */}

            <div className="space-y-6 p-6">

              <div className="rounded-2xl bg-cyan-50 p-5">

                <div className="flex items-center gap-3">

                  <User className="text-cyan-600" />

                  <div>

                    <h3 className="text-xl font-bold">

                      {patient?.name}

                    </h3>

                    <p className="text-slate-500">

                      {patient?.id}

                    </p>

                  </div>

                </div>

              </div>

              {/* Alert */}

              <div className="rounded-2xl border p-5">

                <h3 className="font-bold">

                  Current Alert

                </h3>

                <p className="mt-3 text-lg">

                  {alert?.title}

                </p>

                <p className="mt-2 text-slate-600">

                  {alert?.message}

                </p>

              </div>

              {/* Bed */}

              <div className="grid grid-cols-2 gap-4">

                <div className="rounded-xl border p-4">

                  <BedDouble className="mb-2 text-cyan-600" />

                  <p className="text-sm text-slate-500">

                    ICU Bed

                  </p>

                  <h3 className="text-xl font-bold">

                    {patient?.bed}

                  </h3>

                </div>

                <div className="rounded-xl border p-4">

                  <BrainCircuit className="mb-2 text-violet-600" />

                  <p className="text-sm text-slate-500">

                    AI Risk

                  </p>

                  <h3 className="text-xl font-bold">

                    {(patient?.risk_score * 100).toFixed(0)}%

                  </h3>

                </div>

              </div>

              {/* Vitals */}

              <div>

                <h3 className="mb-4 text-xl font-bold">

                  Live Vitals

                </h3>

                <div className="grid grid-cols-2 gap-4">

                  <VitalCard
                    icon={<HeartPulse />}
                    label="Heart Rate"
                    value={`${patient?.heart_rate} BPM`}
                  />

                  <VitalCard
                    icon={<Activity />}
                    label="Blood Pressure"
                    value={`${patient?.systolic_bp}/${patient?.diastolic_bp}`}
                  />

                  <VitalCard
                    icon={<Droplets />}
                    label="SpO₂"
                    value={`${patient?.spo2}%`}
                  />

                  <VitalCard
                    icon={<Thermometer />}
                    label="Temperature"
                    value={`${patient?.temperature} °C`}
                  />

                </div>

              </div>

              {/* AI Recommendation */}

              <div className="rounded-2xl bg-violet-50 p-5">

                <h3 className="font-bold">

                  AI Recommendation

                </h3>

                <ul className="mt-4 list-disc space-y-2 pl-5 text-slate-700">

                  <li>Start Sepsis Protocol</li>

                  <li>Repeat Lactate Test</li>

                  <li>Obtain Blood Cultures</li>

                  <li>Notify ICU Physician</li>

                </ul>

              </div>

                            {/* Footer */}

              <div className="flex flex-col gap-3">

                <button
                  onClick={handleAcknowledge}
                  disabled={loading}
                  className="rounded-xl bg-cyan-600 py-3 font-semibold text-white hover:bg-cyan-700 disabled:opacity-50"
                >
                  {loading ? "Processing..." : "✓ Acknowledge"}
                </button>

                <button
                  onClick={handleEscalate}
                  disabled={loading}
                  className="rounded-xl bg-red-600 py-3 font-semibold text-white hover:bg-red-700 disabled:opacity-50"
                >
                  {loading ? "Processing..." : "🚨 Escalate"}
                </button>

                <button
                  onClick={handleResolve}
                  disabled={loading}
                  className="rounded-xl bg-emerald-600 py-3 font-semibold text-white hover:bg-emerald-700 disabled:opacity-50"
                >
                  {loading ? "Processing..." : "✔ Resolve"}
                </button>

              </div>

            
            </div>

          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

function VitalCard({
  icon,
  label,
  value,
}) {
  return (
    <div className="rounded-xl border p-4">
      <div className="mb-3 text-cyan-600">
        {icon}
      </div>

      <p className="text-sm text-slate-500">
        {label}
      </p>

      <h3 className="text-xl font-bold">
        {value}
      </h3>
    </div>
  );
}