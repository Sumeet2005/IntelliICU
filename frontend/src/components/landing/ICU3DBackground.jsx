import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import icuRealPhoto from "../../assets/icu_environment_bg.jpg";

export default function ICU3DBackground() {
  const mountRef = useRef(null);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const isMobile = window.innerWidth < 768;

    // 1. WebGL Three.js Scene Setup with ACES Filmic Tone Mapping
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x02060d, 0.004);

    const width = container.clientWidth;
    const height = container.clientHeight;
    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 1000);
    camera.position.set(0, 0, 24);

    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: "high-performance",
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    container.appendChild(renderer.domElement);

    const mainGroup = new THREE.Group();
    scene.add(mainGroup);

    // 2. Layer 1: Single Crisp Photographic ICU Backdrop (Z = -12) (No Duplicates / No Ghosting)
    let photoMesh;
    const textureLoader = new THREE.TextureLoader();
    textureLoader.load(icuRealPhoto, (texture) => {
      texture.colorSpace = THREE.SRGBColorSpace;
      const aspect = texture.image.width / texture.image.height;
      const planeGeo = new THREE.PlaneGeometry(42 * aspect, 42);
      const planeMat = new THREE.MeshBasicMaterial({
        map: texture,
        transparent: true,
        opacity: 0.92,
      });
      photoMesh = new THREE.Mesh(planeGeo, planeMat);
      photoMesh.position.set(5, 0, -12);
      mainGroup.add(photoMesh);
    });

    // 3. Clinical Lighting System
    const ambientLight = new THREE.AmbientLight(0x0a1e38, 2.6);
    scene.add(ambientLight);

    // Cyan Volumetric-Style Spotlight behind Bedside Equipment/HUD
    const cyanLight = new THREE.PointLight(0x00d9ff, 3.5, 55);
    cyanLight.position.set(8, 5, 5);
    scene.add(cyanLight);

    // Soft Medical Green Bedside Monitor Glow Light
    const greenLight = new THREE.PointLight(0x18d6a0, 2.4, 35);
    greenLight.position.set(-2, 1, 4);
    scene.add(greenLight);

    // 4. Layer 2: Curved Natural ICU Medical Telemetry Cable (Lower-Right Foreground)
    const cablePoints = [
      new THREE.Vector3(12, -11, 6),
      new THREE.Vector3(10, -9, 4),
      new THREE.Vector3(8, -8, 2),
      new THREE.Vector3(7, -7, 0),
    ];
    const cableCurve = new THREE.CatmullRomCurve3(cablePoints);
    const cableGeo = new THREE.TubeGeometry(cableCurve, 40, 0.05, 8, false);
    const cableMat = new THREE.MeshStandardMaterial({
      color: 0x07192e,
      roughness: 0.5,
      metalness: 0.8,
    });
    const cableMesh = new THREE.Mesh(cableGeo, cableMat);
    mainGroup.add(cableMesh);

    // 5. Layer 3: Telemetry Stream Spline & Moving Data Pulse (Bedside Monitor -> HUD)
    const streamPoints = [
      new THREE.Vector3(-4, 2.5, -2),
      new THREE.Vector3(-1, 3.2, 0),
      new THREE.Vector3(3, 1.5, 3),
      new THREE.Vector3(7, -0.2, 6),
    ];
    const streamCurve = new THREE.CatmullRomCurve3(streamPoints);
    const streamGeo = new THREE.BufferGeometry().setFromPoints(streamCurve.getPoints(160));
    const streamMat = new THREE.LineBasicMaterial({
      color: 0x00d9ff,
      transparent: true,
      opacity: 0.35,
    });
    const streamLine = new THREE.Line(streamGeo, streamMat);
    mainGroup.add(streamLine);

    // Animated 3D Telemetry Data Pulse Sphere
    const packetGeo = new THREE.SphereGeometry(0.16, 16, 16);
    const packetMat = new THREE.MeshBasicMaterial({ color: 0x18d6a0 });
    const packetMesh = new THREE.Mesh(packetGeo, packetMat);
    mainGroup.add(packetMesh);

    // 6. Layer 4: Subtle 3D Clinical Data Particles (10 Floating Nodes)
    const particleCount = 10;
    const particleGeo = new THREE.BufferGeometry();
    const particlePos = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount; i++) {
      particlePos[i * 3] = (Math.random() - 0.2) * 16;
      particlePos[i * 3 + 1] = (Math.random() - 0.5) * 12;
      particlePos[i * 3 + 2] = (Math.random() - 0.2) * 10;
    }
    particleGeo.setAttribute("position", new THREE.BufferAttribute(particlePos, 3));
    const particleMat = new THREE.PointsMaterial({
      color: 0x00d9ff,
      size: 0.2,
      transparent: true,
      opacity: 0.45,
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    mainGroup.add(particles);

    // 7. Bounded Parallax & Animation Loop
    let mouseX = 0;
    let mouseY = 0;
    const handleMouseMove = (e) => {
      mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
      mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
    };
    if (!isMobile && !prefersReducedMotion) {
      window.addEventListener("mousemove", handleMouseMove);
    }

    let animationFrameId;
    let clock = new THREE.Clock();

    const animate = () => {
      const elapsedTime = clock.getElapsedTime();

      if (!prefersReducedMotion) {
        // Multi-Layer Parallax Offset (2-3px Background, 6-8px Telemetry)
        camera.position.x += (mouseX * 1.1 - camera.position.x) * 0.04;
        camera.position.y += (-mouseY * 0.7 - camera.position.y) * 0.04;
        camera.lookAt(scene.position);

        // Animate Telemetry Data Pulse along Stream Curve
        const progress = (elapsedTime * 0.2) % 1;
        const pt = streamCurve.getPointAt(progress);
        packetMesh.position.copy(pt);

        // Slow Floating Movement on Clinical Particles
        particles.rotation.y = elapsedTime * 0.03;

        // Pulse Cyan Spot Light Intensity
        cyanLight.intensity = 3.2 + Math.sin(elapsedTime * 2.0) * 0.5;
      }

      renderer.render(scene, camera);
      animationFrameId = requestAnimationFrame(animate);
    };

    animate();

    // 8. Resize Handler
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener("resize", handleResize);

    // 9. Cleanup & Proper Disposal on Unmount
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationFrameId);

      scene.traverse((obj) => {
        if (obj.geometry) obj.geometry.dispose();
        if (obj.material) {
          if (Array.isArray(obj.material)) obj.material.forEach((m) => m.dispose());
          else obj.material.dispose();
        }
      });

      if (renderer.domElement && renderer.domElement.parentNode) {
        renderer.domElement.parentNode.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  return (
    <div
      ref={mountRef}
      className="fixed inset-0 pointer-events-none z-0 overflow-hidden"
      aria-hidden="true"
    >
      {/* Soft Localized Radial Overlay (No Heavy Black Patch) */}
      <div className="absolute inset-0 bg-gradient-to-r from-[#02060d]/65 via-[#02060d]/25 to-transparent w-full lg:w-[42%]" />
      <div className="absolute inset-0 bg-gradient-to-t from-[#02060d]/50 via-transparent to-[#02060d]/20" />
    </div>
  );
}

