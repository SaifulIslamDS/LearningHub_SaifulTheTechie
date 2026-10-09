function selectPlayer(selected, player, max = 3) {
  if (selected.some(p => p.id === player.id)) return selected;
  if (selected.length >= max) return selected;
  return [...selected, player];
}
let selected = [];
selected = selectPlayer(selected, { id: 1, name: "Tamim" });
selected = selectPlayer(selected, { id: 2, name: "Shakib" });
selected = selectPlayer(selected, { id: 1, name: "Tamim" });
console.log(selected.map(p => p.name).join(", "));
