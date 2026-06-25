import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        claridata: {
          cian: "#5EEAD4",
          cianClaro: "#A7F3EB",
          azul: "#38BDF8",
          azulOscuro: "#0EA5E9",
          amarillo: "#FDE68A",
          amarilloSuave: "#FEF3C7",
          fondo: "#0B1120",
          superficie: "#111827",
          superficieElevada: "#1A2333",
          texto: "#E5E7EB",
          textoSecundario: "#94A3B8",
        },
      },
      fontFamily: {
        sans: ["system-ui", "sans-serif"],
      },
      transitionTimingFunction: {
        "claridata-expo": "cubic-bezier(0.16, 1, 0.3, 1)",
      },
    },
  },
  plugins: [],
};

export default config;