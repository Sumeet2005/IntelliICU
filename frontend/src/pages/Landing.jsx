import { useState } from "react";
import LandingHeader from "../components/landing/LandingHeader";
import ICU3DBackground from "../components/landing/ICU3DBackground";
import HeroContent from "../components/landing/HeroContent";
import TelemetryHUD from "../components/landing/TelemetryHUD";
import FeatureGrid from "../components/landing/FeatureGrid";
import ClinicalPipeline from "../components/landing/ClinicalPipeline";
import RoleIntelligence from "../components/landing/RoleIntelligence";
import LandingFooter from "../components/landing/LandingFooter";

export default function Landing() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const scrollToSection = (id) => {
    setMobileMenuOpen(false);
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="w-full bg-[#02060d] text-slate-100 font-sans relative overflow-x-hidden min-h-screen flex flex-col justify-between">
      
      {/* 1. Multi-Layer Depth Parallax ICU Backdrop Layer */}
      <ICU3DBackground />

      {/* 2. Top Navigation Bar */}
      <LandingHeader
        mobileMenuOpen={mobileMenuOpen}
        setMobileMenuOpen={setMobileMenuOpen}
        scrollToSection={scrollToSection}
      />

      {/* 3. Main Hero & Content Sections */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 py-6 lg:py-10 space-y-12 lg:space-y-16 flex-1">
        
        {/* Main Hero Section (42% Left Messaging / 58% Right 4-Panel Clinical HUD & Real ICU Scene) */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-8 items-center min-h-[calc(100vh-140px)]">
          <div className="lg:col-span-5">
            <HeroContent scrollToSection={scrollToSection} />
          </div>
          <div className="lg:col-span-7">
            <TelemetryHUD />
          </div>
        </section>

        {/* 6 Core Capabilities Strip */}
        <FeatureGrid />

        {/* End-to-End Decision Pipeline */}
        <ClinicalPipeline />

        {/* Role-Aware Workflows & Explainable AI */}
        <RoleIntelligence />

      </main>

      {/* 4. Footer */}
      <LandingFooter />

    </div>
  );
}

