import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  BrainCircuit,
  Send,
  Sparkles,
  X,
  Bot,
  User,
} from "lucide-react";

export default function FloatingAI() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");

  const messages = [
    {
      role: "assistant",
      text: "Hello Doctor 👋 I'm IntelliAI. How can I assist you today?",
    },
    {
      role: "assistant",
      text: "3 patients require immediate attention based on the latest predictions.",
    },
  ];

  const suggestions = [
    "Show critical patients",
    "Why is Amelia Chen high risk?",
    "Explain Sepsis prediction",
    "Generate clinical summary",
  ];

  return (
    <>
      {/* Floating Button */}

      <motion.button
        whileHover={{ scale: 1.08 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setOpen(true)}
        className="fixed bottom-8 right-8 z-50 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-cyan-500 to-blue-700 text-white shadow-2xl"
      >
        <BrainCircuit size={30} />
      </motion.button>

      {/* Chat Window */}

      <AnimatePresence>

        {open && (

          <motion.div
            initial={{ opacity: 0, y: 40, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 40 }}
            className="fixed bottom-28 right-8 z-50 w-[420px] overflow-hidden rounded-[28px] border border-slate-200 bg-white shadow-2xl"
          >

            {/* Header */}

            <div className="bg-gradient-to-r from-slate-900 via-cyan-900 to-blue-900 p-5 text-white">

              <div className="flex items-center justify-between">

                <div className="flex items-center gap-3">

                  <BrainCircuit />

                  <div>

                    <h2 className="font-bold">

                      IntelliAI Assistant

                    </h2>

                    <p className="text-sm text-cyan-200">

                      Clinical Decision Support

                    </p>

                  </div>

                </div>

                <button onClick={() => setOpen(false)}>

                  <X />

                </button>

              </div>

            </div>

            {/* Messages */}

            <div className="h-[360px] space-y-5 overflow-y-auto bg-slate-50 p-5">

              {messages.map((msg, index) => (

                <div
                  key={index}
                  className={`flex gap-3 ${
                    msg.role === "assistant"
                      ? ""
                      : "justify-end"
                  }`}
                >

                  {msg.role === "assistant" && (
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-cyan-500 text-white">

                      <Bot size={18} />

                    </div>
                  )}

                  <div
                    className={`max-w-[270px] rounded-2xl p-4 ${
                      msg.role === "assistant"
                        ? "bg-white shadow"
                        : "bg-cyan-600 text-white"
                    }`}
                  >
                    {msg.text}
                  </div>

                  {msg.role === "user" && (
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-800 text-white">

                      <User size={18} />

                    </div>
                  )}

                </div>

              ))}

              {/* Suggestions */}

              <div>

                <p className="mb-3 text-sm text-slate-500">

                  Suggested Questions

                </p>

                <div className="flex flex-wrap gap-2">

                  {suggestions.map((item) => (

                    <button
                      key={item}
                      className="rounded-full border border-cyan-200 bg-cyan-50 px-3 py-2 text-sm hover:bg-cyan-100"
                    >
                      {item}
                    </button>

                  ))}

                </div>

              </div>

            </div>

            {/* Input */}

            <div className="border-t bg-white p-4">

              <div className="flex items-center gap-3">

                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask IntelliAI..."
                  className="flex-1 rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-cyan-500"
                />

                <button className="rounded-xl bg-cyan-600 p-3 text-white hover:bg-cyan-700">

                  <Send size={18} />

                </button>

              </div>

              <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">

                <Sparkles size={14} />

                Powered by Qwen 2.5 + RAG + Clinical Knowledge Base

              </div>

            </div>

          </motion.div>

        )}

      </AnimatePresence>
    </>
  );
}