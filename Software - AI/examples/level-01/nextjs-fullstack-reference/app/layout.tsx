import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = { title: "Learning Store", description: "Next.js tutorial project" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><header><Link href="/">Learning Store</Link><nav><Link href="/products">Products</Link><Link href="/dashboard">Dashboard</Link></nav></header><main>{children}</main></body></html>;
}
