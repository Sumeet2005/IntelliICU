import { BarChart3 } from "lucide-react";

import LiveAnalytics from "../../components/dashboardV2/LiveAnalytics";
import HospitalAnalytics from "../../components/dashboardV2/HospitalAnalytics";
import KPISection from "../../components/dashboardV2/KPISection";

export default function Analytics() {
  return (
    <div className="space-y-8">
      <div className="rounded-[32px] border border-slate-200 bg-white p-8 shadow-xl">
        <div className="flex items-center gap-4">
          <div className="rounded-2xl bg-cyan-50 p-4">
            <BarChart3 className="text-cyan-600" size={32} />
          </div>
          <div>
            <h1 className="text-4xl font-black">Hospital Analytics</h1>
            <p className="mt-2 text-slate-500">
              ICU occupancy, outcomes, and AI-assisted clinical metrics
            </p>
          </div>
        </div>
      </div>

      <KPISection />

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-12 xl:col-span-8">
          <LiveAnalytics />
        </div>
        <div className="col-span-12 xl:col-span-4">
          <HospitalAnalytics />
        </div>
      </div>
    </div>
  );
}
