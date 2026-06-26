"use client";

import { DefinicionModo } from "@/tipos/modo";

interface PropiedadesTarjetaModo {
  modo: DefinicionModo;
  estaEnHover: boolean;
  alIniciarHover: () => void;
  alFinalizarHover: () => void;
  alSeleccionar: () => void;
}

export function TarjetaModo({
  modo,
  estaEnHover,
  alIniciarHover,
  alFinalizarHover,
  alSeleccionar,
}: PropiedadesTarjetaModo) {
  const colorTexto = modo.colorAcento === "amarillo" ? "#3F2D03" : "#022C33";
  const colorTextoSecundario =
    modo.colorAcento === "amarillo" ? "#6B4E0A" : "#0A4A52";

  return (
    <button
      type="button"
      onMouseEnter={alIniciarHover}
      onMouseLeave={alFinalizarHover}
      onClick={alSeleccionar}
      aria-label={`Entrar a ${modo.titulo}`}
      style={{
        background: `linear-gradient(135deg, ${modo.degradadoDesde}, ${modo.degradadoHasta})`,
      }}
      className={`
        group relative flex h-full w-full flex-1 flex-col
        items-center justify-center px-6 py-16
        text-center
        transition-all duration-500 ease-claridata-expo
        ${estaEnHover ? "scale-[1.015] brightness-110" : "scale-100 brightness-100"}
      `}
    >
      <h2
        style={{ color: colorTexto }}
        className="text-4xl font-bold tracking-tight md:text-5xl"
      >
        {modo.titulo}
      </h2>

      <p
        style={{ color: colorTextoSecundario }}
        className="mt-4 max-w-sm text-base font-medium md:text-lg"
      >
        {modo.descripcion}
      </p>
    </button>
  );
}