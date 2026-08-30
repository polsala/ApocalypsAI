import React, { useRef, useEffect, useCallback } from 'react';

const TemporalBloomCanvas = ({ frequency, intensity, decay }) => {
  const canvasRef = useRef(null);
  const animationFrameId = useRef(null);
  const particles = useRef([]);

  const initParticles = useCallback((width, height) => {
    particles.current = [];
    for (let i = 0; i < 100; i++) { // Number of initial particles
      particles.current.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 2, // Initial velocity
        vy: (Math.random() - 0.5) * 2,
        life: Math.random() * 100 + 50, // Life span
        maxLife: Math.random() * 100 + 50,
        color: `hsl(${Math.random() * 360}, 70%, 50%)`,
      });
    }
  }, []);

  const draw = useCallback((ctx, width, height) => {
    // Clear canvas with decay effect
    ctx.fillStyle = `rgba(26, 26, 46, ${1 - decay})`; // Match body background, but with decay
    ctx.fillRect(0, 0, width, height);

    // Update and draw particles
    particles.current = particles.current.filter(p => p.life > 0);

    if (particles.current.length < 100 * intensity) { // Maintain particle count based on intensity
      particles.current.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        life: Math.random() * 100 + 50,
        maxLife: Math.random() * 100 + 50,
        color: `hsl(${Math.random() * 360}, 70%, 50%)`,
      });
    }

    particles.current.forEach(p => {
      p.x += p.vx * frequency * 10;
      p.y += p.vy * frequency * 10;
      p.life -= 1;

      // Wrap around edges
      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      // Draw particle
      const alpha = p.life / p.maxLife;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 2 * intensity, 0, Math.PI * 2);
      ctx.fillStyle = p.color.replace('50%)', `${50 * intensity}%, ${alpha})`); // Adjust lightness and alpha
      ctx.fill();
    });
  }, [frequency, intensity, decay]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initParticles(canvas.width, canvas.height); // Re-initialize particles on resize
    };

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas(); // Initial size and particle setup

    const animate = () => {
      draw(ctx, canvas.width, canvas.height);
      animationFrameId.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationFrameId.current);
    };
  }, [draw, initParticles]); // Dependencies for useEffect

  return <canvas ref={canvasRef} aria-label="Temporal Bloom Canvas" role="img" />;
};

export default TemporalBloomCanvas;
