import HeroBanner from "../../components/dashboardV2/HeroBanner";
import KPISection from "../../components/dashboardV2/KPISection";
import LiveAnalytics from "../../components/dashboardV2/LiveAnalytics";
import PatientsSection from "../../components/dashboardV2/PatientsSection";
import AIRecommendation from "../../components/dashboardV2/AIRecommendation";
import ActivityFeed from "../../components/dashboardV2/ActivityFeed";
import HospitalAnalytics from "../../components/dashboardV2/HospitalAnalytics";
import FloatingAI from "../../components/dashboardV2/FloatingAI";
import LiveAlerts from "../../components/dashboardV2/LiveAlerts";

export default function DashboardV2() {
  return (
    <>
      <div className="space-y-8">
        {/* Hero Banner */}
        <HeroBanner />

        {/* KPI Cards */}
        <KPISection />

        {/* Analytics */}
        <div className="grid grid-cols-12 gap-6">
          <div className="col-span-12 xl:col-span-8">
            <LiveAnalytics />
          </div>

          <div className="col-span-12 xl:col-span-4">
            <HospitalAnalytics />
          </div>
        </div>

        {/* Patients + AI Recommendation */}
        <div className="grid grid-cols-12 gap-6">
          <div className="col-span-12 xl:col-span-8">
            <PatientsSection />
          </div>

          <div className="col-span-12 xl:col-span-4">
            <AIRecommendation />
          </div>
        </div>

        {/* Live Alerts + Activity Feed */}
        <div className="grid grid-cols-12 gap-6">
          <div className="col-span-12 xl:col-span-7">
            <LiveAlerts />
          </div>

          <div className="col-span-12 xl:col-span-5">
            <ActivityFeed />
          </div>
        </div>
      </div>

      {/* Floating AI Assistant */}
      <FloatingAI />
    </>
  );
}