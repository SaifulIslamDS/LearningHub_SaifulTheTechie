interface Product {
  id: number;
  name: string;
  price: number;
}

type Preview<T> = Pick<T, "id" & keyof T> & { label: string };

function first<T>(items: T[]): T | undefined {
  return items[0];
}

const products: Product[] = [
  { id: 1, name: "Keyboard", price: 3200 },
  { id: 2, name: "Mouse", price: 1400 }
];
const item = first(products);
const preview: Preview<Product> = { id: item?.id ?? 0, label: item?.name ?? "None" };
console.log(preview);
