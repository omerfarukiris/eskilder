import { useEffect, useState } from "react";
import { useVeri } from "../api.jsx";
import Kart, { KartIskelet, KartIzgara } from "../bilesenler/Kart.jsx";
import { HataKutusu, SayfaUst, useBaslik } from "../bilesenler/ortak.jsx";
import Sayfalama from "../bilesenler/Sayfalama.jsx";
import { tarihSaatYaz } from "../tarih.js";
import stil from "./Icerik.module.css";

const SEKMELER = [["yaklasan", "Yaklaşan"], ["gecmis", "Geçmiş"]];

export default function Etkinlikler() {
  const [zaman, setZaman] = useState(null);
  const [sayfa, setSayfa] = useState(1);
  const yaklasanKontrol = useVeri("/etkinlikler/?zaman=yaklasan");
  useBaslik("Etkinlikler ve Buluşmalar");

  useEffect(() => {
    if (zaman || yaklasanKontrol.yukleniyor) return;
    setZaman(yaklasanKontrol.veri?.count ? "yaklasan" : "gecmis");
  }, [zaman, yaklasanKontrol.yukleniyor, yaklasanKontrol.veri]);

  const { veri, yukleniyor, hata } = useVeri(zaman ? `/etkinlikler/?zaman=${zaman}&sayfa=${sayfa}` : null);
  const sec = (yeni) => { setZaman(yeni); setSayfa(1); };

  return (
    <>
      <SayfaUst etiket="Bir araya geliyoruz" baslik="Etkinlikler ve Buluşmalar"
        aciklama="Eskilli destekçilerimiz, öğrencilerimiz ve aileleriyle buluştuğumuz anlar." />
      <section className="bolum">
        <div className="kap">
          <div className={stil.sekmeler} role="tablist" aria-label="Etkinlik zamanı">
            {SEKMELER.map(([deger, ad]) => (
              <button key={deger} type="button" role="tab" aria-selected={zaman === deger} onClick={() => sec(deger)}>{ad}</button>
            ))}
          </div>
          {!zaman || yukleniyor ? <KartIskelet /> : hata ? <HataKutusu /> : veri?.results?.length ? (
            <>
              <KartIzgara>
                {veri.results.map((e) => (
                  <Kart key={e.slug} to={`/etkinlikler/${e.slug}`} gorsel={e.kapak} rozet={e.tur_adi}
                    ust={`${tarihSaatYaz(e.baslangic)}${e.yer ? ` · ${e.yer}` : ""}`} baslik={e.baslik} />
                ))}
              </KartIzgara>
              <Sayfalama sayfa={sayfa} toplam={veri.count} degistir={setSayfa} />
            </>
          ) : (
            <p className="durum-kutu">{zaman === "yaklasan" ? "Şu an planlanmış bir etkinlik yok. Yeni buluşmalar burada duyurulacak." : "Henüz geçmiş etkinlik yok."}</p>
          )}
        </div>
      </section>
    </>
  );
}
