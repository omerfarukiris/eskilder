import { useAyarlar } from "../api.jsx";
import { HtmlIcerik, SayfaUst, useBaslik } from "../bilesenler/ortak.jsx";

export default function Kvkk() {
  const a = useAyarlar();
  useBaslik("KVKK Aydınlatma Metni");
  return (
    <>
      <SayfaUst baslik="KVKK Aydınlatma Metni" />
      <section className="bolum"><div className="kap metin-kolon"><HtmlIcerik html={a.kvkk_metni} /></div></section>
    </>
  );
}
