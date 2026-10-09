import { notFound } from "next/navigation";
import { getProduct, products } from "@/lib/products";
export function generateStaticParams(){ return products.map(product=>({id:product.id})); }
export default async function ProductPage({params}:{params:Promise<{id:string}>}){ const {id}=await params; const product=await getProduct(id); if(!product) notFound(); return <><h1>{product.name}</h1><p>BDT {product.price}</p></> }
