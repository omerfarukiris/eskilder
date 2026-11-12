import { useAyarlar } from "../api.jsx";
import { HtmlIcerik, SayfaUst, useBaslik } from "../bilesenler/ortak.jsx";
import stil from "./Icerik.module.css";

export default function Hakkimizda() {
  const a = useAyarlar();
  useBaslik("Hakkımızda");
  return (
    <>
      <SayfaUst etiket="Biz kimiz?" baslik="Hakkımızda" aciklama={a.resmi_ad} />
      <section className="bolum">
        <div className="kap metin-kolon">
          <HtmlIcerik html={a.hakkimizda_metni} />
        </div>
      </section>
      {a.kurul?.length > 0 && (
        <section className={`bolum ${stil.acikZemin}`}>
          <div className="kap">
            <span className="ust-etiket">Yönetim</span>
            <h2>Yönetim kurulu</h2>
            <ul className={stil.kurul}>
              {a.kurul.map((k) => (
                <li key={`${k.ad_soyad}-${k.gorev}`}>
                  {k.fotograf ? <img src={k.fotograf} alt="" loading="lazy" /> : (
                    <span className={stil.basHarf} aria-hidden="true">{k.ad_soyad.trim().charAt(0)}</span>
                  )}
                  <strong>{k.ad_soyad}</strong>
                  <span>{k.gorev}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}
    </>
  );
}
