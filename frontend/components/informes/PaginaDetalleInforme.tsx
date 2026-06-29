"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { EncabezadoApp } from "@/components/compartidos/EncabezadoApp";
import { VistaInforme } from "./VistaInforme";
import { obtenerInforme } from "@/lib/api/informes";
import { InformeDetalleRespuesta } from "@/tipos/api";
import { ErrorApiRespuesta, ErrorRed } from "@/lib/api/cliente";

type EstadoCarga = "cargando" | "listo" | "error";

interface PropiedadesPaginaDetalleInforme {
  informeId: string;
}

export function PaginaDetalleInforme({
  informeId,
}: PropiedadesPaginaDetalleInforme) {
  const router = useRouter();
  const [estado, setEstado] = useState<EstadoCarga>("cargando");
  const [informe, setInforme] = useState<InformeDetalleRespuesta | null>(null);
  const [mensajeError, setMensajeError] = useState<string | null>(null);

  useEffect(() => {
    cargarInforme();
  }, [informeId]);

  const cargarInforme = async () => {
    setEstado("cargando");
    try {
      const datos = await obtenerInforme(informeId);
      setInforme(datos);
      setEstado("listo");
    } catch (error) {
      if (error instanceof ErrorApiRespuesta && error.codigoEstado === 404) {
        setMensajeError("Este informe no existe o fue eliminado.");
      } else if (error instanceof ErrorApiRespuesta && error.codigoEstado === 403) {
        setMensajeError("No tienes permiso para ver este informe.");
      } else if (error instanceof ErrorRed) {
        setMensajeError(error.message);
      } else {
        setMensajeError("No fue posible cargar este informe.");
      }
      setEstado("error");
    }
  };

  return (
    <main className="flex min-h-screen w-full flex-col bg-claridata-fondo">
      <EncabezadoApp />

      <div className="flex flex-1 flex-col items-center px-6 py-16 md:px-10">
        <div className="w-full max-w-2xl">
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
                onClick={() => router.push("/informes")}
                className="rounded-full border border-red-400/40 px-5 py-2 text-sm font-medium text-red-300 transition-colors hover:border-red-400"
              >
                Volver a mis informes
              </button>
            </div>
          )}

          {estado === "listo" && informe && (
            <VistaInforme informe={informe} alActualizarInforme={setInforme} />
          )}
        </div>
      </div>
    </main>
  );
}