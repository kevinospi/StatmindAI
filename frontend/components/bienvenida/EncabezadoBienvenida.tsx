import Image from "next/image";

export function EncabezadoBienvenida() {
  return (
    <div className="flex flex-col items-center gap-3 px-6 py-10 text-center">
      <div className="flex items-center gap-3">
        <Image
          src="/logo_claridata.png"
          alt="Claridata"
          width={48}
          height={48}
          priority
        />
        <span className="text-2xl font-bold tracking-tight text-claridata-texto">
          Claridata
        </span>
      </div>

      <p className="max-w-xl text-base text-claridata-textoSecundario md:text-lg">
        Aprende estadística. Analiza datos. Descubre patrones.
      </p>
    </div>
  );
}