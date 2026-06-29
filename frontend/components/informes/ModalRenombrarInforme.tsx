"use client";

import { useEffect, useState } from "react";

interface PropiedadesModalRenombrarInforme {
  abierto: boolean;
  tituloActual: string;
  cargando: boolean;
  alCerrar: () => void;
  alConfirmar: (nuevoTitulo: string) => void;
}

export function ModalRenombrarInforme({
  abierto,
  tituloActual,
  cargando,
  alCerrar,
  alConfirmar,
}: PropiedadesModalRenombrarInforme) {
  const [valor, setValor] = useState(tituloActual);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (abierto) {
      setValor(tituloActual);
      setError(null);
    }
  }, [abierto, tituloActual]);

  if (!abierto) return null;

  const manejarConfirmar = () => {
    const valorLimpio = valor.trim();

    if (valorLimpio.length < 3) {
      setError("El título debe tener al menos 3 caracteres.");
      return;
    }

    if (valorLimpio.length > 150) {
      setError("El título no puede superar los 150 caracteres.");
      return;
    }

    alConfirmar(valorLimpio);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-6">
      <div className="w-full max-w-md rounded-2xl border border-white/10 bg-claridata-superficie p-6">
        <h3 className="text-lg font-semibold text-claridata-texto">
          Renombrar informe
        </h3>

        <input
          type="text"
          value={valor}
          onChange={(evento) => setValor(evento.target.value)}
          maxLength={150}
          autoFocus
          className="mt-4 w-full rounded-xl border border-white/15 bg-white/[0.03] px-4 py-3 text-claridata-texto outline-none focus:border-claridata-marca"
        />

        {error && (
          <p className="mt-2 text-sm font-medium text-red-400">{error}</p>
        )}

        <div className="mt-6 flex justify-end gap-3">
          <button
            type="button"
            onClick={alCerrar}
            disabled={cargando}
            className="rounded-full border border-white/15 px-5 py-2 text-sm font-medium text-claridata-textoSecundario transition-colors hover:border-white/30 hover:text-claridata-texto disabled:opacity-50"
          >
            Cancelar
          </button>
          <button
            type="button"
            onClick={manejarConfirmar}
            disabled={cargando}
            className="rounded-full bg-claridata-marca px-5 py-2 text-sm font-semibold text-[#022C33] transition-transform hover:scale-[1.02] disabled:opacity-50"
          >
            {cargando ? "Guardando..." : "Guardar"}
          </button>
        </div>
      </div>
    </div>
  );
}