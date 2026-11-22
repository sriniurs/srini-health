const input = document.querySelector('#reader-query');
const count = document.querySelector('#reader-count');
const results = [...document.querySelectorAll('#reader-results li')];
const normalize = value => value.normalize('NFD').replace(/\p{Mark}/gu, '').toLocaleLowerCase();
const entries = results.map(item => [item, normalize(item.textContent + " " + item.querySelector("a").pathname.replace(/[-_/]/g, " "))]);
const showMatches = () => {
  const words = normalize(input.value).trim().split(/\s+/).filter(Boolean);
  let visible = 0;
  for (const [item, title] of entries) {
    item.hidden = !words.every(word => title.includes(word));
    if (!item.hidden) visible++;
  }
  count.textContent = visible === 1 ? '1 result' : `${visible} results`;
};
document.querySelector('.reader-search-input').hidden = false;
input.addEventListener('input', showMatches);
showMatches();
