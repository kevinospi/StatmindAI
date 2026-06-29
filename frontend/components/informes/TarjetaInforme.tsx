"use client";

import { useState } from "react";
import { InformeResumenRespuesta } from "@/tipos/api";

interface PropiedadesTarjetaInforme {
  informe: InformeResumenRespuesta;
  alAbrir: () => void;
  alEliminar: () => Promise<void>;
}

function formatearFecha(fechaIso: string): string {
  return new Date(fechaIso).toLocaleString("es-CO", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

export function TarjetaInforme({
  informe,
  alAbrir,
  alEliminar,
}: PropiedadesTarjetaInforme) {
  const [confirmandoEliminar, setConfirmandoEliminar] = useState(false);
  const [eliminando, setEliminando] = useState(false);

  const manejarEliminar = async () => {
    setEliminando(true);
    try {
      await alEliminar();
    } finally {
      setEliminando(false);
      setConfirmandoEliminar(false);
    }
  };

  return (
    <div className="flex items-center justify-between gap-4 rounded-2xl border border-white/10 bg-white/[0.03] px-6 py-5">
      <button
        type="button"
        onClick={alAbrir}
        className="flex flex-1 flex-col items-start text-left"
      >
        <p className="font-medium text-claridata-texto">{informe.titulo}</p>
        <p className="mt-1 text-sm text-claridata-textoSecundario">
          Actualizado el {formatearFecha(informe.fecha_actualizacion)}
        </p>
      </button>

      {confirmandoEliminar ? (
        <div className="flex items-center gap-2">
          <span className="text-sm text-claridata-textoSecundario">
            ¿Eliminar?
          </span>
          <button
            type="button"
            onClick={manejarEliminar}
            disabled={eliminando}
            className="rounded-full bg-red-500/20 px-4 py-2 text-sm font-medium text-red-300 transition-colors hover:bg-red-500/30 disabled:opacity-50"
          >
            {eliminando ? "Eliminando..." : "Sí, eliminar"}
          </button>
          <button
            type="button"
            onClick={() => setConfirmandoEliminar(false)}
            disabled={eliminando}
            className="rounded-full border border-white/15 px-4 py-2 text-sm text-claridata-textoSecundario transition-colors hover:text-claridata-texto disabled:opacity-50"
          >
            Cancelar
          </button>
        </div>
      ) : (
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={alAbrir}
            className="rounded-full border border-white/15 px-4 py-2 text-sm font-medium text-claridata-textoSecundario transition-colors hover:border-white/30 hover:text-claridata-texto"
          >
            Abrir
          </button>
          <button
            type="button"
            onClick={() => setConfirmandoEliminar(true)}
            aria-label="Eliminar informe"
            className="text-claridata-textoSecundario transition-colors hover:text-red-400"
          >
            🗑️
          </button>
        </div>
      )}
    </div>
  );
}