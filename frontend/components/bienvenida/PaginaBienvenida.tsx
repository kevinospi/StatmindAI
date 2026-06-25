import { SelectorModo } from "./SelectorModo";

export function PaginaBienvenida() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-12 bg-claridata-fondo px-6 py-12">
      <div className="text-center">
        <p className="text-sm font-medium uppercase tracking-widest text-claridata-textoSecundario">
          Claridata
        </p>
        <h1 className="mt-3 text-4xl font-bold tracking-tight text-claridata-texto md:text-5xl">
          Hola, ¿qué deseas hacer hoy?
        </h1>
      </div>

      <SelectorModo />
    </main>
  );
}