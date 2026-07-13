import { Activity, Radio } from "lucide-react";

import LiveAnalytics from "../../components/dashboardV2/LiveAnalytics";
import AlertsSection from "../../components/dashboardV2/AlertsSection";
import VitalsOverview from "../../components/patientProfile/VitalsOverview";

export default function Monitoring() {
  return (
    <div className="space-y-8">
      <div className="rounded-[32px] bg-gradient-to-r from-slate-900 via-cyan-900 to-blue-900 p-8 text-white shadow-xl">
        <div className="flex items-center gap-4">
          <div className="rounded-2xl bg-white/10 p-4">
            <Radio size={32} />
          </div>
          <div>
            <h1 className="text-4xl font-black">Live Monitoring</h1>
            <p className="mt-2 text-cyan-100">
              Real-time ICU vitals, alerts, and streaming analytics
            </p>
          </div>
          <div className="ml-auto flex items-center gap-2 rounded-full bg-emerald-500/20 px-4 py-2">
            <Activity className="text-emerald-300" size={18} />
            <span className="font-semibold text-emerald-200">Stream Ready</span>
          </div>
        </div>
      </div>

      <VitalsOverview />

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-12 xl:col-span-8">
          <LiveAnalytics />
        </div>
        <div className="col-span-12 xl:col-span-4">
          <AlertsSection />
        </div>
      </div>
    </div>
  );
}
