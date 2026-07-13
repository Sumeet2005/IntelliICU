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
      <div className="rounded-[32px] border border-slate-200 bg-white p-8 shadow-xl">
        <div className="flex items-center gap-4">
          <div className="rounded-2xl bg-slate-100 p-4">
            <SettingsIcon className="text-slate-700" size={32} />
          </div>
          <div>
            <h1 className="text-4xl font-black">Settings</h1>
            <p className="mt-2 text-slate-500">
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
              className="rounded-[28px] border border-slate-200 bg-white p-8 shadow-lg"
            >
              <Icon className="text-cyan-600" size={28} />
              <h2 className="mt-5 text-2xl font-bold">{section.title}</h2>
              <p className="mt-3 leading-7 text-slate-500">
                {section.description}
              </p>
              <button className="mt-6 rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800">
                Configure
              </button>
            </div>
          );
        })}
      </div>

      <div className="rounded-[28px] border border-slate-200 bg-white p-8 shadow-lg">
        <h2 className="text-2xl font-bold">System Information</h2>
        <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2">
          <div className="rounded-2xl bg-slate-50 p-5">
            <p className="text-sm text-slate-500">API Endpoint</p>
            <p className="mt-1 font-semibold">http://localhost:8000/api</p>
          </div>
          <div className="rounded-2xl bg-slate-50 p-5">
            <p className="text-sm text-slate-500">WebSocket (Prepared)</p>
            <p className="mt-1 font-semibold">ws://localhost:8000/ws/vitals</p>
          </div>
        </div>
      </div>
    </div>
  );
}
