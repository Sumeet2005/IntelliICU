import { motion } from "framer-motion";
import {
  BrainCircuit,
  AlertTriangle,
  ShieldCheck,
  BookOpen,
  Loader2,
  Sparkles,
} from "lucide-react";

import { useClinicalAI } from "../../context/ClinicalAIContext";

export default function AIRecommendation() {
  const { recommendation, loading } = useClinicalAI();

  if (loading) {
    return (
      <div className="rounded-[30px] bg-white border border-slate-200 shadow-xl p-8">

        <div className="flex items-center gap-3">

          <Loader2
            className="animate-spin text-cyan-600"
            size={30}
          />

          <div>

            <h2 className="text-2xl font-bold">

              IntelliAI is analyzing...

            </h2>

            <p className="text-slate-500">

              Running Prediction • RAG • Clinical Reasoning

            </p>

          </div>

        </div>

        <div className="mt-8 space-y-4">

          <div className="h-6 rounded bg-slate-200 animate-pulse"></div>
          <div className="h-6 rounded bg-slate-200 animate-pulse"></div>
          <div className="h-6 rounded bg-slate-200 animate-pulse"></div>
          <div className="h-48 rounded bg-slate-200 animate-pulse"></div>

        </div>

      </div>
    );
  }

  if (!recommendation) {
    return (
      <div className="rounded-[30px] bg-white border border-slate-200 shadow-xl p-10 text-center">

        <BrainCircuit
          size={70}
          className="mx-auto text-cyan-600"
        />

        <h2 className="mt-6 text-3xl font-bold">

          IntelliAI Clinical Assistant

        </h2>

        <p className="mt-4 text-slate-500 leading-8">

          Select a patient from the patient table and click
          <strong> Analyze </strong>
          to generate an evidence-based clinical recommendation.

        </p>

      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >

      {/* Header */}

      <div className="rounded-[30px] overflow-hidden shadow-xl">

        <div className="bg-gradient-to-r from-slate-900 via-cyan-900 to-blue-900 p-7 text-white">

          <div className="flex items-center justify-between">

            <div>

              <div className="flex items-center gap-3">

                <BrainCircuit />

                <span className="font-semibold">

                  IntelliAI Recommendation

                </span>

              </div>

              <h2 className="mt-5 text-3xl font-black">

                Clinical Decision Support

              </h2>

            </div>

            <Sparkles
              size={42}
              className="text-cyan-300"
            />

          </div>

        </div>

      </div>

      {/* Risk */}

      <div className="grid grid-cols-2 gap-5">

        <div className="rounded-3xl bg-red-50 border border-red-200 p-6">

          <AlertTriangle className="text-red-600" />

          <p className="mt-4 text-slate-500">

            Risk Level

          </p>

          <h2 className="text-4xl font-black text-red-700">

            {recommendation.summary?.overall_condition}

          </h2>

        </div>

        <div className="rounded-3xl bg-cyan-50 border border-cyan-200 p-6">

          <ShieldCheck className="text-cyan-700" />

          <p className="mt-4 text-slate-500">

            Risk Score

          </p>

          <h2 className="text-4xl font-black text-cyan-700">

            {recommendation.summary?.confidence ? `${(recommendation.summary.confidence * 100).toFixed(0)}%` : "-"}

          </h2>

        </div>

      </div>

      {/* Recommendation */}

      <div className="rounded-3xl bg-white border border-slate-200 shadow-xl p-7">

        <h2 className="text-2xl font-bold">

          AI Recommendation

        </h2>

        <div className="mt-6 whitespace-pre-wrap leading-8 text-slate-700">

          {recommendation.summary?.clinical_reasoning}

        </div>

      </div>

      {/* Sources */}

      <div className="rounded-3xl bg-white border border-slate-200 shadow-xl p-7">

        <div className="flex items-center gap-3">

          <BookOpen className="text-cyan-600" />

          <h2 className="text-2xl font-bold">

            Evidence Sources

          </h2>

        </div>

        <div className="mt-6 space-y-4">

          {recommendation.recommendations?.map((rec, index) => (

            <motion.div
              key={index}
              whileHover={{ y: -3 }}
              className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
            >

              <h3 className="font-bold">

                {rec.title}

              </h3>

              <p className="mt-2 text-slate-600">

                {rec.description}

              </p>

              <div className="mt-3 flex flex-wrap gap-2">

                <span className="rounded-full bg-cyan-100 px-3 py-1 text-sm text-cyan-700">

                  {rec.priority}

                </span>

              </div>

            </motion.div>

          ))}

        </div>

      </div>

    </motion.div>
  );
}