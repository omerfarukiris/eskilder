import { useEffect } from "react";
import { Link } from "react-router-dom";

export default function Bulunamadi() {
  useEffect(() => { document.title = "Sayfa bulunamadı | Eskilder"; }, []);
  return (
    <section className="bolum">
      <div className="kap metin-kolon">
        <span className="ust-etiket">404</span>
        <h1>Sayfa bulunamadı</h1>
        <p className="soluk">Aradığınız sayfa taşınmış ya da kaldırılmış olabilir.</p>
        <Link to="/" className="buton buton-koyu">Ana sayfaya dön</Link>
      </div>
    </section>
  );
}
