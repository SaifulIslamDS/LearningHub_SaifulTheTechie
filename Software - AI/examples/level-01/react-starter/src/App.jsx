import { useMemo, useState } from 'react';
import './styles.css';
import countries from '../data/countries.sample.json';

function CountryCard({ country, selected, onToggle }) {
  return (
    <article className="card">
      <h2>{country.name}</h2>
      <p>{country.region} · population {country.population.toLocaleString()}</p>
      <button type="button" onClick={() => onToggle(country.id)}>
        {selected ? 'Remove' : 'Select'}
      </button>
    </article>
  );
}

export default function App() {
  const [query, setQuery] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase();
    return q ? countries.filter(c => c.name.toLowerCase().includes(q)) : countries;
  }, [query]);

  function toggle(id) {
    setSelectedIds(current => current.includes(id)
      ? current.filter(value => value !== id)
      : [...current, id]);
  }

  return (
    <main>
      <h1>Countries Explorer — Starter</h1>
      <label>
        Search countries
        <input value={query} onChange={e => setQuery(e.target.value)} />
      </label>
      <p aria-live="polite">Selected: {selectedIds.length}</p>
      <section className="grid" aria-label="Countries">
        {visible.map(country => (
          <CountryCard
            key={country.id}
            country={country}
            selected={selectedIds.includes(country.id)}
            onToggle={toggle}
          />
        ))}
      </section>
    </main>
  );
}
