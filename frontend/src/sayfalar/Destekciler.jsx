import { Link } from "react-router-dom";
import { useVeri } from "../api.jsx";
import { HataKutusu, SayfaUst, Yukleniyor, useBaslik } from "../bilesenler/ortak.jsx";
import stil from "./Icerik.module.css";

export default function Destekciler() {
  const { veri, yukleniyor, hata } = useVeri("/destekciler/");
  useBaslik("Destekçilerimiz");
  const firmalar = (veri || []).filter((d) => d.tur === "firma");
  const kisiler = (veri || []).filter((d) => d.tur !== "firma");
  return (
    <>
      <SayfaUst etiket="Teşekkürler" baslik="Destekçilerimiz"
        aciklama="Burslarımız, memleketine gönül vermiş Eskilli iş insanları ve hayırseverler sayesinde mümkün oluyor." />
      <section className="bolum">
        <div className="kap">
          {yukleniyor ? <Yukleniyor /> : hata ? <HataKutusu /> : (
            <>
              {firmalar.length > 0 && (
                <>
                  <h2>Firmalar</h2>
                  <ul className={stil.firmalar}>
                    {firmalar.map((d) => (
                      <li key={d.ad}>
                        {d.logo && <img src={d.logo} alt="" loading="lazy" />}
                        <strong>{d.ad}</strong>
                        {d.not_metni && <span className={stil.not}>{d.not_metni}</span>}
                      </li>
                    ))}
                  </ul>
                </>
              )}
              {kisiler.length > 0 && (
                <>
                  <h2>Kişiler</h2>
                  <ul className={stil.kisiler}>
                    {kisiler.map((d) => (
                      <li key={d.ad}><strong>{d.ad}</strong>{d.not_metni && <span className={stil.not}>{d.not_metni}</span>}</li>
                    ))}
                  </ul>
                </>
              )}
              {!firmalar.length && !kisiler.length && <p className="durum-kutu">Destekçi listemiz yakında burada.</p>}
              <div className="durum-kutu" style={{ marginTop: 56, borderStyle: "solid" }}>
                <h2 style={{ fontSize: "1.4rem" }}>Siz de destekçimiz olun</h2>
                <p>Bir öğrencinin bursunu üstlenmek ya da derneğimize katkı sunmak için bize ulaşın.</p>
                <Link to="/destek-ol" className="buton buton-ana">Destek Ol</Link>
              </div>
            </>
          )}
        </div>
      </section>
    </>
  );
}
