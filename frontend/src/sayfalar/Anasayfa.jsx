import { useEffect } from "react";
import { Link } from "react-router-dom";
import { useAyarlar, useVeri } from "../api.jsx";
import Kart, { KartIskelet, KartIzgara } from "../bilesenler/Kart.jsx";
import { gunAy, tarihSaatYaz, tarihYaz } from "../tarih.js";
import stil from "./Anasayfa.module.css";

export default function Anasayfa() {
  const a = useAyarlar();
  const duyurular = useVeri("/duyurular/");
  const etkinlikler = useVeri("/etkinlikler/?zaman=yaklasan");
  const destekciler = useVeri("/destekciler/");
  const yaklasan = etkinlikler.veri?.results?.[0];
  const destekciListesi = destekciler.veri || [];

  useEffect(() => { document.title = "Eskilder | Eskil'in çocukları için"; }, []);

  return (
    <>
      <section className={stil.hero}>
        {a.hero_gorsel && <img className={stil.heroGorsel} src={a.hero_gorsel} alt="" />}
        <div className={stil.heroOrtu} />
        <div className={`kap ${stil.heroIc}`}>
          <span className={stil.heroEtiket}>Aksaray · Eskil</span>
          <h1>{a.slogan || "Eskil'in çocukları için"}</h1>
          <p className={stil.heroMetin}>
            {a.hero_metin || "Eskil'den yetişen gençlerin lise ve üniversite yolculuğunda, memleketlileri olarak yanlarındayız."}
          </p>
          <div className={stil.heroButonlar}>
            <Link to="/destek-ol" className="buton buton-ana">Destek Ol</Link>
            <Link to="/iletisim" className={`buton ${stil.butonAcik}`}>Bize Ulaşın</Link>
          </div>
        </div>
      </section>

      {a.rakamlar?.length > 0 && (
        <section className={stil.rakamBand} aria-label="Rakamlarla Eskilder">
          <ul className={`kap ${stil.rakamlar}`}>
            {a.rakamlar.map((r) => (
              <li key={r.etiket}>
                <strong>{r.deger}</strong>
                <span>{r.etiket}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="bolum">
        <div className="kap">
          <div className="bolum-baslik">
            <div><span className="ust-etiket">Güncel</span><h2>Son duyurular</h2></div>
            <Link to="/duyurular" className="buton buton-cizgi">Tüm duyurular</Link>
          </div>
          {duyurular.yukleniyor ? <KartIskelet /> : duyurular.veri?.results?.length ? (
            <KartIzgara>
              {duyurular.veri.results.slice(0, 3).map((d) => (
                <Kart key={d.slug} to={`/duyurular/${d.slug}`} gorsel={d.kapak} ust={tarihYaz(d.yayin_tarihi)}
                  baslik={d.baslik} ozet={d.ozet} rozet={d.one_cikan ? "Öne çıkan" : null} />
              ))}
            </KartIzgara>
          ) : <p className="durum-kutu">Henüz duyuru yok.</p>}
        </div>
      </section>

      {yaklasan && (
        <section className={`bolum ${stil.etkinlikBolum}`}>
          <div className="kap">
            <span className="ust-etiket">Takvim</span>
            <h2>Yaklaşan buluşma</h2>
            <Link to={`/etkinlikler/${yaklasan.slug}`} className={stil.etkinlik}>
              <div className={stil.takvim}>
                <span>{gunAy(yaklasan.baslangic).gun}</span>
                <small>{gunAy(yaklasan.baslangic).ay}</small>
              </div>
              <div>
                <span className={stil.tur}>{yaklasan.tur_adi}</span>
                <h3>{yaklasan.baslik}</h3>
                <p className="soluk">{tarihSaatYaz(yaklasan.baslangic)}{yaklasan.yer ? ` · ${yaklasan.yer}` : ""}</p>
              </div>
              <span className={stil.ok} aria-hidden="true">→</span>
            </Link>
          </div>
        </section>
      )}

      {destekciListesi.length > 0 && (
        <section className="bolum">
          <div className="kap">
            <div className="bolum-baslik">
              <div><span className="ust-etiket">Teşekkürler</span><h2>Destekçilerimiz</h2></div>
              <Link to="/destekcilerimiz" className="buton buton-cizgi">Tüm destekçilerimiz</Link>
            </div>
            <ul className={stil.serit}>
              {destekciListesi.slice(0, 8).map((d) => (
                <li key={d.ad}>
                  {d.logo ? <img src={d.logo} alt={d.ad} loading="lazy" /> : <span>{d.ad}</span>}
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}

      <section className={stil.cagri}>
        <div className={`kap ${stil.cagriIc}`}>
          <div>
            <h2>Bir öğrencinin bursunu üstlenin</h2>
            <p>Eskil'den çıkan bir gencin bir yıllık bursu, onun hayatında kalıcı bir iz bırakır. Siz de memleketinizin geleceğine ortak olun.</p>
          </div>
          <Link to="/destek-ol" className="buton buton-ana">Nasıl destek olurum?</Link>
        </div>
      </section>
    </>
  );
}
