import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Loader2, AlertCircle } from "lucide-react";

import PatientHeader from "../../components/patientProfile/PatientHeader";
import VitalsOverview from "../../components/patientProfile/VitalsOverview";
import AIRecommendationPanel from "../../components/patientProfile/AIRecommendation";
import ClinicalTimeline from "../../components/patientProfile/ClinicalTimeline";
import EvidencePanel from "../../components/patientProfile/EvidencePanel";
import ExplainabilityPanel from "../../components/patientProfile/ExplainabilityPanel";
import LabResults from "../../components/patientProfile/LabResults";

import { patientService } from "../../services/patientService";
import { useClinicalAI } from "../../context/ClinicalAIContext";

export default function PatientProfile() {
  const { patientId } = useParams();
  const navigate = useNavigate();
  const { setSelectedPatient } = useClinicalAI();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadPatient();
  }, [patientId]);

  async function loadPatient() {
    try {
      setLoading(true);
      setError(null);

      const patient = await patientService.getPatientById(patientId);

      if (!patient) {
        setError("Patient not found.");
        setSelectedPatient(null);
        return;
      }

      setSelectedPatient(patient);
    } catch (err) {
      console.error(err);
      setError("Failed to load patient details.");
      setSelectedPatient(null);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-[400px] items-center justify-center">
        <div className="flex items-center gap-3 text-slate-600">
          <Loader2 className="animate-spin" size={28} />
          <span className="text-lg font-semibold">Loading patient profile...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-[30px] border border-red-200 bg-white p-10 text-center shadow-xl">
        <AlertCircle className="mx-auto text-red-500" size={48} />
        <h2 className="mt-4 text-2xl font-bold">{error}</h2>
        <button
          onClick={() => navigate("/dashboard")}
          className="mt-6 rounded-xl bg-cyan-600 px-6 py-3 font-semibold text-white hover:bg-cyan-700"
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PatientHeader />

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-12 space-y-6 xl:col-span-8">
          <VitalsOverview />
          <ClinicalTimeline />
          <LabResults />
        </div>

        <div className="col-span-12 space-y-6 xl:col-span-4">
          <AIRecommendationPanel />
          <EvidencePanel />
          <ExplainabilityPanel />
        </div>
      </div>
    </div>
  );
}
