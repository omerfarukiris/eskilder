import { useCallback, useEffect, useState } from "react";
import Logo from "./Logo.jsx";
import stil from "./Acilis.module.css";

const ANAHTAR = "acilis_goruldu";
export const SURE_MS = 1200;

/** Oturumda ilk kez ve hareket azaltma tercihi yoksa açılış gösterilir. */
export function acilisGosterilsinMi(depo, matchMedia) {
  try {
    if (matchMedia?.("(prefers-reduced-motion: reduce)")?.matches) return false;
  } catch { /* yok say */ }
  try {
    return depo?.getItem(ANAHTAR) !== "1";
  } catch {
    return true;
  }
}

function isaretle() {
  try { sessionStorage.setItem(ANAHTAR, "1"); } catch { /* gizli mod */ }
}

export default function Acilis() {
  const [gorunur, setGorunur] = useState(() => {
    let depo = null;
    try { depo = window.sessionStorage; } catch { /* yok */ }
    return acilisGosterilsinMi(depo, typeof window.matchMedia === "function" ? window.matchMedia.bind(window) : null);
  });

  const kapat = useCallback(() => {
    isaretle();
    setGorunur(false);
  }, []);

  useEffect(() => {
    if (!gorunur) return undefined;
    const zamanlayici = setTimeout(kapat, SURE_MS);
    const tus = (olay) => olay.key === "Escape" && kapat();
    document.addEventListener("keydown", tus);
    return () => {
      clearTimeout(zamanlayici);
      document.removeEventListener("keydown", tus);
    };
  }, [gorunur, kapat]);

  if (!gorunur) return null;
  return (
    <div className={stil.acilis} data-testid="acilis" onClick={kapat} role="presentation" aria-hidden="true">
      <div className={stil.icerik}>
        <Logo acik buyuk />
        <span className={stil.cizgi} />
      </div>
    </div>
  );
}
