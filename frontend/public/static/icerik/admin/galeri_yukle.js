/* Çoklu seçilen fotoğrafları küçültüp tek tek yükler, bitince sayfayı yeniler. */
(function () {
  "use strict";
  var kutu = document.getElementById("galeri-yukle");
  if (!kutu) return;
  var girdi = kutu.querySelector("[data-galeri-girdi]");
  var liste = kutu.querySelector("[data-galeri-durum]");
  var csrf = (document.querySelector("[name=csrfmiddlewaretoken]") || {}).value;

  function satir(metin) {
    var li = document.createElement("li");
    li.textContent = metin;
    liste.appendChild(li);
    return li;
  }

  girdi.addEventListener("change", async function () {
    var dosyalar = Array.from(girdi.files || []);
    if (!dosyalar.length) return;
    girdi.disabled = true;
    var hataVar = false;
    for (var i = 0; i < dosyalar.length; i++) {
      var li = satir((i + 1) + "/" + dosyalar.length + " " + dosyalar[i].name + " — yükleniyor…");
      try {
        var kucuk = window.eskilderKucult ? await window.eskilderKucult(dosyalar[i]) : dosyalar[i];
        var veri = new FormData();
        veri.append("dosya", kucuk);
        var yanit = await fetch(kutu.dataset.url, { method: "POST", body: veri, headers: { "X-CSRFToken": csrf }, credentials: "same-origin" });
        var govde = await yanit.json().catch(function () { return {}; });
        if (!yanit.ok) throw new Error(govde.hata || ("Hata " + yanit.status));
        li.textContent = "✓ " + dosyalar[i].name;
      } catch (hata) {
        hataVar = true;
        li.textContent = "✗ " + dosyalar[i].name + " — " + hata.message;
      }
    }
    girdi.disabled = false;
    girdi.value = "";
    if (!hataVar) window.location.reload();
    else satir("Bazı fotoğraflar yüklenemedi. Başarılı olanları görmek için sayfayı yenileyin.");
  });
})();
