import { Link, useParams } from "react-router-dom";
import { useVeri } from "../api.jsx";
import { Galeri } from "../bilesenler/Lightbox.jsx";
import { HataKutusu, HtmlIcerik, Yukleniyor, useBaslik } from "../bilesenler/ortak.jsx";
import { tarihYaz } from "../tarih.js";
import Bulunamadi from "./Bulunamadi.jsx";
import stil from "./Icerik.module.css";

export default function DuyuruDetay() {
  const { slug } = useParams();
  const { veri, yukleniyor, hata } = useVeri(`/duyurular/${slug}/`);
  useBaslik(veri?.baslik);
  if (hata?.durum === 404) return <Bulunamadi />;
  if (yukleniyor) return <Yukleniyor />;
  if (hata || !veri) return <div className="kap bolum"><HataKutusu /></div>;
  return (
    <article className="bolum">
      <div className={`kap ${stil.detay}`}>
        <Link to="/duyurular" className={stil.geri}>← Tüm duyurular</Link>
        <span className="ust-etiket">{tarihYaz(veri.yayin_tarihi)}</span>
        <h1>{veri.baslik}</h1>
        {veri.ozet && <p className="soluk" style={{ fontSize: "1.15rem" }}>{veri.ozet}</p>}
        {veri.kapak && <img className={stil.detayKapak} src={veri.kapak} alt="" />}
        <HtmlIcerik html={veri.icerik} />
        <Galeri fotograflar={veri.fotograflar} />
      </div>
    </article>
  );
}
