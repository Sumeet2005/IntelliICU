import { motion } from "framer-motion";
import {
  BrainCircuit,
  AlertTriangle,
  ShieldCheck,
  Loader2,
  Sparkles,
} from "lucide-react";

import { useClinicalAI } from "../../context/ClinicalAIContext";

export default function AIRecommendationPanel() {
  const { recommendation, loading, analyzePatient, selectedPatient } =
    useClinicalAI();

  async function handleAnalyze() {
  if (!selectedPatient) return;

  const payload = {
    patient: {
      id: selectedPatient.patient?.id,
      name: selectedPatient.patient?.name,
      age: selectedPatient.patient?.age,
      gender: selectedPatient.patient?.gender,
    },

    admission: {
      bed: selectedPatient.admission?.bed,
      diagnosis: selectedPatient.admission?.diagnosis,
    },

    vitals: {
      heart_rate: selectedPatient.vitals?.heart_rate,
      systolic_bp:
        selectedPatient.vitals?.blood_pressure?.systolic,
      diastolic_bp:
        selectedPatient.vitals?.blood_pressure?.diastolic,
      respiratory_rate:
        selectedPatient.vitals?.respiratory_rate,
      spo2: selectedPatient.vitals?.spo2,
      temperature: selectedPatient.vitals?.temperature,
    },

    labs: {
      lactate: parseFloat(selectedPatient.labs?.Lactate),
      wbc: parseFloat(selectedPatient.labs?.WBC),
      creatinine: parseFloat(selectedPatient.labs?.Creatinine),
    },

    prediction: {
      risk_score: selectedPatient.patient?.risk_score,
      risk_level: selectedPatient.patient?.risk_level,
    },
  };

  await analyzePatient(payload);
}

  if (loading) {
    return (
      <div className="rounded-[30px] border border-slate-200 bg-white p-8 shadow-xl">
        <div className="flex items-center gap-3">
          <Loader2 className="animate-spin text-cyan-600" size={30} />
          <div>
            <h2 className="text-2xl font-bold">IntelliAI is analyzing...</h2>
            <p className="text-slate-500">
              Running Prediction • RAG • Clinical Reasoning
            </p>
          </div>
        </div>
        <div className="mt-8 space-y-4">
          <div className="h-6 animate-pulse rounded bg-slate-200" />
          <div className="h-6 animate-pulse rounded bg-slate-200" />
          <div className="h-48 animate-pulse rounded bg-slate-200" />
        </div>
      </div>
    );
  }

  if (!recommendation) {
    return (
      <div className="rounded-[30px] border border-slate-200 bg-white p-10 text-center shadow-xl">
        <BrainCircuit size={70} className="mx-auto text-cyan-600" />
        <h2 className="mt-6 text-3xl font-bold">IntelliAI Clinical Assistant</h2>
        <p className="mt-4 leading-8 text-slate-500">
          Run AI analysis to generate an evidence-based clinical recommendation
          for this patient.
        </p>
        {selectedPatient && (
          <button
            onClick={handleAnalyze}
            className="mt-6 inline-flex items-center gap-2 rounded-xl bg-cyan-600 px-6 py-3 font-semibold text-white hover:bg-cyan-700"
          >
            <BrainCircuit size={18} />
            Analyze Patient
          </button>
        )}
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div className="overflow-hidden rounded-[30px] shadow-xl">
        <div className="bg-gradient-to-r from-slate-900 via-cyan-900 to-blue-900 p-7 text-white">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3">
                <BrainCircuit />
                <span className="font-semibold">IntelliAI Recommendation</span>
              </div>
              <h2 className="mt-5 text-3xl font-black">
                Clinical Decision Support
              </h2>
            </div>
            <Sparkles size={42} className="text-cyan-300" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-5">
        <div className="rounded-3xl border border-red-200 bg-red-50 p-6">
          <AlertTriangle className="text-red-600" />
          <p className="mt-4 text-slate-500">Risk Level</p>
          <h2 className="text-4xl font-black text-red-700">
            {recommendation.summary?.overall_condition}
          </h2>
        </div>
        <div className="rounded-3xl border border-cyan-200 bg-cyan-50 p-6">
          <ShieldCheck className="text-cyan-700" />
          <p className="mt-4 text-slate-500">Risk Score</p>
          <h2 className="text-4xl font-black text-cyan-700">
            {(recommendation.risk_progress?.current_risk * 100).toFixed(0)}%
          </h2>
        </div>
      </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-7 shadow-xl">
        <h2 className="text-2xl font-bold">AI Recommendation</h2>
        <div className="mt-6 whitespace-pre-wrap leading-8 text-slate-700">
          {recommendation.clinical_recommendation}
        </div>
      </div>
    </motion.div>
  );
}
