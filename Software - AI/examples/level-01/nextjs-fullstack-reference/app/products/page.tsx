import Link from "next/link";
import { getProducts } from "@/lib/products";
export default async function ProductsPage(){ const products=await getProducts(); return <><h1>Products</h1><div className="grid">{products.map(p=><article key={p.id}><h2>{p.name}</h2><p>BDT {p.price}</p><Link href={`/products/${p.id}`}>View</Link></article>)}</div></> }
