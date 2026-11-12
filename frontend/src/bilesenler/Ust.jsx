import { useEffect, useState } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import Logo from "./Logo.jsx";
import stil from "./Ust.module.css";

export const MENU = [
  { yol: "/", ad: "Ana Sayfa" },
  { yol: "/hakkimizda", ad: "Hakkımızda" },
  { yol: "/burs", ad: "Burs" },
  { yol: "/duyurular", ad: "Duyurular" },
  { yol: "/etkinlikler", ad: "Etkinlikler" },
  { yol: "/destekcilerimiz", ad: "Destekçilerimiz" },
  { yol: "/iletisim", ad: "İletişim" },
];

export default function Ust() {
  const [acik, setAcik] = useState(false);
  const konum = useLocation();

  useEffect(() => setAcik(false), [konum.pathname]);
  useEffect(() => {
    if (!acik) return undefined;
    const kapat = (olay) => olay.key === "Escape" && setAcik(false);
    document.addEventListener("keydown", kapat);
    return () => document.removeEventListener("keydown", kapat);
  }, [acik]);

  return (
    <header className={stil.ust}>
      <div className={`kap ${stil.ic}`}>
        <Link to="/" className={stil.logoBag} aria-label="Ana sayfa">
          <Logo />
        </Link>
        <nav id="ana-menu" className={`${stil.menu} ${acik ? stil.menuAcik : ""}`} aria-label="Ana menü">
          <ul>
            {MENU.map((m) => (
              <li key={m.yol}>
                <NavLink to={m.yol} end={m.yol === "/"} onClick={() => setAcik(false)}
                  className={({ isActive }) => (isActive ? stil.aktif : undefined)}>
                  {m.ad}
                </NavLink>
              </li>
            ))}
            <li className={stil.mobilCta}>
              <Link to="/destek-ol" className="buton buton-ana" onClick={() => setAcik(false)}>Destek Ol</Link>
            </li>
          </ul>
        </nav>
        <Link to="/destek-ol" className={`buton buton-ana ${stil.cta}`}>Destek Ol</Link>
        <button type="button" className={stil.hamburger} aria-expanded={acik} aria-controls="ana-menu"
          aria-label={acik ? "Menüyü kapat" : "Menüyü aç"} onClick={() => setAcik((a) => !a)}>
          <span /><span /><span />
        </button>
      </div>
    </header>
  );
}
