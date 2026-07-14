import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  Activity,
  BrainCircuit,
  BarChart3,
  Settings,
  Shield,
  User,
  TrendingUp,
  Building2,
} from "lucide-react";

import { usePermission } from "../hooks/usePermission";

const menu = [
  { icon: LayoutDashboard, title: "Dashboard", path: "/dashboard", permission: "Dashboard" },
  { icon: Users, title: "Patients", path: "/dashboard", permission: "Patients" },
  { icon: Activity, title: "Live Monitoring", path: "/monitoring", permission: "Patients" },
  { icon: TrendingUp, title: "Telemetry Trends", path: "/telemetry", permission: "Patients" },
  { icon: BrainCircuit, title: "AI Assistant", path: "/dashboard", permission: "ClinicalAI" },
  { icon: Building2, title: "Hospital AI", path: "/hospital-assistant", permission: "ClinicalAI" },
  { icon: BarChart3, title: "Analytics", path: "/analytics", permission: "Analytics" },
  { icon: Shield, title: "User Directory", path: "/users", permission: "UserManagement" },
  { icon: User, title: "My Profile", path: "/profile" },
  { icon: Settings, title: "Settings", path: "/settings", permission: "Settings" },
];

export default function Sidebar() {
  const { hasPermission } = usePermission();
  const visibleMenu = menu.filter(item => !item.permission || hasPermission(item.permission));

  return (
    <aside className="flex w-72 flex-col bg-[#07233F] text-white">
      <div className="border-b border-slate-700 px-8 py-8">
        <h1 className="text-3xl font-bold">IntelliICU</h1>
        <p className="mt-1 text-slate-400">Clinical Suite</p>
      </div>

      <nav className="mt-8 flex-1">
        {visibleMenu.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.title}
              to={item.path}
              end={item.path === "/dashboard"}
              className={({ isActive }) =>
                `mx-4 mb-2 flex cursor-pointer items-center gap-4 rounded-xl px-5 py-4 transition ${
                  isActive ? "bg-cyan-700" : "hover:bg-slate-700"
                }`
              }
            >
              <Icon size={22} />
              <span>{item.title}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="border-t border-slate-700 p-6">
        <div className="rounded-xl bg-slate-800 p-4">
          <p className="text-sm">IntelliICU Enterprise</p>
          <p className="text-xs text-slate-400">AI Clinical Decision Support</p>
        </div>
      </div>
    </aside>
  );
}
