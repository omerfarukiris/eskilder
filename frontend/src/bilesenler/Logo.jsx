import { useAyarlar } from "../api.jsx";
import stil from "./Logo.module.css";

/** Panelde logo varsa onu, yoksa yazı logosunu gösterir. */
export default function Logo({ acik = false, buyuk = false }) {
  const ayar = useAyarlar();
  const sinif = [stil.logo, acik && stil.acik, buyuk && stil.buyuk].filter(Boolean).join(" ");
  if (ayar.logo) {
    return <img className={`${sinif} ${stil.resim}`} src={ayar.logo} alt={ayar.kisa_ad || "Eskilder"} />;
  }
  return (
    <span className={sinif} aria-label={ayar.kisa_ad || "Eskilder"}>
      <span className={stil.isaret} aria-hidden="true">E</span>
      <span className={stil.yazi} aria-hidden="true">{ayar.kisa_ad || "Eskilder"}</span>
    </span>
  );
}
