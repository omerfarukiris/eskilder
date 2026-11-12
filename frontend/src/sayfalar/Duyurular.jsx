import { useState } from "react";
import { useVeri } from "../api.jsx";
import Kart, { KartIskelet, KartIzgara } from "../bilesenler/Kart.jsx";
import { HataKutusu, SayfaUst, useBaslik } from "../bilesenler/ortak.jsx";
import Sayfalama from "../bilesenler/Sayfalama.jsx";
import { tarihYaz } from "../tarih.js";

export default function Duyurular() {
  const [sayfa, setSayfa] = useState(1);
  const { veri, yukleniyor, hata } = useVeri(`/duyurular/?sayfa=${sayfa}`);
  useBaslik("Duyurular");
  const degistir = (yeni) => { setSayfa(yeni); window.scrollTo?.(0, 0); };
  return (
    <>
      <SayfaUst etiket="Haberler" baslik="Duyurular" aciklama="Burs dönemleri, buluşmalar ve dernekten haberler." />
      <section className="bolum">
        <div className="kap">
          {yukleniyor ? <KartIskelet adet={6} /> : hata ? <HataKutusu /> : veri?.results?.length ? (
            <>
              <KartIzgara>
                {veri.results.map((d) => (
                  <Kart key={d.slug} to={`/duyurular/${d.slug}`} gorsel={d.kapak} ust={tarihYaz(d.yayin_tarihi)}
                    baslik={d.baslik} ozet={d.ozet} rozet={d.one_cikan ? "Öne çıkan" : null} />
                ))}
              </KartIzgara>
              <Sayfalama sayfa={sayfa} toplam={veri.count} degistir={degistir} />
            </>
          ) : <p className="durum-kutu">Henüz duyuru yok.</p>}
        </div>
      </section>
    </>
  );
}
