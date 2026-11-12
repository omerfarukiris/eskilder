import { useEffect } from "react";

export function useBaslik(baslik) {
  useEffect(() => {
    if (baslik) document.title = `${baslik} | Eskilder`;
  }, [baslik]);
}

export function SayfaUst({ etiket, baslik, aciklama }) {
  return (
    <section className="sayfa-ust">
      <div className="kap">
        {etiket && <span className="ust-etiket" style={{ color: "var(--renk-vurgu-acik)" }}>{etiket}</span>}
        <h1>{baslik}</h1>
        {aciklama && <p>{aciklama}</p>}
      </div>
    </section>
  );
}

/** Sunucuda nh3 ile temizlenmiş HTML'i basar (bkz. backend/ortak/html.py). */
export function HtmlIcerik({ html, className = "" }) {
  if (!html) return null;
  return <div className={`zengin ${className}`} dangerouslySetInnerHTML={{ __html: html }} />;
}

export function Yukleniyor() {
  return (
    <div className="kap bolum" aria-busy="true" aria-label="Yükleniyor">
      <div className="iskelet" style={{ height: 36, width: "60%", marginBottom: 16 }} />
      <div className="iskelet" style={{ height: 18, width: "90%", marginBottom: 10 }} />
      <div className="iskelet" style={{ height: 18, width: "80%" }} />
    </div>
  );
}

export function HataKutusu() {
  return <p className="durum-kutu">İçerik şu anda yüklenemedi. Lütfen biraz sonra tekrar deneyin.</p>;
}
