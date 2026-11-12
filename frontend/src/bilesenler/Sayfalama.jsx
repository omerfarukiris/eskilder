import stil from "./Sayfalama.module.css";

export default function Sayfalama({ sayfa, toplam, boyut = 9, degistir }) {
  const sayfaSayisi = Math.ceil((toplam || 0) / boyut);
  if (sayfaSayisi <= 1) return null;
  return (
    <nav className={stil.sayfalama} aria-label="Sayfalar">
      <button type="button" className="buton buton-cizgi" disabled={sayfa <= 1} onClick={() => degistir(sayfa - 1)}>← Önceki</button>
      <span>{sayfa} / {sayfaSayisi}</span>
      <button type="button" className="buton buton-cizgi" disabled={sayfa >= sayfaSayisi} onClick={() => degistir(sayfa + 1)}>Sonraki →</button>
    </nav>
  );
}
