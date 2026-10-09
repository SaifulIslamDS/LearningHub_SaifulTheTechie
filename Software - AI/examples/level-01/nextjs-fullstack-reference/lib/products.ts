export type Product = { id: string; name: string; price: number };
export const products: Product[] = [
  { id: "keyboard", name: "Keyboard", price: 4500 },
  { id: "mouse", name: "Mouse", price: 1800 },
  { id: "stand", name: "Laptop Stand", price: 2200 },
];
export async function getProducts(){ return products; }
export async function getProduct(id:string){ return products.find(p=>p.id===id) ?? null; }
