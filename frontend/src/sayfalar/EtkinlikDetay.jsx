import { Link, useParams } from "react-router-dom";
import { useVeri } from "../api.jsx";
import { Galeri } from "../bilesenler/Lightbox.jsx";
import { HataKutusu, HtmlIcerik, Yukleniyor, useBaslik } from "../bilesenler/ortak.jsx";
import { tarihSaatYaz } from "../tarih.js";
import Bulunamadi from "./Bulunamadi.jsx";
import stil from "./Icerik.module.css";

export default function EtkinlikDetay() {
  const { slug } = useParams();
  const { veri, yukleniyor, hata } = useVeri(`/etkinlikler/${slug}/`);
  useBaslik(veri?.baslik);
  if (hata?.durum === 404) return <Bulunamadi />;
  if (yukleniyor) return <Yukleniyor />;
  if (hata || !veri) return <div className="kap bolum"><HataKutusu /></div>;
  return (
    <article className="bolum">
      <div className={`kap ${stil.detay}`}>
        <Link to="/etkinlikler" className={stil.geri}>← Tüm etkinlikler</Link>
        <span className="ust-etiket">{veri.tur_adi}</span>
        <h1>{veri.baslik}</h1>
        <div className={stil.bilgiSatiri}>
          <span>📅 {tarihSaatYaz(veri.baslangic)}</span>
          {veri.yer && <span>📍 {veri.yer}</span>}
        </div>
        {veri.kapak && <img className={stil.detayKapak} src={veri.kapak} alt="" />}
        <HtmlIcerik html={veri.aciklama} />
        <Galeri fotograflar={veri.fotograflar} />
      </div>
    </article>
  );
}
