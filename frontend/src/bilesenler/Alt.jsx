import { Link } from "react-router-dom";
import { useAyarlar } from "../api.jsx";
import Logo from "./Logo.jsx";
import { MENU } from "./Ust.jsx";
import stil from "./Alt.module.css";

const SOSYAL = [["facebook", "Facebook"], ["instagram", "Instagram"], ["x", "X"], ["youtube", "YouTube"]];

export default function Alt() {
  const a = useAyarlar();
  const sosyal = SOSYAL.filter(([alan]) => a[alan]);
  return (
    <footer className={stil.alt}>
      <div className={`kap ${stil.izgara}`}>
        <div>
          <Logo acik />
          <p className={stil.tanim}>{a.resmi_ad}</p>
          <p className={stil.tanim}>Eskil'den yetişen gençlerin üniversite yolculuğunda yanlarındayız.</p>
        </div>
        <nav aria-label="Alt menü">
          <h2 className={stil.baslik}>Sayfalar</h2>
          <ul className={stil.liste}>
            {MENU.slice(1).map((m) => <li key={m.yol}><Link to={m.yol}>{m.ad}</Link></li>)}
            <li><Link to="/destek-ol">Destek Ol</Link></li>
          </ul>
        </nav>
        <div>
          <h2 className={stil.baslik}>İletişim</h2>
          <ul className={stil.liste}>
            {a.telefon && <li><a href={`tel:${a.telefon.replace(/[^\d+]/g, "")}`}>{a.telefon}</a></li>}
            {a.eposta && <li><a href={`mailto:${a.eposta}`}>{a.eposta}</a></li>}
            {a.adres && <li className={stil.adres}>{a.adres}</li>}
          </ul>
          {sosyal.length > 0 && (
            <ul className={stil.sosyal}>
              {sosyal.map(([alan, ad]) => (
                <li key={alan}><a href={a[alan]} target="_blank" rel="noopener noreferrer">{ad}</a></li>
              ))}
            </ul>
          )}
        </div>
      </div>
      <div className={`kap ${stil.son}`}>
        <span>© {new Date().getFullYear()} {a.kisa_ad || "Eskilder"}</span>
        <Link to="/kvkk">KVKK Aydınlatma Metni</Link>
      </div>
    </footer>
  );
}
