export type FortuneCategory = "wisdom" | "debugging" | "deployment" | "general";

export interface Fortune {
  message: string;
  category: FortuneCategory;
}
