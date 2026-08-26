import { useState } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { Shield, Lock, User, AlertCircle, Activity, ArrowLeft } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import ICU3DBackground from "../components/landing/ICU3DBackground";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const redirectPath = location.state?.from?.pathname || "/dashboard";

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setError("Please fill out all credentials.");
      return;
    }

    try {
      setError("");
      setLoading(true);
      await login(username, password);
      navigate(redirectPath, { replace: true });
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail || "Authentication failed. Please verify credentials."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full bg-[#070b14] text-slate-100 font-sans relative overflow-x-hidden flex flex-col justify-between">
      <ICU3DBackground />

      <div className="fixed inset-0 bg-[linear-gradient(to_right,#1e293b15_1px,transparent_1px),linear-gradient(to_bottom,#1e293b15_1px,transparent_1px)] bg-[size:4rem_4rem] pointer-events-none z-0" />

      <div className="fixed top-[-10%] left-[-10%] h-[500px] w-[500px] rounded-full bg-cyan-500/10 blur-[160px] pointer-events-none z-0" />
      <div className="fixed bottom-[-10%] right-[-10%] h-[500px] w-[500px] rounded-full bg-blue-600/10 blur-[160px] pointer-events-none z-0" />

      <header className="w-full border-b border-slate-800/80 bg-[#070b14]/85 backdrop-blur-md sticky top-0 z-50 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3 group">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 shadow-md shadow-cyan-500/20 group-hover:scale-105 transition">
              <Activity className="text-white" size={18} />
            </div>
            <div>
              <span className="text-sm font-black tracking-wider uppercase text-white block">
                IntelliICU
              </span>
              <span className="text-[9px] font-bold text-cyan-400 tracking-widest uppercase block">
                Clinical AI Platform
              </span>
            </div>
          </Link>

          <Link
            to="/"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-cyan-400 transition"
          >
            <ArrowLeft size={14} /> Back to Landing
          </Link>
        </div>
      </header>

      <main className="max-w-7xl w-full mx-auto px-4 sm:px-6 py-8 sm:py-12 relative z-10 flex-1 flex items-center justify-center">
        <div className="grid w-full grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
          
          <div className="lg:col-span-7 space-y-6">
            <div className="space-y-3">
              <div className="inline-flex items-center gap-2 rounded-full border border-cyan-500/30 bg-cyan-950/30 px-3.5 py-1">
                <Shield size={12} className="text-cyan-400" />
                <span className="font-mono text-[9px] font-bold text-cyan-400 uppercase tracking-widest">
                  SECURE PORTAL AUTHENTICATION
                </span>
              </div>

              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black leading-tight text-white tracking-tight">
                IntelliICU Clinical <br className="hidden sm:inline" />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-blue-500">
                  Command Center Portal
                </span>
              </h1>

              <p className="text-xs sm:text-sm text-slate-400 leading-relaxed max-w-lg">
                Enter your authorized clinical credentials to access real-time patient telemetry, AI sepsis risk intelligence, and ward surveillance.
              </p>
            </div>

            <div className="grid grid-cols-3 gap-3 font-mono text-xs max-w-lg">
              <div className="bg-slate-900/60 border border-slate-800 p-3 rounded-xl backdrop-blur-md">
                <span className="text-[9px] text-slate-500 block uppercase">CLINICAL AI</span>
                <span className="text-[11px] font-bold text-emerald-400 flex items-center gap-1.5 mt-0.5">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  ONLINE
                </span>
              </div>
              <div className="bg-slate-900/60 border border-slate-800 p-3 rounded-xl backdrop-blur-md">
                <span className="text-[9px] text-slate-500 block uppercase">TELEMETRY</span>
                <span className="text-[11px] font-bold text-cyan-400 flex items-center gap-1.5 mt-0.5">
                  <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-pulse"></span>
                  CONNECTED
                </span>
              </div>
              <div className="bg-slate-900/60 border border-slate-800 p-3 rounded-xl backdrop-blur-md">
                <span className="text-[9px] text-slate-500 block uppercase">ALERT ENGINE</span>
                <span className="text-[11px] font-bold text-teal-400 flex items-center gap-1.5 mt-0.5">
                  <span className="h-1.5 w-1.5 rounded-full bg-teal-400 animate-pulse"></span>
                  ACTIVE
                </span>
              </div>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-xl max-w-lg space-y-3">
              <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                <span className="text-[10px] font-mono font-extrabold uppercase text-slate-400 tracking-wider">
                  SANDBOX CLEARANCE LOGINS
                </span>
                <span className="text-[9px] font-mono text-cyan-400 bg-cyan-950/60 border border-cyan-800/40 px-2 py-0.5 rounded">
                  DEMO ACCOUNTS
                </span>
              </div>
              <div className="space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-slate-300">Administrator</span>
                  <span className="font-mono text-cyan-400 bg-slate-950/80 px-2.5 py-1 rounded border border-slate-800 text-[11px]">
                    admin / admin123
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-slate-300">Intensivist / MD</span>
                  <span className="font-mono text-cyan-400 bg-slate-950/80 px-2.5 py-1 rounded border border-slate-800 text-[11px]">
                    reyes / intensivist123
                  </span>
                </div>
              </div>
            </div>

          </div>

          <div className="lg:col-span-5 w-full flex justify-center">
            <div className="w-full max-w-[420px] rounded-3xl border border-slate-800 bg-slate-900/90 p-6 sm:p-8 backdrop-blur-2xl shadow-2xl space-y-6">
              
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <Shield className="text-cyan-400" size={18} />
                  <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
                    Secure Authentication
                  </h2>
                </div>
                <p className="text-xs text-slate-400 font-medium">
                  Enter your credentials below to access the command center
                </p>
              </div>

              {error && (
                <div className="flex items-start gap-2.5 rounded-xl border border-red-950 bg-red-950/40 p-3.5 text-xs text-red-400 font-semibold">
                  <AlertCircle size={16} className="shrink-0 mt-0.5" />
                  <span>{error}</span>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-[10px] font-mono font-bold uppercase text-slate-400 tracking-wider block">
                    Username or Email
                  </label>
                  <div className="relative">
                    <User size={16} className="absolute left-3.5 top-3.5 text-slate-400" />
                    <input
                      type="text"
                      required
                      disabled={loading}
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      placeholder="Enter username"
                      className="w-full rounded-xl border border-slate-800 bg-slate-950/80 py-3 pl-10 pr-4 text-xs outline-none transition focus:border-cyan-500 focus:bg-slate-950 text-slate-100 font-medium disabled:opacity-50"
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-[10px] font-mono font-bold uppercase text-slate-400 tracking-wider block">
                    Passcode
                  </label>
                  <div className="relative">
                    <Lock size={16} className="absolute left-3.5 top-3.5 text-slate-400" />
                    <input
                      type="password"
                      required
                      disabled={loading}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••••••"
                      className="w-full rounded-xl border border-slate-800 bg-slate-950/80 py-3 pl-10 pr-4 text-xs outline-none transition focus:border-cyan-500 focus:bg-slate-950 text-slate-100 font-medium disabled:opacity-50"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-extrabold py-3.5 text-xs transition duration-300 hover:shadow-lg hover:shadow-cyan-500/25 active:scale-[0.98] disabled:opacity-50 cursor-pointer"
                >
                  {loading ? (
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                  ) : (
                    <>
                      <Shield size={14} />
                      Enter Command Center
                    </>
                  )}
                </button>
              </form>

              <div className="text-[10px] font-mono text-slate-500 text-center border-t border-slate-800/60 pt-4">
                Encrypted Session • Audit Logging Active
              </div>

            </div>
          </div>

        </div>
      </main>

      <footer className="w-full border-t border-slate-800/80 bg-slate-950/80 py-6 px-6 relative z-10">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-2 text-xs text-slate-500">
          <p>© 2026 IntelliICU. Clinical Decision Support System.</p>
          <p className="font-mono text-[10px]">VER 2.0.0 • PRODUCTION READY</p>
        </div>
      </footer>
    </div>
  );
}

