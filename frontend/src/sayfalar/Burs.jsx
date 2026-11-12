import { Link } from "react-router-dom";
import { useAyarlar } from "../api.jsx";
import { HtmlIcerik, SayfaUst, useBaslik } from "../bilesenler/ortak.jsx";
import stil from "./Icerik.module.css";

function uzanti(url) {
  const eslesme = /\.([a-z0-9]+)(?:\?|$)/i.exec(url || "");
  return eslesme ? eslesme[1].toUpperCase() : "DOSYA";
}

export default function Burs() {
  const a = useAyarlar();
  useBaslik("Burs");
  return (
    <>
      <SayfaUst etiket="Burs programı" baslik="Eskilli öğrencilere karşılıksız burs"
        aciklama="Aksaray'ın Eskil ilçesinden yetişen üniversite öğrencilerimizin yanındayız." />
      <section className="bolum">
        <div className={`kap ${stil.ikiKolon}`}>
          <HtmlIcerik html={a.burs_metni} />
          <aside className={stil.yanKutu}>
            <h2>Başvuru belgeleri</h2>
            {a.dokumanlar?.length ? (
              <ul className={stil.belgeler}>
                {a.dokumanlar.map((d) => (
                  <li key={d.dosya}>
                    <a href={d.dosya} target="_blank" rel="noopener noreferrer" download>
                      <span className={stil.belgeIkon}>{uzanti(d.dosya)}</span>{d.baslik}
                    </a>
                  </li>
                ))}
              </ul>
            ) : <p className="soluk">Başvuru formu, başvuru dönemi açıldığında burada yayınlanacak.</p>}
            <p className="soluk">Başvuru tarihleri <Link to="/duyurular">Duyurular</Link> sayfasında ilan edilir. Sorularınız için <Link to="/iletisim">bize yazın</Link>.</p>
          </aside>
        </div>
      </section>
    </>
  );
}
