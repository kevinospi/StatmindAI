import { EncabezadoBienvenida } from "./EncabezadoBienvenida";
import { SelectorModo } from "./SelectorModo";

export function PaginaBienvenida() {
  return (
    <main className="flex h-screen w-full flex-col bg-claridata-fondo">
      <EncabezadoBienvenida />
      <SelectorModo />
    </main>
  );
}