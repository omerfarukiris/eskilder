import { useEffect, useRef, useState } from "react";
import stil from "./Lightbox.module.css";

export default function Lightbox({ fotograflar, index, onKapat }) {
  const [sira, setSira] = useState(index);
  const dokunma = useRef(null);
  const kapatButon = useRef(null);
  const adet = fotograflar.length;
  const git = (fark) => setSira((s) => (s + fark + adet) % adet);

  useEffect(() => {
    const tus = (olay) => {
      if (olay.key === "Escape") onKapat();
      else if (olay.key === "ArrowRight") git(1);
      else if (olay.key === "ArrowLeft") git(-1);
    };
    document.addEventListener("keydown", tus);
    const onceki = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    kapatButon.current?.focus();
    return () => {
      document.removeEventListener("keydown", tus);
      document.body.style.overflow = onceki;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [onKapat, adet]);

  const foto = fotograflar[sira];
  return (
    <div className={stil.perde} role="dialog" aria-modal="true" aria-label="Fotoğraf görüntüleyici" onClick={onKapat}
      onTouchStart={(o) => { dokunma.current = o.touches[0].clientX; }}
      onTouchEnd={(o) => {
        if (dokunma.current === null) return;
        const fark = o.changedTouches[0].clientX - dokunma.current;
        if (Math.abs(fark) > 50) git(fark < 0 ? 1 : -1);
        dokunma.current = null;
      }}>
      <button ref={kapatButon} type="button" className={stil.kapat} onClick={onKapat} aria-label="Kapat">×</button>
      {adet > 1 && <button type="button" className={`${stil.ok} ${stil.sol}`} aria-label="Önceki fotoğraf" onClick={(o) => { o.stopPropagation(); git(-1); }}>‹</button>}
      <figure className={stil.sekil} onClick={(o) => o.stopPropagation()}>
        <img src={foto.gorsel} alt={foto.aciklama || `Fotoğraf ${sira + 1}`} />
        <figcaption>{foto.aciklama} <span>{sira + 1} / {adet}</span></figcaption>
      </figure>
      {adet > 1 && <button type="button" className={`${stil.ok} ${stil.sag}`} aria-label="Sonraki fotoğraf" onClick={(o) => { o.stopPropagation(); git(1); }}>›</button>}
    </div>
  );
}

export function Galeri({ fotograflar }) {
  const [acik, setAcik] = useState(null);
  if (!fotograflar?.length) return null;
  return (
    <>
      <ul className={stil.galeri}>
        {fotograflar.map((f, i) => (
          <li key={f.gorsel}>
            <button type="button" onClick={() => setAcik(i)} aria-label={`Fotoğrafı büyüt: ${f.aciklama || i + 1}`}>
              <img src={f.gorsel} alt={f.aciklama || ""} loading="lazy" />
            </button>
          </li>
        ))}
      </ul>
      {acik !== null && <Lightbox fotograflar={fotograflar} index={acik} onKapat={() => setAcik(null)} />}
    </>
  );
}
