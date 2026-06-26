export type IdModo = "aprender" | "analizar";

export interface DefinicionModo {
  id: IdModo;
  titulo: string;
  descripcion: string;
  ruta: string;
  colorAcento: "amarillo" | "cian";
  degradadoDesde: string;
  degradadoHasta: string;
}