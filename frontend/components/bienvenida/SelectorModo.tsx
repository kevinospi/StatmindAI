"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { TarjetaModo } from "./TarjetaModo";
import { MODOS } from "@/lib/constantes/modos";
import { IdModo } from "@/tipos/modo";

export function SelectorModo() {
  const router = useRouter();
  const [modoEnHover, setModoEnHover] = useState<IdModo | null>(null);
  const [modoSeleccionado, setModoSeleccionado] = useState<IdModo | null>(null);

  const manejarSeleccion = (modo: IdModo, ruta: string) => {
    if (modoSeleccionado) return;

    setModoSeleccionado(modo);

    window.setTimeout(() => {
      router.push(ruta);
    }, 550);
  };

  return (
    <div className="flex h-[60vh] w-full max-w-5xl gap-4">
      {MODOS.map((modo) => (
        <TarjetaModo
          key={modo.id}
          modo={modo}
          estaEnHover={modoEnHover === modo.id && modoSeleccionado === null}
          estaExpandiendo={modoSeleccionado === modo.id}
          estaDesapareciendo={
            modoSeleccionado !== null && modoSeleccionado !== modo.id
          }
          alIniciarHover={() => setModoEnHover(modo.id)}
          alFinalizarHover={() => setModoEnHover(null)}
          alSeleccionar={() => manejarSeleccion(modo.id, modo.ruta)}
        />
      ))}
    </div>
  );
}