import { Link } from "react-router-dom";
import stil from "./Kart.module.css";

/** Duyuru/etkinlik kartı. Kapak yoksa markalı bir zemin gösterilir. */
export default function Kart({ to, gorsel, ust, baslik, ozet, rozet }) {
  return (
    <article className={stil.kart}>
      <Link to={to} className={stil.bag}>
        <div className={stil.gorsel}>
          {gorsel ? <img src={gorsel} alt="" loading="lazy" /> : <span className={stil.bosGorsel} aria-hidden="true">E</span>}
          {rozet && <span className={stil.rozet}>{rozet}</span>}
        </div>
        <div className={stil.govde}>
          {ust && <span className={stil.ust}>{ust}</span>}
          <h3 className={stil.baslik}>{baslik}</h3>
          {ozet && <p className={stil.ozet}>{ozet}</p>}
          <span className={stil.devam}>Devamını oku →</span>
        </div>
      </Link>
    </article>
  );
}

export function KartIzgara({ children }) {
  return <div className={stil.izgara}>{children}</div>;
}

export function KartIskelet({ adet = 3 }) {
  return (
    <div className={stil.izgara} aria-busy="true" aria-label="Yükleniyor">
      {Array.from({ length: adet }, (_, i) => <div key={i} className={`iskelet ${stil.iskelet}`} />)}
    </div>
  );
}
