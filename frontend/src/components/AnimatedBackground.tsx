'use client';

import { useEffect, useRef, useState } from 'react';

export default function AnimatedBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    // Wait for page to load before starting animation
    const timer = setTimeout(() => setIsReady(true), 100);
    
    if (!isReady) return () => clearTimeout(timer);

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Particle system
    class SymmetryParticle {
      x: number;
      y: number;
      baseX: number;
      baseY: number;
      size: number;
      color: string;
      alpha: number;
      angle: number;
      
      constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
        this.baseX = x;
        this.baseY = y;
        this.size = Math.random() * 3.5 + 2;  // Bigger particles! (was 2.5 + 1)
        this.color = this.getColor();
        this.alpha = Math.random() * 0.5 + 0.3;  // More visible (was 0.4 + 0.2)
        this.angle = Math.random() * Math.PI * 2;
      }

      getColor() {
        const colors = [
          'rgba(14, 165, 233, ',
          'rgba(168, 85, 247, ',
          'rgba(59, 130, 246, ',
          'rgba(147, 51, 234, ',
        ];
        return colors[Math.floor(Math.random() * colors.length)];
      }

      update() {
        this.angle += 0.008;
        this.x = this.baseX + Math.sin(this.angle) * 30;  // Bigger movement (was 15)
        this.y = this.baseY + Math.cos(this.angle) * 30;  // Bigger movement (was 15)
        this.alpha = 0.35 + Math.sin(this.angle * 2) * 0.2;  // More alpha variation
      }

      draw() {
        if (!ctx) return;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color + this.alpha + ')';
        ctx.fill();
      }
    }

    // Create 50 particles (reduced from 80)
    const particles: SymmetryParticle[] = [];
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const particleCount = 60;  // Increased from 50

    for (let i = 0; i < particleCount; i++) {
      const angle = (Math.PI * 2 * i) / particleCount;
      const radius = Math.random() * 400 + 150;  // Much bigger spread! (was 180 + 80)
      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;
      particles.push(new SymmetryParticle(x, y));
    }

    let lineAngle = 0;

    function drawSymmetryLines() {
      if (!ctx || !canvas) return;

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const lineCount = 4;

      ctx.strokeStyle = 'rgba(59, 130, 246, 0.20)';  // More visible (was 0.12)
      ctx.lineWidth = 2;  // Thicker lines (was 1.5)

      for (let i = 0; i < lineCount; i++) {
        const angle = (Math.PI * i) / lineCount + lineAngle;
        const length = Math.max(canvas.width, canvas.height);

        ctx.beginPath();
        ctx.moveTo(
          centerX + Math.cos(angle) * length,
          centerY + Math.sin(angle) * length
        );
        ctx.lineTo(
          centerX - Math.cos(angle) * length,
          centerY - Math.sin(angle) * length
        );
        ctx.stroke();
      }

      lineAngle += 0.0008;
    }

    function drawConnections() {
      if (!ctx) return;

      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 180) {  // Longer connections (was 120)
            const opacity = (1 - distance / 180) * 0.25;  // More visible (was 0.15)
            ctx.beginPath();
            ctx.strokeStyle = `rgba(99, 102, 241, ${opacity})`;
            ctx.lineWidth = 1;  // Thicker (was 0.5)
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }
    }

    function drawCenterGlow() {
      if (!ctx || !canvas) return;

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const gradient = ctx.createRadialGradient(
        centerX, centerY, 0,
        centerX, centerY, 400  // Bigger glow (was 250)
      );

      gradient.addColorStop(0, 'rgba(147, 51, 234, 0.12)');  // More visible (was 0.08)
      gradient.addColorStop(0.5, 'rgba(59, 130, 246, 0.06)');  // More visible (was 0.04)
      gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');

      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    let frame = 0;

    function animate() {
      if (!ctx || !canvas) return;

      frame++;

      // Run at 30fps instead of 60fps
      if (frame % 2 === 0) {
        // Fill with white/light gray background first
        ctx.fillStyle = '#f9fafb';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        drawCenterGlow();
        drawSymmetryLines();
        
        particles.forEach(particle => {
          particle.update();
          particle.draw();
        });
        
        drawConnections();
      }

      animationFrameId = requestAnimationFrame(animate);
    }

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationFrameId);
    };
  }, [isReady]);

  return (
    <canvas
      ref={canvasRef}
      className="fixed top-0 left-0 w-full h-full -z-10 pointer-events-none"
      style={{ background: 'linear-gradient(to bottom right, #f9fafb, #f3f4f6)' }}
    />
  );
}