"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { EncabezadoApp } from "@/components/compartidos/EncabezadoApp";
import { TarjetaInforme } from "./TarjetaInforme";
import { obtenerInformes, eliminarInforme } from "@/lib/api/informes";
import { InformeResumenRespuesta } from "@/tipos/api";
import { ErrorRed } from "@/lib/api/cliente";

type EstadoCarga = "cargando" | "listo" | "error";

export function PaginaInformes() {
  const router = useRouter();
  const [estado, setEstado] = useState<EstadoCarga>("cargando");
  const [informes, setInformes] = useState<InformeResumenRespuesta[]>([]);
  const [mensajeError, setMensajeError] = useState<string | null>(null);

  useEffect(() => {
    cargarInformes();
  }, []);

  const cargarInformes = async () => {
    setEstado("cargando");
    try {
      const datos = await obtenerInformes();
      setInformes(datos);
      setEstado("listo");
    } catch (error) {
      setMensajeError(
        error instanceof ErrorRed
          ? error.message
          : "No fue posible cargar tus informes.",
      );
      setEstado("error");
    }
  };

  const manejarEliminar = async (informeId: string) => {
    await eliminarInforme(informeId);
    setInformes((actuales) => actuales.filter((i) => i.id !== informeId));
  };

  return (
    <main className="flex min-h-screen w-full flex-col bg-claridata-fondo">
      <EncabezadoApp />

      <div className="flex flex-1 flex-col items-center px-6 py-16 md:px-10">
        <div className="w-full max-w-2xl">
          <div className="mb-10 text-center">
            <h1 className="text-3xl font-extrabold tracking-tight text-claridata-texto md:text-4xl">
              Mis informes
            </h1>
            <p className="mt-3 text-claridata-textoSecundario">
              Consulta, renombra o elimina tus análisis anteriores.
            </p>
          </div>

          {estado === "cargando" && (
            <div className="flex justify-center py-16">
              <div className="relative h-10 w-10">
                <div className="absolute inset-0 rounded-full border-4 border-white/10" />
                <div className="absolute inset-0 animate-spin rounded-full border-4 border-transparent border-t-claridata-marca" />
              </div>
            </div>
          )}

          {estado === "error" && (
            <div className="flex flex-col items-center gap-4 rounded-2xl border border-red-400/30 bg-red-400/5 px-6 py-8 text-center">
              <p className="text-red-300">{mensajeError}</p>
              <button
                type="button"
                onClick={cargarInformes}
                className="rounded-full border border-red-400/40 px-5 py-2 text-sm font-medium text-red-300 transition-colors hover:border-red-400"
              >
                Intentar de nuevo
              </button>
            </div>
          )}

          {estado === "listo" && informes.length === 0 && (
            <div className="flex flex-col items-center gap-4 py-16 text-center">
              <div className="text-5xl">📭</div>
              <p className="text-claridata-textoSecundario">
                Aún no tienes informes generados.
              </p>
              <button
                type="button"
                onClick={() => router.push("/analizar")}
                className="rounded-full bg-claridata-marca px-6 py-3 text-sm font-semibold text-[#022C33] transition-transform hover:scale-[1.03]"
              >
                Analizar mi primer dataset
              </button>
            </div>
          )}

          {estado === "listo" && informes.length > 0 && (
            <div className="flex flex-col gap-3">
              {informes.map((informe) => (
                <TarjetaInforme
                  key={informe.id}
                  informe={informe}
                  alAbrir={() => router.push(`/informes/${informe.id}`)}
                  alEliminar={() => manejarEliminar(informe.id)}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}