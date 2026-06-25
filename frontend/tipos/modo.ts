export type IdModo = "aprender" | "analizar";

export interface DefinicionModo {
  id: IdModo;
  titulo: string;
  descripcion: string;
  ruta: string;
  icono: string;
  colorAcento: "amarillo" | "cian";
}