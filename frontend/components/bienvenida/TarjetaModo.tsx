"use client";

import { DefinicionModo } from "@/tipos/modo";

interface PropiedadesTarjetaModo {
  modo: DefinicionModo;
  estaEnHover: boolean;
  estaExpandiendo: boolean;
  estaDesapareciendo: boolean;
  alIniciarHover: () => void;
  alFinalizarHover: () => void;
  alSeleccionar: () => void;
}

export function TarjetaModo({
  modo,
  estaEnHover,
  estaExpandiendo,
  estaDesapareciendo,
  alIniciarHover,
  alFinalizarHover,
  alSeleccionar,
}: PropiedadesTarjetaModo) {
  const bordeAcento =
    modo.colorAcento === "amarillo"
      ? "border-claridata-amarillo/40 hover:border-claridata-amarillo"
      : "border-claridata-cian/40 hover:border-claridata-cian";

  const textoAcento =
    modo.colorAcento === "amarillo"
      ? "text-claridata-amarillo"
      : "text-claridata-cian";

  const claseAncho = estaExpandiendo
    ? "w-full"
    : estaDesapareciendo
      ? "w-0 opacity-0"
      : estaEnHover
        ? "w-[58%]"
        : "w-1/2";

  return (
    <button
      type="button"
      onMouseEnter={alIniciarHover}
      onMouseLeave={alFinalizarHover}
      onClick={alSeleccionar}
      aria-label={`Entrar a ${modo.titulo}`}
      className={`
        group relative flex h-full flex-col items-center justify-center
        overflow-hidden rounded-2xl border-2 bg-claridata-superficie
        px-8 py-12 text-center
        transition-all duration-500 ease-claridata-expo
        ${claseAncho}
        ${bordeAcento}
      `}
    >
      <span className="mb-4 text-5xl transition-transform duration-300 group-hover:scale-110">
        {modo.icono}
      </span>

      <h2 className={`text-3xl font-semibold tracking-tight ${textoAcento}`}>
        {modo.titulo}
      </h2>

      <p
        className={`
          mt-4 max-w-xs text-base text-claridata-textoSecundario
          transition-opacity duration-300
          ${estaEnHover || estaExpandiendo ? "opacity-100" : "opacity-0 md:opacity-70"}
        `}
      >
        {modo.descripcion}
      </p>

      <span
        className={`
          mt-6 inline-flex items-center gap-2 rounded-full
          bg-claridata-superficieElevada px-5 py-2 text-sm font-medium
          ${textoAcento}
          transition-all duration-300
          ${estaEnHover ? "translate-y-0 opacity-100" : "translate-y-2 opacity-0"}
        `}
      >
        Entrar
        <span aria-hidden="true">→</span>
      </span>
    </button>
  );
}