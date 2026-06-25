interface PropiedadesSeccionPlaceholder {
  titulo: string;
  colorAcento: "amarillo" | "cian";
}

export function SeccionPlaceholder({
  titulo,
  colorAcento,
}: PropiedadesSeccionPlaceholder) {
  const textoAcento =
    colorAcento === "amarillo"
      ? "text-claridata-amarillo"
      : "text-claridata-cian";

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-claridata-fondo px-6 text-center">
      <h1 className={`text-3xl font-bold tracking-tight ${textoAcento}`}>
        {titulo}
      </h1>
      <p className="text-claridata-textoSecundario">
        Sección en construcción.
      </p>
      
        href="/"
        className="mt-6 text-sm font-medium text-claridata-texto underline-offset-4 hover:underline"
      >
        ← Volver al inicio
      </a>
    </main>
  );
}