import { PaginaDetalleInforme } from "@/components/informes/PaginaDetalleInforme";

interface PropiedadesPagina {
  params: Promise<{ id: string }>;
}

export default async function RutaDetalleInforme({
  params,
}: PropiedadesPagina) {
  const { id } = await params;
  return <PaginaDetalleInforme informeId={id} />;
}