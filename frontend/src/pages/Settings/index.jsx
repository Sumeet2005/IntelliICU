import { Bell, Database, Shield, Settings as SettingsIcon } from "lucide-react";

const settingsSections = [
  {
    icon: Bell,
    title: "Alert Preferences",
    description: "Configure critical alert thresholds and notification channels.",
  },
  {
    icon: Database,
    title: "Knowledge Base",
    description: "Manage RAG document sources and clinical guideline indexing.",
  },
  {
    icon: Shield,
    title: "Security & Compliance",
    description: "HIPAA audit logs, role-based access, and session policies.",
  },
];

export default function Settings() {
  return (
    <div className="space-y-8">
      <div className="clinical-card p-6">
        <div className="flex items-center gap-4">
          <div className="rounded-xl bg-slate-100 p-3">
            <SettingsIcon className="text-slate-700" size={24} />
          </div>
          <div>
            <h1 className="text-2xl font-black text-slate-800">Settings</h1>
            <p className="mt-1 text-xs text-slate-500">
              Configure IntelliICU enterprise preferences
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        {settingsSections.map((section) => {
          const Icon = section.icon;

          return (
            <div
              key={section.title}
              className="clinical-card p-6 flex flex-col justify-between"
            >
              <div>
                <Icon className="text-cyan-600" size={24} />
                <h2 className="mt-4 text-lg font-bold text-slate-800">{section.title}</h2>
                <p className="mt-2 text-xs leading-relaxed text-slate-500">
                  {section.description}
                </p>
              </div>
              <button className="mt-6 rounded-xl bg-slate-900 px-5 py-3.5 text-xs font-bold text-white hover:bg-slate-800 transition">
                Configure
              </button>
            </div>
          );
        })}
      </div>

      <div className="clinical-card p-6">
        <h2 className="text-lg font-bold text-slate-800">System Information</h2>
        <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2 text-xs font-semibold text-slate-500">
          <div className="rounded-xl bg-slate-50/50 border border-slate-100 p-4">
            <p className="text-[10px] text-slate-400 font-extrabold uppercase tracking-wider">API Endpoint</p>
            <p className="mt-1.5 font-bold text-slate-850">http://localhost:8000/api</p>
          </div>
          <div className="rounded-xl bg-slate-50/50 border border-slate-100 p-4">
            <p className="text-[10px] text-slate-400 font-extrabold uppercase tracking-wider">WebSocket (Prepared)</p>
            <p className="mt-1.5 font-bold text-slate-850">ws://localhost:8000/ws/vitals</p>
          </div>
        </div>
      </div>
    </div>
  );
}
